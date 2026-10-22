#!/usr/bin/env python3
"""Compose approved Wavvy scene assets without changing scene content."""

from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
INPUT = HERE.parent
ROOT = HERE.parents[3]
SCENE = HERE / "orange-kitchen-draft-v5.png"
LOGO = ROOT / "brand/logo_wavvy.png"
BACKGROUND = INPUT / "loop.png"
THUMB = INPUT / "thumb.jpg"
PHONE = HERE / "final-thumb-phone-320x180.jpg"

APPROVED_SHA256 = "cf0cfbf5d10b88585a188054ba1ba839a47f7b08fca1b649f2d62c664e97f8c1"
BACKGROUND_SIZE = (3840, 2160)
THUMB_SIZE = (2560, 1440)
PHONE_SIZE = (320, 180)
INK = (36, 41, 35, 255)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if sha256(SCENE) != APPROVED_SHA256:
        raise ValueError("Approved v5 scene SHA-256 differs; stop before composition")
    for path in (BACKGROUND, THUMB, PHONE):
        if path.exists():
            raise FileExistsError(f"Refusing to overwrite: {path}")

    with Image.open(SCENE) as source:
        scene = source.convert("RGB")
    background = scene.resize(BACKGROUND_SIZE, Image.Resampling.LANCZOS)
    background.save(BACKGROUND, format="PNG", optimize=True)

    canvas = background.resize(THUMB_SIZE, Image.Resampling.LANCZOS).convert("RGBA")
    with Image.open(LOGO) as logo_source:
        logo = logo_source.convert("RGBA")
    logo = logo.crop(logo.getchannel("A").getbbox())
    logo = logo.resize((450, 265), Image.Resampling.LANCZOS)
    brand_shape = Image.new("RGBA", logo.size, INK)
    brand_shape.putalpha(logo.getchannel("A"))
    canvas.alpha_composite(brand_shape, (68, 50))

    overlay = Image.new("RGBA", THUMB_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    time_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 92)
    title_font = ImageFont.truetype("/System/Library/Fonts/AppleSDGothicNeo.ttc", 188, index=16)
    draw.text((550, 125), "17:30", font=time_font, fill=INK, anchor="lt")
    title = "기분좋아져라"
    title_width = draw.textlength(title, font=title_font)
    draw.text((THUMB_SIZE[0] - 102 - title_width, 84), title, font=title_font, fill=INK, anchor="lt")
    canvas = Image.alpha_composite(canvas, overlay).convert("RGB")
    canvas.save(THUMB, format="JPEG", quality=91, subsampling=0, optimize=True)
    canvas.resize(PHONE_SIZE, Image.Resampling.LANCZOS).save(
        PHONE, format="JPEG", quality=91, subsampling=0, optimize=True
    )


if __name__ == "__main__":
    main()
