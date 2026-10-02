#!/usr/bin/env python3
"""Look up Freesound sounds by id (or link) or by a search, and fetch their previews with a metadata file each.

Standard library only. Nothing is downloaded without --fetch. Files land in
zombie-radio-datasets/sounds/freesound/<kind>/<id>-<slug>.mp3 + .json, a folder beside this repository's checkout,
outside git; each fetch writes a page of players, zombie-radio-datasets/sounds/pages/index-<start time>.html.

The API key is read from ~/.config/zombie-radio/freesound.key and sent in a header, never printed, never in a URL.
Requests are paced (--pause seconds apart); Freesound allows 60 a minute and 2,000 a day.

  python3 tools/sounds/fetch_freesound.py --kind radio-static --ids 11859,https://freesound.org/people/x/sounds/719588/
  python3 tools/sounds/fetch_freesound.py --kind radio-static --ids-file picks.txt                (a dry run)
  python3 tools/sounds/fetch_freesound.py --kind radio-static --ids-file picks.txt --fetch
  python3 tools/sounds/fetch_freesound.py --kind radio-static --search "shortwave radio static" --duration 20-240
"""

import argparse
import hashlib
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

API = "https://freesound.org/apiv2"
KEY_FILE = Path.home() / ".config" / "zombie-radio" / "freesound.key"
USER_AGENT = "zombie-radio-freesound-fetch/0.1 (+https://github.com/alfre2v/zombie-radio)"
DEFAULT_OUT = Path(__file__).resolve().parents[2].parent / "zombie-radio-datasets" / "sounds"
PREVIEW = "preview-hq-mp3"
FIELDS = ("id,name,username,url,license,duration,samplerate,channels,bitdepth,type,filesize,tags,description,"
          "avg_rating,num_ratings,created,previews")
LICENCES = {"cc0": 'license:"Creative Commons 0"', "cc-by": 'license:"Attribution"'}
KIND = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


class Stats:
    requests = 0
    transferred = 0


class Pacer:
    def __init__(self, pause):
        self.pause = pause
        self.last = 0.0

    def wait(self):
        delay = self.last + self.pause - time.monotonic()
        if delay > 0:
            time.sleep(delay)
        self.last = time.monotonic()


def read_key():
    try:
        key = KEY_FILE.read_text(encoding="utf-8").strip()
    except OSError as e:
        sys.exit(f"cannot read the API key file {KEY_FILE}: {e.strerror}")
    if not key:
        sys.exit(f"the API key file {KEY_FILE} is empty")
    return key


def _open(pacer, url, headers=None, method="GET"):
    pacer.wait()
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})}, method=method)
    try:
        resp = urllib.request.urlopen(req, timeout=60)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            sys.exit("Freesound says too many requests (HTTP 429): stop, wait, and run again later")
        sys.exit(f"HTTP {e.code} from {url.split('?')[0]}")
    Stats.requests += 1
    return resp


def api_json(pacer, key, path, params):
    url = f"{API}/{path}?{urllib.parse.urlencode(params)}"
    with _open(pacer, url, {"Authorization": f"Token {key}"}) as resp:
        data = resp.read()
    Stats.transferred += len(data)
    return json.loads(data)


def parse_ids(items):
    ids = []
    for item in items:
        item = item.strip()
        if not item or item.startswith("#"):
            continue
        m = re.search(r"/sounds/(\d+)", item) or re.fullmatch(r"(\d+)", item)
        if not m:
            sys.exit(f"not a Freesound id or sound link: {item}")
        if int(m.group(1)) not in ids:
            ids.append(int(m.group(1)))
    return ids


def by_ids(pacer, key, ids):
    found = {}
    for start in range(0, len(ids), 50):
        chunk = ids[start:start + 50]
        params = {"filter": "id:(%s)" % " OR ".join(map(str, chunk)), "fields": FIELDS, "page_size": 150}
        for s in api_json(pacer, key, "search/text/", params)["results"]:
            found[s["id"]] = s
    missing = [i for i in ids if i not in found]
    for i in missing:
        print(f"{i}: not found on Freesound (removed, or a wrong id)")
    return [found[i] for i in ids if i in found]


def by_search(pacer, key, query, licence, duration, limit):
    filters = []
    if licence:
        filters.append(LICENCES[licence])
    if duration:
        lo, _, hi = duration.partition("-")
        filters.append(f"duration:[{float(lo)} TO {float(hi or lo)}]")
    params = {"query": query, "filter": " ".join(filters), "sort": "rating_desc", "fields": FIELDS,
              "page_size": min(limit, 150)}
    data = api_json(pacer, key, "search/text/", params)
    print(f'search "{query}" ({" ".join(filters) or "no filter"}): {data["count"]} matches; '
          f"the {min(limit, len(data['results']))} best rated")
    return data["results"][:limit]


def licence_info(s):
    url = s["license"]
    low = url.lower()
    version = re.search(r"/(\d+\.\d+)/?$", url)
    v = f" {version.group(1)}" if version else ""
    if "publicdomain/zero" in low:
        cls, name = "cc0", f"CC0{v}"
    elif "/by-nc" in low:
        cls, name = "cc-by-nc", f"CC BY-NC{v}"
    elif "/by/" in low:
        cls, name = "cc-by", f"CC BY{v}"
    elif "sampling+" in low:
        cls, name = "sampling-plus", f"Sampling+{v}"
    else:
        cls, name = "other", url
    credit = None
    if cls != "cc0":
        credit = f'"{s["name"]}" by {s["username"]} ({s["url"]}), licensed under {name} ({url})'
    return {"name": name, "url": url, "class": cls, "credit": credit}


def slug(name):
    text = re.sub(r"\.(wav|mp3|ogg|flac|aif|aiff|m4a)$", "", name, flags=re.I)
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text[:60].rstrip("-") or "sound"


def preview_size(pacer, url):
    with _open(pacer, url, method="HEAD") as resp:
        return int(resp.headers.get("Content-Length", 0))


def metadata(s, kind, size, digest, fetched_at):
    return {
        "source": "freesound",
        "id": s["id"],
        "page": s["url"],
        "name": s["name"],
        "author": s["username"],
        "author_page": f"https://freesound.org/people/{urllib.parse.quote(s['username'])}/",
        "licence": licence_info(s),
        "file": {"is": PREVIEW, "url": s["previews"][PREVIEW], "bytes": size, "sha256": digest,
                 "downloaded": fetched_at},
        "original": {"type": s.get("type"), "bytes": s.get("filesize"), "seconds": s.get("duration"),
                     "rate": s.get("samplerate"), "channels": s.get("channels"), "bitdepth": s.get("bitdepth")},
        "rating": {"average": s.get("avg_rating"), "count": s.get("num_ratings")},
        "uploaded": s.get("created"),
        "tags": s.get("tags", []),
        "description": s.get("description", ""),
        "ours": {"kind": kind, "verdict": None, "notes": ""},
    }


def show(s, size, state):
    lic = licence_info(s)["name"]
    rating = f"{s['avg_rating']:.1f} ({s['num_ratings']})" if s.get("num_ratings") else "unrated"
    original = f"{s.get('type', '?').upper()} {s.get('samplerate') or 0:g} Hz {s.get('channels', '?')} ch"
    print(f"{s['id']:>7}  {s['name'][:44]:44}  {s['username'][:18]:18}  {lic:13}  {s['duration']:6.1f} s  "
          f"{rating:10}  {original:22}  preview {size / 1024:6.0f} KB  {state}")


def already_here(target):
    meta = target.with_suffix(".json")
    if not (target.exists() and meta.exists()):
        return None
    recorded = json.loads(meta.read_text(encoding="utf-8"))["file"]
    data = target.read_bytes()
    if len(data) == recorded["bytes"] and hashlib.sha256(data).hexdigest() == recorded["sha256"]:
        return len(data)
    return None


def run(sounds, kind, out, pacer, do_fetch):
    started = datetime.now()
    folder = out / "freesound" / kind
    plan_bytes = 0
    done = []
    for s in sounds:
        stem = f"{s['id']}-{slug(s['name'])}"
        target = folder / f"{stem}.mp3"
        size = already_here(target)
        if size is not None:
            show(s, size, "(already here)")
            done.append((s, target))
            continue
        if not do_fetch:
            size = preview_size(pacer, s["previews"][PREVIEW])
            plan_bytes += size
            show(s, size, "(would fetch)")
            continue
        folder.mkdir(parents=True, exist_ok=True)
        with _open(pacer, s["previews"][PREVIEW]) as resp:
            data = resp.read()
        Stats.transferred += len(data)
        plan_bytes += len(data)
        tmp = target.with_suffix(".part")
        tmp.write_bytes(data)
        tmp.replace(target)
        fetched_at = datetime.now().isoformat(timespec="seconds")
        meta = metadata(s, kind, len(data), hashlib.sha256(data).hexdigest(), fetched_at)
        target.with_suffix(".json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        show(s, len(data), "fetched")
        done.append((s, target))
    seconds = sum(s["duration"] for s in sounds)
    classes = {}
    for s in sounds:
        cls = licence_info(s)["class"]
        classes[cls] = classes.get(cls, 0) + 1
    print(f"\n{len(sounds)} sounds, {seconds / 60:.1f} minutes in all; licences: "
          + ", ".join(f"{c} {n}" for c, n in sorted(classes.items())))
    print(f"{'fetched' if do_fetch else 'would fetch'}: {plan_bytes / 1e6:.2f} MB")
    if do_fetch and done:
        write_page(out, kind, done, started)


def page_path(pages, started):
    stamp = started.strftime("%Y-%m-%dT%H:%M:%S")
    path, n = pages / f"index-{stamp}.html", 1
    while path.exists():
        n += 1
        path = pages / f"index-{stamp}-{n}.html"
    return path


def write_page(out, kind, done, started):
    pages = out / "pages"
    pages.mkdir(parents=True, exist_ok=True)
    rows = []
    for s, target in done:
        lic = licence_info(s)
        rel = target.relative_to(out).as_posix()
        rows.append(
            f"<tr><td><a href=\"{html.escape(s['url'])}\">{s['id']}</a></td>"
            f"<td>{html.escape(s['name'])}<br><small>{html.escape(s['username'])}</small></td>"
            f"<td><a href=\"{html.escape(lic['url'])}\">{html.escape(lic['name'])}</a></td>"
            f"<td>{s['duration']:.1f} s</td>"
            f"<td><audio controls preload=\"none\" src=\"../{html.escape(rel)}\"></audio></td></tr>")
    page = ("<!doctype html><meta charset=utf-8><title>Freesound previews</title>"
            "<style>body{font-family:sans-serif}td,th{padding:6px;border-bottom:1px solid #ddd;text-align:left}"
            "small{color:#555}</style>"
            f"<p>Freesound previews ({PREVIEW}), kind <b>{html.escape(kind)}</b>, fetched "
            f"{started.strftime('%Y-%m-%d %H:%M')}. Each file's licence and credit line are in its .json.</p>"
            "<table><tr><th>id</th><th>name, author</th><th>licence</th><th>length</th><th>preview</th></tr>"
            f"{''.join(rows)}</table>")
    path = page_path(pages, started)
    path.write_text(page, encoding="utf-8")
    print(f"page: {path}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--kind", required=True, help="the folder under freesound/, in our words, e.g. radio-static")
    p.add_argument("--ids", help="comma-separated Freesound ids or sound links")
    p.add_argument("--ids-file", type=Path, help="a file of ids or links, one per line (# comments allowed)")
    p.add_argument("--search", help="a text search instead of ids")
    p.add_argument("--license", choices=sorted(LICENCES), help="with --search: only this licence")
    p.add_argument("--duration", help="with --search: a range in seconds, e.g. 20-240")
    p.add_argument("--max", type=int, default=15, help="with --search: how many of the best rated (default 15)")
    p.add_argument("--pause", type=float, default=2.0, help="seconds between requests (default 2)")
    p.add_argument("--fetch", action="store_true", help="download; without it, only show what would be fetched")
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = p.parse_args()
    sys.stdout.reconfigure(line_buffering=True)

    if not KIND.match(args.kind):
        sys.exit("--kind must be kebab-case, e.g. radio-static")
    items = []
    if args.ids:
        items += args.ids.split(",")
    if args.ids_file:
        items += args.ids_file.read_text(encoding="utf-8").splitlines()
    if bool(items) == bool(args.search):
        sys.exit("give ids (--ids or --ids-file) or a --search, not both")

    key = read_key()
    pacer = Pacer(args.pause)
    if items:
        sounds = by_ids(pacer, key, parse_ids(items))
    else:
        sounds = by_search(pacer, key, args.search, args.license, args.duration, args.max)
    run(sounds, args.kind, args.out, pacer, args.fetch)
    print(f"\n[{Stats.requests} requests, {Stats.transferred / 1e6:.3f} MB transferred]")


if __name__ == "__main__":
    main()
