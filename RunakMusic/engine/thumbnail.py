"""Builds a branded 'now playing' thumbnail: the original YouTube thumbnail,
cropped to 16:9, with a dark gradient, the Runak Music brand pill, the track
title, and a duration badge burned in.

Runs synchronously (PIL isn't async) — call it via loop.run_in_executor,
which is what RunakMusic.engine.artist.get_thumbnail does.
"""

import io
import os
import textwrap

import requests
from PIL import Image, ImageDraw, ImageFont

THUMB_DIR = "thumbnails"
CANVAS_SIZE = (1280, 720)

BRAND_NAME = "RUNAK MUSIC"
BRAND_TEXT_COLOR = (255, 255, 255)
ACCENT_COLOR = (255, 61, 113)  # change to taste — this is the pill/badge color

# Installed via `fonts-dejavu-core` in the Dockerfile. Falls back to PIL's
# built-in bitmap font if the ttf isn't present on the host.
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def _font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def _cover_resize(img: Image.Image, size: tuple) -> Image.Image:
    """Resize + center-crop so `img` fills `size` exactly, like CSS
    background-size: cover."""
    target_w, target_h = size
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    new_w, new_h = int(src_w * scale + 0.5), int(src_h * scale + 0.5)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


def generate_thumbnail(video_id: str, title: str, duration: str, thumbnail_url: str):
    """Download `thumbnail_url`, brand it, cache it under thumbnails/{id}.png
    and return the local path — or None if anything about this failed (the
    caller should just fall back to plain text in that case)."""
    os.makedirs(THUMB_DIR, exist_ok=True)
    out_path = os.path.join(THUMB_DIR, f"{video_id}.png")
    if os.path.exists(out_path):
        return out_path

    try:
        resp = requests.get(thumbnail_url, timeout=15)
        resp.raise_for_status()
        base = Image.open(io.BytesIO(resp.content)).convert("RGB")
    except Exception:
        return None

    canvas = _cover_resize(base, CANVAS_SIZE)
    draw = ImageDraw.Draw(canvas, "RGBA")

    # Dark gradient across the bottom third, so white text stays legible
    # over any thumbnail.
    gradient_height = 320
    gradient = Image.new("RGBA", (CANVAS_SIZE[0], gradient_height), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(gradient)
    for y in range(gradient_height):
        alpha = int(200 * (y / gradient_height))
        gdraw.line([(0, y), (CANVAS_SIZE[0], y)], fill=(0, 0, 0, alpha))
    canvas.paste(gradient, (0, CANVAS_SIZE[1] - gradient_height), gradient)

    # Brand pill, top-left.
    brand_font = _font(FONT_BOLD, 34)
    pad_x, pad_y = 22, 12
    bbox = draw.textbbox((0, 0), BRAND_NAME, font=brand_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pill_w, pill_h = tw + pad_x * 2, th + pad_y * 2
    pill_pos = (32, 28)
    draw.rounded_rectangle(
        [pill_pos, (pill_pos[0] + pill_w, pill_pos[1] + pill_h)],
        radius=pill_h // 2,
        fill=(0, 0, 0, 160),
    )
    draw.text(
        (pill_pos[0] + pad_x, pill_pos[1] + pad_y - bbox[1]),
        BRAND_NAME,
        font=brand_font,
        fill=ACCENT_COLOR,
    )

    # Title, wrapped to at most 2 lines with an ellipsis if it's longer.
    title_font = _font(FONT_BOLD, 46)
    lines = textwrap.wrap(title, width=34)
    wrapped = lines[:2]
    if len(lines) > 2:
        wrapped[-1] = wrapped[-1].rstrip() + "…"
    y = CANVAS_SIZE[1] - gradient_height + 40
    for line in wrapped:
        draw.text((40, y), line, font=title_font, fill=BRAND_TEXT_COLOR)
        line_bbox = draw.textbbox((0, 0), line, font=title_font)
        y += (line_bbox[3] - line_bbox[1]) + 14

    # Duration badge, bottom-right ("Live" for livestreams).
    duration_font = _font(FONT_REGULAR, 30)
    badge_text = duration or "Live"
    bbox = draw.textbbox((0, 0), badge_text, font=duration_font)
    bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    badge_x = CANVAS_SIZE[0] - bw - 70
    badge_y = CANVAS_SIZE[1] - bh - 46
    draw.rounded_rectangle(
        [(badge_x - 18, badge_y - 10), (badge_x + bw + 18, badge_y + bh + 14)],
        radius=14,
        fill=ACCENT_COLOR + (230,),
    )
    draw.text((badge_x, badge_y - bbox[1]), badge_text, font=duration_font, fill=(255, 255, 255))

    canvas.convert("RGB").save(out_path, "PNG")
    return out_path
