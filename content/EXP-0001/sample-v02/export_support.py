#!/usr/bin/env python3
"""Export the sample's scene captions and voiceover from content.json."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCENES = json.loads((HERE.parent / "content.json").read_text(encoding="utf-8"))["sample_v02"]["scenes"]


def stamp(seconds):
    millis = round(seconds * 1000)
    hours, millis = divmod(millis, 3600000)
    minutes, millis = divmod(millis, 60000)
    secs, millis = divmod(millis, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


position = 0
srt = []
voice = ["# S007 样段分段口播文稿", "", "仅供后续配音。29秒时间码按静音预览剪辑，实际录音后须重新对齐。", ""]
for index, scene in enumerate(SCENES, 1):
    end = position + scene["duration"]
    caption = scene.get("line1") or scene["heading"]
    srt += [str(index), f"{stamp(position)} --> {stamp(end)}", caption, ""]
    voice += [f"- {position:g}–{end:g}秒：{scene['voiceover']}"]
    position = end
assert position == 29, position
(HERE / "subtitles.srt").write_text("\n".join(srt), encoding="utf-8")
(HERE / "voiceover.md").write_text("\n".join(voice) + "\n", encoding="utf-8")
