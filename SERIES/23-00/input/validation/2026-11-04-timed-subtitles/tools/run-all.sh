#!/bin/zsh
SP="$(cd "$(dirname "$0")" && pwd)"
R="$HOME/Project/wavvy"
for f in $R/SERIES/23-00/input/tracks/*.wav; do
  b=$(basename "$f" .wav)
  if [ -s "$SP/probe-raw/$b-whisper.json" ]; then echo "skip $b"; continue; fi
  $R/.venv/bin/python -I $SP/transcribe.py mlx-community/whisper-large-v3-turbo "$f" "$SP/probe-raw/$b-whisper.json" 2>&1 | tail -3
done
echo ALLDONE
