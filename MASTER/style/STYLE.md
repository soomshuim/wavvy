# Wavvy STYLE.md

Version: 3.1
Last Updated: 2026-03-03
Purpose: Style Prompt 핵심 규칙 (SSOT)

> **Tag Bank**: `style/TAG_BANK.md` 참조

---

## 0. Non-Negotiables

### 0.1 Prompt Length
- **Style Prompt 제한: <= 900자 (공백 포함)**
- 이 문서가 길이 규칙 SSOT.

### 0.2 Pure Input Principle
- 가사 입력 규격은 `LYRICS.md §2` (SSOT)
- 설명형 연출/분위기는 **Style Prompt**에 둔다

### 0.3 Prompt Priority Rule
- **핵심을 앞에**: 첫 3단어가 곡의 방향 결정
- ✅ `Korean Lo-fi R&B, 80 BPM, Eb Major, felt piano...`
- ❌ `Cinematic but restrained, high fidelity, Korean Lo-fi R&B...`

### 0.4 Gravity Words
주의: `pop, beat, bass, catchy, upbeat` → "기본값"으로 수렴

### 0.5 Filler Sounds Ban
**금지:** `eh, uh, hm, ah, oh, yeah, woah, ooh`
**Style:** `No filler sounds. Clean vocal lines only.`

---

## 1. Core Sound DNA

- Texture: high fidelity, wide stereo, cinematic but restrained
- Vocal: dry close-mic, very forward, natural breaths, minimal autotune
- Diction: clear Korean articulation

### 1.1 Default Vocal Persona
**핵심:** `Raw vocal, Solid, Direct, Intimate, Clear, Dry, Unprocessed`
**발성:** `Chest voice, Belting, Raspy, Grit`
**프로덕션 필수:** `articulation, Moderate reverb, room ambience, EQ balanced sound, clean mix`
**피해야 할 단어:** `Airy, Falsetto, Harmonized, Backing vocals, Opera, Whisper`

---

## 1.5 Writing Formula (7요소)

> **키워드 뱅크:** Genre/Tempo → `reference/GENRES.md` | 나머지 → `style/TAG_BANK.md`

| # | 요소 | 형식 | 예시 |
|---|------|------|------|
| 1 | **Genre** | `[큰 장르] + [세부 장르]` (최대 2개, 첫 3-5단어) | `Korean Lo-fi R&B`, `Chillhop Jazz-hop` |
| 2 | **Mood** | `[감정 1-2개] + [시간대]` (선택) | `melancholic, nostalgic, late-night` |
| 3 | **Key/Mode** | `[Key] + [Major/Minor] + [코드 진행]` (선택) | `Eb Major, warm major7 chords` |
| 4 | **Tempo** | `[BPM 숫자]` — Belt 규칙 §4.1 참조 | `78 BPM` |
| 5 | **Parts** | `[Lead 1] + [Rhythm 2-3] + [Bass 1] + [Vocal]` | `Rhodes-led groove, soft shaker, warm bass` |
| 6 | **Texture** | `[질감] + [공간감] + [프로덕션]` | `dusty texture, intimate room, subtle reverb` |
| 7 | **Structure Cues** | `[섹션]: [연출 지시]` (가사 태그 보조) | `Chorus: emotional peak, 1 held note` |

**Parts — Vocal 형식:** `[Gender] vocal: [Tone], [Delivery], [Register], [Production]`
- 예: `Female vocal: Raw, Direct, Chest voice, Dry, articulation`
- 가사 있으면 `articulation` 필수

---

## 2. Harmony Guard (필수)

**초압축 2줄:**
```
Lead vocal remains single and dominant throughout. No stacked or choir-like harmonies.
Vocal line may intensify dynamically (belt, higher register), but no additional vocal layers.
```

**핵심:** 금지=레이어, 허용=에너지(belt, higher register, dynamics)

### 2.1 Energy Permission (필수)
```
Chorus vocal may be delivered with stronger intensity or light belt.
Higher register emphasis is encouraged. Natural vocal strain allowed.
```

---

## 3. Musicality Matrix

- **Verse2 Lift**: last 2 lines MUST rise (higher register encouraged)
- **Chorus Lift**: first line = peak (belt + **1 held note**)
- **Chorus Rule**: hook-first; lyrics repeated identically
- **Chorus2 Expansion**: bigger by arrangement, not vocal layers
- **Bridge Build**: no energy drop into chorus
- **Outro**: instrumental fade

**Fail Fast:** V2 안 올라감 / Chorus 안 올라감 / held note 없음 / 레이어 의존 → FAIL

---

## 4. Energy Switch (Chorus 폭발)

> "후렴 폭발감 부족" 시 Lever A+B 모두 적용

**Lever A (Arrangement):** Bass active / Perc intensity up / Stereo wider / Crash as impact marker
**Lever B (Vocal):** Belt (chorus 첫 줄) / Higher register / **1 held note** / Stronger dynamics

**핵심:** 리드 1명이 더 세게/높게 = OK, 레이어 추가 = 금지

### 4.1 Belt/Tempo Conflict Rule

| BPM | Mood | 보컬 지시 |
|-----|------|----------|
| 70-80 | Chill | higher register + stronger dynamics (NO belt) |
| 80-90 | Hazy | higher register + controlled intensity |
| 90+ | Warm | belt 허용 |

**안전한 대체:** `belt` → `higher register + stronger dynamics`

---

## 5. Variation Slots

| Slot | 선택 |
|------|------|
| Lead Instrument | Nylon guitar / Felt piano / Rhodes / Ambient pad |
| Rhythm Source | No drums / Soft shaker / Brush kit / Understated kick |
| BPM | 컨셉 범위 내 |
| Key/Mode | 최소 3개 key bucket |
| Mood | Chill / Hazy / Ethereal / Nocturne / Sentimental / Melancholic |
| Vocal Persona | Female husky / Female pure / Male soulful / Male soft |

---

## 6. Exclude Style Library

> **최대 3개 그룹, 총 8개 키워드 이내**

**Group A (Vocal FX):** `autotune heavy, vocoder, vocal chop, hyperpop vocal`
**Group B (EDM Arr):** `EDM drops, big room, festival, supersaw lead`
**Group C (Harmony):** `choir, stacked harmonies, backing vocal layers, doubled vocals`

**운영:** Harmony Guard로 먼저 제어 → 실패 시 Exclude 1-2개 추가

---

## 7. Self-QC 슬롯 체크리스트

| # | 슬롯 | 체크 |
|---|------|------|
| S0 | 핵심 앞에 | Genre/BPM 첫 5단어 내 |
| S1 | Raw Vocal | Raw, Solid, Direct, Dry |
| S2 | Vocal Persona | gender + tone + delivery |
| S3 | Chest voice | 진성 강제 |
| S4 | Articulation | articulation |
| S5 | Reverb | Moderate reverb, room ambience |
| S6 | Sound Engineering | EQ balanced sound, clean mix |
| S7 | Harmony Guard | 2줄 필수 |
| S8 | Energy Permission | 에너지 허용 문장 |
| S9 | Musicality | V2 lift, Chorus held note |
| S10 | Exclude | 최대 8개 |

> FAIL 시 재생성 + 900자 이하까지 압축 루프
