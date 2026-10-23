"""Check the objective parts of a Wavvy YouTube title before release."""

from __future__ import annotations

import re


TIME_SLOT = re.compile(r"^(?:[01]\d|2[0-3])-[0-5]\d$")


def validate_youtube_title(title: str, series_name: str) -> list[str]:
    """Return errors for platform length, section boundaries, brand, and slot.

    Genre, uses, and the image in the hook require a person to compare the
    title with the series. Approved titles may also have a different section
    count, such as the 07:00 running mix.
    """
    errors: list[str] = []
    if len(title) > 100:
        errors.append(f"YouTube title exceeds 100 characters ({len(title)})")

    sections = title.split(" | ")
    if any(not section.strip() for section in sections):
        errors.append("YouTube title has an empty section")
    if not sections or sections[0] != "Playlist":
        errors.append("YouTube title must start with 'Playlist | '")

    if TIME_SLOT.fullmatch(series_name):
        expected_slot = series_name.replace("-", ":")
        if len(sections) < 5 or sections[-2] != "Wavvy":
            errors.append("YouTube title must place 'Wavvy' before the series time")
        if sections[-1] != expected_slot:
            errors.append(f"YouTube title must end with series time {expected_slot}")
    elif not (len(sections) >= 3 and sections[-1] == "Wavvy") and not (
        len(sections) >= 4 and sections[-2] == "Wavvy" and bool(sections[-1].strip())
    ):
        errors.append("YouTube compilation title must end with 'Wavvy' or 'Wavvy | series name'")
    return errors
