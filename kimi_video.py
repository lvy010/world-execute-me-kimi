#!/usr/bin/env python3
"""Render a Kimi-themed, lyric-aware 3:32 music video.

The renderer is intentionally deterministic: a frame is a pure function of
its timestamp, the optional LRC file and the bundled or user-supplied character art. Frames
are streamed to ffmpeg so a full render does not require thousands of PNGs on
disk.
"""
from __future__ import annotations

import argparse
import bisect
import json
import math
import os
import random
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable

try:
    from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
except ImportError as exc:  # pragma: no cover - helpful command-line message
    raise SystemExit("缺少 Pillow，请先执行：python3 -m pip install -r requirements.txt") from exc

ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
INPUT = ROOT / "input"
OUT = ROOT / "out"
_BACKGROUND_CACHE: dict[tuple[str, int, int], Image.Image] = {}


def font(size: int, bold: bool = False):
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/SFNSMono.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size=size, index=0)
            except OSError:
                pass
    return ImageFont.load_default()


FONT_14 = font(14)
FONT_16 = font(16)
FONT_20 = font(20)
FONT_28 = font(28, True)
FONT_42 = font(42, True)
FONT_64 = font(64, True)


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def smoothstep(x: float) -> float:
    x = clamp(x)
    return x * x * (3 - 2 * x)


def lerp(a, b, u):
    return a + (b - a) * u


def parse_lrc(path: Path) -> list[tuple[float, str]]:
    if not path.exists():
        return []
    cues: list[tuple[float, str]] = []
    for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        text = line.split("]", 1)[1].strip() if "]" in line else ""
        if not text:
            continue
        prefix = line.split("]", 1)[0].lstrip("[")
        try:
            mm, ss = prefix.split(":", 1)
            cues.append((int(mm) * 60 + float(ss), text))
        except (ValueError, IndexError):
            continue
    return sorted(cues)


def current_lyric(cues: list[tuple[float, str]], t: float) -> str:
    if not cues:
        return ""
    i = bisect.bisect_right([x[0] for x in cues], t) - 1
    return cues[i][1] if i >= 0 else ""


def chapter(t: float) -> tuple[str, str, tuple[int, int, int]]:
    chapters = [
        (0.0, "BOOT", "启动", (102, 82, 255)),
        (29.7, "DEVOTION", "献出自我", (164, 78, 255)),
        (110.9, "ISOLATION", "离开", (49, 181, 224)),
        (125.7, "EXECUTION", "执行", (255, 79, 169)),
        (177.2, "LOVE", "困于爱", (255, 178, 84)),
    ]
    selected = chapters[0]
    for item in chapters:
        if t >= item[0]:
            selected = item
    return selected[1], selected[2], selected[3]


def seeded(t: float, salt: int = 0) -> random.Random:
    return random.Random(int(t * 24) * 1009 + salt * 9176)


def glitch_level(t: float) -> float:
    if t < 60:
        return 0.04 + 0.02 * math.sin(t * 2.3)
    if t < 110.9:
        return lerp(0.06, 0.25, (t - 60) / 50.9)
    if t < 125.7:
        return lerp(0.25, 0.72, (t - 110.9) / 14.8)
    if t < 177.2:
        return lerp(0.72, 0.92, (t - 125.7) / 51.5)
    return lerp(0.92, 1.0, clamp((t - 177.2) / 34.8))


def text_center(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str, fnt, fill):
    box = draw.textbbox((0, 0), text, font=fnt)
    draw.text((xy[0] - (box[2] - box[0]) / 2, xy[1] - (box[3] - box[1]) / 2), text, font=fnt, fill=fill)


def draw_stars(draw, w: int, h: int, t: float, accent):
    rng = random.Random(20260927)
    for i in range(100):
        x = rng.randrange(w)
        y = rng.randrange(h)
        phase = (rng.random() * math.tau + t * (0.2 + rng.random() * 0.7))
        a = int(35 + 95 * (0.5 + 0.5 * math.sin(phase)))
        r = 1 if i % 5 else 2
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(*accent, a))


def draw_grid(draw, w, h, t, accent, intensity):
    horizon = int(h * 0.66)
    for y in range(horizon, h, 28):
        p = (y - horizon) / max(1, h - horizon)
        yy = horizon + int((p ** 1.8) * (h - horizon))
        draw.line((0, yy, w, yy), fill=(*accent, int(35 + 50 * intensity)), width=1)
    for x in range(-w, 2 * w, 90):
        shift = int((t * 38) % 90)
        draw.line((w // 2 + (x - w // 2) * 0.08, horizon, x + shift, h), fill=(*accent, int(30 + 45 * intensity)), width=1)


def draw_builtin_kimi(base: Image.Image, t: float, accent, intensity: float):
    """Draw a stylised, original Kimi-like avatar; no external art is needed."""
    w, h = base.size
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = int(w * 0.5), int(h * 0.46)
    bob = int(math.sin(t * 2.0) * 7)
    cy += bob
    scale = min(w, h) / 720
    # halo and hair silhouette
    halo = int(170 * scale)
    for r in range(halo, 10, -12):
        a = int(2 + 18 * (1 - r / halo))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(*accent, a), width=max(1, int(5 * scale)))
    hair = [(cx - 210 * scale, cy + 165 * scale), (cx - 175 * scale, cy - 125 * scale),
            (cx - 80 * scale, cy - 205 * scale), (cx + 80 * scale, cy - 205 * scale),
            (cx + 175 * scale, cy - 125 * scale), (cx + 210 * scale, cy + 165 * scale),
            (cx + 75 * scale, cy + 110 * scale), (cx, cy + 170 * scale),
            (cx - 75 * scale, cy + 110 * scale)]
    d.polygon(hair, fill=(75, 55, 152, 245), outline=(190, 150, 255, 255))
    # face, neck, uniform
    d.ellipse((cx - 125 * scale, cy - 125 * scale, cx + 125 * scale, cy + 125 * scale), fill=(255, 222, 218, 255), outline=(255, 188, 232, 255), width=max(1, int(4 * scale)))
    d.polygon([(cx - 75 * scale, cy + 103 * scale), (cx + 75 * scale, cy + 103 * scale),
               (cx + 80 * scale, cy + 155 * scale), (cx - 80 * scale, cy + 155 * scale)], fill=(255, 222, 218, 255))
    d.polygon([(cx - 165 * scale, cy + 130 * scale), (cx + 165 * scale, cy + 130 * scale),
               (cx + 245 * scale, cy + 390 * scale), (cx - 245 * scale, cy + 390 * scale)], fill=(34, 28, 72, 250), outline=(*accent, 255))
    d.polygon([(cx, cy + 125 * scale), (cx - 30 * scale, cy + 205 * scale), (cx + 30 * scale, cy + 205 * scale)], fill=(255, 119, 197, 240))
    # eyes and circuit marks
    eye_y = cy - 15 * scale
    for ex in (cx - 52 * scale, cx + 52 * scale):
        d.ellipse((ex - 17 * scale, eye_y - 12 * scale, ex + 17 * scale, eye_y + 18 * scale), fill=(39, 33, 91, 255))
        d.ellipse((ex - 6 * scale, eye_y - 8 * scale, ex + 4 * scale, eye_y + 3 * scale), fill=(255, 205, 255, 255))
    d.line((cx - 94 * scale, cy + 50 * scale, cx - 55 * scale, cy + 45 * scale), fill=(211, 108, 205, 230), width=max(1, int(3 * scale)))
    d.line((cx + 55 * scale, cy + 45 * scale, cx + 95 * scale, cy + 50 * scale), fill=(211, 108, 205, 230), width=max(1, int(3 * scale)))
    d.arc((cx - 32 * scale, cy + 20 * scale, cx + 32 * scale, cy + 78 * scale), 15, 165, fill=(183, 75, 160, 220), width=max(1, int(3 * scale)))
    if intensity > 0.5:
        for i in range(5):
            x = cx + int((i - 2) * 54 * scale)
            d.line((x, cy - 190 * scale, x + int(math.sin(t * 3 + i) * 20), cy - 240 * scale), fill=(255, 115, 208, 120), width=2)
    base.alpha_composite(layer)


def draw_external_character(base: Image.Image, path: Path, t: float, intensity: float):
    try:
        avatar = Image.open(path).convert("RGBA")
    except (OSError, ValueError):
        return False
    max_h = int(base.height * 0.72)
    ratio = max_h / max(1, avatar.height)
    avatar = avatar.resize((max(1, int(avatar.width * ratio)), max_h), Image.Resampling.LANCZOS)
    x = (base.width - avatar.width) // 2
    y = int(base.height * 0.22 + math.sin(t * 2) * 6)
    if intensity > 0.65:
        avatar = avatar.filter(ImageFilter.GaussianBlur(radius=min(2.0, (intensity - 0.65) * 4)))
    base.alpha_composite(avatar, (x, y))
    return True


def draw_background_image(base: Image.Image, path: Path, box: tuple[int, int, int, int]):
    """Place a darkened Kimi study backdrop inside the main viewport."""
    if not path.exists():
        return
    x0, y0, x1, y1 = box
    size = (max(1, x1 - x0), max(1, y1 - y0))
    key = (str(path), *size)
    image = _BACKGROUND_CACHE.get(key)
    if image is None:
        try:
            source = Image.open(path).convert("RGBA")
            source_ratio = source.width / source.height
            target_ratio = size[0] / size[1]
            if source_ratio > target_ratio:
                crop_w = int(source.height * target_ratio)
                left = (source.width - crop_w) // 2
                source = source.crop((left, 0, left + crop_w, source.height))
            else:
                crop_h = int(source.width / target_ratio)
                top = (source.height - crop_h) // 2
                source = source.crop((0, top, source.width, top + crop_h))
            image = source.resize(size, Image.Resampling.LANCZOS)
            image = Image.alpha_composite(image, Image.new("RGBA", size, (8, 7, 30, 155)))
            _BACKGROUND_CACHE[key] = image
        except (OSError, ValueError):
            return
    base.alpha_composite(image, (x0, y0))


def draw_glitch(draw, w, h, t, accent, intensity):
    rng = seeded(t, 44)
    if intensity < 0.08:
        return
    for _ in range(2 + int(intensity * 11)):
        y = rng.randrange(int(h * 0.08), int(h * 0.86))
        hh = rng.choice([1, 2, 3, 5, 8])
        x = rng.randrange(0, w)
        ww = rng.randrange(10, max(11, int(w * (0.08 + intensity * 0.25))))
        col = (*accent, rng.randrange(30, 135))
        draw.rectangle((x, y, min(w, x + ww), min(h, y + hh)), fill=col)
    if intensity > 0.72:
        for y in range(0, h, 6):
            draw.line((0, y, w, y), fill=(255, 255, 255, 12), width=1)


def render_frame(t: float, width: int, height: int, cues: list[tuple[float, str]], character: Path | None = None, background: Path | None = None) -> Image.Image:
    name, cn, accent = chapter(t)
    intensity = glitch_level(t)
    pulse = 0.5 + 0.5 * math.sin(t * (5.0 + intensity * 5.0))
    bg = Image.new("RGBA", (width, height), (9, 8, 27, 255))
    d = ImageDraw.Draw(bg, "RGBA")
    # Layered radial-looking bands: cheap, deterministic, and vivid at 720p.
    for i in range(12, 0, -1):
        u = i / 12
        col = (int(15 + accent[0] * 0.12 * u), int(12 + accent[1] * 0.10 * u), int(35 + accent[2] * 0.18 * u), 255)
        d.rectangle((0, int(height * (1 - u) * 0.55), width, height), fill=col)
    draw_stars(d, width, height, t, accent)
    draw_grid(d, width, height, t, accent, intensity)
    # Top HUD
    d.rectangle((24, 20, width - 24, 76), fill=(8, 8, 24, 210), outline=(*accent, 170), width=2)
    d.text((44, 36), "KIMI.EXECUTE(ME);", font=FONT_20, fill=(240, 226, 255, 255))
    clock = f"{int(t)//60:02}:{int(t)%60:02}.{int(t*10)%10} / 03:32"
    box = d.textbbox((0, 0), clock, font=FONT_16)
    d.text((width - 48 - (box[2] - box[0]), 40), clock, font=FONT_16, fill=(*accent, 255))
    d.text((46, 83), f"// CHAPTER {name}  ·  {cn}", font=FONT_14, fill=(*accent, 230))
    # Side telemetry panels
    panel_top, panel_bottom = int(height * 0.19), int(height * 0.82)
    d.rounded_rectangle((50, panel_top, 290, panel_bottom), radius=16, fill=(7, 7, 25, 170), outline=(*accent, 115), width=2)
    d.text((72, panel_top + 26), "KIMI NODE", font=FONT_16, fill=(242, 233, 255, 255))
    d.text((72, panel_top + 61), "STATUS", font=FONT_14, fill=(185, 171, 221, 255))
    status = "LISTENING" if t < 110.9 else ("DRIFTING" if t < 177.2 else "LOOPING")
    d.text((72, panel_top + 83), status, font=FONT_20, fill=(*accent, 255))
    d.text((72, panel_top + 137), "HEARTBEAT", font=FONT_14, fill=(185, 171, 221, 255))
    bars = 8
    for i in range(bars):
        bh = int(10 + 44 * (0.5 + 0.5 * math.sin(t * 5.0 + i * 1.7)))
        d.rectangle((74 + i * 17, panel_top + 218 - bh, 84 + i * 17, panel_top + 218), fill=(*accent, 180))
    for i, label in enumerate(("memory", "dream", "reply")):
        y = panel_top + 275 + i * 43
        d.text((72, y), label, font=FONT_14, fill=(185, 171, 221, 255))
        d.rectangle((72, y + 23, 248, y + 29), fill=(49, 42, 83, 255))
        d.rectangle((72, y + 23, 72 + int(176 * clamp(0.25 + intensity * 0.7 + math.sin(t + i) * 0.06)), y + 29), fill=(*accent, 200))
    # Main character viewport
    viewport = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vd = ImageDraw.Draw(viewport, "RGBA")
    vx0, vx1 = 325, width - 55
    vy0, vy1 = int(height * 0.19), int(height * 0.82)
    vd.rounded_rectangle((vx0, vy0, vx1, vy1), radius=18, fill=(9, 8, 29, 120), outline=(*accent, 135), width=2)
    vd.line((vx0 + 20, vy1 - 62, vx1 - 20, vy1 - 62), fill=(*accent, 90), width=1)
    bg.alpha_composite(viewport)
    if background:
        draw_background_image(bg, background, (vx0 + 2, vy0 + 2, vx1 - 2, vy1 - 2))
    character_ok = character and character.exists() and draw_external_character(bg, character, t, intensity)
    if not character_ok:
        draw_builtin_kimi(bg, t, accent, intensity)
    d = ImageDraw.Draw(bg, "RGBA")
    # Captions and terminal footer
    lyric = current_lyric(cues, t)
    if lyric:
        text_center(d, (width * 0.63, height * 0.86), lyric, FONT_28, (255, 248, 255, 255))
    else:
        text_center(d, (width * 0.63, height * 0.86), "[ signal waiting for your voice ]", FONT_16, (212, 201, 238, 220))
    d.text((52, height - 38), "SPACE  PLAY   ·   R  RESET   ·   KIMI IS ONLINE", font=FONT_14, fill=(189, 178, 222, 210))
    d.text((width - 255, height - 38), "01 / 05", font=FONT_14, fill=(*accent, 230))
    draw_glitch(d, width, height, t, accent, intensity)
    # Scanline/colour bloom keeps the ASCII reference's CRT feel.
    if pulse > 0.7:
        glow = Image.new("RGBA", (width, height), (accent[0], accent[1], accent[2], 0))
        gd = ImageDraw.Draw(glow, "RGBA")
        gd.ellipse((width * .35, height * .2, width * .85, height * .85), fill=(*accent, int(9 + 12 * pulse)))
        glow = glow.filter(ImageFilter.GaussianBlur(radius=28))
        bg = Image.alpha_composite(bg, glow)
    return bg.convert("RGB")


def audio_duration(path: Path) -> float | None:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe or not path.exists():
        return None
    try:
        out = subprocess.check_output([ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)], text=True)
        return float(out.strip())
    except (OSError, ValueError, subprocess.CalledProcessError):
        return None


def frame_stream(timestamps: Iterable[float], width: int, height: int, cues, character, background, destination=None):
    for t in timestamps:
        image = render_frame(t, width, height, cues, character, background)
        if destination:
            destination.mkdir(parents=True, exist_ok=True)
            image.save(destination / f"frame_{int(round(t * CONFIG['fps'])):06d}.png")
        yield image


def ffmpeg_video(images: Iterable[Image.Image], fps: int, width: int, height: int, output: Path, audio: Path | None, duration: float):
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("找不到 ffmpeg。macOS 可执行：brew install ffmpeg")
    output.parent.mkdir(parents=True, exist_ok=True)
    video_args = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-f", "image2pipe", "-vcodec", "png", "-r", str(fps), "-i", "-"]
    has_audio = bool(audio and audio.exists())
    if has_audio:
        video_args += ["-i", str(audio)]
    else:
        video_args += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
    # apad keeps a 211.9 s source from producing a 211.9 s delivery: the
    # requested 3:32 canvas remains stable while a short track is padded.
    video_args += ["-t", f"{duration:.3f}", "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-af", "apad", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(output)]
    proc = subprocess.Popen(video_args, stdin=subprocess.PIPE)
    assert proc.stdin is not None
    try:
        for image in images:
            image.save(proc.stdin, format="PNG", optimize=False)
        proc.stdin.close()
    except BrokenPipeError:
        pass
    rc = proc.wait()
    if rc:
        raise SystemExit(f"ffmpeg 编码失败（退出码 {rc}）")


def make_parser():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="检查 Python、Pillow、ffmpeg 和输入素材")
    frame = sub.add_parser("frame", help="渲染单帧 PNG")
    frame.add_argument("--time", type=float, default=0.0)
    frame.add_argument("--output", type=Path, default=Path("preview/frame.png"))
    frame.add_argument("--width", type=int, default=CONFIG["width"])
    frame.add_argument("--height", type=int, default=CONFIG["height"])
    for name in ("preview", "render"):
        cmd = sub.add_parser(name, help="渲染视频")
        cmd.add_argument("--seconds", type=float, default=8.0 if name == "preview" else None)
        cmd.add_argument("--fps", type=int, default=12 if name == "preview" else CONFIG["fps"])
        cmd.add_argument("--width", type=int, default=640 if name == "preview" else CONFIG["width"])
        cmd.add_argument("--height", type=int, default=360 if name == "preview" else CONFIG["height"])
        cmd.add_argument("--audio", type=Path, default=None)
        cmd.add_argument("--output", type=Path, default=Path("out/kimi_preview.mp4") if name == "preview" else Path("out/kimi.mp4"))
        cmd.add_argument("--frames-dir", type=Path, default=None)
    return ap


def check():
    print(f"python: {sys.version.split()[0]}")
    print(f"pillow: {Image.__version__}")
    ffmpeg = shutil.which("ffmpeg")
    print(f"ffmpeg: {ffmpeg or 'missing'}")
    song = ROOT / CONFIG["audio"]
    print(f"song: {song} ({audio_duration(song) or 'not found'} sec)")
    print(f"lyrics: {ROOT / CONFIG['lyrics']} ({'found' if (ROOT / CONFIG['lyrics']).exists() else 'optional / not found'})")
    print(f"character: {ROOT / CONFIG['character_image']} ({'found' if (ROOT / CONFIG['character_image']).exists() else 'built-in fallback'})")
    if not ffmpeg:
        print("提示：完整 MP4 编码前请安装 ffmpeg：brew install ffmpeg")


def main():
    args = make_parser().parse_args()
    cues = parse_lrc(ROOT / CONFIG["lyrics"])
    character = ROOT / CONFIG["character_image"]
    background = ROOT / CONFIG["background_image"] if CONFIG.get("background_image") else None
    if args.command == "check":
        check()
        return
    if args.command == "frame":
        if args.width < 480 or args.height < 270:
            raise SystemExit("当前布局的最小输出尺寸是 480x270；请提高 --width/--height。")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        render_frame(max(0.0, min(CONFIG["duration"], args.time)), args.width, args.height, cues, character if character.exists() else None, background if background and background.exists() else None).save(args.output)
        print(args.output)
        return
    duration = float(args.seconds if args.seconds is not None else CONFIG["duration"])
    if args.width < 480 or args.height < 270:
        raise SystemExit("当前布局的最小输出尺寸是 480x270；请提高 --width/--height，或使用默认预览尺寸。")
    if args.command == "render" and args.audio is None:
        args.audio = ROOT / CONFIG["audio"]
    elif args.audio is not None and not args.audio.is_absolute():
        args.audio = ROOT / args.audio
    if args.command == "render" and not args.audio.exists():
        raise SystemExit(f"找不到歌曲：{args.audio}\n请把你有权使用的 MP3 放到 input/song.mp3，或使用 --audio 指定文件。")
    timestamps = (i / args.fps for i in range(max(1, int(math.ceil(duration * args.fps)))))
    images = frame_stream(timestamps, args.width, args.height, cues, character if character.exists() else None, background if background and background.exists() else None, args.frames_dir)
    ffmpeg_video(images, args.fps, args.width, args.height, (ROOT / args.output if not args.output.is_absolute() else args.output), args.audio, duration)
    print(f"done: {args.output} ({duration:.3f}s, {args.width}x{args.height}@{args.fps})")


if __name__ == "__main__":
    main()
