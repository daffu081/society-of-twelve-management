#!/usr/bin/env python3
"""Spec-parity check — closes the requirement <-> task <-> spec gaps.

Run from check-spec-cache.sh every turn. Reports (exit 2) three failures the
rest of the system can't see, because AC identity is the load-bearing link
between the client's ask and what got built:

  1. Requirement<->spec drift  — a business-context AC that no requirement owns
     (the built spec diverged from the gathered requirement).                [#1]
  2. AC id collision           — the same AC id reused across a feature's
     requirement files (phases), so identity is ambiguous.                   [#2]
  3. Coverage gap              — a requirement AC in the ACTIVE phase that no
     task delivers (gathered but forgotten, so never built).                 [#3]
  4. Stale contract pin        — a feature's depends_on pins another at @N but
     that feature is now at a different contract_version (silent break).      [#8]

AC ids are feature-scoped and permanent: AC1, AC2, ... never restart, never
reused. That invariant is what makes requirement AC N == spec AC N == task AC N.

# ponytail: id-level parity only. Text drift within the same id (a requirement
# AC reworded after build) is caught by rule, not here — built ACs are
# append-only (see gather-requirement.md). Add text hashing only if that rule
# proves too weak in practice.

Self-test:  python3 spec-parity.py --selftest
"""
import os, re, sys, glob

AC_HEADING = re.compile(r'^### (AC\d+)\b', re.M)   # requirement / business-context headings
AC_TOKEN   = re.compile(r'\bAC\d+\b')              # any AC reference (task tables)
FEATURE_FM = re.compile(r'^feature:\s*(\S+)\s*$', re.M)


def _read(p):
    return open(p, encoding='utf-8').read()


def _heading_acs(path):
    return set(AC_HEADING.findall(_read(path))) if os.path.exists(path) else set()


def check(ctx):
    """Return a list of (severity, msg). severity is 'block' (corruption — the spec lies)
    or 'warn' (incompleteness — normal until phase-finish). Coverage gaps are 'warn' because
    "gathered but not yet tasked" is the expected state between /gather-requirement and
    /create-task; blocking on it would trip every turn during normal work."""
    errors = []
    features_dir = os.path.join(ctx, '05-features')
    phase_dir = os.path.join(ctx, '06-phase')
    if not os.path.isdir(phase_dir):
        return errors

    # requirement ACs per feature, tracking which files each id came from
    req_ac_files = {}   # feature -> {ac_id: [phase, ...]}
    for req in glob.glob(os.path.join(phase_dir, '*', 'requirement', '*', 'requirement.md')):
        parts = req.split(os.sep)
        phase, feature = parts[-4], parts[-2]
        bucket = req_ac_files.setdefault(feature, {})
        for ac in AC_HEADING.findall(_read(req)):
            bucket.setdefault(ac, []).append(phase)

    # 2. AC id collision across a feature's requirement files
    for feature, acs in req_ac_files.items():
        for ac, phases in acs.items():
            if len(phases) > 1:
                errors.append(('block',
                    f"AC id collision: {feature} {ac} appears in multiple requirements "
                    f"({', '.join(phases)}) — ids are permanent per feature, never reuse"))

    # 1. requirement<->spec parity: every built AC must trace to a requirement
    for d in sorted(glob.glob(os.path.join(features_dir, '*'))):
        if not os.path.isdir(d) or os.path.basename(d) == '_template':
            continue
        feature = os.path.basename(d)
        built = _heading_acs(os.path.join(d, 'business-context.md'))
        gathered = set(req_ac_files.get(feature, {}))
        for ac in sorted(built - gathered):
            errors.append(('block',
                f"requirement<->spec drift: {feature} business-context has {ac} but no "
                f"requirement owns it (spec diverged from the gathered requirement)"))

    # 3. coverage: every ACTIVE-phase requirement AC must be delivered by a task
    active = _active_phase(phase_dir)
    if active:
        adir = os.path.join(phase_dir, active)
        # AC ids each feature's tasks in this phase deliver
        task_acs = {}   # feature -> set(ac_id)
        for t in glob.glob(os.path.join(adir, 'task-T*.md')):
            txt = _read(t)
            fm = FEATURE_FM.search(txt)
            if not fm:
                continue
            task_acs.setdefault(fm.group(1), set()).update(AC_TOKEN.findall(txt))
        for req in glob.glob(os.path.join(adir, 'requirement', '*', 'requirement.md')):
            feature = req.split(os.sep)[-2]
            covered = task_acs.get(feature, set())
            for ac in sorted(_heading_acs(req) - covered):
                errors.append(('warn',
                    f"coverage gap: {active} requirement {feature} {ac} has no task "
                    f"(run /create-task so it gets built)"))

    # 4. contract-pin parity: every depends_on pin must match the target's current version
    index_yml = os.path.join(features_dir, 'INDEX.yml')
    feats = _parse_index(index_yml)
    for feature, info in feats.items():
        for dep, pin in info['deps']:
            if dep not in feats:
                errors.append(('block',
                    f"stale contract pin: {feature} depends on {dep}@{pin} but no such feature "
                    f"in INDEX.yml"))
            elif feats[dep]['cv'] is not None and pin != feats[dep]['cv']:
                errors.append(('block',
                    f"stale contract pin: {feature} pins {dep}@{pin} but {dep} is at "
                    f"contract_version {feats[dep]['cv']} (bump the pin or the consumer breaks)"))
    return errors


def _parse_index(path):
    """Parse 05-features/INDEX.yml -> {feature: {cv:int|None, deps:[(name,ver)]}}."""
    feats = {}
    if not os.path.exists(path):
        return feats
    cur = None
    for line in _read(path).splitlines():
        m = re.match(r'^  (\S+):\s*$', line)
        if m:
            cur = m.group(1)
            feats[cur] = {'cv': None, 'deps': []}
            continue
        if cur is None:
            continue
        cv = re.match(r'^\s+contract_version:\s*(\d+)', line)
        if cv:
            feats[cur]['cv'] = int(cv.group(1))
            continue
        dep = re.match(r'^\s+depends_on:\s*\[(.*)\]', line)
        if dep:
            for tok in re.findall(r'([A-Za-z0-9_-]+)@(\d+)', dep.group(1)):
                feats[cur]['deps'].append((tok[0], int(tok[1])))
    return feats


def _active_phase(phase_dir):
    idx = os.path.join(phase_dir, 'index.yml')
    if os.path.exists(idx):
        m = re.search(r'^active:\s*(\S+)\s*$', _read(idx), re.M)
        if m and m.group(1) not in ('null', '_none_', '~'):
            return m.group(1)
    return None


def main():
    ctx = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')), 'context')
    if not os.path.isdir(ctx):
        return 0
    findings = check(ctx)
    for sev, msg in findings:
        label = 'spec-parity[warn]: ' if sev == 'warn' else 'spec-parity: '
        sys.stderr.write(label + msg + '\n')
    # only corruption blocks; coverage warnings are advisory (normal until phase-finish)
    return 2 if any(sev == 'block' for sev, _ in findings) else 0


def selftest():
    import tempfile, shutil
    tmp = tempfile.mkdtemp()
    try:
        ctx = os.path.join(tmp, 'context')
        # feature "notes": AC1/AC2 gathered in phase-01, plus a colliding AC1 in phase-02
        for ph, acs in [('phase-01', ['AC1', 'AC2']), ('phase-02', ['AC1'])]:
            rd = os.path.join(ctx, '06-phase', ph, 'requirement', 'notes')
            os.makedirs(rd)
            open(os.path.join(rd, 'requirement.md'), 'w').write(
                ''.join(f'### {a}: t\n' for a in acs))
        open(os.path.join(ctx, '06-phase', 'index.yml'), 'w').write('active: phase-01\n')
        # a task delivering only AC1 -> AC2 is an uncovered coverage gap
        open(os.path.join(ctx, '06-phase', 'phase-01', 'task-T01-x.md'), 'w').write(
            'feature: notes\n\n| AC | \n| AC1 | \n')
        # business-context claims AC9 that no requirement owns -> drift
        fd = os.path.join(ctx, '05-features', 'notes')
        os.makedirs(fd)
        open(os.path.join(fd, 'business-context.md'), 'w').write('### AC1: t\n### AC9: t\n')
        # contract pins: billing pins notes@1 but notes is at contract_version 2 -> stale
        open(os.path.join(ctx, '05-features', 'INDEX.yml'), 'w').write(
            'features:\n'
            '  notes:\n    contract_version: 2\n    depends_on: []\n'
            '  billing:\n    contract_version: 1\n    depends_on: [notes@1]\n')

        findings = check(ctx)
        errs = '\n'.join(m for _, m in findings)
        sev = {m: s for s, m in findings}
        assert 'collision' in errs and 'notes AC1' in errs, errs
        assert 'drift' in errs and 'AC9' in errs, errs
        assert 'coverage gap' in errs and 'AC2' in errs, errs
        assert 'stale contract pin' in errs and 'billing pins notes@1' in errs, errs
        # coverage is advisory; the other three are blocking
        assert all(s == 'warn' for m, s in sev.items() if 'coverage gap' in m), sev
        assert all(s == 'block' for m, s in sev.items() if 'coverage gap' not in m), sev
        # clean tree: no violations
        assert check(os.path.join(tmp, 'nope')) == []
        print('selftest: OK')
    finally:
        shutil.rmtree(tmp)


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        selftest()
    else:
        sys.exit(main())
