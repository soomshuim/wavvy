"""Run summaries and QC report builder."""

from __future__ import annotations

from llm_loop.config import RunConfig
from llm_loop.loader import SeriesContext
from llm_loop.rules_hard import HardRuleResult
from llm_loop.rules_soft import SoftRuleResult
from llm_loop.versioning import ArtifactPaths


def build_run_summary(
    cfg: RunConfig, context: SeriesContext, artifacts: ArtifactPaths, *, dry_run: bool
) -> str:
    mode = "DRY-RUN" if dry_run else "WRITE"
    return "\n".join(
        [
            f"[llm_loop] mode={mode}",
            f"series={cfg.series} track={cfg.track:02d} version=v{artifacts.version}",
            f"provider={cfg.provider} model={cfg.model} iterations={cfg.max_iterations}",
            f"cross_series={cfg.cross_series_mode} temperature={cfg.temperature}",
            f"concept_exists={'yes' if context.has_concept else 'no'} path={context.concept_path}",
            f"lyrics={artifacts.lyrics}",
            f"style={artifacts.style}",
            f"exclude={artifacts.exclude}",
            f"qc={artifacts.qc}",
        ]
    )


def build_qc_report(
    cfg: RunConfig,
    context: SeriesContext,
    artifacts: ArtifactPaths,
    hard: HardRuleResult,
    soft: SoftRuleResult | None,
    revisions: list[str],
    verdict: str,
) -> str:
    hard_rows = ["| Rule | Status | Notes |", "|------|--------|-------|"]
    for row in hard.rows:
        hard_rows.append(f"| {row.rule} | {row.status} | {row.notes} |")

    if soft is None:
        soft_lines = ["- Not evaluated (dry-run or pre-LLM stage)."]
    else:
        soft_lines = [
            f"- recommendation: {soft.recommendation}",
            f"- risk_level: {soft.risk_level}",
        ]
        for key, value in soft.scores.items():
            soft_lines.append(f"- score.{key}: {value}")
        for note in soft.notes:
            soft_lines.append(f"- note: {note}")

    return "\n".join(
        [
            "# llm_loop QC Report",
            "",
            "## Run Metadata",
            f"- series: {cfg.series}",
            f"- track: {cfg.track:02d}",
            f"- provider: {cfg.provider}",
            f"- model: {cfg.model}",
            f"- version: v{artifacts.version}",
            f"- max_iterations: {cfg.max_iterations}",
            f"- cross_series: {cfg.cross_series_mode}",
            f"- concept_exists: {'yes' if context.has_concept else 'no'}",
            "",
            "## Hard Rule Table",
            *hard_rows,
            "",
            "## Soft Rule Notes",
            *soft_lines,
            "",
            "## Revision Summary",
            *([f"- {r}" for r in revisions] or ["- none"]),
            "",
            "## Final Verdict",
            f"- {verdict}",
            "",
        ]
    )
