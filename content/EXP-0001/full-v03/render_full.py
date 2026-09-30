#!/usr/bin/env python3
"""Render the silent, evidence-led process draft from the shared content.json."""

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)
PROJECT_ROOT = Path(os.environ.get("AI_DRAMA_ROOT", Path.home() / "Documents/ChatGPT/AI_Drama"))
FFMPEG = PROJECT_ROOT / "backend-node/tools/ffmpeg/ffmpeg"
FONT = Path("/System/Library/Fonts/STHeiti Medium.ttc")
BASE = PROJECT_ROOT / "backend-node/data/storage/projects/0006_20260926_亡国公主·全角色重制版"
SOURCES = {
    "raw": (BASE / "videos/vg_46_ecfddff9.mp4", "e0f8d3bfef73503f7d63d8d953cba858af232354528bd6bf69d56e8ecdad2f40", "video", "crop=1080:1440:700:0"),
    "edit": (BASE / "videos/s007-action-v05-editorial.mp4", "8a88d6ec1799f8bb073af8d1651d09a4681dab96ed1777295ab6674f3aeaff95", "video", "crop=1080:1440:700:0"),
    "final": (BASE / "exports/action-v06/jinyang-EP01-action-v06c-720p.mp4", "b7066a812e9801f7b3d4b6ab8874a483bb52ca106851f7e07e681a48b4c16029", "video", "crop=600:720:340:0"),
    "script_screen": (HERE / "assets/replay-script.png", "9f229ed438bc784388479c93665d59f3eb8a36dc195356772395a27397cd7fa4", "image", "crop=850:700:200:140"),
    "storyboard_screen": (HERE / "assets/replay-storyboard.png", "948710d824150cb4d8ea8d0474ffa10f695ff6cce32f8dcd92ad59207c32c466", "image", "crop=700:700:650:170"),
    "first_pass": (PROJECT_ROOT / "backend-node/data/production/jinyang-rebuild-v01/contact-first-pass.jpg", "96456ab556a7e987210efe06edd2f2abb41504eec36855858ffa2ffd36f5fce6", "image", "crop=900:1200:0:((in_h-1200)*n/216)"),
    "bad_shackle": (BASE / "images/ig_c179b089.jpg", "c5d5eadce7f933a645e8d4709921e328ac22c2cf0b14dc16c6bb80b72785bfc3", "image", "crop=850:850:900:580"),
    "cast_v04": (BASE / "characters/cast-v04-20.png", "5b04385eac64e5d645687c9c71991d697a444fb644e4f88f5c0f8d06c146269d", "image", "crop=950:949:0:0"),
}


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(args):
    subprocess.run([str(FFMPEG), "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def textfile(name, value):
    path = OUT / name
    path.write_text(value, encoding="utf-8")
    return path


def wrap(value, max_chars=21):
    if "\n" in value:
        return value
    if len(value) <= max_chars:
        return value
    midpoint = min(range(1, len(value)), key=lambda n: abs(n - max_chars) + (0 if value[n - 1] in "，；、。 " else 3))
    return value[:midpoint].strip() + "\n" + value[midpoint:].strip()


def overlay(scene, clean):
    if clean:
        return ""
    heading = textfile(f"{scene['id']}-heading.txt", scene["headline"])
    caption = textfile(f"{scene['id']}-caption.txt", wrap(scene["caption"]))
    mark_text = ("工作台今日只读回看 / 未发布草稿" if scene["asset"] in {"script_screen", "storyboard_screen"}
                 else "AI OPC · 真实实验 / 未发布草稿")
    mark = textfile(f"{scene['id']}-mark.txt", mark_text)
    return (
        ",drawbox=x=40:y=1000:w=640:h=3:color=0xe9b65b:t=fill"
        f",drawtext=fontfile='{FONT}':textfile='{heading}':fontcolor=white:fontsize=41:x=40:y=105"
        f",drawtext=fontfile='{FONT}':textfile='{caption}':fontcolor=white:fontsize=29:x=40:y=1050:line_spacing=15"
        f",drawtext=fontfile='{FONT}':textfile='{mark}':fontcolor=0xb7c2c0:fontsize=18:x=40:y=1222"
    )


def render_single(scene, clean):
    path, _, kind, crop = SOURCES[scene["asset"]]
    inputs = (["-ss", str(scene.get("source_start", 0)), "-t", str(scene["duration"]), "-i", str(path)]
              if kind == "video" else
              ["-loop", "1", "-framerate", "24", "-t", str(scene["duration"]), "-i", str(path)])
    filt = (
        "[0:v]fps=24,split=2[fg0][bg0];"
        "[bg0]scale=720:1280:force_original_aspect_ratio=increase:flags=fast_bilinear,"
        "crop=720:1280,boxblur=12:1,eq=brightness=-0.43[bg];"
        f"[fg0]{crop},scale=656:840:force_original_aspect_ratio=decrease:flags=lanczos[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2:shortest=1"
        + overlay(scene, clean) + "[v]"
    )
    result = OUT / f"{scene['id']}{'-clean' if clean else ''}.mp4"
    run([*inputs, "-filter_complex", filt, "-map", "[v]", "-an", "-c:v", "libx264",
         "-preset", "veryfast", "-crf", "27", "-pix_fmt", "yuv420p", "-r", "24",
         "-t", str(scene["duration"]), str(result)])
    return result


def render_compare(scene, clean):
    raw, edit = SOURCES["raw"][0], SOURCES["edit"][0]
    filt = (
        "[0:v]fps=24,scale=656:369:flags=lanczos[a];"
        "[1:v]fps=24,scale=656:369:flags=lanczos[b];"
        "color=c=0x11171b:s=720x1280:r=24[bg];"
        "[bg][a]overlay=32:235:shortest=1[half];"
        "[half][b]overlay=32:650:shortest=1"
        + overlay(scene, clean) + "[v]"
    )
    result = OUT / f"{scene['id']}{'-clean' if clean else ''}.mp4"
    run(["-t", "6", "-i", str(raw), "-t", "6", "-i", str(edit),
         "-filter_complex", filt, "-map", "[v]", "-an", "-c:v", "libx264",
         "-preset", "veryfast", "-crf", "27", "-pix_fmt", "yuv420p", "-r", "24",
         "-t", "6", str(result)])
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=("captioned", "clean"), default="captioned")
    parser.add_argument("--only-scene", help="Re-render one scene, then assemble existing segments")
    args = parser.parse_args()
    facts = json.loads((HERE.parent / "content.json").read_text(encoding="utf-8"))
    scenes = facts["full_v03"]["scenes"]
    assert sum(s["duration"] for s in scenes) == facts["full_v03"]["duration_seconds"]
    for key, (path, expected, _, _) in SOURCES.items():
        assert digest(path) == expected, f"Source SHA mismatch: {key}"
    clean = args.variant == "clean"
    segments = []
    for scene in scenes:
        result = OUT / f"{scene['id']}{'-clean' if clean else ''}.mp4"
        if not args.only_scene or scene["id"] == args.only_scene:
            result = render_compare(scene, clean) if scene["asset"] == "compare" else render_single(scene, clean)
            print(f"rendered {scene['id']}", flush=True)
        segments.append(result)
    if args.only_scene and args.only_scene not in {scene["id"] for scene in scenes}:
        parser.error(f"Unknown scene: {args.only_scene}")
    manifest = OUT / f"concat-{args.variant}.txt"
    manifest.write_text("".join(f"file '{p.name}'\n" for p in segments), encoding="utf-8")
    result = OUT / f"OPC-2-full-process-{args.variant}.mp4"
    run(["-f", "concat", "-safe", "0", "-i", str(manifest), "-c", "copy", "-movflags", "+faststart", str(result)])
    print(result)


if __name__ == "__main__":
    main()
