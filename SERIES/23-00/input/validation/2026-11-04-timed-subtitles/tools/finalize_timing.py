#!/usr/bin/env python3
"""Write the 23:00 timing map + subtitle manifest, then validate with a patched copy of the harness
(in the scratchpad, NOT in the repository) inside a temporary copy of the series."""
import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path

REPO = Path.home() / "Project/wavvy"
SP = Path(__file__).resolve().parent  # scratch layout: probe-raw/, probe-clips/, patched/ were scratch folders; retained copies live in ../audio-probe/
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(SP))
import build_timing as B  # noqa: E402

SERIES = REPO / "SERIES/23-00"
VAL = SERIES / "input/validation/2026-11-04-timed-subtitles"
PROBE = VAL / "audio-probe"


UNSUNG_EXTRA_EVIDENCE = {2: ["check-02-bridge-weak-95-135"], 12: ["check-12-breakdown-140-180"]}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_patched():
    spec = importlib.util.spec_from_file_location("subtitles_patched", SP / "patched/subtitles_patched.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_map(srt_sha=None):
    cues_by_track, warnings, evidence_used = B.build_all()
    report = B.report
    tracks, starts, repeat, offset, duration = load_patched()._layout(report)
    concept = B.concept
    lines = B.LINES
    untimed = "\n\n".join("\n".join(lines[int(t["order"])]) for t in tracks)
    untimed = "\n\n".join([untimed] * repeat) + "\n"
    source_digest = hashlib.sha256(untimed.encode("utf-8")).hexdigest()
    evidence = {f"audio-probe/{p.name}": sha(p) for p in sorted(PROBE.glob("*.json"))}
    allowed, repeat_evidence = {}, {}
    for (tn, ls, occ, stem, _) in B.EXTRAS:
        if occ < 2:
            continue
        key = f"{tn}:{ls[0]}" if len(ls) == 1 else f"{tn}:{ls[0]}-{ls[-1]}"
        allowed[key] = len(ls)
        repeat_evidence[key] = [f"audio-probe/{stem}-whisper.json"]
    track_items = []
    displayed = 0
    for i, t in enumerate(tracks):
        n = int(t["order"])
        unsung = []
        for ln, reason in sorted(B.UNSUNG.get(n, {}).items()):
            refs = [f"audio-probe/{B.FULL(n)}"] + [f"audio-probe/{c}-whisper.json" for c in UNSUNG_EXTRA_EVIDENCE.get(n, [])]
            unsung.append({"source_line": ln, "text": lines[n][ln - 1], "reason": reason, "evidence": refs})
        cues = cues_by_track[n]
        for c in cues:
            c.pop("first_line", None)
            c.pop("last_line", None)
        displayed += sum(len(c["source_line_occurrences"]) for c in cues)
        item = {"track": n, "title": t["title"], "start_ms": starts[i], "source_lines": len(lines[n])}
        if unsung:
            item["unsung_source_lines"] = unsung
        item["cues"] = cues
        track_items.append(item)
    timing = {
        "schema": "wavvy.subtitle-timing.v1",
        "status": "ASR_ESTIMATED_TIMING_FOR_CONTROLLER_REVIEW_NOT_UPLOADED_NOT_HUMAN_LISTENED",
        "method": ("mlx-whisper 0.4.3, mlx-community/whisper-large-v3-turbo, language ko, temperature 0, "
                   "word timestamps, one pass per full track plus short re-recognition windows for weak lines, "
                   "sung repeats and instrumental gaps. Approved lyric lines are placed on the time axis by a "
                   "monotone syllable alignment (tools/); recognized text never replaces approved lyrics."),
        "original_source_sha256": source_digest,
        "repeat_offset_ms": offset,
        "source_lines_per_pass": sum(len(lines[int(t["order"])]) for t in tracks),
        "unsung_source_lines_per_pass": sum(len(v) for v in B.UNSUNG.values()),
        "displayed_lines_per_pass": displayed,
        "allowed_added_source_lines_per_pass": allowed,
        "audio_evidence_sha256": evidence,
        "limitations": [
            "Timing is inferred from automatic speech recognition (Whisper word times) and is an estimate; no human listened to the result.",
            "Whisper word ends are often stretched to the next onset; cue ends are capped at the next cue start minus 100 ms.",
            "Lines with weak ASR text matches (anchor class weak_asr_match) were re-recognized in a short window; their onsets rest on partial syllable matches.",
            "Whisper word onsets after a short pause can precede the sung onset by up to the pause length; full-track and short-window recognitions of the same lines agreed at a median of tens of milliseconds, with isolated differences above one second (self-check-result.json).",
            "Lines listed under unsung_source_lines are approved text that the audio does not sing; they are not timed and not shown.",
            "Hallucinated ASR text at the end of tracks ('다음 영상에서 만나요' and similar) was ignored; it matches no approved line.",
        ],
        "tracks": track_items,
    }
    if srt_sha:
        timing["srt_cues"] = displayed * repeat
        timing["srt_sha256"] = srt_sha
    return timing, warnings, source_digest


def main():
    timing, warnings, source_digest = build_map()
    map_path = VAL / "all-tracks-timed-checked.json"
    manifest_path = SERIES / "input/subtitles.json"
    report_sha = sha(SERIES / "output/report.json")

    def write_all(timing):
        map_path.write_text(json.dumps(timing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest = {
            "schema": "wavvy.subtitles.v1",
            "report": {"path": "output/report.json", "sha256": report_sha},
            "timing_map": {"path": "input/validation/2026-11-04-timed-subtitles/all-tracks-timed-checked.json", "sha256": sha(map_path)},
            "srt": {"path": "output/youtube_subtitles_ko_timed_estimated.srt"},
            "required_extra_occurrences": timing["allowed_added_source_lines_per_pass"],
            "repeat_evidence": {k: v for (k, v) in REPEAT_EVIDENCE.items()},
        }
        return manifest

    # repeat evidence from the map builder
    global REPEAT_EVIDENCE
    REPEAT_EVIDENCE = {}
    for (tn, ls, occ, stem, _) in B.EXTRAS:
        if occ >= 2:
            key = f"{tn}:{ls[0]}" if len(ls) == 1 else f"{tn}:{ls[0]}-{ls[-1]}"
            REPEAT_EVIDENCE[key] = [f"audio-probe/{stem}-whisper.json"]

    # pass 1: no srt hash -> patched prepare in a temp series to learn the SRT digest
    tmp = SP / "tmp-series"
    if tmp.exists():
        shutil.rmtree(tmp)

    def stage_tmp():
        (tmp / "output").mkdir(parents=True)
        (tmp / "input/validation").mkdir(parents=True)
        shutil.copy(SERIES / "concept.md", tmp / "concept.md")
        shutil.copy(SERIES / "output/report.json", tmp / "output/report.json")
        shutil.copytree(VAL, tmp / "input/validation/2026-11-04-timed-subtitles")
        shutil.copy(manifest_path, tmp / "input/subtitles.json")

    manifest = write_all(timing)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    stage_tmp()
    P = load_patched()
    result = P.prepare_timed(tmp, tmp / "input/validation/2026-11-04-timed-subtitles/all-tracks-timed-checked.json")
    srt_sha = result["sha256"]
    print("pass1 prepare:", {k: result[k] for k in ("result", "cues", "sha256")})
    # pass 2: map with srt hash/count, manifest with hashes
    timing, warnings, source_digest = build_map(srt_sha=srt_sha)
    manifest = write_all(timing)
    manifest["srt"]["sha256"] = srt_sha
    manifest["source_sha256"] = source_digest
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.rmtree(tmp)
    stage_tmp()
    # (patched) full prepare + verify in the temporary series
    result2 = P.prepare_timed(tmp, tmp / "input/validation/2026-11-04-timed-subtitles/all-tracks-timed-checked.json")
    verify = P.verify_prepared(tmp)
    print("pass2 prepare:", {k: result2[k] for k in ("result", "cues", "sha256")})
    print("verify_prepared (patched copy, temp series):", {k: verify[k] for k in ("result", "stage", "cues", "duration_ms", "sha256")})
    shutil.copy(tmp / "output/youtube_subtitles_ko_timed_estimated.srt", SP / "candidate.srt")
    print("warnings:", warnings)


if __name__ == "__main__":
    main()
