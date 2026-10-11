#!/bin/zsh
set -euo pipefail
PROJECT_ROOT=$(cd "$(dirname "$0")" && pwd)
OUTPUT=${1:?Pass a new absolute MP4 path}
if [[ -e "$OUTPUT" ]]; then
  echo 'Output exists; choose a new path.' >&2
  exit 1
fi
python3 "$PROJECT_ROOT/prepare_full.py"
python3 "$PROJECT_ROOT/prepare_media.py"
cd "$PROJECT_ROOT/studio"
npm run lint
npx remotion render OPC-Full-F "$OUTPUT" --codec=h264 --crf=20 --browser-executable='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' --concurrency=3
