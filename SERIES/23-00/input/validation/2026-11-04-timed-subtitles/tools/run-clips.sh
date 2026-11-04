#!/bin/zsh
SP="$(cd "$(dirname "$0")" && pwd)"
R="$HOME/Project/wavvy"
# order label start end
while read order label s e; do
  [ -z "$order" ] && continue
  f=$(ls $R/SERIES/23-00/input/tracks/${order}__*.wav)
  out="$SP/probe-clips/check-${order}-${label}-${s}-${e}-whisper.json"
  [ -s "$out" ] && { echo "skip $out"; continue; }
  $R/.venv/bin/python -I $SP/transcribe.py mlx-community/whisper-large-v3-turbo "$f" "$out" $s $e 2>&1 | grep '^OK'
done <<'LIST'
02 bridge-weak 95 135
05 weak-line29 80 110
06 weak-line36 125 160
09 weak-line43 120 150
13 weak-final-chorus 140 175
15 verse2-missing 75 115
15 verse2-missing-b 105 145
08 extra-repeat-a 100 135
08 extra-repeat-b 140 175
10 extra-chorus 85 153
16 extra-chorus 165 206
12 breakdown 140 180
12 ending 190 214
03 gap-instrumental 60 100
05 gap-instrumental 55 100
07 gap-instrumental 50 100
09 gap-instrumental 55 100
12 gap-instrumental 70 105
14 gap-instrumental 40 90
16 gap-instrumental 100 150
08 gap-instrumental-b 125 165
LIST
echo CLIPSDONE
