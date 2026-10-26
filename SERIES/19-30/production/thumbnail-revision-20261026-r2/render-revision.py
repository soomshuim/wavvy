#!/usr/bin/env python3
"""Compose the requested logo, true Bold pixel type and smooth light bloom."""
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
import hashlib
import json
import shutil

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SERIES = ROOT / "SERIES/19-30"
R1 = SERIES / "production/thumbnail-final-20261026"
LOOP = SERIES / "input/loop.png"
THUMB = SERIES / "input/thumb.jpg"
LOGO = HERE / "logo-pixel-generated.png"
FONT = HERE / "fonts/PixelifySans-variable.ttf"
SIZE = (3840, 2160)
GRID = (384, 216)
EXPECTED_LOOP = "349391ef58a643a3e10bf09c8cadd65dbfd5d565676bc9130325b43304422564"
EXPECTED_R1 = "2eee7e97a26fdaff03df1e6681c645bbd1cdcaf023be8cc7408103ab92842c56"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path):
    return str(path.relative_to(ROOT))


def text_mask(text, size, weight):
    font = ImageFont.truetype(str(FONT), size)
    font.set_variation_by_axes([weight])
    bbox = font.getbbox(text)
    mask = Image.new("L", (bbox[2] - bbox[0], bbox[3] - bbox[1]))
    ImageDraw.Draw(mask).text((-bbox[0], -bbox[1]), text, font=font, fill=255)
    return mask.point(lambda value: 255 if value >= 128 else 0)


def translated(mask, xy):
    result = Image.new("L", SIZE)
    result.paste(mask, xy)
    return result


def bloom(background, mask):
    # A narrow contrast edge sits beneath additive, continuously blurred light.
    edge = mask.filter(ImageFilter.MaxFilter(13))
    shadow = Image.new("RGB", SIZE, (3, 4, 20))
    background = Image.composite(shadow, background, edge.point(lambda v: v * 175 // 255))
    passes = [
        (96, (255, 30, 185), 210, (18, 12)),
        (60, (0, 211, 255), 190, (-9, -4)),
        (30, (255, 45, 201), 120, (8, 6)),
        (12, (15, 230, 255), 170, (-3, -2)),
    ]
    for radius, color, opacity, xy in passes:
        blurred = translated(mask, xy).filter(ImageFilter.GaussianBlur(radius))
        blurred = blurred.point(lambda v: v * opacity // 255)
        light = Image.composite(Image.new("RGB", SIZE, color), Image.new("RGB", SIZE), blurred)
        background = ImageChops.screen(background, light)
    return background


def main():
    assert sha(LOOP) == EXPECTED_LOOP, "Approved background changed"
    previous_path = HERE / "previous-thumb-r1.jpg"
    if not previous_path.exists():
        assert sha(THUMB) == EXPECTED_R1, "Unexpected thumbnail before backup"
        shutil.copy2(THUMB, previous_path)
    assert sha(previous_path) == EXPECTED_R1
    r1_manifest = json.loads((R1 / "manifest.json").read_text())

    with Image.open(LOOP) as image:
        background = image.convert("RGB")
    assert background.size == SIZE
    with Image.open(LOGO) as source_logo:
        assert source_logo.mode == "RGBA"
        logo = source_logo.resize((640, 349), Image.Resampling.NEAREST)
    logo_canvas = Image.new("RGBA", SIZE)
    logo_canvas.alpha_composite(logo, (140, 100))

    title = text_mask("Running Mix", 20, 700)
    bpm = text_mask("170BPM", 52, 700)
    text_grid = Image.new("L", GRID)
    text_grid.paste(title, (14, 143))
    text_grid.paste(bpm, (14, 164))
    text_alpha = text_grid.resize(SIZE, Image.Resampling.NEAREST)
    all_alpha = ImageChops.lighter(text_alpha, logo_canvas.getchannel("A"))
    composed = bloom(background, all_alpha)
    composed = Image.composite(Image.new("RGB", SIZE, (248, 254, 255)), composed, text_alpha)
    composed = Image.alpha_composite(composed.convert("RGBA"), logo_canvas).convert("RGB")

    master = HERE / "thumb-master.png"
    composed.save(master, compress_level=9)
    revision_jpg = HERE / "thumb-r2.jpg"
    for quality in (96, 94, 92, 90, 88, 86, 84, 82, 80):
        output = BytesIO()
        composed.save(output, format="JPEG", quality=quality, subsampling=0, optimize=True)
        encoded = output.getvalue()
        if len(encoded) <= 2_000_000:
            break
    revision_jpg.write_bytes(encoded)
    shutil.copy2(revision_jpg, THUMB)
    assert sha(THUMB) == sha(revision_jpg)
    with Image.open(THUMB) as final:
        assert final.size == SIZE
        for size, name in [((960, 540), "thumb-preview-960.png"), ((320, 180), "thumb-phone-320.png")]:
            final.resize(size, Image.Resampling.LANCZOS).save(HERE / name)
    assert sha(LOOP) == EXPECTED_LOOP
    medium = text_mask("170BPM", 52, 500)
    bold_fill = sum(bpm.histogram()[1:])
    medium_fill = sum(medium.histogram()[1:])
    manifest = {
        "schema": "wavvy.thumbnail_revision.v2",
        "revision": "r2",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "latest_request_exact": "로고는 좌측 상단이고 픽셀 퀄리티를 높여야해. 아예 픽셀버전 로고타입을 생성해서 합치는게 낫지 않을까? 글로우 효과는 픽셀이 아니어도 돼. 전혀 글로우 같지 않아. 폰트도 픽셀폰트지만 더 두껍고 가독성 좋은걸로",
        "previous_revision": {"manifest": rel(R1 / "manifest.json"), "review": rel(R1 / "isolated-review.md"), "telegram_record": rel(R1 / "telegram-delivery.json"), "preserved_thumb": rel(previous_path), "sha256": EXPECTED_R1},
        "approved_scene": r1_manifest["approved_source"],
        "background": {"path": rel(LOOP), "sha256": EXPECTED_LOOP, "untouched": True, "size": list(SIZE), "native_4k": False},
        "logo": {"path": rel(LOGO), "sha256": sha(LOGO), "generation_tool": "built-in image_gen.imagegen", "reference_path": "brand/logo_wavvy.png", "prompt_path": rel(HERE / "logo-prompt.txt"), "transparent_background": True, "spelling_visual_check": "Wavvy: uppercase W and lowercase a v v y; flowing underline retained", "process": "new generated pixel lettering; preserve generated RGBA, nearest-neighbor scale only; no low-resolution threshold extraction", "placement": "upper left", "xy": [140, 100], "size": list(logo.size)},
        "typography": {"font": "Pixelify Sans Bold", "font_path": rel(FONT), "font_sha256": sha(FONT), "weight_axis": 700, "previous_weight": 500, "bold_nonzero_fill_vs_medium": bold_fill / medium_fill, "font_source": "https://github.com/google/fonts/tree/main/ofl/pixelifysans", "font_license": rel(HERE / "fonts/OFL.txt"), "text_exact": ["Running Mix", "170BPM"], "pixel_grid": list(GRID), "output_scale": 10, "Running Mix": {"xy": [140, 1430], "size": [title.width * 10, title.height * 10], "font_size_grid": 20}, "170BPM": {"xy": [140, 1640], "size": [bpm.width * 10, bpm.height * 10], "font_size_grid": 52}},
        "glow": {"method": "smooth Gaussian cyan/magenta light bloom composed with screen blend", "blur_radii_full_resolution": [96, 60, 30, 12], "narrow_contrast_edge_radius": 6, "no_pixel_band_glow": True, "no_rectangular_backing": True},
        "references": r1_manifest["references"],
        "bpm_copy_is_user_requested_not_audio_conversion_completion": True,
        "time_digits_added": False,
        "outputs": [{"path": rel(path), "sha256": sha(path), "bytes": path.stat().st_size, "size": list(Image.open(path).size)} for path in [THUMB, revision_jpg, master, HERE / "thumb-preview-960.png", HERE / "thumb-phone-320.png"]],
        "jpeg": {"quality": quality, "bytes": len(encoded), "subsampling": 0},
        "validation": {"approved_background_hash_unchanged": True, "r1_backup_hash_matches": True, "full_size_visual": "pending", "phone_size_visual": "pending"},
        "review_status": "pending_controller_review",
        "telegram_delivery": "not_sent_pending_controller_review",
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"thumb": rel(THUMB), "preview": rel(HERE / "thumb-preview-960.png"), "phone": rel(HERE / "thumb-phone-320.png"), "size": list(SIZE), "jpeg_bytes": len(encoded), "bold_fill_ratio_vs_medium": bold_fill / medium_fill, "loop_unchanged": sha(LOOP) == EXPECTED_LOOP}, ensure_ascii=False))


if __name__ == "__main__":
    main()
