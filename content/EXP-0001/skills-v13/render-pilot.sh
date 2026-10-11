#!/bin/zsh
set -euo pipefail
PROJECT_ROOT=$(cd "$(dirname "$0")" && pwd)
OUTPUT=${1:?Pass a new absolute output MP4 path}
if [[ -e "$OUTPUT" || -e "$OUTPUT.raw.mp4" ]]; then
  echo 'Output already exists; choose a new version path.' >&2
  exit 1
fi
python3 "$PROJECT_ROOT/prepare.py"
cd "$PROJECT_ROOT/studio"
npm run lint
npx remotion render OPC-Pilot "$OUTPUT.raw.mp4" --codec=h264 --crf=20 --browser-executable='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

ffmpeg -v error -n -i "$OUTPUT.raw.mp4" -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=9 -c:a aac -b:a 160k -ar 48000 -movflags +faststart "$OUTPUT"
