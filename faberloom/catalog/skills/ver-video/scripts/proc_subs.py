"""Extrae meta.json, desc.txt y transcript.txt del volcado de yt-dlp.
Parte de la skill ver-video (MWT). Sin dependencias externas: solo stdlib.
Uso: python proc_subs.py <dir>
"""
import json, os, re, sys

d = sys.argv[1]

info = os.path.join(d, "v.info.json")
if os.path.exists(info):
    j = json.load(open(info, encoding="utf-8"))
    meta = {k: j.get(k) for k in (
        "title", "channel", "uploader", "upload_date",
        "duration", "view_count", "like_count", "webpage_url")}
    meta["chapters"] = [
        {"t": c.get("start_time"), "title": c.get("title")}
        for c in (j.get("chapters") or [])
    ]
    with open(os.path.join(d, "meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    with open(os.path.join(d, "desc.txt"), "w", encoding="utf-8") as fh:
        fh.write(j.get("description") or "")


def rank(name):
    for i, p in enumerate((".en.", ".en-orig.", ".es.", ".pt.")):
        if p in name:
            return i
    return 9


lines = []
cands = [f for f in os.listdir(d) if f.endswith(".vtt")]
if cands:
    vtt = os.path.join(d, sorted(cands, key=rank)[0])
    ts = last = None
    seen = set()
    for raw in open(vtt, encoding="utf-8").read().splitlines():
        m = re.match(r"(\d\d:\d\d:\d\d)\.\d+ -->", raw)
        if m:
            ts = m.group(1)
            continue
        if not raw.strip() or raw.startswith(("WEBVTT", "Kind:", "Language:")):
            continue
        t = re.sub(r"<[^>]+>", "", raw).strip()
        if not t or t == last or t in seen:
            continue
        last = t
        seen.add(t)
        lines.append("[%s] %s" % (ts, t))

with open(os.path.join(d, "transcript.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))

print(len(lines))
