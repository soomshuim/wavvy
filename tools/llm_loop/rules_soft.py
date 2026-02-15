"""Soft rule evaluation."""

from __future__ import annotations

import json
from dataclasses import dataclass
import re

from llm_loop.llm_client import LLMConfig, generate_text
from llm_loop.renderer import load_template, render_template


@dataclass(frozen=True)
class SoftRuleResult:
    scores: dict[str, int]
    risk_level: str
    notes: list[str]
    recommendation: str
    raw: str


def evaluate_soft_rules(
    *,
    prompt_dir,
    llm_cfg: LLMConfig,
    values: dict[str, object],
) -> SoftRuleResult:
    template = load_template(prompt_dir, "validate_soft.md")
    prompt = render_template(template, values)
    text = generate_text(llm_cfg, prompt)
    parsed = _parse_json_block_safe(text)
    return SoftRuleResult(
        scores=parsed.get("scores", {}),
        risk_level=parsed.get("risk_level", "unknown"),
        notes=parsed.get("notes", []),
        recommendation=parsed.get("recommendation", "NEEDS_REWRITE"),
        raw=text,
    )


def _parse_json_block_safe(text: str) -> dict:
    stripped = text.strip()
    candidates = [stripped]

    if stripped.startswith("```"):
        block = stripped.strip("`")
        if block.startswith("json"):
            block = block[4:].strip()
        candidates.append(block)

    brace_match = re.search(r"\{.*\}", stripped, flags=re.DOTALL)
    if brace_match:
        candidates.append(brace_match.group(0))

    for candidate in candidates:
        try:
            data = json.loads(candidate)
            if isinstance(data, dict):
                return _normalize_soft_result(data)
        except json.JSONDecodeError:
            continue

    # Fallback: keep pipeline alive and request rewrite by default.
    return {
        "scores": {},
        "risk_level": "high",
        "notes": ["soft validation parse failed; manual review required"],
        "recommendation": "NEEDS_REWRITE",
    }


def _normalize_soft_result(data: dict) -> dict:
    scores = data.get("scores", {})
    if not isinstance(scores, dict):
        scores = {}
    norm_scores: dict[str, int] = {}
    for key, value in scores.items():
        try:
            norm_scores[str(key)] = int(value)
        except (TypeError, ValueError):
            continue

    notes = data.get("notes", [])
    if not isinstance(notes, list):
        notes = [str(notes)]
    notes = [str(note) for note in notes]

    recommendation = str(data.get("recommendation", "NEEDS_REWRITE")).upper().strip()
    if recommendation not in {"READY_FOR_REVIEW", "NEEDS_REWRITE"}:
        recommendation = "NEEDS_REWRITE"

    risk = str(data.get("risk_level", "unknown")).lower().strip()
    if risk not in {"low", "medium", "high"}:
        risk = "unknown"

    return {
        "scores": norm_scores,
        "risk_level": risk,
        "notes": notes,
        "recommendation": recommendation,
    }
