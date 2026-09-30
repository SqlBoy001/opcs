#!/usr/bin/env python3
"""Export the 90-second storyboard, provisional voiceover and SRT."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
doc = json.loads((HERE.parent / "content.json").read_text(encoding="utf-8"))
base = {scene["id"]: scene for scene in doc["full_v03"]["scenes"]}
scenes = doc["short_v04"]["scenes"]


def stamp(seconds):
    return f"{seconds // 3600:02}:{seconds // 60 % 60:02}:{seconds % 60:02},000"


storyboard = ["# OPC-2 · 90 秒主版分镜", "", "基于同一份 `content.json` 和 v03 证据；静音待审，未发布。", ""]
voice = ["# OPC-2 · 90 秒口播稿（未配音）", "", "配音后须逐句校时。", ""]
subs = []
elapsed = 0
for index, short in enumerate(scenes, 1):
    full = base[short["id"]]
    end = elapsed + short["duration"]
    span = f"{elapsed // 60:02}:{elapsed % 60:02}–{end // 60:02}:{end % 60:02}"
    storyboard.extend([
        f"## {index:02} · {span} · {full['headline']}", "",
        f"- 画面：`{full['asset']}`",
        f"- 屏幕文字：{full['caption'].replace(chr(10), ' / ')}",
        f"- 口播：{short['voiceover']}",
        f"- 证据：{full['evidence']}", "",
    ])
    voice.append(f"{span}  {short['voiceover']}")
    subs.append(f"{index}\n{stamp(elapsed)} --> {stamp(end)}\n{full['headline']}\n{full['caption']}\n")
    elapsed = end

assert elapsed == 90
(HERE / "storyboard.md").write_text("\n".join(storyboard) + "\n", encoding="utf-8")
(HERE / "voiceover.md").write_text("\n".join(voice) + "\n", encoding="utf-8")
(HERE / "subtitles.srt").write_text("\n".join(subs) + "\n", encoding="utf-8")
