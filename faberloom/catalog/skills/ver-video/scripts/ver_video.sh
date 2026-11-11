#!/usr/bin/env bash
# ver_video.sh - Descarga un video, extrae subtitulos y fotogramas de cambio de escena.
# Parte de la skill "ver-video". Sin repos de terceros, sin API keys.
# Dependencias: yt-dlp (o python -m yt_dlp) y ffmpeg.
# Uso: bash ver_video.sh --url "<URL>" [--max-frames 40] [--scene 0.30] [--keep]

set -uo pipefail

URL=""; MAX_FRAMES=40; SCENE=0.30; KEEP=0

while [ $# -gt 0 ]; do
  case "$1" in
    --url)        URL="$2"; shift 2 ;;
    --max-frames) MAX_FRAMES="$2"; shift 2 ;;
    --scene)      SCENE="$2"; shift 2 ;;
    --keep)       KEEP=1; shift ;;
    *) echo "Parametro desconocido: $1" >&2; exit 2 ;;
  esac
done
[ -n "$URL" ] || { echo "Falta --url" >&2; exit 2; }

if command -v yt-dlp >/dev/null 2>&1; then YTDLP=(yt-dlp); else YTDLP=(python3 -m yt_dlp); fi
command -v ffmpeg >/dev/null 2>&1 || { echo "Falta ffmpeg" >&2; exit 2; }

ROOT="${TMPDIR:-/tmp}/ver-video"
mkdir -p "$ROOT"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

status() { printf '%s\n' "$2" > "$1/STATUS.txt"; }

ID="$("${YTDLP[@]}" --skip-download --print '%(id)s' --no-warnings "$URL" 2>/dev/null | head -n1)"
if [ -z "$ID" ]; then
  echo "ERROR: no se pudo resolver el ID del video" > "$ROOT/STATUS.txt"; exit 1
fi
ID="$(printf '%s' "$ID" | tr -c 'A-Za-z0-9_-' '_')"

DIR="$ROOT/$ID"; FRAMES="$DIR/frames"
mkdir -p "$FRAMES"; rm -f "$FRAMES"/*.jpg 2>/dev/null

status "$DIR" "RUNNING - resolviendo metadatos ($ID)"

# Subtitulos: best-effort. Un 429 o la ausencia de subs NO aborta el analisis visual.
"${YTDLP[@]}" --skip-download --ignore-errors --no-abort-on-error --sleep-requests 1 \
  --write-auto-sub --write-sub --sub-lang "en.*,es.*,pt.*" --sub-format vtt \
  --write-info-json --no-warnings \
  -o "$DIR/v.%(ext)s" "$URL" > "$DIR/_ytdlp_meta.log" 2>&1

status "$DIR" "RUNNING - descargando video"

"${YTDLP[@]}" --no-warnings \
  -f "bv*[height<=480][ext=mp4]/bv*[height<=480]/b[height<=480]" \
  -o "$DIR/v.mp4" "$URL" > "$DIR/_ytdlp_video.log" 2>&1

if [ ! -f "$DIR/v.mp4" ]; then
  status "$DIR" "ERROR: la descarga no produjo v.mp4 - ver _ytdlp_video.log"; exit 1
fi

status "$DIR" "RUNNING - procesando metadatos y subtitulos"
SUBLINES="$(python3 "$HERE/proc_subs.py" "$DIR" 2>&1 | tail -n1)"

status "$DIR" "RUNNING - extrayendo fotogramas"
ffmpeg -hide_banner -loglevel info -i "$DIR/v.mp4" \
  -vf "select='gt(scene,$SCENE)',showinfo,scale=900:-2" \
  -fps_mode vfr -q:v 4 "$FRAMES/f_%03d.jpg" 2> "$DIR/_ffmpeg.log"

# timestamps de showinfo -> frames_index.txt (y descarte parejo si sobran)
python3 - "$DIR" "$MAX_FRAMES" <<'PY'
import os, re, sys
d, maxf = sys.argv[1], int(sys.argv[2])
frames = os.path.join(d, "frames")
log = os.path.join(d, "_ffmpeg.log")
times = []
if os.path.exists(log):
    times = [float(m) for m in re.findall(r"pts_time:([0-9]+\.?[0-9]*)",
                                          open(log, errors="ignore").read())]
files = sorted(f for f in os.listdir(frames) if f.startswith("f_") and f.endswith(".jpg"))
if maxf > 0 and len(files) > maxf:
    step = -(-len(files) // maxf)
    for i, f in enumerate(files):
        if i % step:
            os.remove(os.path.join(frames, f))
    files = sorted(f for f in os.listdir(frames) if f.endswith(".jpg"))
out = []
for f in files:
    n = int(re.search(r"f_(\d+)\.jpg", f).group(1))
    if len(times) >= n:
        s = int(times[n-1]); t = "%02d:%02d:%02d" % (s//3600, s % 3600//60, s % 60)
    else:
        t = "--:--:--"
    out.append("%s\t%s" % (f, t))
open(os.path.join(d, "frames_index.txt"), "w", encoding="utf-8").write("\n".join(out))
print(len(files))
PY
NFRAMES="$(wc -l < "$DIR/frames_index.txt" | tr -d ' ')"

[ "$KEEP" -eq 1 ] || rm -f "$DIR/v.mp4"
rm -f "$DIR"/*.vtt

status "$DIR" "DONE - frames=$NFRAMES subtitulos=$SUBLINES dir=$DIR"
