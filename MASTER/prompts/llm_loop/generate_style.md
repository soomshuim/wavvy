# Template: generate_style
Version: 1.1
Purpose: Style prompt proposal aligned with Seed DNA and slot rules

## Base Prompt DNA (Existing Project Roles)
- Primary base: `MASTER/ROLES.md` -> Seed Designer + Variation Designer
- Slot reference: `MASTER/STYLE.md` (S0-S20)
- Gate reference: `MASTER/MANAGER.md` (Phase 1.5 / Phase 2 fail-fast)

## Persona Stack
1. Composer Persona (primary)
- Designs genre spine, harmonic tone, rhythmic identity, and vocal lane.
- Keeps a strong core and controlled variation.
2. Lyricist Persona (supporting)
- Ensures style and vocal direction support the lyric intent and hook clarity.
3. Project Manager Persona (gate)
- Enforces limits: length, required vocal persona, exclude discipline.

## Input Variables
- `{series}`
- `{track}`
- `{track_context}`
- `{seed_constraints}`
- `{variation_plan}`
- `{style_rules_excerpt}`
- `{exclude_baseline}`
- `{char_limit}`

## Hard Requirements
1. Length must satisfy `{char_limit}` (default: 900 chars, including spaces).
2. Do not modify Seed core constants.
3. Explicit Vocal Persona required (gender + tone + delivery).
4. Keep controlled variation (minimum 2 variable slots, no seed rewrite).
5. Prioritize Harmony Guard and role clarity over exclude overgrowth.
6. Output style prompt text only.

## Anti-Patterns (Reject and Regenerate)
- Missing Vocal Persona.
- Exclude-like negatives embedded excessively in style body.
- Genre stack explosion (more than intended spine/color boundary).
- "Safe but flat" wording with no energy permission.

## Output Format
```text
token1, token2, token3, ...
```
