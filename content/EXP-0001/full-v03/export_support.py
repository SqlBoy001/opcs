#!/usr/bin/env python3
"""Export scene plan, provisional voiceover and on-screen subtitles from content.json."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
scenes = json.loads((HERE.parent / "content.json").read_text(encoding="utf-8"))["full_v03"]["scenes"]


def stamp(seconds):
    return f"{seconds // 3600:02}:{seconds // 60 % 60:02}:{seconds % 60:02},000"


plan = ["# OPC-2 全流程短视频 · 分镜与证据", "", "117 秒竖屏静音草稿，未发布。工作台画面是今日只读回看。", ""]
voice = ["# 口播稿（未配音）", "", "本稿用于后续 TTS / 人声录制，接入音轨后须逐句校时。", ""]
subs = []
elapsed = 0
for number, scene in enumerate(scenes, 1):
    end = elapsed + scene["duration"]
    timecode = f"{elapsed // 60:02}:{elapsed % 60:02}–{end // 60:02}:{end % 60:02}"
    plan.extend([
        f"## {number:02} · {timecode} · {scene['headline']}",
        "",
        f"- 画面：`{scene['asset']}`",
        f"- 屏幕文字：{scene['caption'].replace(chr(10), ' / ')}",
        f"- 口播：{scene['voiceover']}",
        f"- 证据：{scene['evidence']}",
        "",
    ])
    voice.append(f"{timecode}  {scene['voiceover']}")
    subs.append(f"{number}\n{stamp(elapsed)} --> {stamp(end)}\n{scene['headline']}\n{scene['caption']}\n")
    elapsed = end

assert elapsed == 117
(HERE / "storyboard.md").write_text("\n".join(plan) + "\n", encoding="utf-8")
(HERE / "voiceover.md").write_text("\n".join(voice) + "\n", encoding="utf-8")
(HERE / "subtitles.srt").write_text("\n".join(subs) + "\n", encoding="utf-8")
