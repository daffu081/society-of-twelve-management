#!/usr/bin/env python3
import json, re, pathlib, threading, webbrowser, time
from http.server import HTTPServer, BaseHTTPRequestHandler

ROOT = pathlib.Path(__file__).parent.parent
PORT = 8765

SOURCES = [
    ("active",       "06-phase/ACTIVE.md"),
    ("backlog",      "06-phase/BACKLOG.md"),
    ("vision",       "03-business/vision.md"),
    ("features_yml", "05-features/INDEX.yml"),
]

def collect():
    d = {k: (ROOT / p).read_text() if (ROOT / p).exists() else "" for k, p in SOURCES}
    m = re.search(r"(phase-\d+)", d["active"])
    folder = ROOT / "06-phase" / m.group(1) if m else ROOT / "06-phase"
    phase_md = folder / "phase.md"
    d["phase"] = phase_md.read_text() if phase_md.exists() else ""
    d["tasks"] = {f.stem: f.read_text() for f in sorted(folder.glob("task-T*.md"))}
    d["active_phase"] = m.group(1) if m else ""
    d["phases"] = _all_phases(ROOT / "06-phase")
    d["feature_bc"] = _feature_bc(ROOT / "05-features")
    d["health"] = _health(d)
    return d

def _field(text, key):
    mm = re.search(rf"^{key}:\s*(.+)$", text, re.M)
    return mm.group(1).strip().strip('"') if mm else ""

def _all_phases(base):
    out = []
    for folder in sorted(base.glob("phase-*")):
        pm = folder / "phase.md"
        text = pm.read_text() if pm.exists() else ""
        tasks = []
        for tf in sorted(folder.glob("task-T*.md")):
            tt = tf.read_text()
            tasks.append({
                "id":     _field(tt, "id") or tf.stem.split("-")[1] if "-" in tf.stem else tf.stem,
                "title":  _field(tt, "title") or tf.stem,
                "status": _field(tt, "status") or "todo",
            })
        out.append({
            "id":     folder.name,
            "title":  _field(text, "title") or folder.name,
            "status": _field(text, "status") or "unknown",
            "goal":   _field(text, "goal"),
            "tasks":  tasks,
        })
    return out

def _feature_bc(base):
    out = {}
    if not base.exists():
        return out
    for folder in sorted(base.glob("*")):
        bc = folder / "business-context.md"
        if bc.exists():
            out[folder.name] = bc.read_text()
    return out

def _health(d):
    checks = []

    def ck(label, ok, detail="", warn=False):
        checks.append({"label": label, "status": "ok" if ok else ("warn" if warn else "error"), "detail": detail})

    ck("Vision defined",       bool(d.get("vision","").strip()),       "03-business/vision.md is empty or missing")
    ck("Features index exists", bool(d.get("features_yml","").strip()), "05-features/INDEX.yml is missing", warn=True)
    ck("Active phase set",      bool(d.get("active_phase")),            "06-phase/ACTIVE.md doesn't reference a phase folder")

    if d.get("active_phase"):
        pt = d.get("phase", "")
        ck("Active phase has title", bool(_field(pt, "title")), "phase.md missing title field", warn=True)
        ck("Active phase has goal",  bool(_field(pt, "goal")),  "phase.md missing goal field",  warn=True)
        tasks = d.get("tasks", {})
        if tasks:
            bad = [s for s, t in tasks.items() if not _field(t, "title") or not _field(t, "status")]
            ck("Task frontmatter complete", not bad,
               f"{len(bad)} task(s) missing title/status: {', '.join(bad)}", warn=True)
        else:
            ck("Active phase has tasks", False, "No task-T*.md files in active phase folder", warn=True)

    feat_names = re.findall(r"^  ([\w-]+):\s*$", d.get("features_yml",""), re.M)
    bc = d.get("feature_bc", {})
    missing_bc = [f for f in feat_names if f not in bc and not f.startswith("_")]
    if feat_names:
        ck("Features have business-context", not missing_bc,
           f"Missing business-context.md: {', '.join(missing_bc)}", warn=True)

    arch_dir = ROOT / "04-architecture"
    ck("Architecture documented", bool(list(arch_dir.glob("*.md"))) if arch_dir.exists() else False,
       "04-architecture/ has no .md files", warn=True)

    ok_n   = sum(1 for c in checks if c["status"] == "ok")
    warns  = sum(1 for c in checks if c["status"] == "warn")
    errors = sum(1 for c in checks if c["status"] == "error")
    score  = round((ok_n + warns * 0.5) / len(checks) * 100) if checks else 100
    return {"score": score, "checks": checks, "ok": ok_n, "warns": warns, "errors": errors}

def _build_analyze_prompt():
    SKIP_DIRS = {".git", "node_modules", "__pycache__", "dashboard", ".claude", ".venv", "venv", "dist", "build"}
    CODE_EXTS = {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".java", ".rb", ".rs", ".cs", ".cpp", ".c", ".swift", ".kt"}
    ctx_files, code_files = {}, {}

    for f in ROOT.rglob("*"):
        if not f.is_file():
            continue
        rel = f.relative_to(ROOT)
        if any(p in SKIP_DIRS for p in rel.parts):
            continue
        try:
            text = f.read_text(errors="replace")
        except Exception:
            continue
        snippet = text[:1400] + ("\n…(truncated)" if len(text) > 1400 else "")
        if f.suffix in (".md", ".yml", ".yaml"):
            ctx_files[str(rel)] = snippet
        elif f.suffix in CODE_EXTS:
            code_files[str(rel)] = snippet

    ctx_body  = "\n\n".join(f"=== {p} ===\n{c}" for p, c in sorted(ctx_files.items()))
    code_body = "\n\n".join(f"=== {p} ===\n{c}" for p, c in sorted(code_files.items()))
    code_section = f"\n\nSOURCE CODE FILES:\n{code_body}" if code_body else "\n\n(No source code files found outside skip dirs)"

    return f"""You are auditing a software project's context boilerplate at {ROOT}.

Convention: numbered dirs 01-source … 14-seeds each carry a README.md (and index.yml where present).
05-features/INDEX.yml is the feature registry; each feature has a folder with 3 files: business-context.md, technical-context.md, test-context.md.
06-phase/index.yml is the phase registry; tasks (task-T*.md) need frontmatter: task_id, feature, status.
Content must not be unfilled placeholder/template text (TODO, "example", boilerplate never filled in).

CONTEXT FILES:
{ctx_body}
{code_section}

Find ALL issues across these categories:
1. Missing required files or frontmatter fields
2. Placeholder/template content never filled in
3. Inconsistencies within context (features in INDEX.yml vs actual folders, task statuses vs phase status, etc.)
4. Context vs code mismatches — does the context accurately describe what the code actually does? Are features/APIs/modules described in context but absent in code, or vice versa?
5. Stale context — descriptions that contradict the current code implementation

Be thorough and specific. Name exact files. Output ONLY valid JSON (no markdown fences):
{{"summary":"one-sentence health overview","score":0-100,"issues":[{{"severity":"error|warn|info","path":"relative/path","message":"specific problem"}}],"recommendations":["specific actionable step"]}}"""

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Project Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:    #1b1c1e;
  --s1:    #232428;
  --s2:    #2a2b2f;
  --s3:    #313438;
  --s4:    #3a3c42;
  --bd:    #3e4045;
  --bd2:   #52555c;
  --tx:    #e8eaed;
  --mu:    #9aa0a6;
  --mu2:   #5f6368;
  --cyan:  #13b9fd;
  --blue:  #1a73e8;
  --blue2: #4a90d9;
  --green: #34a853;
  --gd:    #0d2414;
  --red:   #ea4335;
  --rd:    #2a0a08;
  --yel:   #fbbc04;
  --yd:    #2a2000;
  --pur:   #a142f4;
  --pd:    #1e0a38;
}
html,body{height:100%;background:var(--bg);color:var(--tx);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Roboto",sans-serif;
  font-size:13px;overflow:hidden}

/* ── App Shell ── */
.app{display:flex;flex-direction:column;height:100vh}

/* ── Topbar ── */
.topbar{
  flex-shrink:0;
  background:var(--s1);
  border-bottom:1px solid var(--bd);
  display:flex;align-items:center;gap:0;
  padding:0;
  height:48px;
}
.logo{
  display:flex;align-items:center;gap:8px;
  padding:0 20px;
  border-right:1px solid var(--bd);
  height:100%;
  font-weight:700;font-size:14px;color:#fff;
  white-space:nowrap;
}
.logo-mark{
  width:24px;height:24px;border-radius:6px;
  background:linear-gradient(135deg,var(--blue),var(--cyan));
  display:flex;align-items:center;justify-content:center;
  font-size:12px;
}
/* ── Animated tab indicator ── */
.topbar-tabs{
  display:flex;height:100%;flex:1;overflow-x:auto;
  scrollbar-width:none;position:relative;
}
.topbar-tabs::-webkit-scrollbar{display:none}
.tab-ink{
  position:absolute;bottom:0;height:2px;background:var(--cyan);
  border-radius:2px 2px 0 0;
  transition:left .2s ease,width .2s ease;
  pointer-events:none;
}
.ttab{
  display:flex;align-items:center;gap:6px;
  padding:0 18px;height:100%;
  font-size:12.5px;font-weight:500;color:var(--mu);
  cursor:pointer;white-space:nowrap;flex-shrink:0;
  transition:color .15s;user-select:none;
}
.ttab:hover{color:var(--tx)}
.ttab.on{color:var(--cyan)}
.ttab-n{
  background:var(--s3);color:var(--mu);
  font-size:10px;font-weight:700;padding:1px 6px;border-radius:10px;
}
.topbar-right{
  display:flex;align-items:center;gap:12px;
  padding:0 18px;border-left:1px solid var(--bd);height:100%;
  flex-shrink:0;
}
.live{display:flex;align-items:center;gap:5px;font-size:11px;color:var(--green);transition:color .3s}
.live.stale{color:var(--mu)}
.dot{width:6px;height:6px;border-radius:50%;background:currentColor;
  box-shadow:0 0 6px currentColor;animation:pulse 2s infinite;transition:background .3s}
.live.stale .dot{animation:none;opacity:.5}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
.ts{font-size:11px;color:var(--mu);font-variant-numeric:tabular-nums}

/* ── Progress strip ── */
.pstrip{flex-shrink:0;height:3px;background:var(--s3)}
.pfill{height:100%;background:linear-gradient(90deg,var(--blue),var(--cyan));transition:width .7s ease}

/* ── Content ── */
.content{flex:1;display:flex;overflow:hidden}
.page{flex:1;overflow-y:auto;overflow-x:hidden;padding:20px 24px}

/* ── Left sidebar (wide screens) ── */
.sidebar{
  flex-shrink:0;width:210px;
  background:var(--s1);border-right:1px solid var(--bd);
  display:none;flex-direction:column;overflow-y:auto;overflow-x:hidden;
}
@media(min-width:860px){
  .sidebar{display:flex}
  .topbar-tabs{display:none !important}
}
.sb-sec{font-size:9px;font-weight:700;text-transform:uppercase;
  letter-spacing:.1em;color:var(--mu2);padding:14px 14px 4px}
.sb-item{
  display:flex;align-items:center;gap:8px;
  padding:7px 10px;margin:1px 6px;border-radius:6px;
  cursor:pointer;color:var(--mu);font-size:12px;font-weight:500;
  user-select:none;transition:background .1s,color .1s;
}
.sb-item:hover{background:var(--s2);color:var(--tx)}
.sb-item.on{background:var(--s3);color:#fff;font-weight:600;border-left:2px solid var(--cyan);padding-left:8px}
.sb-item.on .sb-icon{color:var(--cyan)}
.sb-icon{font-size:13px;width:16px;text-align:center;flex-shrink:0;color:var(--mu2)}
.sb-badge{margin-left:auto;background:var(--s4);color:var(--mu);
  font-size:9px;font-weight:700;padding:1px 6px;border-radius:8px}
.sb-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0}
.sb-label{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.sb-foot{
  margin-top:auto;border-top:1px solid var(--bd);
  padding:12px 14px;display:flex;flex-direction:column;gap:7px;
}
.sb-row{display:flex;justify-content:space-between;align-items:center}
.sb-rl{font-size:10px;color:var(--mu)}
.sb-rv{font-size:11px;font-weight:700;color:var(--tx)}

/* ── Phase summary bar ── */
.phasebar{
  background:var(--s2);border:1px solid var(--bd);border-radius:8px;
  padding:14px 18px;margin-bottom:18px;
  display:flex;align-items:center;gap:20px;flex-wrap:wrap;
  max-width:900px;
  border-left:3px solid var(--cyan);
}
.phasebar-left{flex:1;min-width:200px}
.phasebar-title{font-size:15px;font-weight:700;color:#fff;margin-bottom:3px}
.phasebar-sub{font-size:11px;color:var(--mu);margin-bottom:10px}
.pbar-track{height:6px;background:var(--s4);border-radius:3px;overflow:hidden}
.pbar-fill{height:100%;background:linear-gradient(90deg,var(--blue),var(--cyan));border-radius:3px;transition:width .7s}
.phasebar-stats{display:flex;gap:24px;flex-shrink:0}
.stat{text-align:center}
.stat-n{font-size:22px;font-weight:800;line-height:1}
.stat-l{font-size:10px;color:var(--mu);margin-top:3px;text-transform:uppercase;letter-spacing:.05em}

/* ── Board ── */
.board{display:grid;grid-template-columns:repeat(var(--cols,3),1fr);gap:12px;align-items:stretch}
@media(max-width:700px){.board{grid-template-columns:1fr}}
.col{background:var(--s2);border:1px solid var(--bd);border-radius:8px;overflow:hidden}
.col[data-col]::before{content:'';display:block;height:3px;background:var(--col-c)}
.col-head{
  display:flex;align-items:center;gap:8px;
  padding:10px 12px;background:var(--s3);border-bottom:1px solid var(--bd);
}
.col-pip{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.col-name{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.07em;flex:1}
.col-ct{background:var(--s4);color:var(--mu);font-size:10px;padding:1px 7px;border-radius:8px;font-weight:700}
.col-body{padding:10px}

/* ── Task card ── */
.card{
  background:var(--s1);border:1px solid var(--bd);border-radius:6px;
  border-left:3px solid var(--card-c, var(--bd));
  padding:11px 12px 11px 10px;margin-bottom:8px;cursor:pointer;
  transition:border-color .15s,box-shadow .15s,transform .15s;
}
.card:last-child{margin-bottom:0}
.card:hover{border-color:var(--bd2);transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,.5)}
.card.sel{border-left-color:var(--cyan);box-shadow:0 0 0 1px var(--cyan)}
.cid{font-size:9px;font-weight:800;color:var(--mu);letter-spacing:.07em;margin-bottom:5px;font-family:monospace}
.ctitle{font-size:13px;font-weight:500;color:var(--tx);line-height:1.4;margin-bottom:8px}
.cfoot{display:flex;align-items:center;gap:5px;flex-wrap:wrap}
.cfeat{background:var(--pd);color:var(--pur);font-size:9px;font-weight:700;padding:2px 7px;border-radius:3px}
.cdep{font-size:9px;color:var(--mu2);display:flex;align-items:center;gap:3px}
.copy-id{cursor:pointer;transition:color .15s}
.copy-id:hover{color:var(--cyan)}
.copy-toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);
  background:var(--s3);color:var(--tx);border:1px solid var(--bd);
  padding:6px 14px;border-radius:20px;font-size:11px;
  opacity:0;transition:opacity .2s;pointer-events:none;z-index:99}
.cac{margin-left:auto;font-size:10px;color:var(--mu);font-variant-numeric:tabular-nums}
.mbar{height:3px;background:var(--s4);border-radius:2px;margin:6px 0 3px;overflow:hidden}
.mfill{height:100%;background:linear-gradient(90deg,var(--blue),var(--cyan));border-radius:2px}
.col-empty{
  margin:8px;padding:20px 12px;text-align:center;color:var(--mu2);font-size:12px;
  border:1.5px dashed var(--bd);border-radius:6px;
}

/* ── List view ── */
.tlist{display:flex;flex-direction:column;gap:4px}
.trow{
  display:flex;align-items:center;gap:10px;
  padding:9px 12px;background:var(--s2);border:1px solid var(--bd);border-radius:6px;cursor:pointer;
  transition:border-color .1s;
}
.trow:hover{border-color:var(--bd2)}
.trow.sel{border-color:var(--cyan);background:var(--s3)}
.tid{font-size:9px;font-weight:800;color:var(--mu);letter-spacing:.06em;min-width:46px;font-family:monospace}
.ttitle{flex:1;font-size:12.5px;font-weight:500;color:var(--tx);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tacs{font-size:10px;color:var(--mu);font-variant-numeric:tabular-nums}

/* ── Badges ── */
.badge{display:inline-flex;align-items:center;gap:3px;padding:2px 8px;border-radius:12px;font-size:10px;font-weight:600;white-space:nowrap}
.badge::before{content:'';width:5px;height:5px;border-radius:50%}
.b-todo{background:var(--s4);color:var(--mu);border:1px solid var(--bd2)}
.b-todo::before{background:var(--mu)}
.b-planned{background:var(--pd);color:var(--pur);border:1px solid #4a1a80}
.b-planned::before{background:var(--pur)}
.b-in_progress{background:#0d2040;color:var(--blue2);border:1px solid #1a3a70}
.b-in_progress::before{background:var(--blue2)}
.b-done{background:var(--gd);color:var(--green);border:1px solid #1a5a2a}
.b-done::before{background:var(--green)}
.b-blocked{background:var(--rd);color:var(--red);border:1px solid #5a1a15}
.b-blocked::before{background:var(--red)}

/* ── Markdown ── */
.md{color:var(--tx);line-height:1.75;font-size:13px}
.md h1,.md h2{color:#fff;font-size:13px;font-weight:700;margin:16px 0 6px;padding-bottom:5px;border-bottom:1px solid var(--bd);text-transform:uppercase;letter-spacing:.04em}
.md h3{color:var(--cyan);font-size:11px;font-weight:700;margin:12px 0 4px;text-transform:uppercase;letter-spacing:.06em}
.md h4{color:var(--tx);font-size:12px;font-weight:600;margin:8px 0 3px}
.md p{margin:5px 0;color:var(--tx);line-height:1.7}
.md strong{color:#fff;font-weight:600}
.md em{color:var(--mu);font-style:italic}
.md table{border-collapse:collapse;width:100%;margin:10px 0;font-size:12px;border-radius:6px;overflow:hidden}
.md th{background:var(--s3);color:var(--mu);font-size:9px;text-transform:uppercase;letter-spacing:.06em;font-weight:700;border:1px solid var(--bd);padding:7px 10px;text-align:left}
.md td{border:1px solid var(--bd);padding:7px 10px;color:var(--tx);vertical-align:top}
.md tr:nth-child(even) td{background:var(--s2)}
.md tr:hover td{background:var(--s3)}
.md code{background:var(--s3);padding:1px 6px;border-radius:4px;font-size:11px;font-family:"SF Mono","Cascadia Code","Fira Code",ui-monospace,monospace;color:var(--cyan);border:1px solid var(--bd)}
.md pre{background:var(--s2);padding:12px 14px;border-radius:6px;overflow-x:auto;margin:8px 0;border:1px solid var(--bd)}
.md pre code{background:none;border:none;padding:0;font-size:12px;color:var(--tx)}
.md blockquote{border-left:3px solid var(--blue);padding:8px 14px;background:var(--s2);border-radius:0 6px 6px 0;color:var(--mu);margin:8px 0;font-style:italic}
.md ul,.md ol{padding-left:18px;margin:4px 0}
.md li{margin:4px 0;color:var(--tx)}
.md li code{font-size:11px}
.md a{color:var(--cyan);text-decoration:none;border-bottom:1px solid rgba(19,185,253,.3)}
.md a:hover{border-bottom-color:var(--cyan)}
.md hr{border:none;border-top:1px solid var(--bd);margin:12px 0}

/* ── Feature cards ── */
.feat-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,220px));gap:10px}
.feat-card{background:var(--s2);border:1px solid var(--bd);border-radius:8px;padding:14px}
.feat-pip{width:8px;height:8px;border-radius:50%;margin-bottom:8px}
.feat-name{font-size:13px;font-weight:600;color:#fff;margin-bottom:4px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.feat-desc{font-size:11px;color:var(--mu);line-height:1.5}

/* ── Overview stats grid ── */
.ov-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:10px;margin-bottom:20px;max-width:700px}
.ov-card{background:var(--s2);border:1px solid var(--bd);border-radius:8px;padding:16px 14px}
.ov-n{font-size:28px;font-weight:800;line-height:1}
.ov-l{font-size:10px;color:var(--mu);margin-top:4px;text-transform:uppercase;letter-spacing:.06em}

/* ── Resize handle ── */
.resize-handle{
  flex-shrink:0;width:4px;cursor:col-resize;
  background:transparent;position:relative;
  display:none;
  transition:background .15s;
}
.resize-handle::after{
  content:'';position:absolute;inset:0 -2px;
}
.resize-handle:hover,.resize-handle.dragging{background:var(--cyan)}

/* ── Right panel (task detail) ── */
.panel{
  width:0;flex-shrink:0;overflow:hidden;
  border-left:1px solid var(--bd);background:var(--s1);
  display:flex;flex-direction:column;
  transition:width .22s ease;
}
.panel.on{width:340px}
.panel.resizing{transition:none}
.d-top{
  flex-shrink:0;display:flex;align-items:flex-start;gap:10px;
  padding:14px 16px 12px;border-bottom:1px solid var(--bd);
  background:var(--s1);
}
.d-id{font-size:9px;font-weight:800;color:var(--cyan);letter-spacing:.1em;font-family:monospace;margin-bottom:4px}
.d-title{font-size:14px;font-weight:700;color:#fff;line-height:1.35;flex:1}
.d-close{background:none;border:1px solid var(--bd);color:var(--mu);cursor:pointer;
  font-size:13px;padding:3px 8px;border-radius:5px;flex-shrink:0;transition:background .12s;align-self:flex-start}
.d-close:hover{background:var(--s3);color:var(--tx)}
.d-meta{flex-shrink:0;display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--bd);border-bottom:1px solid var(--bd)}
.d-mi{background:var(--s2);padding:9px 14px}
.d-ml{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.07em;color:var(--mu);margin-bottom:4px}
.d-mv{font-size:12px;color:var(--tx)}
.d-body{flex:1;overflow-y:auto;padding:14px 16px;display:flex;flex-direction:column;gap:16px}
.sec{display:flex;flex-direction:column;gap:8px}
.sec-h{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--mu);padding-bottom:5px;border-bottom:1px solid var(--bd)}
.sec-tx{font-size:12px;color:var(--tx);line-height:1.65}
.ac-list{display:flex;flex-direction:column;gap:4px}
.ac{display:flex;align-items:flex-start;gap:10px;padding:8px 10px;
  border-radius:6px;background:var(--s2);border:1px solid var(--bd)}
.ac.ok{background:var(--gd);border-color:#1a5a2a}
.ac-box{width:15px;height:15px;border-radius:3px;border:1.5px solid var(--bd2);flex-shrink:0;
  display:flex;align-items:center;justify-content:center;font-size:8px;margin-top:1px}
.ac.ok .ac-box{background:var(--green);border-color:var(--green);color:#000}
.ac-id{font-size:9px;font-weight:700;color:var(--mu);font-family:monospace}
.ac-lb{font-size:12px;color:var(--tx);margin-top:1px;line-height:1.4}

/* ── Search ── */
.search-wrap{display:flex;align-items:center;gap:8px;margin-left:auto;position:relative}
.search-icon{position:absolute;left:10px;color:var(--mu2);font-size:12px;pointer-events:none}
.search-box{
  background:var(--s2);border:1px solid var(--bd);border-radius:20px;
  color:var(--tx);font-size:12px;padding:5px 14px 5px 28px;outline:none;width:180px;
  transition:border-color .15s,width .2s,box-shadow .15s;
}
.search-box:focus{border-color:var(--cyan);width:220px;box-shadow:0 0 0 3px rgba(19,185,253,.1)}
.search-box::placeholder{color:var(--mu2)}
.filter-chip{
  display:inline-flex;align-items:center;gap:5px;
  background:var(--pd);color:var(--pur);border:1px solid #4a1a80;
  font-size:10px;font-weight:600;padding:3px 8px;border-radius:12px;
}
.filter-chip button{background:none;border:none;color:var(--pur);cursor:pointer;padding:0;font-size:11px;line-height:1}
.filter-bar{display:flex;align-items:center;gap:8px;margin-bottom:12px;flex-wrap:wrap}

/* ── DoD checklist ── */
.dod-list{display:flex;flex-direction:column;gap:4px}
.dod-item{display:flex;align-items:flex-start;gap:8px;font-size:12px;color:var(--tx);padding:4px 0}
.dod-cb{width:14px;height:14px;border-radius:3px;border:1.5px solid var(--bd2);flex-shrink:0;
  display:flex;align-items:center;justify-content:center;font-size:8px;margin-top:1px}
.dod-item.done .dod-cb{background:var(--green);border-color:var(--green);color:#000}
.dod-item.done span{color:var(--mu);text-decoration:line-through}

/* ── Health ── */
.h-hero{display:flex;align-items:center;gap:28px;margin-bottom:22px;flex-wrap:wrap}
.h-ring-wrap{position:relative;width:130px;height:130px;flex-shrink:0}
.h-ring-wrap svg{display:block}
.h-ring-center{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1px}
.h-ring-num{font-size:32px;font-weight:800;line-height:1}
.h-ring-sub{font-size:9px;color:var(--mu);letter-spacing:.08em;text-transform:uppercase}
.h-ring-grade{font-size:13px;font-weight:800;margin-top:2px;padding:1px 8px;border-radius:4px}
.h-meta{display:flex;flex-direction:column;gap:12px}
.h-counters{display:flex;gap:16px}
.h-ct{display:flex;align-items:center;gap:7px}
.h-ct-n{font-size:20px;font-weight:800;line-height:1;min-width:28px;text-align:right}
.h-ct-bar{width:3px;height:20px;border-radius:2px;flex-shrink:0}
.h-ct-l{font-size:11px;color:var(--mu)}
.h-btn{
  display:inline-flex;align-items:center;gap:8px;
  padding:9px 20px;border-radius:8px;border:none;cursor:pointer;
  font-size:13px;font-weight:600;color:#fff;
  background:linear-gradient(135deg,#1a73e8,#13b9fd);
  box-shadow:0 4px 18px rgba(19,185,253,.3);
  transition:opacity .15s,transform .12s,box-shadow .15s;
}
.h-btn:hover{opacity:.9;transform:translateY(-1px);box-shadow:0 6px 24px rgba(19,185,253,.4)}
.h-btn:disabled{opacity:.45;cursor:not-allowed;transform:none;box-shadow:none}
.h-btn-spin{display:inline-block;animation:spin .9s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.h-section{margin-bottom:16px;max-width:660px}
.h-sec-hd{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;
  color:var(--mu);padding-bottom:6px;border-bottom:1px solid var(--bd);margin-bottom:8px;
  display:flex;align-items:center;gap:8px}
.hcheck{display:flex;align-items:flex-start;gap:10px;padding:9px 12px;
  border-radius:6px;margin-bottom:5px;border:1px solid transparent;
  transition:opacity .1s}
.hcheck.ok   {background:var(--gd);border-color:#1a5a2a}
.hcheck.warn {background:var(--yd);border-color:#4a3a00}
.hcheck.error{background:var(--rd);border-color:#5a1a15}
.hcheck-icon{width:20px;height:20px;border-radius:4px;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800}
.hcheck.ok    .hcheck-icon{background:var(--green);color:#000}
.hcheck.warn  .hcheck-icon{background:var(--yel);color:#000}
.hcheck.error .hcheck-icon{background:var(--red);color:#fff}
.hcheck-label{font-size:12.5px;font-weight:500;color:var(--tx);line-height:1.4}
.hcheck-detail{font-size:10.5px;color:var(--mu);margin-top:2px;font-family:monospace}
/* Analysis */
.analysis-wrap{max-width:660px;margin-top:22px;border-top:1px solid var(--bd);padding-top:18px}
.analysis-stream{
  background:#0d0f10;border:1px solid var(--bd);border-radius:6px;
  padding:12px 14px;font-family:"SF Mono","Cascadia Code",ui-monospace,monospace;font-size:11px;
  color:#7ec8a0;line-height:1.7;max-height:180px;overflow-y:auto;
  white-space:pre-wrap;word-break:break-all;
}
.analysis-result{margin-top:14px}
.ai-summary{
  padding:13px 16px;
  background:linear-gradient(135deg,rgba(26,115,232,.12),rgba(19,185,253,.07));
  border:1px solid rgba(19,185,253,.25);border-radius:8px;
  font-size:13px;color:var(--tx);margin-bottom:14px;line-height:1.65;
}
.ai-score-row{display:flex;align-items:center;gap:10px;margin-bottom:14px}
.ai-score-pill{font-size:11px;font-weight:700;padding:3px 10px;border-radius:20px}
.ai-issue{display:flex;align-items:flex-start;gap:10px;padding:8px 12px;
  border-radius:6px;margin-bottom:5px;border:1px solid transparent}
.ai-issue.error{background:var(--rd);border-color:#5a1a15}
.ai-issue.warn {background:var(--yd);border-color:#4a3a00}
.ai-issue.info {background:var(--s2);border-color:var(--bd)}
.ai-sev{font-size:9px;font-weight:800;padding:2px 7px;border-radius:3px;flex-shrink:0;
  text-transform:uppercase;letter-spacing:.06em;margin-top:1px;white-space:nowrap}
.ai-issue.error .ai-sev{background:var(--red);color:#fff}
.ai-issue.warn  .ai-sev{background:var(--yel);color:#000}
.ai-issue.info  .ai-sev{background:var(--s4);color:var(--mu)}
.ai-msg{font-size:12px;color:var(--tx);line-height:1.5}
.ai-path{font-size:10px;color:var(--mu2);font-family:monospace;margin-top:2px}
.ai-rec{padding:9px 12px;background:var(--s2);border:1px solid var(--bd);border-radius:6px;
  margin-bottom:5px;font-size:12px;color:var(--tx);display:flex;gap:10px;align-items:flex-start;line-height:1.5}
.ai-rec-arrow{color:var(--cyan);flex-shrink:0;font-weight:700;margin-top:1px}

/* ── Empty ── */
.empty{text-align:center;padding:48px 20px;color:var(--mu2);font-size:12px}

/* ── Scrollbar ── */
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:transparent;border-radius:3px;transition:background .2s}
*:hover::-webkit-scrollbar-thumb{background:var(--bd2)}
</style>
</head>
<body>
<div class="app">

<!-- Topbar -->
<div class="topbar">
  <div class="logo">
    <div class="logo-mark">◆</div>
    <span id="proj-name">Project</span>
  </div>
  <div class="topbar-tabs" id="tabs"></div>
  <div class="topbar-right">
    <div class="search-wrap">
      <span class="search-icon">⌕</span>
      <input class="search-box" id="search" placeholder="Search tasks…" oninput="onSearch(this.value)">
    </div>
    <div class="live"><div class="dot"></div>live</div>
    <div class="ts" id="ts">–</div>
  </div>
</div>

<!-- Progress strip -->
<div class="pstrip"><div class="pfill" id="pfill" style="width:0"></div></div>

<!-- Content area -->
<div class="content">
  <nav class="sidebar" id="sidebar"></nav>
  <div class="page" id="page"></div>
  <div class="resize-handle" id="resize-handle"></div>
  <div class="panel" id="panel">
    <div class="d-top">
      <div style="flex:1;min-width:0">
        <div class="d-id" id="d-id"></div>
        <div class="d-title" id="d-title"></div>
      </div>
      <button class="d-close" onclick="closeDetail()">✕</button>
    </div>
    <div class="d-meta" id="d-meta"></div>
    <div class="d-body" id="d-body"></div>
  </div>
</div>

</div>
<div class="copy-toast" id="toast">Copied!</div>
<script>
let view = localStorage.getItem('dash-view') || 'board', selId = null, snap = null, lastData = null;
let searchQ = '', featFilter = null, selPhase = null, selFeat = null;
let analysisResult = null, analysisDone = false, analysisRunning = false, analysisStreamBuf = '';

/* ── Parsers ── */
const fm = (t,k) => { const m=t&&t.match(new RegExp(`^${k}:\\s*(.+)`,'m')); return m?m[1].trim().replace(/^["']|["']$/g,''):''; };
const sec = (t,h) => { const m=t&&t.match(new RegExp(`## ${h}[\\s\\S]*?\\n([\\s\\S]*?)(?=\\n## |$)`)); return m?m[1].trim():''; };

function parseACs(t) {
  if (!t) return [];
  return [...t.matchAll(/\|\s*(AC\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(⬜|✅)\s*\|/g)]
    .map(r => ({id:r[1], title:r[2].trim(), done:r[4]==='✅'}));
}

function parseTasks(obj) {
  return Object.entries(obj||{}).map(([id,t]) => {
    const acs = parseACs(t);
    const dod = [...(t||'').matchAll(/- \[(x| )\] (.+)/gi)]
      .map(m => ({done: m[1].toLowerCase()==='x', text: m[2].trim()}));
    return {
      id, raw:t,
      title: fm(t,'title').replace(/^T\d+\s*[—–-]\s*/,'').replace(/\(.*?\)$/,'').trim(),
      status: fm(t,'status')||'todo',
      feature: fm(t,'feature'), phase: fm(t,'phase'),
      depends: fm(t,'depends_on').replace(/[\[\]]/g,'').trim(),
      ac_count: acs.length || parseInt(fm(t,'ac_count')||'0'),
      ac_done: acs.filter(a=>a.done).length, acs,
      desc: sec(t,'Description')||sec(t,'Goal'),
      instructions: sec(t,'Agent Instructions'),
      dod,
    };
  });
}

function filterTasks(tasks) {
  let out = tasks;
  if (featFilter) out = out.filter(t => t.feature === featFilter);
  if (searchQ)    out = out.filter(t =>
    t.title.toLowerCase().includes(searchQ) ||
    t.id.toLowerCase().includes(searchQ) ||
    (t.feature||'').toLowerCase().includes(searchQ)
  );
  return out;
}

function parseFeatures(yml) {
  const out=[]; let cur=null;
  for (const line of (yml||'').split('\n')) {
    const m=line.match(/^  ([\w-]+):\s*$/);
    if (m){cur={name:m[1]};out.push(cur);continue}
    if (cur){const kv=line.match(/^\s{4}(\w+):\s+(.+)/);if(kv)cur[kv[1]]=kv[2].replace(/#.*/,'').replace(/['"[\]]/g,'').trim()}
  }
  return out;
}

function badge(s) {
  return `<span class="badge b-${s||'todo'}">${(s||'todo').replace(/_/g,' ')}</span>`;
}

function pipColor(s) {
  return (s==='done'||s==='locked')?'var(--green)':s==='in_progress'?'var(--blue2)':s==='planned'?'var(--pur)':'var(--mu2)';
}

/* ── Tabs ── */
function renderTabs(tasks, blCount, health) {
  const hi = health && (health.errors + health.warns) > 0 ? (health.errors + health.warns) : '';
  const vs = [
    {id:'board',     label:'Board'},
    {id:'list',      label:'Tasks',     n:tasks.length},
    {id:'backlog',   label:'Backlog',   n:blCount||''},
    {id:'phases',    label:'Phases'},
    {id:'features',  label:'Features'},
    {id:'overview',  label:'Overview'},
    {id:'health',    label:'Health',    n:hi},
  ];
  const tabs = document.getElementById('tabs');
  tabs.innerHTML = vs.map(v =>
    `<div class="ttab${view===v.id?' on':''}" onclick="setView('${v.id}')">
      ${v.label}${v.n?`<span class="ttab-n">${v.n}</span>`:''}
    </div>`).join('') + '<div class="tab-ink" id="tab-ink"></div>';
  requestAnimationFrame(() => {
    const active = tabs.querySelector('.ttab.on');
    const ink = document.getElementById('tab-ink');
    if (active && ink) {
      ink.style.left = active.offsetLeft + 'px';
      ink.style.width = active.offsetWidth + 'px';
    }
  });
}

/* ── Sidebar ── */
function renderSidebar(tasks, features, acG, acT) {
  const sb = document.getElementById('sidebar');
  if (!sb) return;
  const hi = snap && JSON.parse(snap).health;
  const hiBadge = hi && (hi.errors+hi.warns)>0 ? (hi.errors+hi.warns) : '';
  const views = [
    {id:'board',     icon:'⊞', label:'Board'},
    {id:'list',      icon:'☰', label:'Tasks',     n:tasks.length},
    {id:'backlog',   icon:'○', label:'Backlog'},
    {id:'phases',    icon:'▤', label:'Phases'},
    {id:'features',  icon:'◈', label:'Features',  n:features.length},
    {id:'overview',  icon:'◎', label:'Overview'},
    {id:'health',    icon:'◉', label:'Health',     n:hiBadge},
  ];
  const navHtml = views.map(v=>`
    <div class="sb-item${view===v.id?' on':''}" onclick="setView('${v.id}')">
      <span class="sb-icon">${v.icon}</span>
      <span class="sb-label">${v.label}</span>
      ${v.n?`<span class="sb-badge">${v.n}</span>`:''}
    </div>`).join('');

  const done   = tasks.filter(t=>t.status==='done').length;
  const active = tasks.filter(t=>t.status==='in_progress').length;

  const featHtml = features.slice(0,8).map(f=>`
    <div class="sb-item${featFilter===f.name?' on':''}" style="font-size:11px" onclick="filterFeat('${f.name}')">
      <span class="sb-dot" style="background:${pipColor(f.status)}"></span>
      <span class="sb-label">${f.name}</span>
    </div>`).join('') || `<div style="padding:4px 14px;font-size:11px;color:var(--mu2)">No features</div>`;

  sb.innerHTML = `
    <div class="sb-sec">Views</div>
    ${navHtml}
    <div class="sb-sec" style="margin-top:6px">Features</div>
    ${featHtml}
    <div class="sb-foot">
      <div class="sb-row"><span class="sb-rl">Done</span><span class="sb-rv" style="color:var(--green)">${done}/${tasks.length}</span></div>
      <div class="sb-row"><span class="sb-rl">Active</span><span class="sb-rv" style="color:var(--blue2)">${active}</span></div>
      ${acT?`<div class="sb-row"><span class="sb-rl">ACs</span><span class="sb-rv" style="color:var(--cyan)">${acG}/${acT}</span></div>`:''}
    </div>`;
}

/* ── Phase bar ── */
function phaseBar(title, sub, acG, acT, status) {
  if (!title) return '';
  const pct = acT>0 ? Math.round(acG/acT*100) : 0;
  return `<div class="phasebar">
    <div class="phasebar-left">
      <div class="phasebar-title">${title}</div>
      <div class="phasebar-sub">${sub} ${badge(status)}</div>
      <div class="pbar-track"><div class="pbar-fill" style="width:${pct}%"></div></div>
    </div>
    ${acT?`<div class="phasebar-stats">
      <div class="stat"><div class="stat-n" style="color:var(--cyan)">${pct}%</div><div class="stat-l">Complete</div></div>
      <div class="stat"><div class="stat-n" style="color:var(--green)">${acG}</div><div class="stat-l">ACs green</div></div>
      <div class="stat"><div class="stat-n" style="color:var(--mu)">${acT}</div><div class="stat-l">ACs total</div></div>
    </div>`:''}
  </div>`;
}

function filterBar() {
  if (!featFilter && !searchQ) return '';
  return `<div class="filter-bar">
    ${featFilter?`<span class="filter-chip">◈ ${featFilter}<button onclick="filterFeat(null)">✕</button></span>`:''}
    ${searchQ?`<span class="filter-chip" style="background:#0d2040;color:var(--blue2);border-color:#1a3a70">⌕ "${searchQ}"<button style="color:var(--blue2)" onclick="clearSearch()">✕</button></span>`:''}
  </div>`;
}

/* ── Board ── */
function renderBoard(tasks) {
  tasks = filterTasks(tasks);
  const cols = [{key:'todo',label:'Todo',c:'var(--mu)'},{key:'in_progress',label:'In Progress',c:'var(--blue2)'},{key:'done',label:'Done',c:'var(--green)'}];
  if (tasks.some(t=>t.status==='blocked')) cols.push({key:'blocked',label:'Blocked',c:'var(--red)'});
  return filterBar()+`<div class="board" style="--cols:${cols.length}">${cols.map(col => {
    const ct = tasks.filter(t=>t.status===col.key);
    return `<div class="col" data-col="${col.key}" style="--col-c:${col.c}">
      <div class="col-head">
        <div class="col-pip" style="background:${col.c}"></div>
        <span class="col-name" style="color:${col.c}">${col.label}</span>
        <span class="col-ct">${ct.length}</span>
      </div>
      <div class="col-body">
        ${ct.map(t => {
          const pct = t.ac_count>0 ? Math.round(t.ac_done/t.ac_count*100) : -1;
          return `<div class="card${selId===t.id?' sel':''}" style="--card-c:${col.c}" onclick="selectTask('${t.id}')">
            <div class="cid">${t.id}</div>
            <div class="ctitle">${t.title||t.id}</div>
            ${pct>=0?`<div class="mbar"><div class="mfill" style="width:${pct}%"></div></div>`:''}
            <div class="cfoot">
              ${t.feature?`<span class="cfeat">${t.feature}</span>`:''}
              ${t.depends?`<span class="cdep">⛓ ${t.depends}</span>`:''}
              ${t.ac_count>0?`<span class="cac">${t.ac_done}/${t.ac_count} AC</span>`:''}
            </div>
          </div>`;
        }).join('')||`<div class="col-empty">Empty</div>`}
      </div>
    </div>`;
  }).join('')}</div>`;
}

/* ── List ── */
function renderList(tasks) {
  tasks = filterTasks(tasks);
  if (!tasks.length) return filterBar()+'<div class="empty">No tasks match</div>';
  return filterBar()+`<div class="tlist">${tasks.map(t=>`
    <div class="trow${selId===t.id?' sel':''}" onclick="selectTask('${t.id}')">
      <span class="tid">${t.id}</span>
      <span class="ttitle">${t.title||t.id}</span>
      ${badge(t.status)}
      ${t.feature?`<span class="cfeat">${t.feature}</span>`:''}
      ${t.ac_count>0?`<span class="tacs">${t.ac_done}/${t.ac_count}</span>`:''}
    </div>`).join('')}</div>`;
}

/* ── Phases ── */
function renderPhases(data) {
  const phases = data.phases || [];
  if (!phases.length) return '<div class="empty">No phases found in 06-phase/</div>';
  const done = phases.filter(p=>p.status==='locked').length;
  const rows = phases.slice().reverse().map(p=>{
    const active = p.id===data.active_phase;
    const nt = (p.tasks||[]).length;
    const icon = p.status==='locked' ? '🔒' : (p.status==='in_progress' ? '🟡' : '○');
    return `<div class="trow${selPhase===p.id?' sel':''}" onclick="selectPhase('${p.id}')">
      <span style="width:16px;text-align:center">${icon}</span>
      <span class="ttitle">${p.title}</span>
      ${badge(p.status)}
      <span class="tacs">${nt} task${nt===1?'':'s'}</span>
      ${active?'<span style="font-size:10px;color:var(--ac)">ACTIVE</span>':''}
    </div>`;
  }).join('');
  return `<div style="font-size:12px;color:var(--mu);margin:0 0 12px">${done} of ${phases.length} phases finished (locked)</div>
    <div class="tlist">${rows}</div>`;
}

/* ── Features ── */
function renderFeatures(features, tasks) {
  if (!features.length) return '<div class="empty">No features defined in 05-features/INDEX.yml</div>';
  return `<div class="tlist">${features.map(f=>{
    const ftasks = (tasks||[]).filter(t=>t.feature===f.name);
    const fdone  = ftasks.filter(t=>t.status==='done').length;
    return `<div class="trow${selFeat===f.name?' sel':''}" onclick="selectFeature('${f.name}')">
      <span class="feat-pip" style="background:${pipColor(f.status)};position:static;flex:none"></span>
      <span class="ttitle">${f.name}</span>
      ${f.status?badge(f.status):''}
      ${ftasks.length?`<span class="tacs">${fdone}/${ftasks.length}</span>`:''}
    </div>`;
  }).join('')}</div>`;
}

/* ── Overview ── */
function renderOverview(data, tasks, features, acG, acT, status, phaseTitle) {
  const done=tasks.filter(t=>t.status==='done').length;
  const inprog=tasks.filter(t=>t.status==='in_progress').length;
  const blocked=tasks.filter(t=>t.status==='blocked').length;
  const stats=[
    {n:done,    l:'Done',      c:'var(--green)'},
    {n:inprog,  l:'In Progress',c:'var(--blue2)'},
    {n:blocked, l:'Blocked',   c:'var(--red)'},
    {n:tasks.length,l:'Total Tasks',c:'var(--tx)'},
    {n:features.length,l:'Features',c:'var(--pur)'},
    {n:acT>0?Math.round(acG/acT*100)+'%':'—',l:'Phase Complete',c:'var(--cyan)'},
  ];
  return `
    ${phaseBar(phaseTitle, tasks.length+' tasks', acG, acT, status)}
    <div class="ov-grid">${stats.map(s=>`
      <div class="ov-card">
        <div class="ov-n" style="color:${s.c}">${s.n}</div>
        <div class="ov-l">${s.l}</div>
      </div>`).join('')}
    </div>
    ${data.vision?`<div style="margin-bottom:18px"><div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--mu);margin-bottom:10px">Vision</div><div class="md">${marked.parse(data.vision)}</div></div>`:''}
    ${data.decisions?`<div><div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--mu);margin-bottom:10px">Recent Decisions</div><div class="md">${marked.parse(data.decisions)}</div></div>`:''}`;
}

/* ── Right panel ── */
function renderDetail(tasks) {
  const t = tasks.find(t=>t.id===selId);
  const panel = document.getElementById('panel');
  if (!t) { panel.classList.remove('on'); return; }

  document.getElementById('d-id').innerHTML = `<span class="copy-id" title="Copy ID" onclick="copyId('${t.id}')">${t.id} ⎘</span>`;
  document.getElementById('d-title').textContent = t.title||t.id;
  document.getElementById('d-meta').innerHTML = `
    <div class="d-mi"><div class="d-ml">⬡ Status</div><div class="d-mv">${badge(t.status)}</div></div>
    <div class="d-mi"><div class="d-ml">◈ Feature</div><div class="d-mv">${t.feature?`<span class="cfeat">${t.feature}</span>`:'<span style="color:var(--mu2)">—</span>'}</div></div>
    <div class="d-mi"><div class="d-ml">⊙ Phase</div><div class="d-mv" style="color:var(--tx)">${t.phase||'—'}</div></div>
    <div class="d-mi"><div class="d-ml">✦ Progress</div><div class="d-mv">${t.ac_count>0?`${t.ac_done}/${t.ac_count} ACs`:'—'}</div></div>`;

  const acHtml = t.acs.length
    ? t.acs.map(a=>`<div class="ac${a.done?' ok':''}">
        <div class="ac-box">${a.done?'✓':''}</div>
        <div><div class="ac-id">${a.id}</div><div class="ac-lb">${marked.parseInline(a.title)}</div></div>
      </div>`).join('')
    : (t.ac_count>0
        ? Array.from({length:t.ac_count},(_,i)=>`<div class="ac"><div class="ac-box"></div><div><div class="ac-id">AC${i+1}</div></div></div>`).join('')
        : '');

  const dodHtml = t.dod.length ? t.dod.map(d=>`
    <div class="dod-item${d.done?' done':''}">
      <div class="dod-cb">${d.done?'✓':''}</div>
      <span>${marked.parseInline(d.text)}</span>
    </div>`).join('') : '';

  document.getElementById('d-body').innerHTML = `
    ${t.desc?`<div class="sec"><div class="sec-h">Description</div><div class="md" style="font-size:12px">${marked.parse(t.desc)}</div></div>`:''}
    ${acHtml?`<div class="sec">
      <div class="sec-h">Acceptance Criteria${t.ac_count>0?` · ${t.ac_done}/${t.ac_count} done`:''}</div>
      <div class="ac-list">${acHtml}</div>
    </div>`:''}
    ${dodHtml?`<div class="sec"><div class="sec-h">Definition of Done</div><div class="dod-list">${dodHtml}</div></div>`:''}
    ${t.instructions?`<div class="sec"><div class="sec-h">Agent Instructions</div><div class="md" style="font-size:12px">${marked.parse(t.instructions)}</div></div>`:''}`;

  panel.classList.add('on');
  const savedW = localStorage.getItem('dash-panel-w');
  if (savedW) panel.style.width = savedW;
}

function openPanel(idHtml, title, metaHtml, bodyHtml) {
  document.getElementById('d-id').innerHTML = idHtml;
  document.getElementById('d-title').textContent = title;
  document.getElementById('d-meta').innerHTML = metaHtml;
  document.getElementById('d-body').innerHTML = bodyHtml;
  const panel = document.getElementById('panel');
  panel.classList.add('on');
  const savedW = localStorage.getItem('dash-panel-w');
  if (savedW) panel.style.width = savedW;
}

/* Phase detail — overview of what tasks are in / done for a phase */
function renderPhaseDetail(data) {
  const p = (data.phases||[]).find(p=>p.id===selPhase);
  const panel = document.getElementById('panel');
  if (!p) { panel.classList.remove('on'); return; }
  const ts = p.tasks||[];
  const done = ts.filter(t=>t.status==='done'||p.status==='locked').length;
  const rowsHtml = ts.length ? ts.map(t=>{
    const ok = t.status==='done' || p.status==='locked';
    return `<div class="dod-item${ok?' done':''}">
      <div class="dod-cb">${ok?'✓':''}</div>
      <span><b style="color:var(--mu)">${t.id}</b> ${t.title.replace(/^T\d+\s*[—–-]\s*/,'')}</span>
    </div>`;
  }).join('') : '<div style="color:var(--mu2);font-size:12px">No task files.</div>';
  const meta = `
    <div class="d-mi"><div class="d-ml">⬡ Status</div><div class="d-mv">${badge(p.status)}</div></div>
    <div class="d-mi"><div class="d-ml">▤ Tasks</div><div class="d-mv" style="color:var(--tx)">${done}/${ts.length} done</div></div>`;
  const body = `
    ${p.goal?`<div class="sec"><div class="sec-h">Goal</div><div class="md" style="font-size:12px">${marked.parse(p.goal)}</div></div>`:''}
    <div class="sec"><div class="sec-h">Tasks · ${done}/${ts.length} done</div><div class="dod-list">${rowsHtml}</div></div>`;
  openPanel(`<span style="color:var(--mu)">${p.id}</span>`, p.title, meta, body);
}

/* Feature detail — business-context only */
function renderFeatureDetail(data) {
  const panel = document.getElementById('panel');
  let bc = (data.feature_bc||{})[selFeat];
  if (bc===undefined) { panel.classList.remove('on'); return; }
  bc = bc.replace(/^\s*---\n[\s\S]*?\n---\s*\n?/, '');  // strip YAML frontmatter
  const meta = `<div class="d-mi"><div class="d-ml">◈ Feature</div><div class="d-mv"><span class="cfeat">${selFeat}</span></div></div>`;
  const body = `<div class="sec"><div class="sec-h">Business context</div><div class="md" style="font-size:12px">${marked.parse(bc||'*No business-context.md*')}</div></div>`;
  openPanel(`<span style="color:var(--mu)">business-context</span>`, selFeat, meta, body);
}

/* ── Health ── */
function renderHealth(data) {
  const h = data.health;
  if (!h) return '<div class="empty">No health data</div>';
  const score = h.score;
  const scoreColor = score>=80?'var(--green)':score>=50?'var(--yel)':'var(--red)';
  const scoreHex   = score>=80?'#34a853':score>=50?'#fbbc04':'#ea4335';
  const grade      = score>=90?'A':score>=80?'B':score>=70?'C':score>=50?'D':'F';
  const gradeBg    = score>=80?'rgba(52,168,83,.18)':score>=50?'rgba(251,188,4,.18)':'rgba(234,67,53,.18)';

  /* SVG ring — r=52, circ≈326.7 */
  const R=52, circ=2*Math.PI*R, fill=(circ*score/100).toFixed(1);
  const ring = `<svg width="130" height="130" viewBox="0 0 130 130">
    <circle cx="65" cy="65" r="${R}" fill="none" stroke="var(--s3)" stroke-width="10"/>
    <circle cx="65" cy="65" r="${R}" fill="none" stroke="${scoreHex}" stroke-width="10"
      stroke-dasharray="${fill} ${circ.toFixed(1)}" stroke-linecap="round"
      transform="rotate(-90 65 65)" style="transition:stroke-dasharray .8s ease"/>
  </svg>`;

  const icons = {ok:'✓', warn:'!', error:'✕'};
  const checks = (h.checks||[]).map(c=>`
    <div class="hcheck ${c.status}">
      <div class="hcheck-icon">${icons[c.status]}</div>
      <div>
        <div class="hcheck-label">${c.label}</div>
        ${c.status!=='ok'&&c.detail?`<div class="hcheck-detail">${c.detail}</div>`:''}
      </div>
    </div>`).join('');

  /* button state */
  const btnDisabled = analysisRunning ? 'disabled' : '';
  const btnLabel    = analysisDone
    ? (analysisResult==='error' ? '✕ Failed — retry?' : '✓ Analysis done')
    : analysisRunning
    ? '<span class="h-btn-spin">◌</span> Analyzing context…'
    : '◉ Run Health Check';
  const btnStyle = analysisDone && analysisResult!=='error'
    ? 'background:linear-gradient(135deg,var(--s3),var(--s4));box-shadow:none;color:var(--mu);cursor:default'
    : '';

  /* analysis area */
  let analysisHtml = '';
  if (analysisRunning) {
    analysisHtml = `<div class="analysis-wrap">
      <div class="h-sec-hd">◉ Claude Analysis <span class="h-btn-spin" style="font-size:10px;margin-left:4px">◌</span></div>
      <div class="analysis-stream" id="astream">${analysisStreamBuf||'Connecting to Claude…'}</div>
    </div>`;
  } else if (analysisDone && analysisResult && analysisResult!=='error') {
    analysisHtml = renderAnalysisResult(analysisResult);
  } else if (analysisDone && analysisResult==='error') {
    analysisHtml = `<div class="analysis-wrap"><div style="color:var(--red);font-size:12px">
      Analysis failed — is <code style="font-size:11px">claude</code> CLI installed and authenticated?</div></div>`;
  }

  return `
    <div class="h-hero">
      <div class="h-ring-wrap">
        ${ring}
        <div class="h-ring-center">
          <div class="h-ring-num" style="color:${scoreColor}">${score}</div>
          <div class="h-ring-sub">/ 100</div>
          <div class="h-ring-grade" style="color:${scoreColor};background:${gradeBg}">${grade}</div>
        </div>
      </div>
      <div class="h-meta">
        <div class="h-counters">
          <div class="h-ct">
            <div class="h-ct-n" style="color:var(--green)">${h.ok}</div>
            <div class="h-ct-bar" style="background:var(--green)"></div>
            <div class="h-ct-l">Passing</div>
          </div>
          <div class="h-ct">
            <div class="h-ct-n" style="color:var(--yel)">${h.warns}</div>
            <div class="h-ct-bar" style="background:var(--yel)"></div>
            <div class="h-ct-l">Warnings</div>
          </div>
          <div class="h-ct">
            <div class="h-ct-n" style="color:var(--red)">${h.errors}</div>
            <div class="h-ct-bar" style="background:var(--red)"></div>
            <div class="h-ct-l">Errors</div>
          </div>
        </div>
        <button class="h-btn" ${btnDisabled} onclick="runAnalysis()" style="${btnStyle}">${btnLabel}</button>
      </div>
    </div>
    <div class="h-section">
      <div class="h-sec-hd">
        Context Checks
        <span style="color:var(--green)">✓ ${h.ok}</span>
        ${h.warns?`<span style="color:var(--yel)">! ${h.warns}</span>`:''}
        ${h.errors?`<span style="color:var(--red)">✕ ${h.errors}</span>`:''}
      </div>
      ${checks}
    </div>
    ${analysisHtml}`;
}

function renderAnalysisResult(r) {
  if (!r || r==='error') return '';
  const sc = r.score;
  const scColor = sc>=80?'var(--green)':sc>=50?'var(--yel)':'var(--red)';
  const scHex   = sc>=80?'#34a853':sc>=50?'#fbbc04':'#ea4335';
  const issues = (r.issues||[]).sort((a,b)=>
    ['error','warn','info'].indexOf(a.severity) - ['error','warn','info'].indexOf(b.severity));
  const issueHtml = issues.map(i=>`
    <div class="ai-issue ${i.severity||'info'}">
      <span class="ai-sev">${i.severity||'info'}</span>
      <div>
        <div class="ai-msg">${i.message}</div>
        ${i.path?`<div class="ai-path">${i.path}</div>`:''}
      </div>
    </div>`).join('');
  const recHtml = (r.recommendations||[]).map(rec=>`
    <div class="ai-rec"><span class="ai-rec-arrow">→</span><span>${rec}</span></div>`).join('');
  return `<div class="analysis-wrap">
    <div class="h-sec-hd">◉ Claude Analysis <span style="color:var(--mu2);font-size:9px;margin-left:4px">AI-powered · ${issues.length} issue${issues.length!==1?'s':''} found</span></div>
    ${r.summary?`<div class="ai-summary">${r.summary}</div>`:''}
    ${sc!==undefined?`<div class="ai-score-row">
      <span style="font-size:11px;color:var(--mu)">AI score:</span>
      <span class="ai-score-pill" style="background:${scHex}22;color:${scColor};border:1px solid ${scHex}44">${sc}/100</span>
    </div>`:''}
    ${issueHtml?`<div style="margin-bottom:14px">${issueHtml}</div>`:'<div style="color:var(--green);font-size:12px;margin-bottom:14px">✓ No issues found</div>'}
    ${recHtml?`<div><div class="h-sec-hd" style="margin-top:0">Recommendations</div>${recHtml}</div>`:''}
  </div>`;
}

function runAnalysis() {
  if (analysisRunning) return;
  if (analysisDone && analysisResult && analysisResult!=='error') return;
  analysisRunning = true;
  analysisStreamBuf = '';
  if (lastData) render(lastData);

  const src = new EventSource('/analyze');
  src.onmessage = e => {
    const d = JSON.parse(e.data);
    const el = document.getElementById('astream');
    if (d.msg !== undefined) {
      analysisStreamBuf += '▸ ' + d.msg + '\n';
      if (el) { el.textContent = analysisStreamBuf; el.scrollTop = el.scrollHeight; }
    }
    if (d.chunk !== undefined) {
      analysisStreamBuf += d.chunk;
      if (el) { el.textContent = analysisStreamBuf; el.scrollTop = el.scrollHeight; }
    }
    if (d.error) {
      src.close();
      analysisRunning = false; analysisDone = true; analysisResult = 'error';
      analysisStreamBuf += '\n✕ Error: ' + d.error;
      if (lastData) render(lastData);
    }
    if (d.done) {
      src.close();
      analysisRunning = false; analysisDone = true;
      try {
        const m = d.result.match(/\{[\s\S]*\}/);
        analysisResult = m ? JSON.parse(m[0]) : null;
      } catch(_) { analysisResult = null; }
      if (lastData) render(lastData);
    }
  };
  src.onerror = () => {
    src.close();
    analysisRunning = false; analysisDone = true; analysisResult = 'error';
    if (lastData) render(lastData);
  };
}

/* ── Render ── */
function render(data) {
  lastData = data;
  document.getElementById('ts').textContent = new Date().toLocaleTimeString();

  const tasks    = parseTasks(data.tasks);
  const features = parseFeatures(data.features_yml);
  const ptitle   = fm(data.phase,'title') || '';
  const acT      = parseInt(fm(data.phase,'ac_total')||'0');
  const acG      = parseInt(fm(data.phase,'ac_green')||'0');
  const status   = fm(data.phase,'status')||'';
  const blRows   = (data.backlog||'').split('\n').filter(l => /^\|\s*\d/.test(l));

  const pm = ptitle.match(/phase[- ]?0*(\d+)/i);
  document.getElementById('proj-name').textContent = pm ? `Phase ${pm[1]}` : (ptitle || 'Project');
  document.getElementById('pfill').style.width = (acT>0?acG/acT*100:0)+'%';

  renderTabs(tasks, blRows.length, data.health);
  renderSidebar(tasks, features, acG, acT);

  const inprog = tasks.filter(t=>t.status==='in_progress').length;
  const sub = `${tasks.length} task${tasks.length!==1?'s':''} · ${inprog} in progress`;

  let html = '';
  if (view==='board')       html = phaseBar(ptitle, sub, acG, acT, status) + renderBoard(tasks);
  else if(view==='list')    html = phaseBar(ptitle, sub, acG, acT, status) + renderList(tasks);
  else if(view==='backlog') html = `<div class="md">${marked.parse(data.backlog||'*No backlog.*')}</div>`;
  else if(view==='phases')  html = renderPhases(data);
  else if(view==='features') html = renderFeatures(features, tasks);
  else if(view==='health')   html = renderHealth(data);
  else html = renderOverview(data, tasks, features, acG, acT, status, ptitle);

  document.getElementById('page').innerHTML = html;
  if (selId) renderDetail(tasks);
  else if (selPhase) renderPhaseDetail(data);
  else if (selFeat) renderFeatureDetail(data);
}

function setView(v) {
  view = v;
  localStorage.setItem('dash-view', v);
  if (lastData) render(lastData);
}

function onSearch(q) {
  searchQ = q.toLowerCase().trim();
  if (lastData && (view==='board'||view==='list')) render(lastData);
}

function clearSearch() {
  searchQ = '';
  document.getElementById('search').value = '';
  if (lastData) render(lastData);
}

function filterFeat(name) {
  featFilter = featFilter===name ? null : name;
  if (view!=='board' && view!=='list') view = 'board';
  if (lastData) render(lastData);
}

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    if (selId || selPhase || selFeat) closeDetail();
    else if (searchQ) clearSearch();
    else if (featFilter) filterFeat(null);
  }
});

function selectTask(id) {
  selId = selId===id ? null : id;
  selPhase = null; selFeat = null;
  if (lastData) {
    renderDetail(parseTasks(lastData.tasks));
    document.querySelectorAll('.card,.trow').forEach(el => {
      const eid = el.getAttribute('onclick')?.match(/'([^']+)'/)?.[1];
      el.classList.toggle('sel', eid===selId);
    });
  }
}

function selectPhase(id) {
  selPhase = selPhase===id ? null : id;
  selId = null; selFeat = null;
  if (lastData) render(lastData);
}

function selectFeature(name) {
  selFeat = selFeat===name ? null : name;
  selId = null; selPhase = null;
  if (lastData) render(lastData);
}

function closeDetail() {
  selId = null; selPhase = null; selFeat = null;
  const panel = document.getElementById('panel');
  panel.classList.remove('on');
  panel.style.width = '';
  document.querySelectorAll('.card,.trow,.feat-card').forEach(el=>el.classList.remove('sel'));
}

/* ── Resize panel ── */
(function(){
  const handle = document.getElementById('resize-handle');
  const panel  = document.getElementById('panel');
  let dragging = false, startX = 0, startW = 0;

  handle.addEventListener('mousedown', e => {
    if (!panel.classList.contains('on')) return;
    dragging = true;
    startX = e.clientX;
    startW = panel.offsetWidth;
    panel.classList.add('resizing');
    handle.classList.add('dragging');
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
    e.preventDefault();
  });

  document.addEventListener('mousemove', e => {
    if (!dragging) return;
    const delta = startX - e.clientX;          // drag left = wider
    const w = Math.min(700, Math.max(220, startW + delta));
    panel.style.width = w + 'px';
  });

  document.addEventListener('mouseup', () => {
    if (!dragging) return;
    dragging = false;
    panel.classList.remove('resizing');
    handle.classList.remove('dragging');
    document.body.style.cursor = '';
    document.body.style.userSelect = '';
    if (panel.style.width) localStorage.setItem('dash-panel-w', panel.style.width);
  });

  // Show/hide handle with panel
  const obs = new MutationObserver(() => {
    handle.style.display = panel.classList.contains('on') ? 'block' : 'none';
  });
  obs.observe(panel, { attributes: true, attributeFilter: ['class'] });
})();

/* ── Copy task ID ── */
function copyId(id) {
  navigator.clipboard.writeText(id).catch(()=>{});
  const t = document.getElementById('toast');
  t.style.opacity = '1';
  setTimeout(() => t.style.opacity = '0', 1500);
}

/* ── Click outside panel to close ── */
document.getElementById('page').addEventListener('click', e => {
  if (selId && !e.target.closest('.card') && !e.target.closest('.trow')) closeDetail();
});

/* ── Restore panel width ── */
(function(){
  const w = localStorage.getItem('dash-panel-w');
  if (w) document.getElementById('panel').style.setProperty('--saved-w', w);
})();

/* ── Poll ── */
async function poll() {
  const live = document.querySelector('.live');
  try {
    const data = await (await fetch('/data')).json();
    if (live) live.classList.remove('stale');
    const s = JSON.stringify(data);
    if (s===snap) { document.getElementById('ts').textContent=new Date().toLocaleTimeString(); return; }
    snap=s; render(data);
  } catch(_) {
    if (live) live.classList.add('stale');
  }
}
poll(); setInterval(poll,3000);
</script>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_): pass
    def do_GET(self):
        if self.path == "/data":
            body = json.dumps(collect()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/analyze":
            import shutil, os, subprocess
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            def evt(**kw):
                self.wfile.write(f"data: {json.dumps(kw)}\n\n".encode())
                self.wfile.flush()
            try:
                evt(msg="Reading context files…")
                prompt = _build_analyze_prompt()
                n_files = prompt.count("=== ")
                evt(msg=f"Collected {n_files} context files ({len(prompt)//1000}k chars)")

                extra = [os.path.expanduser("~/.local/bin"), "/usr/local/bin",
                         "/opt/homebrew/bin", "/opt/homebrew/sbin"]
                env = {**os.environ, "PATH": os.environ.get("PATH","") + ":" + ":".join(extra)}
                claude_bin = shutil.which("claude", path=env["PATH"])

                if not claude_bin:
                    evt(error="claude CLI not found — checked PATH + ~/.local/bin + /usr/local/bin + /opt/homebrew/bin")
                    return

                evt(msg=f"Found Claude at {claude_bin}")
                evt(msg="Sending context to Claude for deep analysis…")

                proc = subprocess.Popen(
                    [claude_bin, "-p", prompt],
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, cwd=str(ROOT), env=env
                )

                evt(msg="Claude is thinking…\n")
                buf = ""
                while True:
                    chunk = proc.stdout.read(128)
                    if not chunk:
                        break
                    buf += chunk
                    evt(chunk=chunk)
                proc.wait()

                evt(msg="\nParsing results…")
                evt(done=True, result=buf.strip())
            except Exception as e:
                evt(error=str(e))
        else:
            body = HTML.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(body)


if __name__ == "__main__":
    threading.Thread(
        target=lambda: (time.sleep(0.8), webbrowser.open(f"http://localhost:{PORT}")),
        daemon=True
    ).start()
    print(f"Dashboard → http://localhost:{PORT}  (Ctrl+C to stop)")
    HTTPServer(("", PORT), Handler).serve_forever()
