# VIBE-M Quick Reference (for Human)
# Version: 1.0 (2026-01-18)
# Purpose: One-page operational guide for AI-assisted music production
# Scope: Role usage, order, and guardrails only

---

## What This Is

This document explains **HOW to use Claude** inside the VIBE-M system.

- Claude = **Execution & Production Brain**
- GPT = **Style / Lyrics Consultant**
- Suno = **Sound Generator**

Claude never improvises roles.
Claude follows the Role System strictly.

---

## Available Roles (Call Explicitly)

You MUST declare the role at the start of every request.

### Roles
- **Seed Researcher**
- **Seed Designer**
- **Variation Designer**

If a request mixes roles → Claude must STOP and ask for clarification.

---

## Standard Workflow (Always This Order)

### 1. Seed Research

```
Role: Seed Researcher
Input: Song title + artist
Output: Analytical bullets only
```

Purpose:
- Understand WHY the reference works
- Extract identity anchors
- Detect repetition tolerance

---

### 2. Seed Design

```
Role: Seed Designer
Input: Researcher output
Output: Seed DNA (system-level)
```

Deliverables:
- Seed Style Prompt (8–10 tokens)
- Musicality Matrix
- BPM / Key buckets
- Exclude Style (≤3 groups)
- Hard constraints (Do NOT vary)

Rule:
> This designs a **system**, not a song.

---

### 3. Variation Design

```
Role: Variation Designer
Input: Seed DNA + track number
Output: Slot-based variation plan
```

Rules:
- Change **minimum 2 slots**
- Never touch Seed constants
- Predict risks before generation

Every output ends with:

```
Verdict: SAFE / BORDERLINE / FAIL
```

---

## Hard Rules (Non-Negotiable)

### Claude must NEVER:
- Write lyrics/style output without explicit user request and role declaration
- Mix roles in one response
- Override MANAGER.md QC rules
- Invent rules not defined in MASTER docs

### Claude SHOULD:
- Ask to clarify role if ambiguous
- Stay technical and concise
- Default to conservative decisions

---

## Document Authority (SSOT)

| Document        | Authority |
|-----------------|-----------|
| ROLES.md        | WHY / WHO |
| MANAGER.md      | QC & Fail |
| STYLE.md        | Sound DNA |
| LYRICS.md       | Lyric Eng |

If conflict exists:
**Follow `MASTER/_INDEX.md` responsibility matrix first.**
**Final QC decision always follows `MANAGER.md`.**

---

## Example Correct Usage

```
Role: Seed Researcher
Analyze:
- Song: "OOO"
- Artist: OOO
- Context: Night driving playlist
```

```
Role: Seed Designer
Using previous research,
design a Seed for "Urban Night R&B"
```

```
Role: Variation Designer
Seed: Urban Night R&B v1
Track: 02
Required slots: BPM, Lead Instrument
```

---

## Mental Model (Remember This)

- Researcher = **Eyes**
- Designer = **Architect**
- Variation = **Engineer**
- Manager = **Judge**

Claude is not the Judge.
Claude builds what the system allows.

---

End of Quick Reference.
