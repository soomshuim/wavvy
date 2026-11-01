#!/bin/bash
# B2 step 5: run the template check and the three gates for tracks 11-15 only.
# Raw stdout -> NN-<check>.json (template check: its own --json-out file plus NN-template-check.out), exit code -> NN-<check>.exit, stderr -> NN-<check>.err
set -u
cd "$HOME/Project/wavvy" || exit 99
V=.ai/validation/2026-11-02-2300-styles
declare -a SONGS=("11 라디오" "12 스웨터" "13 편지" "14 기타" "15 노을")
for entry in "${SONGS[@]}"; do
  n="${entry%% *}"
  t="${entry#* }"
  rec=".ai/lyrics/2026-11-01_23-00_${n}_${t}-full-draft.md"
  txt="SERIES/23-00/input/tracks/${n}_${t}.txt"
  python3 .ai/plans/2026-11-01-2300-template-check.py "$n" --json-out "$V/${n}-template-check.json" >"$V/${n}-template-check.out" 2>"$V/${n}-template-check.err"
  echo $? >"$V/${n}-template-check.exit"
  python3 wavvy.py lyrics-skill SERIES/23-00 --artifact "$rec" --mode full-lyric-draft --draft-scope full-song --json >"$V/${n}-lyrics-skill.json" 2>"$V/${n}-lyrics-skill.err"
  echo $? >"$V/${n}-lyrics-skill.exit"
  python3 wavvy.py gate SERIES/23-00 --stage lyrics-review --artifact "$rec" --mode full-lyric-draft --draft-scope full-song --json >"$V/${n}-lyrics-review.json" 2>"$V/${n}-lyrics-review.err"
  echo $? >"$V/${n}-lyrics-review.exit"
  python3 wavvy.py gate SERIES/23-00 --stage track-prompt --artifact "$txt" --json >"$V/${n}-track-prompt.json" 2>"$V/${n}-track-prompt.err"
  echo $? >"$V/${n}-track-prompt.exit"
done
echo done
