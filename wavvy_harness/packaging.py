"""Opt-in, machine-readable packaging and thumbnail checks for a series."""

from __future__ import annotations

import json
import re
from pathlib import Path


def packaging_contract(series_path: Path) -> tuple[dict | None, list[str]]:
    """Read only the dedicated concept section; older series have no contract."""
    try:
        concept = (series_path / "concept.md").read_text(encoding="utf-8")
    except OSError as error:
        return None, [f"Packaging contract: cannot read concept.md: {error}"]
    match = re.search(r"(?m)^## Packaging Contract\s*$", concept)
    if not match:
        return None, []
    next_heading = re.search(r"(?m)^## ", concept[match.end():])
    body = concept[match.end():match.end() + next_heading.start()] if next_heading else concept[match.end():]
    fields: dict[str, list[str]] = {}
    for key, value in re.findall(r"(?m)^-\s+(Playlist repeat|Thumbnail layout):\s*(.*?)\s*$", body):
        fields.setdefault(key, []).append(value.strip("` "))
    errors: list[str] = []
    for key in ("Playlist repeat", "Thumbnail layout"):
        if len(fields.get(key, [])) != 1:
            errors.append(f"Packaging contract requires exactly one '{key}' field")
    if errors:
        return None, errors
    repeat_text = fields["Playlist repeat"][0]
    if not re.fullmatch(r"[1-9]\d*", repeat_text):
        errors.append("Packaging contract Playlist repeat must be a positive integer")
    layout_name = fields["Thumbnail layout"][0]
    layout_path = (series_path / layout_name).resolve()
    if not layout_path.is_relative_to(series_path.resolve()) or layout_path.suffix != ".json":
        errors.append("Packaging contract Thumbnail layout must be a JSON file inside the series")
    if errors:
        return None, errors
    return {"repeat": int(repeat_text), "layout_path": layout_path}, []


def _mask_bbox(mask) -> tuple[int, int, int, int] | None:
    return mask.getbbox()


def _actual_overlay_mask(thumbnail, scene, region):
    from PIL import Image

    thumb_pixels = thumbnail.crop(region).convert("RGB").tobytes()
    scene_pixels = scene.crop(region).convert("RGB").tobytes()
    values = bytearray()
    for offset in range(0, len(thumb_pixels), 3):
        target = thumb_pixels[offset:offset + 3]
        original = scene_pixels[offset:offset + 3]
        # Source and JPEG differ by 0-3 in untouched areas. The white overlay
        # exceeds this margin by dozens even on the dawn sky.
        values.append(255 if max(t - s for t, s in zip(target, original)) > 55 and min(target) > 175 else 0)
    return Image.frombytes("L", (region[2] - region[0], region[3] - region[1]), bytes(values))


def _mask_iou(actual, expected) -> float:
    from PIL import ImageChops

    overlap = ImageChops.lighter(actual, expected)
    union_pixels = sum(bool(value) for value in overlap.tobytes())
    if not union_pixels:
        return 0.0
    intersection = ImageChops.darker(actual, expected)
    return sum(bool(value) for value in intersection.tobytes()) / union_pixels


def check_thumbnail_layout(series_path: Path, repo_root: Path, layout_path: Path) -> tuple[list[dict], list[str]]:
    """Compare rendered white marks with the real logo and Pacifico glyphs."""
    from PIL import Image, ImageDraw, ImageFont

    errors: list[str] = []
    checks: list[dict] = []
    try:
        layout = json.loads(layout_path.read_text(encoding="utf-8"))
        if layout.get("schema") != "wavvy.thumbnail_layout.v1":
            raise ValueError("unsupported schema")
        if set(layout) != {"schema", "scene", "thumbnail", "logo", "time", "cadence", "tempo", "reference_psds"}:
            raise ValueError("unexpected or missing fields")
        scene_path = (series_path / layout["scene"]).resolve()
        thumbnail_path = (series_path / layout["thumbnail"]).resolve()
        asset_path = (repo_root / layout["logo"]["asset"]).resolve()
        for path, parent in ((scene_path, series_path), (thumbnail_path, series_path), (asset_path, repo_root)):
            if not path.is_relative_to(parent.resolve()):
                raise ValueError(f"path escapes its parent: {path}")
        if asset_path != (repo_root / "brand" / "logo_wavvy.png").resolve():
            raise ValueError("logo asset must be brand/logo_wavvy.png")
        if layout["time"]["font"] != "Pacifico-Regular":
            raise ValueError("time font must be Pacifico-Regular")
        if layout["cadence"].get("text") != "Cadence" or layout["cadence"].get("font") != "SF-Pro-Display-Thin":
            raise ValueError("cadence must use 'Cadence' in SF Pro Display Thin")
        if layout["tempo"].get("text") != "180 BPM" or layout["tempo"].get("font") != "HelveticaNeue-CondensedBlack":
            raise ValueError("tempo must use '180 BPM' in Helvetica Neue Condensed Black")
        if layout["reference_psds"] != ["SERIES/06-00/input/thumb.psd", "SERIES/11-00/input/thumb.psd"]:
            raise ValueError("reference PSDs must be the inspected 06:00 and 11:00 originals")
        logo = layout["logo"]
        time = layout["time"]
        logo_x, logo_y, logo_w = (int(logo[key]) for key in ("x", "y", "source_width"))
        time_x, time_y, font_size = (int(time[key]) for key in ("x", "y", "font_size"))
        if logo_w <= 0 or font_size <= 0 or time["text"] != f"{series_path.name.replace('-', ':')}":
            raise ValueError("invalid logo width, font size, or series time text")
        with Image.open(thumbnail_path) as image:
            thumbnail = image.convert("RGB")
        with Image.open(scene_path) as image:
            scene = image.convert("RGB")
        if thumbnail.size != scene.size:
            raise ValueError("scene and thumbnail dimensions differ")
        width, height = thumbnail.size
        if width < 640 or height < 360:
            raise ValueError("thumbnail is too small for layout inspection")
        with Image.open(asset_path) as image:
            logo_asset = image.convert("RGBA")
        scaled_height = round(logo_asset.height * logo_w / logo_asset.width)
        logo_alpha = logo_asset.resize((logo_w, scaled_height), Image.Resampling.LANCZOS).getchannel("A")
        font = ImageFont.truetype("Pacifico-Regular.ttf", font_size)
        if font.getname() != ("Pacifico", "Regular"):
            raise ValueError("loaded time font is not Pacifico Regular")
        expected_logo = Image.new("L", (width, height))
        expected_logo.paste(logo_alpha, (logo_x, logo_y))
        expected_logo = expected_logo.point(lambda value: 255 if value > 127 else 0)
        expected_time = Image.new("L", (width, height))
        ImageDraw.Draw(expected_time).text((time_x, time_y), time["text"], font=font, fill=255)
        expected_time = expected_time.point(lambda value: 255 if value > 127 else 0)
        logo_box = _mask_bbox(expected_logo)
        time_box = _mask_bbox(expected_time)
        if not logo_box or not time_box or logo_box[2] >= time_box[0]:
            raise ValueError("logo and time masks are missing or overlap")
        divide = (logo_box[2] + time_box[0]) // 2
        top = round(height * 0.27)
        logo_region = (0, 0, divide, top)
        time_region = (divide, 0, round(width * 0.36), top)
        for label, region, expected, threshold in (
            ("logo", logo_region, expected_logo, 0.87),
            ("time", time_region, expected_time, 0.85),
        ):
            actual = _actual_overlay_mask(thumbnail, scene, region)
            wanted = expected.crop(region)
            score = _mask_iou(actual, wanted)
            passed = score >= threshold
            checks.append({"name": f"thumbnail_{label}_pixels", "status": "PASS" if passed else "FAIL", "detail": f"mask_iou={score:.3f} minimum={threshold:.2f}"})
            if not passed:
                errors.append(f"thumbnail {label} differs from the required logo/Pacifico raster (IoU {score:.3f})")
        actual_logo = _actual_overlay_mask(thumbnail, scene, logo_region).getbbox()
        actual_time = _actual_overlay_mask(thumbnail, scene, time_region).getbbox()
        if not actual_logo or not actual_time:
            raise ValueError("logo or time overlay is not visible")
        logo_w_visible = actual_logo[2] - actual_logo[0]
        logo_h_visible = actual_logo[3] - actual_logo[1]
        time_w_visible = actual_time[2] - actual_time[0]
        time_h_visible = actual_time[3] - actual_time[1]
        # 06:00/11:00 PSD layers: logo 377x223 on widths 2608/2532,
        # time 188x47 / 162x47 on height 1424. The approved 07:00 is
        # 264x154 and 134x34 on 1672x941. The bands allow export variation.
        size_ok = (0.13 <= logo_w_visible / width <= 0.165
                   and 0.029 <= time_h_visible / height <= 0.038
                   and 0.18 <= time_h_visible / logo_h_visible <= 0.245
                   and 0.055 <= time_w_visible / width <= 0.09)
        detail = (f"logo={logo_w_visible}x{logo_h_visible}/{width}x{height}; "
                  f"time={time_w_visible}x{time_h_visible}/{width}x{height}")
        checks.append({"name": "thumbnail_reference_proportions", "status": "PASS" if size_ok else "FAIL", "detail": detail})
        if not size_ok:
            errors.append("thumbnail logo/time proportions differ from 06:00 and 11:00 PSD references")
        actual_text_boxes: dict[str, tuple[int, int, int, int]] = {}
        for label, font_file, font_index, expected_name, min_iou, width_band, height_band in (
            ("cadence", "SF-Pro-Display-Thin.otf", 0, ("SF Pro Display", "Thin"), 0.60, (0.09, 0.13), (0.03, 0.05)),
            ("tempo", "HelveticaNeue.ttc", 9, ("Helvetica Neue", "Condensed Black"), 0.75, (0.29, 0.36), (0.10, 0.14)),
        ):
            field = layout[label]
            field_x, field_y, field_size = (int(field[key]) for key in ("x", "y", "font_size"))
            if field_size <= 0:
                raise ValueError(f"{label} font size must be positive")
            field_font = ImageFont.truetype(font_file, field_size, index=font_index)
            if field_font.getname() != expected_name:
                raise ValueError(f"{label} font file does not match required family/style")
            expected = Image.new("L", (width, height))
            ImageDraw.Draw(expected).text((field_x, field_y), field["text"], font=field_font, fill=255)
            expected = expected.point(lambda value: 255 if value > 127 else 0)
            bbox = expected.getbbox()
            if not bbox:
                raise ValueError(f"{label} expected raster is empty")
            region = (max(0, bbox[0] - 10), max(0, bbox[1] - 20),
                      min(width, bbox[2] + 10), min(height, bbox[3] + 20))
            actual = _actual_overlay_mask(thumbnail, scene, region)
            score = _mask_iou(actual, expected.crop(region))
            actual_box = actual.getbbox()
            if actual_box:
                actual_text_boxes[label] = (region[0] + actual_box[0], region[1] + actual_box[1],
                                            region[0] + actual_box[2], region[1] + actual_box[3])
            proportion_ok = bool(actual_box and width_band[0] <= (actual_box[2] - actual_box[0]) / width <= width_band[1]
                                 and height_band[0] <= (actual_box[3] - actual_box[1]) / height <= height_band[1])
            passed = score >= min_iou and proportion_ok
            checks.append({"name": f"thumbnail_{label}_pixels", "status": "PASS" if passed else "FAIL",
                           "detail": f"mask_iou={score:.3f} minimum={min_iou:.2f}; proportions={'ok' if proportion_ok else 'bad'}"})
            if not passed:
                errors.append(f"thumbnail {label} text/raster is missing or differs from the approved design")
        cadence_box = actual_text_boxes.get("cadence")
        tempo_box = actual_text_boxes.get("tempo")
        lower_left_ok = bool(
            cadence_box and tempo_box
            and 0.02 <= cadence_box[0] / width <= 0.12
            and 0.02 <= tempo_box[0] / width <= 0.12
            and tempo_box[2] / width <= 0.50
            and 0.68 <= cadence_box[1] / height <= 0.79
            and 0.77 <= tempo_box[1] / height <= 0.86
            and tempo_box[3] / height <= 0.97
            and cadence_box[3] < tempo_box[1]
            and abs(cadence_box[0] - tempo_box[0]) / width <= 0.03
        )
        checks.append({"name": "thumbnail_lower_left_layout", "status": "PASS" if lower_left_ok else "FAIL",
                       "detail": f"actual cadence={cadence_box} tempo={tempo_box} image={width}x{height}"})
        if not lower_left_ok:
            errors.append("thumbnail Cadence/180 BPM must be aligned at lower left, with Cadence above 180 BPM")
    except (OSError, ValueError, KeyError, TypeError, ImportError) as error:
        checks.append({"name": "thumbnail_layout_contract", "status": "FAIL", "detail": str(error)})
        errors.append(f"thumbnail layout cannot be verified: {error}")
    return checks, errors
