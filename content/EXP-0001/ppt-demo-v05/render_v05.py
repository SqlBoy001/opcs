#!/usr/bin/env python3
"""Locally draw the prep visuals and render the 90-second PPT + evidence cut."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(HERE.parent / "full-v03"))
import render_full as v03  # noqa: E402  Reuse its verified source inventory.

W, H = 720, 1280
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
WHITE = (244, 248, 247)
MUTED = (185, 203, 207)
GOLD = (248, 196, 96)
TEAL = (71, 199, 180)
INK = (13, 24, 32)


def font(size):
    return ImageFont.truetype(FONT, size)


def bg():
    image = Image.new("RGB", (W, H))
    pixels = image.load()
    for y in range(H):
        mix = y / (H - 1)
        color = (int(11 + 8 * mix), int(25 + 15 * mix), int(35 + 18 * mix))
        for x in range(W):
            pixels[x, y] = color
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((380, 120, 940, 710), fill=(45, 170, 168, 68))
    gd.ellipse((-250, 790, 250, 1330), fill=(244, 164, 71, 48))
    return Image.alpha_composite(image.convert("RGBA"), glow.filter(ImageFilter.GaussianBlur(90)))


def box(draw, bounds, fill=(29, 48, 59, 255), outline=None, radius=28, width=2):
    draw.rounded_rectangle(bounds, radius=radius, fill=fill, outline=outline, width=width)


def text(draw, xy, value, size, color=WHITE, spacing=12, anchor=None):
    draw.multiline_text(xy, value, font=font(size), fill=color, spacing=spacing, anchor=anchor)


def pill(draw, xy, value, fill=(31, 66, 73, 255), color=TEAL):
    x, y = xy
    width = int(draw.textlength(value, font=font(21))) + 34
    box(draw, (x, y, x + width, y + 43), fill=fill, radius=21)
    text(draw, (x + 17, y + 8), value, 21, color)


def shell(title, subtitle, tag="流程示意 · 非历史录屏"):
    im = bg()
    d = ImageDraw.Draw(im)
    pill(d, (40, 45), "AI OPC · 真实实验")
    text(d, (40, 130), title, 49, WHITE, spacing=8)
    d.line((40, 1115, 680, 1115), fill=GOLD, width=3)
    text(d, (40, 1140), subtitle, 27, WHITE)
    text(d, (40, 1230), tag, 17, MUTED)
    return im


def framed(im, source, bounds, crop=None, outline=GOLD):
    src = Image.open(source).convert("RGB")
    if crop:
        src = src.crop(crop)
    x0, y0, x1, y1 = bounds
    fitted = ImageOps.fit(src, (x1 - x0, y1 - y0), method=Image.Resampling.LANCZOS)
    mask = Image.new("L", fitted.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, fitted.width - 1, fitted.height - 1), radius=24, fill=255)
    im.paste(fitted, (x0, y0), mask)
    ImageDraw.Draw(im).rounded_rectangle(bounds, radius=24, outline=outline, width=3)


def grab(source, seconds, name):
    dest = OUT / name
    if not dest.exists():
        subprocess.run([str(v03.FFMPEG), "-hide_banner", "-loglevel", "error", "-y", "-ss", str(seconds),
                        "-i", str(source), "-frames:v", "1", str(dest)], check=True)
    return dest


def hook(scene):
    im = shell("刷到很多 AI 漫剧\n副业内容", scene["caption"], "个人观察示意 · 非平台截图")
    d = ImageDraw.Draw(im)
    frames = [grab(v03.SOURCES["raw"][0], sec, f"hook-raw-{sec}.png") for sec in (0, 2, 4)]
    for i, frame in enumerate(frames):
        x = 45 + i * 214
        box(d, (x, 370 + 36 * (i % 2), x + 194, 920 - 30 * (i % 2)), fill=(19, 31, 38, 255), radius=26)
        framed(im, frame, (x + 9, 381 + 36 * (i % 2), x + 185, 822 - 30 * (i % 2)), outline=(60, 85, 91))
        text(d, (x + 14, 838 - 30 * (i % 2)), ["故事", "生成", "返工"][i], 24, GOLD)
    pill(d, (42, 980), "不报班，先自己验证")
    return im


def question(scene):
    im = shell("一个人做 AI 漫剧", scene["caption"])
    d = ImageDraw.Draw(im)
    box(d, (105, 335, 615, 900), fill=(24, 47, 57, 255), outline=(73, 121, 126), radius=44)
    # A lone maker at a laptop, drawn locally rather than a fake production still.
    d.ellipse((305, 420, 415, 530), fill=(243, 204, 153))
    d.pieslice((273, 384, 447, 559), 180, 360, fill=(22, 33, 41))
    box(d, (255, 535, 465, 735), fill=(76, 152, 153, 255), radius=72)
    box(d, (165, 680, 555, 833), fill=(55, 72, 80, 255), outline=TEAL, radius=18)
    d.line((220, 854, 500, 854), fill=GOLD, width=12)
    for cx, cy, symbol in [(175, 435, "剧本"), (535, 435, "图像"), (170, 900, "视频"), (535, 900, "费用")]:
        d.ellipse((cx - 48, cy - 48, cx + 48, cy + 48), fill=(34, 75, 80), outline=TEAL, width=3)
        text(d, (cx, cy), symbol, 21, WHITE, anchor="mm")
    return im


def checklist(scene, stage=4):
    im = shell("我先拆成四件事", "准备清单是问题框架，不是课程配方")
    d = ImageDraw.Draw(im)
    items = [("01", "故事与节奏", "先能讲清冲突"), ("02", "人物与场景", "参考图要可复用"),
             ("03", "模型与工作台", "谁写、谁画、谁出视频"), ("04", "预算与验收", "怎么算钱，怎样算过关")]
    for i, (number, title, sub) in enumerate(items):
        x = 40 + (i % 2) * 330
        y = 350 + (i // 2) * 310
        active = i < stage
        box(d, (x, y, x + 310, y + 280), fill=(26, 50, 60, 255) if active else (22, 37, 45, 255),
            outline=(62, 113, 116) if active else (37, 62, 70), radius=26)
        if not active:
            continue
        text(d, (x + 25, y + 24), number, 52, GOLD)
        d.line((x + 25, y + 105, x + 275, y + 105), fill=TEAL, width=3)
        text(d, (x + 25, y + 128), title, 31)
        text(d, (x + 25, y + 200), sub, 20, MUTED)
    return im


def screenshot(scene, key, crop):
    im = shell(scene["headline"], scene["caption"], "工作台今日只读回看 · 非历史录屏")
    path = v03.SOURCES[key][0]
    framed(im, path, (35, 335, 685, 1025), crop=crop)
    return im


def tools_slide(scene, stage=3):
    im = shell("准备②：工具各做什么？", "本集实际分工 · GPT 图片代理当时未打通")
    d = ImageDraw.Draw(im)
    entries = [("01", "DeepSeek", "人物资料"), ("02", "Seedream 4.5", "角色与分镜图"),
               ("03", "Seedance 2.5", "视频镜头")]
    for i, (number, model, role) in enumerate(entries):
        y = 340 + i * 230
        active = i < stage
        box(d, (55, y, 665, y + 180), fill=(25, 53, 63, 255) if active else (22, 37, 45, 255),
            outline=(68, 112, 120) if active else (37, 62, 70), radius=26)
        if not active:
            continue
        box(d, (77, y + 28, 161, y + 112), fill=(28, 87, 91, 255), radius=22)
        text(d, (119, y + 71), number, 28, GOLD, anchor="mm")
        text(d, (188, y + 34), model, 36, WHITE)
        text(d, (188, y + 105), role, 25, MUTED)
        if i < 2 and i + 1 < stage:
            d.line((360, y + 183, 360, y + 224), fill=GOLD, width=4)
            d.polygon([(350, y + 215), (370, y + 215), (360, y + 230)], fill=GOLD)
    return im


def chapter(scene, image, crop, number):
    im = bg()
    framed(im, image, (0, 230, 720, 1020), crop=crop, outline=(30, 50, 58))
    dim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(dim).rectangle((0, 230, W, 1020), fill=(9, 20, 28, 150))
    im = Image.alpha_composite(im, dim)
    d = ImageDraw.Draw(im)
    pill(d, (40, 65), f"第 {number} 关 · 真实问题")
    text(d, (40, 360), scene["headline"], 55, WHITE)
    text(d, (40, 985), scene["caption"], 30, GOLD)
    text(d, (40, 1228), "章节讲解 · 下一镜展示真实素材", 18, MUTED)
    return im


def shackle(scene):
    im = shell("服装回来了，\n脚镣又错了", "真实分镜图 · 脚镣被放大成圆环", "项目6真实图片 · 非示意图")
    path = v03.SOURCES["bad_shackle"][0]
    framed(im, path, (35, 350, 685, 1000), crop=(900, 580, 1750, 1430))
    d = ImageDraw.Draw(im)
    d.ellipse((135, 752, 598, 952), outline=(255, 113, 91), width=8)
    box(d, (58, 920, 400, 982), fill=(122, 42, 43, 245), radius=18)
    text(d, (78, 935), "异常：夸大的脚镣", 25, WHITE)
    return im


def cost(scene):
    im = shell("账单只回答一部分", "完整制作成本仍未知", "OPC-1 v2 验证报告 · 部分费用口径")
    d = ImageDraw.Draw(im)
    box(d, (40, 345, 680, 900), fill=(25, 51, 60, 255), outline=(72, 124, 124), radius=32)
    text(d, (75, 390), "9 月 28 日筛选账单现金", 29, MUTED)
    text(d, (75, 480), "74.92", 116, GOLD)
    text(d, (483, 548), "元", 36, GOLD)
    d.line((80, 690, 640, 690), fill=(75, 111, 117), width=3)
    text(d, (76, 745), "非整集成本", 39, WHITE)
    text(d, (76, 815), "未逐请求排他归因", 25, MUTED)
    return im


def next_slide(scene):
    im = shell("值不值得继续？", "先听审，再找真实观众", "下一步实验 · 尚未执行")
    d = ImageDraw.Draw(im)
    steps = [("01", "听完 60 秒原声", "台词 / 情绪 / 口型"),
             ("02", "请观众复述冲突", "看是否真的看懂"),
             ("03", "再问是否想追看", "验证兴趣，不猜市场")]
    for i, (number, title, sub) in enumerate(steps):
        y = 360 + i * 220
        box(d, (55, y, 665, y + 175), fill=(25, 51, 60, 255), outline=(60, 107, 114), radius=26)
        text(d, (80, y + 27), number, 45, GOLD)
        text(d, (180, y + 27), title, 32, WHITE)
        text(d, (180, y + 94), sub, 23, MUTED)
    return im


def make_slide(scene):
    key = scene["asset"]
    if key == "hook": return hook(scene)
    if key == "question": return question(scene)
    if key == "checklist": return checklist(scene)
    if key == "script": return screenshot(scene, "script_screen", (90, 100, 1120, 900))
    if key == "tools": return tools_slide(scene)
    if key == "workbench": return screenshot(scene, "storyboard_screen", (370, 130, 1300, 960))
    if key == "chapter_roles":
        return chapter(scene, v03.SOURCES["first_pass"][0], (0, 0, 900, 1450), "01")
    if key == "chapter_image":
        return chapter(scene, v03.SOURCES["bad_shackle"][0], (700, 400, 1900, 1400), "02")
    if key == "shackle": return shackle(scene)
    if key == "chapter_action":
        frame = grab(v03.SOURCES["raw"][0], 2, "action-frame.png")
        return chapter(scene, frame, None, "03")
    if key == "cost": return cost(scene)
    if key == "next": return next_slide(scene)
    raise KeyError(key)


def video_overlay(scene, clean):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if clean:
        return layer
    d = ImageDraw.Draw(layer)
    box(d, (20, 40, 700, 180), fill=(8, 22, 30, 207), radius=24)
    text(d, (42, 73), scene["headline"], 36)
    box(d, (20, 1030, 700, 1190), fill=(8, 22, 30, 215), radius=24)
    text(d, (42, 1055), scene["caption"], 26, WHITE)
    source_note = ("本实验画面示意 · 个人观察" if scene["asset"] == "hook_video"
                   else "真实项目素材 · 未发布草稿")
    text(d, (42, 1154), source_note, 17, MUTED)
    return layer


def run(args):
    subprocess.run([str(v03.FFMPEG), "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def render_scene(scene, clean):
    dest = OUT / f"{scene['id']}{'-clean' if clean else ''}.mp4"
    frames = 24 * scene["duration"]
    if scene["kind"] == "slide":
        if scene["asset"] in {"checklist", "tools"}:
            stages = 4 if scene["asset"] == "checklist" else 3
            assert frames % stages == 0
            parts = []
            for stage in range(1, stages + 1):
                art = OUT / f"{scene['id']}-stage{stage}.png"
                draw_stage = checklist if scene["asset"] == "checklist" else tools_slide
                draw_stage(scene, stage).convert("RGB").save(art)
                part = OUT / f"{scene['id']}-stage{stage}.mp4"
                run(["-loop", "1", "-framerate", "24", "-i", str(art),
                     "-frames:v", str(frames // stages), "-c:v", "libx264", "-preset", "veryfast",
                     "-crf", "26", "-pix_fmt", "yuv420p", str(part)])
                parts.append(part)
            manifest = OUT / f"{scene['id']}-stages.txt"
            manifest.write_text("".join(f"file '{p.name}'\n" for p in parts), encoding="utf-8")
            run(["-f", "concat", "-safe", "0", "-i", str(manifest), "-c", "copy", str(dest)])
            return dest
        art = OUT / f"{scene['id']}.png"
        make_slide(scene).convert("RGB").save(art)
        run(["-loop", "1", "-framerate", "24", "-i", str(art), "-frames:v", str(frames),
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-pix_fmt", "yuv420p", str(dest)])
    else:
        source_key = {"hook_video": "09-raw-clean.mp4", "roles": "05-characters-clean.mp4",
                      "compare": "11-compare-clean.mp4", "result": "12-result-clean.mp4"}[scene["asset"]]
        source = HERE.parent / "full-v03/output" / source_key
        assert source.exists(), f"Render full-v03 clean first: {source}"
        over = OUT / f"{scene['id']}-overlay.png"
        video_overlay(scene, clean).save(over)
        speed = "setpts=(PTS-STARTPTS)*0.6666667,fps=24" if scene["asset"] == "roles" else "fps=24"
        filt = f"[0:v]{speed}[base];[base][1:v]overlay=0:0:shortest=1[v]"
        run(["-i", str(source), "-loop", "1", "-framerate", "24", "-i", str(over),
             "-filter_complex", filt, "-map", "[v]", "-frames:v", str(frames), "-an",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "27", "-pix_fmt", "yuv420p", str(dest)])
    return dest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=("captioned", "clean"), default="captioned")
    ap.add_argument("--only-scene", help="Re-render one scene and reassemble existing clips")
    args = ap.parse_args()
    data = json.loads((HERE.parent / "content.json").read_text(encoding="utf-8"))["ppt_demo_v05"]
    scenes = data["scenes"]
    assert sum(s["duration"] for s in scenes) == 90
    for key in ("final", "raw", "first_pass", "bad_shackle", "script_screen", "storyboard_screen"):
        path, expected, _, _ = v03.SOURCES[key]
        assert v03.digest(path) == expected, f"Source SHA mismatch: {key}"
    hook(scenes[0]).convert("RGB").save(OUT / "cover.png")
    clean = args.variant == "clean"
    clips = []
    for scene in scenes:
        clip = OUT / f"{scene['id']}{'-clean' if clean else ''}.mp4"
        if not args.only_scene or scene["id"] == args.only_scene:
            clip = render_scene(scene, clean)
            print(f"rendered {scene['id']}", flush=True)
        clips.append(clip)
    if args.only_scene and args.only_scene not in {scene["id"] for scene in scenes}:
        ap.error(f"Unknown scene: {args.only_scene}")
    manifest = OUT / f"concat-{args.variant}.txt"
    manifest.write_text("".join(f"file '{p.name}'\n" for p in clips), encoding="utf-8")
    target = OUT / f"OPC-2-ppt-demo-90s-{args.variant}.mp4"
    run(["-f", "concat", "-safe", "0", "-i", str(manifest), "-c", "copy", "-movflags", "+faststart", str(target)])
    print(target)


if __name__ == "__main__":
    main()
