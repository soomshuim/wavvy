#!/usr/bin/env python3
"""Finish the approved v5 artwork with local sizing and exact pixel typography."""
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
import hashlib
import json
import shutil
import struct

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageStat

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SERIES = ROOT / "SERIES/19-30"
DRAFTS = SERIES / "production/thumbnail-drafts"
SOURCE = DRAFTS / "pixel-runner-v5.png"
LOGO = ROOT / "brand/logo_wavvy.png"
FONT = Path.home() / "Project/agent-center/skills/synced/635a1b15-68c4-4499-b29a-02a6deccccfb_b60ad9a3-6cf9-4a1f-beb2-457a1a47c205/canvas-design/canvas-fonts/PixelifySans-Medium.ttf"
EXPECTED_SOURCE = "b963bc8b0a3512e43f3b9558b524c0f051acdb228e687e74c50d981a292ed8f1"
SIZE = (3840, 2160)
GRID = (384, 216)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path):
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def preserve(path):
    if not path.exists():
        return None
    backup = HERE / "backups" / (path.stem + "-" + sha(path)[:12] + path.suffix)
    backup.parent.mkdir(exist_ok=True)
    if not backup.exists():
        shutil.copy2(path, backup)
    assert sha(path) == sha(backup)
    return rel(backup)


def reference_layers():
    path = ROOT / "SERIES/07-00/input/thumb.psd"
    data = path.read_bytes()
    u32 = lambda p: struct.unpack_from(">I", data, p)[0]
    p = 26
    p += 4 + u32(p)
    p += 4 + u32(p)
    p += 8
    count = abs(struct.unpack_from(">h", data, p)[0])
    p += 2
    result = []
    for _ in range(count):
        top, left, bottom, right = struct.unpack_from(">iiii", data, p)
        p += 16
        channels = struct.unpack_from(">H", data, p)[0]
        p += 2 + 6 * channels + 12
        n = u32(p)
        p += 4
        extra = data[p:p + n]
        p += n
        q = 0
        q += 4 + struct.unpack_from(">I", extra, q)[0]
        q += 4 + struct.unpack_from(">I", extra, q)[0]
        length = extra[q]
        name = extra[q + 1:q + 1 + length].decode("mac_roman", "replace")
        if name in ("180BPM", "Running Mix"):
            box = [left, top, right, bottom]
            result.append({"layer": name, "bbox": box,
                           "normalized_bbox": [left / 2532, top / 1424, right / 2532, bottom / 1424],
                           "height_ratio": (bottom - top) / 1424,
                           "width_ratio": (right - left) / 2532})
    with Image.open(path) as a, Image.open(ROOT / "SERIES/07-00/input/thumb.jpg") as b:
        difference = ImageStat.Stat(ImageChops.difference(a.convert("RGB"), b.convert("RGB"))).mean
    return {"path": rel(path), "jpg_path": "SERIES/07-00/input/thumb.jpg", "sha256": sha(path),
            "size": [2532, 1424], "measurement": "PSD layer pixel bounds; current JPG/composite compared",
            "jpg_composite_mean_absolute_difference_rgb": difference, "elements": result}


def reference_17():
    path = ROOT / "SERIES/17-00/input/thumb.jpg"
    result = []
    with Image.open(path) as im:
        for name, roi in [("AUTUMN", (40, 480, 1080, 710)),
                          ("WALK", (40, 700, 850, 930)),
                          ("Wavvy logo, excluding time digits", (40, 20, 450, 330))]:
            crop = im.crop(roi).convert("RGB")
            mask = Image.new("L", crop.size)
            mask.putdata([255 if min(c) > 190 and max(c) - min(c) < 45 else 0 for c in crop.getdata()])
            box = mask.getbbox()
            assert box
            box = [box[0] + roi[0], box[1] + roi[1], box[2] + roi[0], box[3] + roi[1]]
            result.append({"element": name, "bbox": box,
                           "normalized_bbox": [box[0] / im.width, box[1] / im.height, box[2] / im.width, box[3] / im.height]})
    return {"path": rel(path), "sha256": sha(path), "size": [2532, 1424],
            "measurement": "near-white pixel bounds in isolated dark-background regions", "elements": result}


def text_mask(text, size):
    font = ImageFont.truetype(str(FONT), size)
    box = font.getbbox(text)
    mask = Image.new("L", (box[2] - box[0], box[3] - box[1]))
    ImageDraw.Draw(mask).text((-box[0], -box[1]), text, font=font, fill=255)
    return mask.point(lambda value: 255 if value >= 128 else 0)


def place(destination, source, xy):
    destination.paste(source, xy)


def paint_pixel_glow(base, mask):
    # Discrete square-pixel bands, with a dark keyline instead of a backing plate.
    for radius, color, opacity in [(4, (238, 22, 183), 42), (3, (0, 218, 255), 75),
                                   (1, (5, 3, 24), 250), (0, (247, 253, 255), 255)]:
        band = mask if radius == 0 else mask.filter(ImageFilter.MaxFilter(radius * 2 + 1))
        band = band.point(lambda value: value * opacity // 255)
        layer = Image.new("RGBA", GRID, (*color, 0))
        layer.putalpha(band)
        base = Image.alpha_composite(base, layer.resize(SIZE, Image.Resampling.NEAREST))
    return base


def main():
    assert sha(SOURCE) == EXPECTED_SOURCE, "Approved source changed"
    assert FONT.is_file()
    HERE.mkdir(exist_ok=True)
    reference_07 = reference_layers()
    reference17 = reference_17()
    with Image.open(SOURCE) as original:
        assert original.size == (1672, 941)
        background = original.convert("RGB").resize(SIZE, Image.Resampling.NEAREST)
    loop_path = SERIES / "input/loop.png"
    thumb_path = SERIES / "input/thumb.jpg"
    backups = {rel(p): preserve(p) for p in (loop_path, thumb_path)}
    background.save(loop_path, compress_level=9)
    core_mask = Image.new("L", GRID)
    # 07:00 source: label y=.6601H, BPM y=.7591H; left=.0355-.0403W.
    # Keep that hierarchy, with the main line narrowed slightly to clear the approved shoe.
    title = text_mask("Running Mix", 20)
    bpm = text_mask("170BPM", 52)
    place(core_mask, title, (14, 143))
    place(core_mask, bpm, (14, 164))
    with Image.open(LOGO) as original_logo:
        alpha = original_logo.getchannel("A")
        alpha = alpha.crop(alpha.getbbox()).resize((60, 35), Image.Resampling.LANCZOS)
        alpha = alpha.point(lambda value: 255 if value >= 96 else 0)
        place(core_mask, alpha, (14, 103))
    thumbnail = paint_pixel_glow(background.convert("RGBA"), core_mask).convert("RGB")
    master_path = HERE / "thumb-master.png"
    thumbnail.save(master_path, compress_level=9)
    selected_quality = None
    selected_bytes = None
    for quality in (96, 94, 92, 90, 88, 86, 84, 82, 80):
        candidate = BytesIO()
        thumbnail.save(candidate, format="JPEG", quality=quality, subsampling=0, optimize=True)
        selected_quality, selected_bytes = quality, candidate.getvalue()
        if len(selected_bytes) <= 2_000_000:
            break
    thumb_path.write_bytes(selected_bytes)
    with Image.open(thumb_path) as saved_jpg:
        preview_source = saved_jpg.convert("RGB")
    preview_source.resize((960, 540), Image.Resampling.LANCZOS).save(HERE / "thumb-preview-960.png")
    preview_source.resize((320, 180), Image.Resampling.LANCZOS).save(HERE / "thumb-phone-320.png")
    with Image.open(loop_path) as saved:
        assert saved.size == SIZE and ImageChops.difference(saved.convert("RGB"), background).getbbox() is None
    with Image.open(thumb_path) as saved:
        assert saved.size == SIZE
    assert sha(SOURCE) == EXPECTED_SOURCE
    manifest = {
        "schema": "wavvy.final_artwork.v1", "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "approved_source": {"path": rel(SOURCE), "sha256": EXPECTED_SOURCE, "size": [1672, 941]},
        "approval": {"user_reply_exact": "1", "selected_option_exact": "이 배치로 진행 — 현재 인물 위치와 배경을 유지해요.",
                     "evidence_source": "controller relay of the latest v5 approval"},
        "latest_typography_request_exact": "로고도 픽셀 버전에 픽셀 글로우 효과 / 좌측하단 / Running Mix / 170BPM / 텍스트도 픽셀 폰트 글로우 효과 넣어서",
        "precedent_request_exact": "폰트 크기나 배치는 이전 시리즈 참고해",
        "method": {"image_generation_used_for_final": False, "native_4k": False,
                   "background": "Pillow RGB nearest-neighbor resize, 1672x941 to 3840x2160, no crop or new scene generation",
                   "scale_x": 3840 / 1672, "scale_y": 2160 / 941,
                   "composition": "local Pillow graphics, exact supplied copy; typography at 384x216 and nearest-neighbor x10",
                   "font_path": str(FONT), "font_sha256": sha(FONT), "font_name": "Pixelify Sans Medium",
                   "logo_path": rel(LOGO), "logo_sha256": sha(LOGO),
                   "logo_process": "real alpha silhouette, crop alpha bounds, downsample 60x35, binary threshold 96, nearest-neighbor x10",
                   "pixel_glow": "discrete magenta/cyan alpha bands, dark 1-grid-pixel keyline, near-white core; no rectangular plate"},
        "text": ["Running Mix", "170BPM"], "time_digits_added": False,
        "bpm_copy_is_user_requested_not_a_new_audio_measurement": True,
        "layout_grid": {"size": list(GRID), "output_scale": 10,
                        "logo": {"xy": [14, 103], "size": [60, 35]},
                        "Running Mix": {"xy": [14, 143], "size": list(title.size), "font_size": 20},
                        "170BPM": {"xy": [14, 164], "size": list(bpm.size), "font_size": 52},
                        "core_left_margin_ratio": 14 / 384,
                        "core_bottom_margin_ratio": (216 - 164 - bpm.height) / 216,
                        "reason_for_main_line_size": "nearest pixel-font fit to 07:00's 17.06% height while keeping the glow left of the woman's shoe; resulting height 15.74%"},
        "references": [reference_07, reference17],
        "prompt_chain": [{"path": rel(p), "sha256": sha(p)} for p in [DRAFTS / "prompt.txt", DRAFTS / "prompt-v2.txt", DRAFTS / "prompt-v3.txt", DRAFTS / "prompt-v4.txt", DRAFTS / "prompt-v5.txt"]],
        "outputs": [{"path": rel(p), "sha256": sha(p), "bytes": p.stat().st_size,
                     "size": list(Image.open(p).size)} for p in [loop_path, thumb_path, master_path, HERE / "thumb-preview-960.png", HERE / "thumb-phone-320.png"]],
        "jpeg": {"quality": selected_quality, "subsampling": 0, "bytes": len(selected_bytes)},
        "backups": backups,
        "validation": {"loop_exactly_matches_nearest_scaled_v5": True, "source_hash_unchanged": True,
                       "full_size_visual_inspection": "pending", "phone_size_visual_inspection": "pending"},
        "telegram_delivery": "withheld_for_controller_visual_review"
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"loop": rel(loop_path), "thumb": rel(thumb_path), "master": rel(master_path),
                      "size": list(SIZE), "jpeg_quality": selected_quality, "jpeg_bytes": len(selected_bytes),
                      "manifest": rel(HERE / "manifest.json"), "layout": manifest["layout_grid"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
