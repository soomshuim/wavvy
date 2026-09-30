"""Header and section parsing shared by track-source archiving and gates."""

from __future__ import annotations

import re


SOURCE_SECTION_RE = re.compile(r"^===\s*([^=]+?)\s*===\s*$", re.MULTILINE)
SOURCE_HEADER_RE = re.compile(r"^([A-Za-z][A-Za-z0-9 _-]*):\s*(.*)$")
CANONICAL_HEADER_NAMES = {
    name.casefold(): name
    for name in (
        "Track", "Order", "Status", "Draft Scope", "Genre", "Type", "BPM",
        "Key", "Vocal", "Length", "Target Duration", "Meter", "Section Bars",
    )
}


def parse_track_source_fields(content: str) -> tuple[dict[str, str], dict[str, str]]:
    """Return canonical header metadata and sections, rejecting duplicate names."""
    matches = list(SOURCE_SECTION_RE.finditer(content))
    header = content[:matches[0].start()] if matches else content
    metadata: dict[str, str] = {}
    seen_header_names: set[str] = set()
    for line in header.splitlines():
        match = SOURCE_HEADER_RE.match(line.strip())
        if not match:
            continue
        normalized_name = " ".join(match.group(1).split())
        folded_name = normalized_name.casefold()
        if folded_name in seen_header_names:
            raise ValueError(f"duplicate {normalized_name} header field")
        seen_header_names.add(folded_name)
        metadata[CANONICAL_HEADER_NAMES.get(folded_name, normalized_name)] = match.group(2).strip()
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        name = match.group(1).strip().upper()
        if name in sections:
            raise ValueError(f"duplicate === {name} === section")
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        sections[name] = content[match.end():end].strip()
    return metadata, sections
