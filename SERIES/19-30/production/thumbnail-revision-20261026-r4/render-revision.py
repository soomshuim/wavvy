#!/usr/bin/env python3
"""R4: approved scene plus unchanged R3 white pixel logo/glow, without text layers."""
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
import hashlib
import json
import shutil
import numpy as np
from PIL import Image, ImageChops, ImageFilter

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SERIES = ROOT / "SERIES/19-30"
R3 = SERIES / "production/thumbnail-revision-20261026-r3"
LOOP = SERIES / "input/loop.png"
THUMB = SERIES / "input/thumb.jpg"
SIZE = (3840, 2160)
EXPECTED_LOOP = "349391ef58a643a3e10bf09c8cadd65dbfd5d565676bc9130325b43304422564"
EXPECTED_R3 = "357cf1812ae79d03f46310f4989dc877998ec668a04df42bd4dd06e652aa0234"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path):
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)

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
    assert sha(R3 / "thumb-r3.jpg") == EXPECTED_R3
    previous = HERE / "previous-thumb-r3.jpg"
    if not previous.exists():
        assert sha(THUMB) == EXPECTED_R3
        shutil.copy2(THUMB, previous)
    assert sha(previous) == EXPECTED_R3
    prior = json.loads((R3 / "manifest.json").read_text())
    with Image.open(LOOP) as image:
        background = image.convert("RGB")
    with Image.open(R3 / "logo-white-r3.png") as image:
        logo = image.convert("RGBA")
    assert logo.size == (640, 349)
    logo_canvas = Image.new("RGBA", SIZE)
    logo_canvas.alpha_composite(logo, (140, 100))
    # Exactly the R3 logo-only glow pass. Neither text mask nor text glow is used.
    composed = glow(background, logo_canvas.getchannel("A"), (140, 100, 780, 449))
    composed = Image.alpha_composite(composed.convert("RGBA"), logo_canvas).convert("RGB")
    editable = HERE / "thumb-editable.png"
    composed.save(editable, compress_level=9)
    revision = HERE / "thumb-r4.jpg"
    for quality in (96, 94, 92, 90, 88, 86, 84, 82, 80):
        buffer = BytesIO()
        composed.save(buffer, format="JPEG", quality=quality, subsampling=0, optimize=True)
        encoded = buffer.getvalue()
        if len(encoded) <= 2_000_000:
            break
    revision.write_bytes(encoded)
    shutil.copy2(revision, THUMB)
    with Image.open(THUMB) as final:
        for size, name in [((960, 540), "thumb-preview-960.png"), ((320, 180), "thumb-phone-320.png")]:
            final.resize(size, Image.Resampling.LANCZOS).save(HERE / name)
    with Image.open(R3 / "thumb-master.png") as old:
        upper = ImageChops.difference(old.convert("RGB").crop((0,0,3840,800)), composed.crop((0,0,3840,800))).getbbox()
        lower_changed = ImageChops.difference(old.convert("RGB").crop((0,1200,2200,2160)), composed.crop((0,1200,2200,2160))).getbbox() is not None
    lower_background_match = ImageChops.difference(composed.crop((0,1000,3840,2160)), background.crop((0,1000,3840,2160))).getbbox() is None
    assert upper is None
    assert lower_changed and lower_background_match
    assert sha(LOOP) == EXPECTED_LOOP
    manifest = {
        "schema": "wavvy.thumbnail_revision.v4", "revision": "r4", "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "user_request_exact": "그냥 좌하단 텍스트 없애라 내가 할게",
        "change": "Omit both lower-left Running Mix / 170BPM text cores and their glow passes; keep the approved scene and upper-left R3 logo/glow unchanged.",
        "approved_scene": prior["approved_scene"], "background": prior["background"],
        "previous_revision": {"manifest": rel(R3 / "manifest.json"), "review": rel(R3 / "isolated-review.md"), "telegram_record": rel(R3 / "telegram-delivery.json"), "preserved_thumb": rel(previous), "sha256": EXPECTED_R3},
        "logo": {**prior["logo"], "composition_asset": rel(R3 / "logo-white-r3.png"), "unchanged_from_r3": True},
        "glow": {**prior["glow"], "applied_to": ["Wavvy logo"], "unchanged_logo_glow_from_r3": True},
        "typography": {"text_exact": [], "removed": ["Running Mix", "170BPM"], "text_glow_removed": True, "user_will_add_text": True},
        "outputs": [{"path": rel(path), "sha256": sha(path), "bytes": path.stat().st_size, "size": list(Image.open(path).size)} for path in [THUMB, revision, editable, HERE / "thumb-preview-960.png", HERE / "thumb-phone-320.png"]],
        "jpeg": {"quality": quality, "bytes": len(encoded), "subsampling": 0},
        "validation": {"loop_unchanged": True, "r3_preserved": True, "upper_800px_identical_to_r3_lossless": upper is None, "lower_text_region_changed": lower_changed, "entire_lower_1160px_matches_plain_background_exactly": lower_background_match, "text_masks_used": False, "text_glow_used": False, "full_visual": "pending", "phone_visual": "pending"},
        "review_status": "pending_controller_direct_visual_confirmation_no_separate_review_required",
        "telegram_delivery": "not_sent_pending_controller_confirmation",
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"thumb": rel(THUMB), "editable": rel(editable), "preview": rel(HERE / "thumb-preview-960.png"), "phone": rel(HERE / "thumb-phone-320.png"), "size": list(SIZE), "jpeg_bytes": len(encoded), "png_bytes": editable.stat().st_size, "checks": manifest["validation"]}, ensure_ascii=False))

if __name__ == "__main__":
    main()
