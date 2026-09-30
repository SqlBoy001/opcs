#!/usr/bin/env python3
"""Render a silent, evidence-led 29-second S007 comparison sample.

Only reads local, already generated project media. No provider/API calls.
"""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)
FFMPEG = Path("/Users/shenzihao/Documents/ChatGPT/AI_Drama/backend-node/tools/ffmpeg/ffmpeg")
PROJECT = Path("/Users/shenzihao/Documents/ChatGPT/AI_Drama/backend-node/data/storage/projects/0006_20260926_亡国公主·全角色重制版")
RAW = PROJECT / "videos/vg_46_ecfddff9.mp4"
EDIT = PROJECT / "videos/s007-action-v05-editorial.mp4"
FINAL = PROJECT / "exports/action-v06/jinyang-EP01-action-v06c-720p.mp4"
FONT = Path("/System/Library/Fonts/STHeiti Medium.ttc")


def run(args):
    subprocess.run([str(FFMPEG), "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def txt(value, name):
    path = OUT / f"{name}.txt"
    path.write_text(value, encoding="utf-8")
    return path


def draw(path, size, y, color="white"):
    return (f"drawtext=fontfile='{FONT}':textfile='{path}':reload=0:"
            f"fontcolor={color}:fontsize={size}:x=72:y={y}")


def single(name, src, start, length, heading, line1, line2, footer, speed=1, clean=False):
    title = txt(heading, f"{name}-title")
    note1 = txt(line1, f"{name}-line1")
    note2 = txt(line2, f"{name}-line2")
    foot = txt(footer, f"{name}-footer")
    filt = (
        "[0:v]setpts=(PTS-STARTPTS)/" + str(speed) + ",fps=24,split=2[fgsrc][bgsrc];"
        "[fgsrc]scale=936:527:flags=lanczos[clip];"
        "[bgsrc]scale=1080:1920:force_original_aspect_ratio=increase:flags=fast_bilinear,"
        "crop=1080:1920,boxblur=18:1,eq=brightness=-0.37[bg];"
        "[bg][clip]overlay=72:490:shortest=1"
    )
    if not clean:
        filt += (",drawbox=x=72:y=1080:w=936:h=4:color=0xe9b65b:t=fill,"
                 + draw(title, 68, 215) + ","
                 + draw(note1, 49, 1180) + ","
                 + draw(note2, 42, 1260, "0xc9d2d1") + ","
                 + draw(foot, 29, 1730, "0x889694"))
    filt += "[v]"
    path = OUT / f"{name}{'-clean' if clean else ''}.mp4"
    run(["-ss", str(start), "-t", str(length / speed), "-i", str(src),
         "-filter_complex", filt, "-map", "[v]", "-an", "-c:v", "libx264",
         "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-t", str(length), str(path)])
    return path


def comparison(scene, clean=False):
    name = "05-compare"
    title = txt(scene["heading"], f"{name}-title")
    left = txt(scene["left_label"], f"{name}-left")
    right = txt(scene["right_label"], f"{name}-right")
    foot = txt(scene["footer"], f"{name}-footer")
    filt = (
        "[0:v]fps=24,scale=936:527:flags=lanczos[raw];"
        "[1:v]fps=24,scale=936:527:flags=lanczos[edit];"
        "color=c=0x11171b:s=1080x1920:r=24[bg];"
        "[bg][raw]overlay=72:365:shortest=1[b1];"
        "[b1][edit]overlay=72:1040:shortest=1"
    )
    if not clean:
        filt += (",drawbox=x=72:y=914:w=936:h=3:color=0xe9b65b:t=fill,"
                 + draw(title, 58, 145) + ","
                 + draw(left, 42, 295, "0xe9b65b") + ","
                 + draw(right, 42, 965, "0xe9b65b") + ","
                 + draw(foot, 32, 1700, "0xc9d2d1"))
    filt += "[v]"
    path = OUT / f"{name}{'-clean' if clean else ''}.mp4"
    run(["-t", "6", "-i", str(RAW), "-t", "6", "-i", str(EDIT),
         "-filter_complex", filt, "-map", "[v]", "-an", "-c:v", "libx264",
         "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-t", "6", str(path)])
    return path


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=("clean", "captioned"), default="captioned")
    args = parser.parse_args()
    clean = args.variant == "clean"
    facts = json.loads((HERE.parent / "content.json").read_text(encoding="utf-8"))
    sources = {"raw": RAW, "edit": EDIT, "final": FINAL}
    for key, path in sources.items():
        expected = facts["sample_v02"]["sources"][key]["sha256"]
        assert digest(path) == expected, f"Source SHA mismatch: {key}"
    segments = []
    for scene in facts["sample_v02"]["scenes"]:
        if scene["kind"] == "comparison":
            segments.append(comparison(scene, clean=clean))
        else:
            segments.append(single(scene["id"], sources[scene["source"]], scene["source_start"],
                                   scene["duration"], scene["heading"], scene["line1"],
                                   scene["line2"], scene["footer"], scene.get("speed", 1), clean=clean))
    manifest = OUT / f"concat-{args.variant}.txt"
    manifest.write_text("".join(f"file '{p.name}'\n" for p in segments), encoding="utf-8")
    result = OUT / f"OPC-2-S007-style-sample-{args.variant}.mp4"
    run(["-f", "concat", "-safe", "0", "-i", str(manifest), "-c", "copy", "-movflags", "+faststart", str(result)])
    print(json.dumps({"result": str(result), "segments": [str(p) for p in segments]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
