"""Build an audition page for the ambience's takes: one row per prompt, each take with keep / drop, a summary to copy.

  uv run python tools/sounds/ambience_page.py tools/sounds/ambience.yaml \\
      /Users/alfredo/workspace/hackTNT_2026/zombie-radio-datasets/ambience/round1
The page is written into the takes' folder as index.html; ratings stay in the browser.
"""

import html
import json
import sys
from pathlib import Path

import yaml

PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Ambience audition</title>
<style>
:root{--bg:#fafaf7;--fg:#1d1d1b;--muted:#6b6b66;--line:#ddd9cf;--card:#fff;--accent:#b4441c}
@media (prefers-color-scheme:dark){:root{--bg:#161614;--fg:#ecebe6;--muted:#9a9890;--line:#33322e;--card:#1f1f1c;--accent:#ef8a5a}}
body{background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,sans-serif;margin:0 auto;padding:20px 16px 60px;max-width:1000px}
h1{font-size:22px;margin:0 0 4px} p.lead{color:var(--muted)} h2{font-size:15px;margin:22px 0 8px;color:var(--accent)}
.row{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 14px;margin-bottom:8px}
.tag{font-weight:600} .kind{color:var(--muted);font-size:13px} .prompt{color:var(--muted);font-size:13px;margin:2px 0 6px}
.take{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:4px 0} audio{width:100%;max-width:420px;height:32px}
label{font-size:13px;white-space:nowrap} textarea{width:100%;box-sizing:border-box;height:200px;background:var(--card);color:var(--fg);
border:1px solid var(--line);border-radius:6px;font:13px ui-monospace,monospace;padding:8px} button{font:inherit;padding:6px 12px;margin:8px 8px 0 0}
</style></head><body><h1>Ambience audition</h1>
<p class="lead">Each take: <b>keep</b> or <b>drop</b>. Ratings stay in this browser; copy the summary at the bottom.</p>
<div id="rows"></div><h2>Summary</h2><textarea id="summary" readonly></textarea><br>
<button id="copy">Copy</button><button id="clear">Clear all</button>
<script>
const DATA = __DATA__, KEY = "ambience-" + __KEY__;
let marks = {}; try { marks = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) {}
function save() { try { localStorage.setItem(KEY, JSON.stringify(marks)); } catch (e) {} summarize(); }
function summarize() {
  const keep = [], drop = [], open = [];
  for (const x of DATA) for (const s of x.seeds) { const id = `${x.tag}/${s}`; (marks[id] === "keep" ? keep : marks[id] === "drop" ? drop : open).push(id); }
  document.getElementById("summary").value = `keep (${keep.length}): ${keep.join(", ")}\\ndrop (${drop.length}): ${drop.join(", ")}\\nnot rated (${open.length}): ${open.join(", ")}`;
}
let group = "";
const rows = document.getElementById("rows");
for (const x of DATA) {
  if (x.group !== group) { group = x.group; const h = document.createElement("h2"); h.textContent = group; rows.append(h); }
  const row = document.createElement("div"); row.className = "row";
  row.innerHTML = `<span class="tag">${x.tag}</span> <span class="kind">· ${x.kind} · ${x.seconds} s</span><div class="prompt">${x.prompt}</div>`;
  for (const s of x.seeds) {
    const id = `${x.tag}/${s}`, take = document.createElement("div"); take.className = "take";
    const a = document.createElement("audio"); a.controls = true; a.preload = "metadata"; a.src = `${x.tag}/sa3-${s}.wav`;
    take.append(`seed ${s} `, a);
    for (const m of ["keep", "drop"]) {
      const l = document.createElement("label"), i = document.createElement("input");
      i.type = "radio"; i.name = id; i.value = m; i.checked = marks[id] === m; i.onchange = () => { marks[id] = m; save(); };
      l.append(i, " " + m); take.append(l);
    }
    row.append(take);
  }
  rows.append(row);
}
document.getElementById("copy").onclick = () => { const t = document.getElementById("summary"); t.select(); try { navigator.clipboard.writeText(t.value); } catch (e) { document.execCommand("copy"); } };
document.getElementById("clear").onclick = () => { if (confirm("Clear every mark?")) { marks = {}; save(); location.reload(); } };
summarize();
</script></body></html>
"""

def group_of(x):
    if x["tag"].startswith("dead-"):
        return f"The dead — {x['kind']}s"
    if x["tag"].startswith(("gun", "explosion", "grenade")):
        return "Fighting — spots"
    if x["kind"] == "spot":
        return "People — spots"
    return "The city — textures"


def main():
    prompts = yaml.safe_load(Path(sys.argv[1]).read_text())["prompts"]
    takes = Path(sys.argv[2])
    data = []
    for x in prompts:
        found = sorted(int(w.stem.split("-")[1]) for w in (takes / x["tag"]).glob("sa3-*.wav"))
        if found:
            data.append({**{k: html.escape(str(v)) for k, v in x.items()}, "seeds": found, "group": group_of(x)})
    page = PAGE.replace("__DATA__", json.dumps(data)).replace("__KEY__", json.dumps(takes.name))
    (takes / "index.html").write_text(page)
    print(f"{takes / 'index.html'}: {len(data)} prompts, {sum(len(x['seeds']) for x in data)} takes")


if __name__ == "__main__":
    main()
