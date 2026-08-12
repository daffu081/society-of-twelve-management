#!/usr/bin/env python3
"""Stop hook — auto-reconciles DERIVED context fields after every agent turn.

Only touches mechanical, single-source fields (never prose):
  1. ac_count in 05-features/INDEX.yml
        <- count of `### AC<n>` headings in that feature's business-context.md
  2. last_review -> today, on context/*.md files changed in the last 5 min

Frontmatter-value edits only; it never rewrites body text. Exits 0 (it fixes,
it does not block). Prose context (requirements, what a feature does, decisions)
is NOT auto-written — that needs judgment and stays in /gather-requirement and
/implement-task.

Self-test:  python3 context-autosync.py --selftest
"""
import os, re, sys, glob, time
from datetime import date

TODAY = date.today().isoformat()
AC_RE = re.compile(r'^### AC\d', re.M)


def set_fm_field(path, key, value):
    """Replace `key: ...` inside the first --- frontmatter block. Returns True if changed."""
    txt = open(path, encoding='utf-8').read()
    if not txt.startswith('---'):
        return False
    end = txt.find('\n---', 3)
    if end == -1:
        return False
    head, body = txt[:end], txt[end:]
    pat = re.compile(rf'^(\s*){re.escape(key)}:\s*.*$', re.M)
    new_head, n = pat.subn(rf'\g<1>{key}: {value}', head)
    if n == 0 or new_head == head:
        return False
    open(path, 'w', encoding='utf-8').write(new_head + body)
    return True


def set_index_yml_ac(index_yml, feature, count):
    """Set `ac_count: <count>` inside the given feature's block. Returns True if changed."""
    if not os.path.exists(index_yml):
        return False
    lines = open(index_yml, encoding='utf-8').read().splitlines(keepends=True)
    in_feat, changed = False, False
    for i, line in enumerate(lines):
        m = re.match(r'^ {2}(\S+):\s*$', line)
        if m:
            in_feat = (m.group(1) == feature)
            continue
        if in_feat:
            am = re.match(r'^(\s+ac_count:\s*)(\d+)(.*)$', line)
            if am and am.group(2) != str(count):
                lines[i] = f'{am.group(1)}{count}{am.group(3)}\n'
                changed = True
    if changed:
        open(index_yml, 'w', encoding='utf-8').write(''.join(lines))
    return changed


def reconcile(features_dir):
    """Sync ac_count from each business-context.md -> INDEX.yml. Returns list of notes."""
    notes = []
    index_yml = os.path.join(features_dir, 'INDEX.yml')
    for d in sorted(glob.glob(os.path.join(features_dir, '*'))):
        if not os.path.isdir(d) or os.path.basename(d) == '_template':
            continue
        feature = os.path.basename(d)
        bc = os.path.join(d, 'business-context.md')
        if not os.path.exists(bc):
            continue
        count = len(AC_RE.findall(open(bc, encoding='utf-8').read()))
        if set_index_yml_ac(index_yml, feature, count):
            notes.append(f'INDEX.yml {feature}.ac_count -> {count}')
    return notes


def bump_last_review(ctx_dir, window_s=300):
    """Set last_review -> today on context .md files modified within window_s. Returns notes."""
    notes, now = [], time.time()
    for f in glob.glob(os.path.join(ctx_dir, '**', '*.md'), recursive=True):
        if now - os.path.getmtime(f) > window_s:
            continue
        head = open(f, encoding='utf-8').read()[:600]
        # never touch a frozen file — stamping it would trip the freeze guard in check-spec-cache.sh
        if re.search(r'^\s*frozen:\s*true\s*$', head, re.M):
            continue
        # only if it already carries a real (non-placeholder, non-today) date
        m = re.search(r'^\s*last_review:\s*(.+)$', head, re.M)
        if not m or m.group(1).strip() in ('', TODAY):
            continue
        if set_fm_field(f, 'last_review', TODAY):
            notes.append(f'{os.path.relpath(f, ctx_dir)} last_review -> {TODAY}')
    return notes


def main():
    repo = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    ctx = os.path.join(repo, 'context')
    features = os.path.join(ctx, '05-features')
    if not os.path.isdir(features):
        return 0  # nothing to sync
    notes = reconcile(features) + bump_last_review(ctx)
    if notes:
        sys.stderr.write('context-autosync: ' + '; '.join(notes) + '\n')
    return 0


def selftest():
    import tempfile, shutil
    tmp = tempfile.mkdtemp()
    try:
        fd = os.path.join(tmp, '05-features', 'foo')
        os.makedirs(fd)
        open(os.path.join(fd, 'business-context.md'), 'w').write(
            '# Foo\n### AC1: a\n### AC2: b\n### AC3: c\n')
        open(os.path.join(tmp, '05-features', 'INDEX.yml'), 'w').write(
            'features:\n  foo:\n    status: planned\n    ac_count: 0\n')
        reconcile(os.path.join(tmp, '05-features'))
        yml = open(os.path.join(tmp, '05-features', 'INDEX.yml')).read()
        assert 'ac_count: 3' in yml, yml
        # idempotent: no crash / no change on second run
        reconcile(os.path.join(tmp, '05-features'))
        print('selftest: OK')
    finally:
        shutil.rmtree(tmp)


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        selftest()
    else:
        sys.exit(main())
