#!/usr/bin/env python3
"""Cut the evidence-led v03 scene renders to the 90-second primary draft."""

import argparse
import json
import os
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)
V03 = HERE.parent / "full-v03/output"
ROOT = Path(os.environ.get("AI_DRAMA_ROOT", Path.home() / "Documents/ChatGPT/AI_Drama"))
FFMPEG = ROOT / "backend-node/tools/ffmpeg/ffmpeg"


def run(args):
    subprocess.run([str(FFMPEG), "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=("captioned", "clean"), default="captioned")
    args = parser.parse_args()
    doc = json.loads((HERE.parent / "content.json").read_text(encoding="utf-8"))
    scenes = doc["short_v04"]["scenes"]
    assert sum(s["duration"] for s in scenes) == 90
    clips = []
    for scene in scenes:
        label = scene["id"]
        source = V03 / f"{label}{'-clean' if args.variant == 'clean' else ''}.mp4"
        assert source.exists(), f"Render full-v03 first: {source}"
        dest = OUT / f"{label}-{args.variant}.mp4"
        # Center the 7-second contact-sheet pass within its 9-second source.
        start = 1 if label == "05-characters" else 0
        run(["-ss", str(start), "-i", str(source), "-an", "-frames:v", str(24 * scene["duration"]),
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "27", "-pix_fmt", "yuv420p",
             "-r", "24", str(dest)])
        clips.append(dest)
        print(f"cut {label}", flush=True)
    manifest = OUT / f"concat-{args.variant}.txt"
    manifest.write_text("".join(f"file '{p.name}'\n" for p in clips), encoding="utf-8")
    result = OUT / f"OPC-2-process-90s-{args.variant}.mp4"
    run(["-f", "concat", "-safe", "0", "-i", str(manifest), "-c", "copy", "-movflags", "+faststart", str(result)])
    print(result)


if __name__ == "__main__":
    main()
