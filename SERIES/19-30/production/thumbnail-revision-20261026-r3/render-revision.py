#!/usr/bin/env python3
"""Keep the pixel scene/logo, compose real Thin/Black sans and colored bloom."""
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
import hashlib
import json
import math
import shutil

import numpy as np
from fontTools.ttLib import TTFont
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SERIES = ROOT / "SERIES/19-30"
R2 = SERIES / "production/thumbnail-revision-20261026-r2"
LOOP = SERIES / "input/loop.png"
THUMB = SERIES / "input/thumb.jpg"
LOGO = R2 / "logo-pixel-generated.png"
THIN = Path.home() / "Library/Fonts/Pretendard-Thin.otf"
BLACK = Path.home() / "Library/Fonts/Pretendard-Black.otf"
SIZE = (3840, 2160)
EXPECTED_LOOP = "349391ef58a643a3e10bf09c8cadd65dbfd5d565676bc9130325b43304422564"
EXPECTED_R2 = "47c09e51bc26d6f64245ceabca281384da4f92ee4b8d3be6cd238d2b5abb5c04"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path):
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def type_mask(text, path, size):
    # Supersampling preserves the font's real outline with smooth alpha edges.
    font = ImageFont.truetype(str(path), size * 3)
    box = font.getbbox(text)
    high = Image.new("L", (box[2] - box[0], box[3] - box[1]))
    ImageDraw.Draw(high).text((-box[0], -box[1]), text, font=font, fill=255)
    return high.resize((math.ceil(high.width / 3), math.ceil(high.height / 3)), Image.Resampling.LANCZOS)


def place(mask, xy):
    canvas = Image.new("L", SIZE)
    canvas.paste(mask, xy)
    return canvas


def spectrum(box, phase):
    # Spatially distinct hues avoid a stack of colors mixing into a white haze.
    colors = np.array([(0, 245, 255), (255, 12, 170), (157, 35, 255), (18, 94, 255), (0, 245, 255)], dtype=float)
    x = ((np.arange(SIZE[0]) - box[0]) / (box[2] - box[0]) + phase) % 1.0
    stops = np.linspace(0, 1, len(colors))
    line = np.stack([np.interp(x, stops, colors[:, channel]) for channel in range(3)], axis=-1).astype(np.uint8)
    return Image.fromarray(line[None, :, :]).resize(SIZE, Image.Resampling.NEAREST)


def glow(base, mask, box):
    # Colored light only. There is no dark edge, hard outline or stroked core.
    settings = [(140, 100, 0.48), (70, 150, 0.20), (32, 190, 0.00), (14, 210, 0.00)]
    for radius, peak, phase in settings:
        halo = mask.filter(ImageFilter.GaussianBlur(radius))
        maximum = halo.getextrema()[1]
        if maximum:
            halo = halo.point(lambda v: min(255, round(v * peak / maximum)))
        light = Image.composite(spectrum(box, phase), Image.new("RGB", SIZE), halo)
        base = ImageChops.screen(base, light)
    return base


def main():
    assert sha(LOOP) == EXPECTED_LOOP
    assert TTFont(THIN)["OS/2"].usWeightClass == 100
    assert TTFont(BLACK)["OS/2"].usWeightClass == 900
    previous = HERE / "previous-thumb-r2.jpg"
    if not previous.exists():
        assert sha(THUMB) == EXPECTED_R2
        shutil.copy2(THUMB, previous)
    assert sha(previous) == EXPECTED_R2
    r2_manifest = json.loads((R2 / "manifest.json").read_text())
    assert sha(LOGO) == r2_manifest["logo"]["sha256"]

    with Image.open(LOOP) as image:
        background = image.convert("RGB")
    with Image.open(LOGO) as image:
        original_logo = image.resize((640, 349), Image.Resampling.NEAREST)
        logo = Image.new("RGBA", original_logo.size, (255, 255, 255, 0))
        logo.putalpha(original_logo.getchannel("A"))
    logo.save(HERE / "logo-white-r3.png")
    logo_canvas = Image.new("RGBA", SIZE)
    logo_canvas.alpha_composite(logo, (140, 100))
    title = type_mask("Running Mix", THIN, 190)
    bpm = type_mask("170BPM", BLACK, 468)
    assert bpm.width <= 1860
    title_alpha = place(title, (140, 1430))
    bpm_alpha = place(bpm, (140, 1640))
    masks = [(logo_canvas.getchannel("A"), (140, 100, 780, 449)),
             (title_alpha, (140, 1430, 140 + title.width, 1430 + title.height)),
             (bpm_alpha, (140, 1640, 140 + bpm.width, 1640 + bpm.height))]
    composed = background
    for mask, box in masks:
        composed = glow(composed, mask, box)
    # Exact original logo and exact font cores are composed above every light halo.
    text_alpha = ImageChops.lighter(title_alpha, bpm_alpha)
    composed = Image.composite(Image.new("RGB", SIZE, (255, 255, 255)), composed, text_alpha)
    composed = Image.alpha_composite(composed.convert("RGBA"), logo_canvas).convert("RGB")
    master = HERE / "thumb-master.png"
    composed.save(master, compress_level=9)
    revision = HERE / "thumb-r3.jpg"
    for quality in (96, 94, 92, 90, 88, 86, 84, 82, 80):
        buffer = BytesIO()
        composed.save(buffer, format="JPEG", quality=quality, subsampling=0, optimize=True)
        encoded = buffer.getvalue()
        if len(encoded) <= 2_000_000:
            break
    revision.write_bytes(encoded)
    shutil.copy2(revision, THUMB)
    with Image.open(THUMB) as final:
        assert final.size == SIZE
        for size, name in [((960, 540), "thumb-preview-960.png"), ((320, 180), "thumb-phone-320.png")]:
            final.resize(size, Image.Resampling.LANCZOS).save(HERE / name)
    assert sha(LOOP) == EXPECTED_LOOP
    title.save(HERE / "running-mix-core-alpha.png")
    bpm.save(HERE / "170bpm-core-alpha.png")
    manifest = {
        "schema": "wavvy.thumbnail_revision.v3", "revision": "r3", "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "user_requests_exact": ["아니 running mix와 170bpm은 일반 산셰리프로 하고 글로우만 줘.", "Pretendard 최대 최소 굵기로", "글로우는 더 강하고 다양한 컬러로. 로고 글로우도 마찬가지", "로고 외곽에 스트로크 안보이게. 폰트든 로고든 흰 컬러만 있어야해. 글로우 제외", "글로우 제외는 글로우 빼란 말 아님"],
        "approved_scene": r2_manifest["approved_scene"],
        "previous_revision": {"manifest": rel(R2 / "manifest.json"), "review": rel(R2 / "isolated-review.md"), "telegram_record": rel(R2 / "telegram-delivery.json"), "preserved_thumb": rel(previous), "sha256": EXPECTED_R2},
        "background": {"path": rel(LOOP), "sha256": EXPECTED_LOOP, "untouched": True, "native_4k": False},
        "logo": {**r2_manifest["logo"], "white_composite_asset": rel(HERE / "logo-white-r3.png"), "core_color": "#FFFFFF", "original_alpha_preserved": True, "preserved_r2_shape_and_placement": True, "glow_updated_per_latest_request": True},
        "typography": {"family": "Pretendard", "core_color": "#FFFFFF", "rendering": "full-resolution vector font rasterization with 3x supersampling and Lanczos alpha antialiasing; no pixel grid, alpha threshold, or hard outline", "text_exact": ["Running Mix", "170BPM"], "Running Mix": {"path": str(THIN), "sha256": sha(THIN), "style": "Thin", "weight": 100, "font_size": 190, "xy": [140, 1430], "size": list(title.size)}, "170BPM": {"path": str(BLACK), "sha256": sha(BLACK), "style": "Black", "weight": 900, "font_size": 468, "xy": [140, 1640], "size": list(bpm.size)}, "synthetic_weight": False, "ordinary_sans_copy_only_logo_pixel": True},
        "glow": {"colors": ["cyan", "hot pink", "violet", "electric blue"], "radii": [140, 70, 32, 14], "peak_alpha_per_halo": [100, 150, 190, 210], "spatial_hue_crossovers": True, "method": "smooth multi-radius Gaussian colored bloom with screen blend, pure-white font/logo cores above all light", "applied_to": ["Wavvy logo", "Running Mix", "170BPM"], "pixel_outline": False, "stroke_width": 0, "dark_keyline": False},
        "references": r2_manifest["references"],
        "font_precedent": {"source": "SERIES/07-00/input/thumb.psd", "Running Mix": "Pretendard-Thin", "previous_bpm": "Pretendard-ExtraBold", "latest_override": "170BPM uses actual Pretendard-Black weight900 per user request; Running Mix uses actual Thin100"},
        "bpm_copy_is_user_requested_not_audio_conversion_completion": True,
        "outputs": [{"path": rel(path), "sha256": sha(path), "bytes": path.stat().st_size, "size": list(Image.open(path).size)} for path in [THUMB, revision, master, HERE / "thumb-preview-960.png", HERE / "thumb-phone-320.png"]],
        "jpeg": {"quality": quality, "bytes": len(encoded), "subsampling": 0},
        "validation": {"loop_unchanged": True, "r2_backup_matches": True, "logo_source_unchanged": True, "actual_font_weights": [100, 900], "title_antialias_levels": len(set(title.tobytes())), "bpm_antialias_levels": len(set(bpm.tobytes())), "full_visual": "pending", "phone_visual": "pending"},
        "review_status": "pending_controller_review", "telegram_delivery": "not_sent_pending_controller_review",
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"thumb": rel(THUMB), "preview": rel(HERE / "thumb-preview-960.png"), "phone": rel(HERE / "thumb-phone-320.png"), "size": list(SIZE), "bytes": len(encoded), "title_size": title.size, "bpm_size": bpm.size, "loop_unchanged": True}, ensure_ascii=False))


if __name__ == "__main__":
    main()
