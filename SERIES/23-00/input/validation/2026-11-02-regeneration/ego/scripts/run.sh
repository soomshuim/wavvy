#!/bin/bash
# usage: run.sh ORDER DRY(true|false) EXPECTED_CREDITS  -> assembles lib.mjs + params + submit2.mjs and runs it in ego lite
D=/Users/zenkim_office/Project/wavvy/SERIES/23-00/input/validation/2026-11-02-regeneration/ego/scripts
TMP=/private/tmp/claude-501/-Users-zenkim-office-Project-wavvy/b2585a9e-89e5-48a0-b2cb-d35470aebd29/scratchpad
{ cat $D/lib.mjs; echo "const ORDER = $1; const DRY = $2; const EXPECTED_CREDITS = $3;"; cat $D/submit2.mjs; } > $TMP/run-track-$1-$2.mjs
ego-browser nodejs < $TMP/run-track-$1-$2.mjs
