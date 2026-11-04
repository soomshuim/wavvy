#!/usr/bin/env python3
"""Word-timestamp ASR probe with mlx-whisper (Wavvy 23:00 timed-subtitle evidence).

Usage: transcribe.py MODEL_REPO AUDIO_WAV OUT_JSON [clip_start_s clip_end_s]
A clip is cut with ffmpeg first, so word times in the JSON are clip-relative
(same convention as the 17:30 retained probes: clip_start + word start = track time).
Output layout follows the 17:30 probes (engine/model_dir/audio/audio_sha256/
parameters/elapsed_seconds/transcription).  ASR text never replaces approved lyrics.
"""
import hashlib
import importlib.metadata
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import mlx_whisper
from huggingface_hub import snapshot_download

model_repo, audio, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
clip = None
if len(sys.argv) >= 6:
    clip = (float(sys.argv[4]), float(sys.argv[5]))

model_dir = snapshot_download(model_repo)
source_sha = hashlib.sha256(audio.read_bytes()).hexdigest()
params = dict(
    language="ko",
    temperature=0,
    condition_on_previous_text=False,
    initial_prompt=None,
    word_timestamps=True,
)
work_audio = audio
tmpdir = None
extra = {}
if clip:
    tmpdir = tempfile.TemporaryDirectory()
    work_audio = Path(tmpdir.name) / "clip.wav"
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-ss", str(clip[0]), "-t", str(clip[1] - clip[0]),
         "-i", str(audio), "-ac", "2", "-ar", "48000", "-c:a", "pcm_f32le", str(work_audio)],
        check=True,
    )
    extra = {
        "clip_source_audio": str(audio),
        "clip_source_audio_sha256": source_sha,
        "clip_start_s": clip[0],
        "clip_end_s": clip[1],
        "clip_audio_sha256": hashlib.sha256(work_audio.read_bytes()).hexdigest(),
    }
t0 = time.time()
result = mlx_whisper.transcribe(str(work_audio), path_or_hf_repo=model_dir, verbose=None, **params)
elapsed = round(time.time() - t0, 3)
payload = {
    "engine": "mlx-whisper",
    "engine_version": importlib.metadata.version("mlx-whisper"),
    "model_repo": model_repo,
    "model_dir": model_dir,
    "audio": str(audio),
    "audio_sha256": source_sha,
    "parameters": {**params, "clip_timestamps": f"{clip[0]},{clip[1]}" if clip else "default_0"},
    **extra,
    "elapsed_seconds": elapsed,
    "transcription": result,
}
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"OK {audio.name} {elapsed}s segments={len(result.get('segments', []))}", flush=True)
if tmpdir:
    tmpdir.cleanup()
