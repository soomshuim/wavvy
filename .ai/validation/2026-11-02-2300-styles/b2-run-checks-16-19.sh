#!/bin/bash
# B2 checks for tracks 16-19 only. Raw output + exit code per check under .ai/validation/2026-11-02-2300-styles/.
cd ~/Project/wavvy || exit 99
V=.ai/validation/2026-11-02-2300-styles
for NN in 16 17 18 19; do
  case $NN in 16) T=여름밤;; 17) T=막차;; 18) T=벚꽃;; 19) T=그네;; esac
  REC=".ai/lyrics/2026-11-01_23-00_${NN}_${T}-full-draft.md"
  TXT="SERIES/23-00/input/tracks/${NN}_${T}.txt"
  [ -f "$REC" ] && [ -f "$TXT" ] || { echo "missing input for $NN: $REC / $TXT"; exit 98; }
  python3 .ai/plans/2026-11-01-2300-template-check.py $NN --json-out $V/${NN}-template-check.json > $V/${NN}-template-check.out 2> $V/${NN}-template-check.err; echo $? > $V/${NN}-template-check.exit
  python3 wavvy.py lyrics-skill SERIES/23-00 --artifact "$REC" --mode full-lyric-draft --draft-scope full-song --json > $V/${NN}-lyrics-skill.json 2> $V/${NN}-lyrics-skill.err; echo $? > $V/${NN}-lyrics-skill.exit
  python3 wavvy.py gate SERIES/23-00 --stage lyrics-review --artifact "$REC" --mode full-lyric-draft --draft-scope full-song --json > $V/${NN}-lyrics-review.json 2> $V/${NN}-lyrics-review.err; echo $? > $V/${NN}-lyrics-review.exit
  python3 wavvy.py gate SERIES/23-00 --stage track-prompt --artifact "$TXT" --json > $V/${NN}-track-prompt.json 2> $V/${NN}-track-prompt.err; echo $? > $V/${NN}-track-prompt.exit
done
