# Mixed vocal prompt gate

## Cause

The track-prompt gate read only the first gender in the `Vocal` header but collected every gender in `STYLE`. An explicitly approved female-verse/male-and-female-chorus prompt therefore failed despite matching declarations.

## Scope

- Parse the same set of explicit male/female labels from both fields and compare the sets.
- Preserve single-gender matching and reject unknown or missing header gender.
- Cover matching male, female, mixed English/Korean, mismatched, and unknown cases through the existing CLI gate.

## Verification

- Focused track-prompt tests: 3 passed.
- Full harness suite: 37 passed.
- Python compilation and `git diff --check`: passed.
- Keep series policy and source/concept/session edits with their separate owner.
