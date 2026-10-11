#!/bin/zsh
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
SKILL_DIR='/Users/shenzihao/.hifox/organizations/040a2449-fbf3-4ec1-b87e-18aeaed0d2a4/runs/2026/09/d5cdf3e3-63cc-42cb-9cd2-65a1e2551c6a/codex-home/skills/adu-motion-video'
OUTPUT=${1:?Pass a NEW absolute MP4 output path; existing versions are not overwritten}
python3 "$SKILL_DIR/scripts/pipeline.py" audio "$ROOT/project"
python3 "$SKILL_DIR/scripts/pipeline.py" mix "$ROOT/project"
W=1080 H=1920 FPS=60 python3 "$SKILL_DIR/scripts/pipeline.py" render "$ROOT/project" "$OUTPUT" 4
python3 "$SKILL_DIR/scripts/pipeline.py" check "$OUTPUT"
