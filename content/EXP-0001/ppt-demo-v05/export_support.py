#!/usr/bin/env python3
"""Export storyboard, provisional narration and subtitles from content.json."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
data = json.loads((HERE.parent / "content.json").read_text(encoding="utf-8"))["ppt_demo_v05"]
scenes = data["scenes"]


def stamp(seconds):
    return f"{seconds // 3600:02}:{seconds // 60 % 60:02}:{seconds % 60:02},000"


plan = ["# OPC-2 v05 · PPT 讲解 + 真实视频拆解", "", "90 秒竖屏静音草稿，未发布。示意插画与今日工作台回看均已单独标示。", ""]
voice = ["# OPC-2 v05 · 口播稿（未配音）", "", "接入声音后须逐句校时。", ""]
subs = []
elapsed = 0
for i, scene in enumerate(scenes, 1):
    end = elapsed + scene["duration"]
    span = f"{elapsed // 60:02}:{elapsed % 60:02}–{end // 60:02}:{end % 60:02}"
    plan.extend([
        f"## {i:02} · {span} · {scene['headline']}", "",
        f"- 画面：`{scene['kind']}` / `{scene['asset']}`",
        f"- 屏幕文字：{scene['caption']}",
        f"- 口播：{scene['voiceover']}",
        f"- 证据：{scene['evidence']}", "",
    ])
    voice.append(f"{span}  {scene['voiceover']}")
    subs.append(f"{i}\n{stamp(elapsed)} --> {stamp(end)}\n{scene['headline']}\n{scene['caption']}\n")
    elapsed = end
assert elapsed == 90
(HERE / "storyboard.md").write_text("\n".join(plan) + "\n", encoding="utf-8")
(HERE / "voiceover.md").write_text("\n".join(voice) + "\n", encoding="utf-8")
(HERE / "subtitles.srt").write_text("\n".join(subs) + "\n", encoding="utf-8")
