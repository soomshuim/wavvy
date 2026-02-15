#!/usr/bin/env python3
"""CLI entrypoint for GPT Loop Sidecar."""

from __future__ import annotations

import re
from pathlib import Path

import click

from llm_loop.config import RunConfig, resolve_openai_api_key, validate_config
from llm_loop.cross_series import build_cross_series_context
from llm_loop.llm_client import LLMClientError, LLMConfig, generate_text
from llm_loop.loader import load_series_context
from llm_loop.renderer import load_template, render_template
from llm_loop.reporter import build_qc_report, build_run_summary
from llm_loop.rules_hard import HardRuleResult, run_hard_rules
from llm_loop.rules_soft import SoftRuleResult, evaluate_soft_rules
from llm_loop.versioning import build_artifact_paths, ensure_no_overwrite


EXIT_OK = 0
EXIT_INPUT_ERROR = 1
EXIT_API_OR_NETWORK = 2
EXIT_VALIDATION_FAIL = 3
EXIT_INTERNAL = 4


@click.command()
@click.argument("command_name", type=click.Choice(["run"]))
@click.option("--series", required=True, type=str, help="Series name, e.g. PM_0900")
@click.option("--track", required=True, type=int, help="Track number, e.g. 7")
@click.option(
    "--provider",
    type=click.Choice(["openai"]),
    default="openai",
    show_default=True,
)
@click.option("--model", default="gpt-5.2", show_default=True)
@click.option("--max-iterations", default=3, show_default=True, type=int)
@click.option(
    "--cross-series",
    "cross_series_mode",
    type=click.Choice(["off", "lite", "embed"]),
    default="lite",
    show_default=True,
)
@click.option("--dry-run", is_flag=True, default=False, help="Do not write outputs")
@click.option("--temperature", default=1.0, show_default=True, type=float)
@click.option("--seed", default="", type=str, help="Optional reproducibility hint")
@click.option(
    "--output-dir",
    default="",
    type=str,
    help="Override output directory. Default: SERIES/<series>",
)
@click.option("--verbose", is_flag=True, default=False)
def main(
    command_name: str,
    series: str,
    track: int,
    provider: str,
    model: str,
    max_iterations: int,
    cross_series_mode: str,
    dry_run: bool,
    temperature: float,
    seed: str,
    output_dir: str,
    verbose: bool,
) -> None:
    """Run M1 sidecar flow with versioning and dry-run support."""
    del command_name  # reserved for future subcommands

    try:
        project_root = Path(__file__).resolve().parents[1]
        default_series_dir = project_root / "SERIES" / series
        target_dir = Path(output_dir) if output_dir else default_series_dir
        prompt_dir = project_root / "MASTER" / "prompts" / "llm_loop"
        cfg = RunConfig(
            project_root=project_root,
            series=series,
            track=track,
            provider=provider,
            model=model,
            max_iterations=max_iterations,
            cross_series_mode=cross_series_mode,
            dry_run=dry_run,
            temperature=temperature,
            seed=seed,
            output_dir=target_dir,
            verbose=verbose,
            prompt_dir=prompt_dir,
            openai_api_key=resolve_openai_api_key(),
        )
        validate_config(cfg)

        context = load_series_context(cfg)
        artifacts = build_artifact_paths(cfg.output_dir, cfg.track)
        ensure_no_overwrite(artifacts)

        if cfg.dry_run:
            click.echo(build_run_summary(cfg, context, artifacts, dry_run=True))
            raise SystemExit(EXIT_OK)

        cfg.output_dir.mkdir(parents=True, exist_ok=True)
        llm_cfg = LLMConfig(
            provider=cfg.provider,
            model=cfg.model,
            temperature=cfg.temperature,
            api_key=cfg.openai_api_key,
        )
        cross_series_context = build_cross_series_context(
            cfg.project_root, cfg.series, cfg.cross_series_mode
        )

        values = _build_template_values(cfg, context, cross_series_context)
        lyrics = _generate_from_template(cfg, llm_cfg, "generate_lyrics.md", values)
        style = _generate_from_template(cfg, llm_cfg, "generate_style.md", values)
        exclude = _generate_from_template(cfg, llm_cfg, "generate_exclude.md", values)

        revisions: list[str] = []
        hard = run_hard_rules(cfg, lyrics=lyrics, style=style, exclude=exclude)

        for iteration in range(1, cfg.max_iterations + 1):
            if hard.passed:
                break
            revisions.append(f"iteration {iteration}: hard-fail -> revise")
            revised = _revise_outputs(cfg, llm_cfg, values, lyrics, style, exclude, hard)
            lyrics, style, exclude = revised
            hard = run_hard_rules(cfg, lyrics=lyrics, style=style, exclude=exclude)

        soft: SoftRuleResult | None = None
        verdict = "NEEDS_REWRITE"
        if hard.passed:
            soft_values = dict(values)
            soft_values.update(
                {
                    "lyrics_text": lyrics,
                    "style_text": style,
                    "exclude_text": exclude,
                    "soft_rules_excerpt": context.rules_excerpt.get("lyrics", ""),
                }
            )
            soft = evaluate_soft_rules(prompt_dir=cfg.prompt_dir, llm_cfg=llm_cfg, values=soft_values)
            verdict = soft.recommendation
        else:
            revisions.append("hard-rules failed at max iterations")

        artifacts.lyrics.write_text(lyrics + "\n", encoding="utf-8")
        artifacts.style.write_text(style + "\n", encoding="utf-8")
        artifacts.exclude.write_text(exclude + "\n", encoding="utf-8")
        artifacts.qc.write_text(
            build_qc_report(cfg, context, artifacts, hard, soft, revisions, verdict),
            encoding="utf-8",
        )

        click.echo(build_run_summary(cfg, context, artifacts, dry_run=False))
        raise SystemExit(EXIT_OK if verdict == "READY_FOR_REVIEW" else EXIT_VALIDATION_FAIL)
    except click.ClickException as exc:
        click.echo(f"[ERROR] {exc.message}", err=True)
        raise SystemExit(EXIT_INPUT_ERROR) from exc
    except LLMClientError as exc:
        click.echo(f"[ERROR] LLM call failed: {exc}", err=True)
        raise SystemExit(EXIT_API_OR_NETWORK) from exc
    except SystemExit:
        raise
    except Exception as exc:  # pragma: no cover - defensive catch for CLI stability
        click.echo(f"[ERROR] Internal failure: {exc}", err=True)
        raise SystemExit(EXIT_INTERNAL) from exc


def _build_template_values(cfg: RunConfig, context, cross_series_context: str) -> dict[str, object]:
    return {
        "series": cfg.series,
        "track": f"{cfg.track:02d}",
        "track_context": context.track_section or context.concept_excerpt[:1200],
        "seed_constraints": context.rules_excerpt.get("roles", ""),
        "variation_plan": "minimum 2 variable slots, keep seed core fixed",
        "lyrics_rules_excerpt": context.rules_excerpt.get("lyrics", ""),
        "style_rules_excerpt": context.rules_excerpt.get("style", ""),
        "exclude_rules_excerpt": context.rules_excerpt.get("style", ""),
        "exclude_baseline": "Airy, Falsetto, Whisper, Harmonized, Backing vocals, Choir, Doubled vocals",
        "char_limit": cfg.style_char_limit,
        "forbidden_patterns": "arrangement/mix/mastering directives in lyrics",
        "cross_series_context": cross_series_context,
    }


def _generate_from_template(cfg: RunConfig, llm_cfg: LLMConfig, template_name: str, values: dict[str, object]) -> str:
    template = load_template(cfg.prompt_dir, template_name)
    prompt = render_template(template, values)
    return generate_text(llm_cfg, prompt).strip()


def _revise_outputs(
    cfg: RunConfig,
    llm_cfg: LLMConfig,
    values: dict[str, object],
    lyrics: str,
    style: str,
    exclude: str,
    hard: HardRuleResult,
) -> tuple[str, str, str]:
    revised_values = dict(values)
    revised_values.update(
        {
            "lyrics_text": lyrics,
            "style_text": style,
            "exclude_text": exclude,
            "hard_fail_items": "\n".join(hard.fail_items),
            "soft_improvement_items": "",
        }
    )
    template = load_template(cfg.prompt_dir, "revise.md")
    prompt = render_template(template, revised_values)
    raw = generate_text(llm_cfg, prompt)
    return _parse_revise_sections(raw, lyrics, style, exclude)


def _parse_revise_sections(
    text: str, fallback_lyrics: str, fallback_style: str, fallback_exclude: str
) -> tuple[str, str, str]:
    lyrics = _extract_section(text, "LYRICS") or fallback_lyrics
    style = _extract_section(text, "STYLE") or fallback_style
    exclude = _extract_section(text, "EXCLUDE") or fallback_exclude
    return lyrics.strip(), style.strip(), exclude.strip()


def _extract_section(text: str, name: str) -> str:
    pattern = rf"\[{name}\]\s*(.*?)(?=\n\[[A-Z]+\]|\Z)"
    match = re.search(pattern, text, flags=re.DOTALL)
    return match.group(1).strip() if match else ""


if __name__ == "__main__":
    main()
