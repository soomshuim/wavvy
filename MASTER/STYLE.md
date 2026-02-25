# VIBE-M STYLE.md
Version: 2.8
Last Updated: 2026-02-16
Purpose: Raw Vocal 기본값 + 진성 강제 + 커뮤니티 베스트 프랙티스 통합

---

## 0) Non-Negotiables (Always ON)

### 0.1 Prompt Length
- **Style Prompt 제한: <= 900자 (공백 포함 문자 수 기준)**
- If longer: compress descriptors into fewer tokens (8–10 token rule for core identity).
- 900자는 운영 안전 한계이며, 본 문서가 길이 규칙 SSOT다.

### 0.2 Pure Input Principle
- **가사 입력 규격은 LYRICS.md §2를 따른다** (SSOT)
- 요약: 순수 가창 텍스트 + 구조 태그 + 구조 직후 1행 `()` 메타만 허용
- 설명형 연출/분위기/편곡 전략은 **Style Prompt**에 둔다.

### 0.3 Technical Accuracy
- Use correct music terms: `rim-shot / rim-click` (NOT rim light).
- Avoid overly broad excludes like "Electric keyboard" unless necessary—be precise.

### 0.4 Prompt Priority Rule

> **"핵심을 앞에"** - 첫 3단어가 곡의 방향을 결정한다

**규칙:**
- Style Prompt의 첫 3-5 단어가 가장 중요
- Genre/BPM을 반드시 앞에 배치
- 부가 설명은 뒤로
- 프롬프트가 짧을 때는 Major/Minor를 맨 앞에 배치 가능

**예시:**
- ✅ `Korean Lo-fi R&B, 80 BPM, Eb Major, felt piano...`
- ✅ `Minor, Lo-fi R&B, 80 BPM, felt piano...` (짧은 프롬프트)
- ❌ `Cinematic but restrained, high fidelity, Korean Lo-fi R&B...`

### 0.5 Gravity Words (중력 우물)

> 특정 단어가 결과를 "대중적 평균값"으로 끌어당기는 현상

**주의 단어 (원치 않는 경우에만 회피):**
```
pop, beat, bass, catchy, upbeat
```

**해석:**
- 이 단어들이 포함되면 Suno가 "기본값" 사운드로 수렴하는 경향
- **Pop을 원하면 "pop" 사용 OK**
- R&B/Lo-fi를 원하는데 Pop 느낌 피하려면 → Exclude에 배치

**예시:**
- R&B 원하는데 Pop 섞임 방지: `Exclude: "Pop, dance-pop"`
- Lo-fi 원하는데 EDM 느낌 방지: `Exclude: "EDM beats, festival"`

### 0.6 Broad Genre Labels Rule

> **광범위한 장르 라벨보다 구체적 묘사가 안전하다**

**원칙:**
- 추상적 장르 라벨 대신 **구체적 악기 + 리듬 + 보컬 프로덕션** 묘사 우선
- "Lo-fi / Chill" 같은 단어도 결과를 평준화할 수 있음

**예시:**
- ❌ `Chill R&B vibe` (추상적)
- ✅ `felt piano-led, soft shaker, dry close-mic vocal, 80 BPM` (구체적)

**적용:**
- 장르 라벨은 첫 1-2단어로 방향 설정 후
- 나머지는 악기/프로덕션/보컬 묘사로 채우기

### 0.7 Filler Sounds Ban (추임새 금지)

> **Hip-hop 계열 장르를 제외한 모든 장르에서 추임새 금지**

**금지 대상:**
```
eh, uh, hm, ah, oh, yeah, woah, ooh (as filler/ad-lib)
```

**적용 장르 (금지):**
- Ballad, R&B Ballad, City Pop, Neo-Soul, Chillhop, Lo-fi, Jazz
- 기타 Hip-hop 요소가 없는 장르

**예외 장르 (허용):**
- Hip-hop, Trap, Boom Bap, K-hip-hop
- 장르명에 "hip-hop" 또는 "rap"이 포함된 경우

**Style Prompt 적용:**
```
No filler sounds. No "eh" "uh" "hm" ad-libs. Clean vocal lines only.
```

**Exclude 적용:**
```
Filler sounds, Ad-libs, Vocal ad-libs
```

**Scat/Humming 예외:**
- Outro에서 의도적 scat은 허용 가능 (Style에 명시 시)
- 예: `Outro: scat allowed here only`

---

## 1) Core Sound DNA (Project Constant)

Use these as the "always-on" identity baseline (pick only the essentials to stay under 900 chars).

- Texture: **high fidelity, wide stereo, cinematic but restrained**
- Vocal production: **dry close-mic, very forward, natural breaths, minimal autotune**
- Diction: **clear Korean articulation**
- Default mood: **minimal, intimate, restrained (Verse) → release (Chorus)**

---

## 1.1) Default Vocal Persona (Raw Vocal Baseline)

> **별도 요청 없으면 이 기본값 적용**

### Style Prompt 필수 키워드 (기본)

**핵심 (반드시 포함):**
```
Raw vocal, Solid, Direct, Intimate, Clear, Dry, Unprocessed
```

**발성 묘사 (상황에 따라 선택):**
```
Chest voice, Belting, Raspy, Grit
```

**목소리 톤:**
- 남성: `Deep male vocal, Mature voice`
- 여성: `Contralto, Mature voice` (중저음)

**프로덕션 필수 (v2.6.2 NEW):**
```
articulation
Moderate reverb, room ambience
EQ balanced sound, clean mix
```

> **위 3개 키워드 없으면 QC FAIL**
> - Articulation: 발음 명확성 확보
> - Reverb: 공간감 제어
> - Sound Engineering: 믹스 품질

**추천 조합 예시:**
```
raw vocal, direct, solid, dry recording, chest voice dominant, clear Korean diction, no harmony, precise articulation, moderate reverb, EQ balanced sound
```

### 피해야 할 단어 (Exclude 또는 Style에서 제외)

> **이 단어들이 Style에 있으면 얇은/가성 보컬 유발**

```
Airy, Falsetto, Harmonized, Backing vocals, Opera, Whisper, Auto-tune, Ethereal voice
```

### 적용 규칙

| 요청 | 적용 |
|------|------|
| 기본 (별도 요청 없음) | Raw Vocal Baseline 적용 |
| "powerful" 요청 | Powerful, Strong attack 추가 |
| "husky" 요청 | Raspy, Grit 추가 |
| "airy" 요청 | Airy, Breathy 허용 (예외) |
| "soft" 요청 | Intimate, Gentle 추가 |

> **참고**: `Powerful`은 기본값이 아니라 **곡 컨셉에 따라 요청 시** 추가 (airy, husky와 동일)

---

## 2) Harmony Guard (Mandatory Safety Lines) — v1.6 Energy Permission

> This block MUST appear in every Style Prompt. **금지는 레이어에만, 허용은 에너지에.**

**초압축 Harmony Guard (붙박이 2줄)**
```
Lead vocal remains single and dominant throughout. No stacked or choir-like harmonies.
Vocal line may intensify dynamically (belt, higher register), but no additional vocal layers.
```

**EDM 처리 금지 (별도 1줄)**
```
No EDM vocal processing (no vocoder, no vocal chops, minimal autotune).
```

**핵심 원칙 (v1.6 분리)**
- **금지 대상**: 보컬 레이어 (backing, doubles, choir, stacks)
- **허용 대상**: 보컬 에너지 (belt, higher register, dynamics, strain)
- "리드 한 명이 더 세게/높게 부르는 것" = 허용 (encouraged)
- "보컬을 겹치는 것" = 금지

**v1.5 → v1.6 변경점**
- ❌ "vocals unchanged" → 모델이 "보컬 에너지 상승도 금지"로 오해
- ✅ "vocal line may intensify dynamically" → 에너지 상승 명시 허용
- ❌ "Single lead vocal ONLY" → 너무 강압적
- ✅ "Lead vocal remains single and dominant" → 톤 다운

**운영 팁 (Style Prompt 본문에 넣지 말 것)**
- end-line ad-libs가 정말 필요하면 Exclude 옆 메모로 관리
- "If any support happens..." 문장은 모델이 오해하므로 사용 금지

**Reason**
- v1.5에서 "금지 규칙이 에너지 규칙을 덮어버림" 문제 발생
- 모델이 가성/레지스터 상승을 "보컬 변형"으로 오인 → 회피
- 해결: "금지는 레이어에만" 명확히 분리

---

## 2.1) Energy Permission (Mandatory)

> **This block MUST appear with Safety Lines. 금지와 허용은 항상 쌍으로.**

```
Energy Permission:

Chorus vocal may be delivered with stronger intensity or light belt.
Higher register emphasis is encouraged.
Natural vocal strain allowed.
Energy increase must come from vocal delivery, not harmony layers.
```

**핵심 원칙:**
- Safety Lines 바로 아래에 이 블록 배치 (같은 섹션, 같은 문단)
- "금지했다" 만으로는 부족 → "금지 + 허가했다" = 살아있는 곡
- Verse2/Chorus에서 보컬 강도(intensity) 상승은 **필수**이자 **권장**

**FAIL if missing:**
- Energy Permission 없이 Safety Lines만 있으면 → 무난함 발생 → FAIL

---

## 3) Musicality Matrix (Always ON) — v1.7 Fail Fast

Include these in Style Prompt, in compressed form.

- **Verse2 Lift (MUST):** same melodic contour as Verse1; **last 2 lines MUST rise in emotional intensity**: higher register OR light upper register lift is **encouraged**. Natural vocal strain **allowed**.
- **Chorus Lift:** chorus first line hits peak: **belt/higher register + exactly 1 held note (longer sustain than any verse note)**. Lead vocal energy may increase.
- **Chorus Rule:** hook-first; **lyrics repeated identically**. No other sustained notes should appear in chorus besides the 1 held note.
- **Chorus2 Expansion:** bigger **by arrangement** (bass/drums energy, wider stereo instruments); **lead vocal energy may increase, but no new vocal layers**.
- **Bridge Build:** build every bar; **no energy drop into chorus**.
- **Outro:** instrumental fade; return to minimal texture.

**V2 → Chorus 연결 원칙:**
> V2 last 2 lines (emotional intensity rise: higher register encouraged (chest-dominant)) → Chorus first line = peak (1 held note, longer sustain than any verse note + belt)

**Energy Reference (QC 기준, 프롬프트용 아님):**
> Chorus peak note should sustain at least **1.5x longer** than any Verse note.

**v1.7 Fail Fast 조건 (위반 시 즉시 FAIL):**
- ❌ FAIL if Verse2 last 2 lines do not audibly rise in register or intensity
- ❌ FAIL if Chorus first line is not perceptibly higher or more intense than Verse2
- ❌ FAIL if Chorus lacks the 1 held note event
- ❌ FAIL if Chorus relies on vocal layering instead of energy increase

**v1.6 표현 원칙 (유지):**
- ❌ "vocals unchanged" → 에너지까지 억제
- ❌ "keep SINGLE lead" → 너무 강압적
- ✅ "lead vocal energy may increase, but no new vocal layers" → 에너지 허용 + 레이어 금지 분리
- ✅ "higher register is encouraged" → 권한 부여

---

## 4) Energy Switch (Chorus Explosion Without AI Choir) — v1.6

> "후렴 폭발감 부족"이 뜨면 아래 2개 레버를 모두 적용.

### 4.1 Lever A: Arrangement Lift

| 요소 | 적용 방법 |
|------|----------|
| Bass | more active movement / locked to groove |
| Perc | shaker intensity up / add rim-click accents |
| Drums | (if allowed) kick enters or doubles energy **for the first time** in chorus |
| Stereo | wider instruments + extra layer (pad/guitar/piano voicing) |
| Accents | crash/ride only as impact markers (avoid over-busy) |

### 4.2 Lever B: Lead Vocal Lift (에너지 허용)

| 요소 | 적용 방법 |
|------|----------|
| Belt | chorus first line = stronger attack, more intensity |
| Register | higher register than verse (noticeable lift) |
| Held Note | **1 held note** on hook (longer sustain, event-like) |
| Dynamics | stronger dynamics, natural vocal strain allowed |
| Upper Register | brief upper register lift encouraged (especially V2 ending, chest-dominant) |

**핵심 (v1.6):**
- 리드 한 명이 더 세게/높게 부르는 것 = **encouraged**
- 가성/레지스터 상승 = **allowed/encouraged**
- "1 held note + higher register + stronger dynamics" = 정량화된 폭발 이벤트

**금지 (레이어만):**
- 보컬 레이어 추가로 폭발감 만드는 것 = 금지

### 4.4 Belt/Tempo Conflict Rule — NEW (v2.0)

> **"belt"는 Chill/Lo-fi/Soft 트랙에서 충돌 위험이 있다.**

**충돌 케이스:**
- ❌ "soft airy tone" + "belt" → 모델이 아이돌 팝/EDM 보컬로 튐
- ❌ "Chill R&B 76 BPM" + "belt" → 에너지 불일치
- ❌ "minimal, intimate" + "belt" → 분위기 파괴

**해결: BPM/Mood별 보컬 강도 매칭**

| BPM | Mood | 보컬 지시 |
|-----|------|----------|
| 70-80 | Chill/Ethereal | higher register + stronger dynamics (NO belt) |
| 80-90 | Hazy/Nocturne | higher register + controlled intensity |
| 90-100+ | Sentimental/Warm | belt/higher register 허용 |

**안전한 대체 표현:**
- ❌ `belt/higher register` → ✅ `higher register + stronger dynamics`
- ❌ `falsetto encouraged` → ✅ `higher register (chest-dominant)`
- 진성 기반 유지하면서 에너지 상승 = 가장 안전

### 4.5 Energy Direction Rule (에너지 방향 규칙) — v2.2

> **폭발은 금지하지 말고, 방식만 제한하라.**

**핵심 원칙:**
1. **에너지 지시 충돌 금지** — "soft/understated" + "폭발" 동시 사용 시 모델 혼란
2. **진성 허용 문장 필수** — Exclude보다 Style 내 허용 문장이 더 중요
3. **belt는 Exclude 금지** — belt 제외하면 falsetto만 남음

---

**Rule 1: 폭발은 금지하지 말고, 방식만 제한**

| ❌ 에너지 차단 (재발 원인) | ✅ 방식 제한 (정답) |
|---------------------------|-------------------|
| "Chorus same energy as verse" | "Chorus reaches emotional peak via chest voice, no added layers" |
| "Melody understated" + "intimate throughout" | "Verse intimate; Chorus opens with controlled intensity" |
| "gentle sustained note" | "sustained note with chest voice" |

---

**Rule 2: 진성 허용 문장 필수**

Style Prompt에 반드시 포함:
```
Chest voice dominant. Avoid falsetto as primary register.
```

이 문장이 Exclude의 "falsetto" 보다 더 중요함.

---

**Rule 3: Exclude에서 belt 절대 빼지 말 것**

| ❌ 치명적 실수 | ✅ 올바른 Exclude |
|---------------|------------------|
| `falsetto, belt, ...` | `falsetto (as primary), choir, stacked harmonies, doubled vocals, vocoder, vocal chop, EDM drops` |

**belt를 Exclude에 넣으면:**
- 진성 고음 선택지 사라짐
- 모델이 falsetto/head voice로 도망감
- 가성 증가 재발

**belt는:**
- "계속 벨팅하라"가 아니라
- "필요할 때 쓸 수 있는 선택지"로 열어둬야 함

---

**Exclude 작성법 (최대 8개):**
```
falsetto (as primary), choir, stacked harmonies, doubled vocals, vocoder, vocal chop, EDM drops, autotune heavy
```

---

**성공 패턴 키워드 (여전히 유효):**
- `conversational phrasing` — 대화체 유도
- `controlled vibrato` — 과한 비브라토 억제
- `dry/close-mic, very forward` — 보컬 프로덕션
- `natural breaths, minimal pitch correction` — 자연스러움

---

## 5) Variation Slots (Per-Track Choices)

Pick values per track; keep it minimal to prevent model confusion.

### Slot A — Lead Instrument (choose 1)
- Nylon guitar-led (cold arpeggio)
- Felt piano-led (soft voicing)
- Rhodes/EP-led (hazy chords)
- Ambient synth pad-led (atmospheric textures)

### Slot B — Rhythm Source (choose 1)
- No drums (perc only)
- Soft shaker + rim-shot/rim-click
- Brush kit
- Tight understated kick (heartbeat-like)

### Slot C — BPM Bucket
- Choose within concept range (ex: 75–85 for chill nightwalk)

### Slot D — Structure Emphasis
- Hook entry timing / bridge presence / pre-chorus tension cue

### Slot E — Key/Mode Bucket
- Maintain at least 3 key buckets per project (avoid fingerprint sameness)

### Slot F — Mood Bucket (파일명용) — NEW (v2.0)
> **Mood 슬롯이 하나로 계속 가면 플리에서 체감 변주가 줄어든다.**

| Mood | 적합한 BPM | 특징 |
|------|-----------|------|
| **Chill** | 70-80 | 차분, 편안 |
| **Hazy** | 75-88 | 몽환, 흐릿 |
| **Ethereal** | 70-85 | 초현실, 공기감 |
| **Nocturne** | 75-90 | 밤, 고요 |
| **Sentimental** | 85-100 | 감성, 서정 |
| **Melancholic** | 80-95 | 우울, 쓸쓸 |

**적용 규칙:**
- 10곡 플리에서 **최소 3개 Mood** 사용 권장
- 파일명 형식: `NN__제목__Mood__Genre__BPM.mp3`
- 같은 Mood 연속 3곡 이상 금지

### Slot G — Vocal Persona (Mandatory)
- Female husky / Female pure / Male soulful / Male soft
- Always specify: **gender + tone + delivery**.

---

## 6) Exclude Style Library — 강화

> **Exclude가 너무 길면 모델이 "금지 리스트"에 주의를 뺏겨 보컬이 이상해질 수 있다.**

**핵심 규칙 (통일):**
- **최대 3개 그룹** 선택 (A+B+C 또는 A+B+D 등)
- **총 8개 키워드 이내**로 압축
- 그룹 전체를 나열하지 말고 **핵심 항목만** 선택
- 과도한 Exclude = 오히려 부작용

Pick up to 3 groups depending on the track risk. **그룹명에 사용 목적 표기.**

### Group A (Vocal FX) — 보컬 프로세싱 차단
```
autotune heavy, hard tune, vocoder, vocal chop, formant shift, hyperpop vocal, pitchy EDM lead
```

### Group B (EDM Arr) — EDM 편곡 차단
```
EDM drops, big room, festival, supersaw lead, sidechain pumping
```

### Group C (Harmony/Choir) — 합창/화성 차단
```
choir, gospel choir, stacked harmonies, harmony stack, ensemble vocals, backing vocal layers, doubled vocals
```

### (선택) Group D (Aggressive) — 공격적 스타일 차단
```
shouting, screaming, metal, heavy distortion
```

### 6.1 Exclude 운영 규칙

> **Exclude는 '증상 기반 최소 세트'로 시작한다**

**핵심 원칙:**
1. **문제 발생 전**: 기본 Exclude만 사용 (2-3그룹)
2. **문제 재발 시**: 1-2개씩만 추가 (한꺼번에 추가 금지)
3. **우선순위**: Exclude보다 **Harmony Guard(역할 지정)**가 1순위

**운영 순서:**
```
Step 1: Harmony Guard 문장으로 먼저 제어 시도
Step 2: 실패 시 Exclude에 1-2개 키워드 추가
Step 3: 여전히 실패 시 Style Prompt 자체 재검토
```

**금지:**
- ❌ 문제 예방 목적으로 Exclude 과다 추가
- ❌ "혹시 몰라서" 키워드 추가
- ❌ 8개 초과 키워드

**기억:**
> "하모니 과잉"은 Exclude보다 Harmony Guard가 더 효과적이다.

---

## 7) Prompt Assembly Template (Copy & Fill)

### 7.1 Style Prompt (<=900 chars, EXCLUDE excluded)

**순서:**
1. Genre/BPM/Key + Lead Inst + Rhythm
2. Vocal Persona + Vocal Production
3. Harmony Guard (compressed)
4. Musicality Matrix (compressed)
5. Outro

### 7.2 Exclude (separate field)
- Choose max 3 groups above.

---

## 8) Self-QC Checklist (Claude must pass)

**"요소 빠짐 방지"를 구조로 강제하는 3-Step 프로세스:**

```
Step 1: S0-S20 슬롯 값 먼저 채우기 (빈칸 있으면 FAIL)
Step 2: 그 값으로 Style Prompt 생성
Step 3: 글자수 체크 (Style만 900자 이하, 공백 포함 문자 기준) → 넘으면 압축 루프
```

### Style Prompt 슬롯 체크리스트

> **SSOT: STYLE.md §7-8 (이 문서)**
> CLAUDE.md는 작업용 요약 매뉴얼이며, 충돌 시 이 문서가 우선

**핵심 슬롯 요약 (전체는 STYLE.md §7-8 참조):**

| # | 슬롯 | 체크 내용 |
|---|------|----------|
| S0 | 핵심 앞에 | Genre/BPM이 첫 5단어 내 |
| S1 | Raw Vocal Baseline | Raw, Solid, Direct, Dry |
| S2 | Vocal Persona | gender + tone + delivery 명시 |
| S3-S4 | Vocal | Chest voice 강제 + Processing |
| S5-S8 | Arrangement | Lead Inst + Rhythm + BPM + Key |
| S9-S11 | Structure | Musicality Matrix + Harmony Guard + Chorus Layer Block |
| S12-S14 | Exclude | 필수 항목 + 제한 + 모호 형용사 제거 |
| S15-S17 | Constraints | 글자수 + Supportive + Density |
| **S18** | **Articulation** | **articulation** |
| **S19** | **Reverb** | **Moderate reverb, room ambience** |
| **S20** | **Sound Engineering** | **EQ balanced sound, clean mix** |

**If any FAIL:** regenerate and shorten until 20/20 PASS + <=900 chars.

---

## 9) Quick Reference — v1.7

### 9.1 Harmony Guard 초압축 (붙박이 2줄)
```
Lead vocal remains single and dominant throughout. No stacked or choir-like harmonies.
Vocal line may intensify dynamically (belt, higher register), but no additional vocal layers.
```

### 9.2 Musicality Matrix 압축
```
Verse2: same melodic contour, last 2 lines MUST rise in emotional intensity (higher register encouraged (chest-dominant), natural strain allowed).
Chorus: hook-first, repeat identical; chorus first line hits peak with belt/higher register + 1 held note (longer sustain than any verse note). Lead vocal energy may increase.
Chorus2: bigger by arrangement (bass/drums energy, wider stereo); lead vocal energy may increase, but no new vocal layers.
Bridge: build every bar, no energy drop into chorus.
Outro: instrumental fade.
```

### 9.3 V2 → Chorus Lift 연결 (에너지 허용)
```
Verse2 last 2 lines: emotional intensity MUST rise (higher register encouraged (chest-dominant), natural strain allowed).
Chorus first line: 1 held note (longer sustain) + belt/higher register. Lead vocal energy may increase.
```

### 9.4 물안개 예시 (v1.6 적용)
```
articulation, Korean Lo-fi R&B, 80 BPM, Eb Major, felt piano-led, soft shaker, hazy ambient pad, cinematic but restrained, high fidelity, wide stereo.
Male vocal: warm soulful tone, dry close-mic, very forward, clear Korean diction, natural breaths, minimal autotune, straight delivery.
Lead vocal remains single and dominant. No stacked or choir-like harmonies. Vocal line may intensify dynamically, but no additional vocal layers. No EDM vocal processing.
Verse2 same melodic contour as v1; last 2 lines MUST rise in emotional intensity (higher register encouraged (chest-dominant)).
Chorus hook-first, repeat identical; chorus first line hits peak with belt/higher register + 1 held note (longer sustain than any verse note). Lead vocal energy may increase.
Chorus2 bigger by arrangement (bass/drums energy, wider stereo); lead vocal energy may increase, but no new vocal layers.
Bridge builds every bar; no energy drop into chorus. Outro felt piano fades.
```

### 9.5 금지 표현 vs 권장 표현 (v1.7)
| 금지 | 권장 |
|------|------|
| vocals unchanged | lead vocal energy may increase, but no new vocal layers |
| keep SINGLE lead vocal | lead vocal remains single and dominant |
| Single lead vocal ONLY | Lead vocal remains single and dominant |
| If any support happens... | (예외 조항 사용 금지) |
| bigger chorus with backing vocals | bigger by arrangement |

### 9.6 Fail Fast 조건 요약 (v1.7)
```
FAIL if:
- Verse2 last 2 lines do not audibly rise in register or intensity
- Chorus first line is not perceptibly higher or more intense than Verse2
- Chorus lacks the 1 held note event
- Chorus relies on vocal layering instead of energy increase

INVALID if:
- Vocal Persona not explicitly stated (gender + tone + delivery)
- Any mandatory slot missing
```

---

## 10) A/B Testing Rules (DEBUG/PROD Mode)

> 체계적 반복으로 크레딧 절약 + 결과 예측 + 문제 추적

### 10.0 PROD vs DEBUG 모드

> **다양성 생산과 문제 디버깅은 다른 규칙이 필요하다**

| 모드 | 목적 | 변경 변수 | 사용 시점 |
|------|------|----------|----------|
| **PROD** | 다양성 생산 | 최소 2개 슬롯 변주 | 정상 트랙 제작 |
| **DEBUG** | 문제 원인 추적 | **1개 변수만** | 하모니/가성/EDM 보컬 재발 시 |

**DEBUG 모드 예시:**
```
문제: Chorus에서 합창 발생
DEBUG A: Harmony Guard 문장만 강화
DEBUG B: Exclude에 "choir" 1개만 추가
→ A/B 비교로 원인 특정
```

**모드 전환 기준:**
- 2회 연속 같은 문제 발생 → DEBUG 모드 전환
- DEBUG에서 원인 특정 후 → PROD 복귀

### 10.1 한 번에 1개 변수만 (DEBUG 모드)

**DEBUG 모드에서 변경 시 한 가지만:**
- Harmony Guard 문장만 변경 OR
- Exclude 1단어만 변경 OR
- BPM만 변경 OR
- 보컬 성별만 변경

**금지:** 여러 변수 동시 변경 → 어떤 게 효과인지 알 수 없음

### 10.2 선택 규칙

- 10개 생성 → **1개만** 선택
- 선택 이유 **1줄 메모** (concept.md에 기록)
- "왜 이게 좋았는지" 기록해야 다음에 재현 가능

### 10.3 템플릿 저장

- 성공한 프롬프트 템플릿 저장
- 다음 트랙에서 작은 변주로 재사용
- concept.md에 "Style Prompt v1, v2..." 버전 관리

### 10.4 DEBUG 기록 양식

문제 재발 시 concept.md에 기록:
```
## DEBUG Log
- 문제: [Chorus 합창 발생]
- DEBUG A: [Harmony Guard 강화] → 결과: [실패/성공]
- DEBUG B: [Exclude choir 추가] → 결과: [실패/성공]
- 결론: [Exclude보다 Harmony Guard가 효과적]
```

---

## 11) Co-occurrence Hints (장르 조합)

> 함께 쓰면 잘 작동하는 장르 조합 + **Genre Mix Pattern**

### 11.0 Genre Mix Pattern (필수)

> **Spine 1개 + Color 1개, 최대 2개 장르**

**구조:**
- **Spine (척추)**: 코어 장르, 정체성 결정
- **Color (색깔)**: 서브 장르, 변주 제공

**규칙:**
1. Spine은 시리즈 전체 고정
2. Color는 트랙별 변경 가능
3. **3개 이상 장르 스택 절대 금지**

**예시:**
| 시리즈 | Spine | Color 옵션 |
|--------|-------|-----------|
| PM_0900 밤산책 | City Pop | Neo-Soul, Funk, R&B Ballad |
| AM_0400 새벽 | Lo-fi R&B | Jazz, Ambient |

**적용:**
```
✅ Korean City Pop + Neo-Soul (2개)
✅ Korean City Pop + Funk (2개)
❌ City Pop + Neo-Soul + Funk + Jazz (4개 → 혼란)
```

### 11.1 VIBE-M 권장 조합

| 기본 장르 | 조합 권장 | 조합 회피 |
|----------|----------|----------|
| **R&B** | Soul, Lo-fi, Acoustic, Jazz | EDM, Metal, Festival |
| **Lo-fi** | Chill, Jazz, R&B, Ambient | Big Room, Trap, Dubstep |
| **Ambient** | Electronic, Chill, R&B | Trap, Metal |
| **Acoustic** | Folk, Ballad, R&B | EDM, Synth |
| **Ballad** | Orchestral, Piano, R&B | Trap, EDM |

### 11.2 사용법

- **Spine 1개** (메인 장르) + **Color 1개** (보조 색깔)
- 예: `Korean R&B` (spine) + `Lo-fi texture` (color)
- **3개 이상 장르 스택 → 결과 혼란**

**예시:**
- ✅ `Korean Lo-fi R&B, 80 BPM` (R&B + Lo-fi)
- ✅ `Acoustic R&B Ballad, 88 BPM` (R&B + Acoustic)
- ❌ `Lo-fi R&B Jazz Ambient Chill` (5개 스택 → 혼란)

---

## 12) Tag Bank (키워드 사전)

> 상황에 맞는 키워드 선택용 참고 자료

### 12.1 보컬 스타일 키워드

**기본 (Raw Vocal Baseline):**
```
Raw, Solid, Direct, Intimate, Clear, Dry, Unprocessed
```

**요청 시 추가:**
| 컨셉 | 키워드 |
|------|--------|
| Powerful | Powerful, Strong attack, Belt |
| Husky | Raspy, Grit, Husky |
| Airy | Airy, Breathy, Soft |
| Warm | Warm, Soulful, Smooth |
| Emotional | Emotional, Expressive, Heartfelt |

### 12.2 분위기/감정 키워드

```
melancholic, dreamy, mysterious, hopeful, nostalgic, peaceful,
dramatic, reflective, tender, whimsical, serene, intimate,
bittersweet, contemplative, ethereal
```

### 12.3 프로덕션 키워드

**공간감/질감:**
```
high fidelity, wide stereo, cinematic but restrained,
subtle room reverb, intimate atmosphere, spacious mix,
let the mix breathe, clear separation between instruments
```

**다이내믹:**
```
build intensity gradually, soft verses powerful chorus,
dynamic range, controlled crescendo
```

### 12.4 악기/사운드 키워드

**피아노 계열:**
```
felt piano, acoustic piano, Rhodes, electric piano, warm keys
```

**기타 계열:**
```
nylon guitar, acoustic guitar, cold arpeggio, fingerstyle
```

**리듬 계열:**
```
soft shaker, brush kit, rim-shot, rim-click, soft percussion,
layback groove, understated kick
```

**앰비언스:**
```
ambient pad, hazy texture, atmospheric synth, subtle strings
```

### 12.5 Texture Lines (믹스/공간 제어)

> **복붙 가능한 믹스 질감 제어 문장 라이브러리**
> 출처: museA 자료집 + Style Prompt Guide 2.0

**공간감 (Spaciousness):**
```
Let the mix breathe; keep clear separation between instruments.
Intimate small-room space; soft natural room reverb.
Make the space feel close and personal, not wide.
Focus on clarity rather than loudness.
```

**밀도 제어 (Density):**
```
Keep the arrangement spacious; avoid cluttered arrangements.
Leave space between instruments; reduce density in the middle section.
Build intensity gradually toward the end.
```

**악기 분리감 (Separation):**
```
Keep clear separation between instruments.
Make each instrument feel distinct.
Avoid cluttered arrangements; focus on clarity.
```

**사용법:**
- 위 문장 중 1-2개를 Style Prompt 끝에 추가
- 전체 추가 금지 (900자 제한 고려)
- "pop" 같은 평준화 키워드가 아닌 **엔지니어링 컨트롤 문장**이라 안전

### 12.6 FX/Production 키워드

> 출처: Style Prompt Guide 2.0 Tag Bank

**리버브/딜레이:**
```
subtle room reverb, tape delay, gated reverb, long reverb tails
```

**프로덕션 FX:**
```
lo-fi vinyl crackle, stereo wideners, sidechain pump (EDM 시에만)
```

**Era/Influence:**
```
90s R&B nostalgia, 80s synth aesthetic, retro production
```

### 12.7 장르 키워드 (2026 트렌드)

> 출처: museA Suno 자료집 (2026-02 업데이트)

**숏폼 & 인터넷 네이티브:**
```
Hyperpop, Phonk, Drift Phonk, Glitchcore, Sped Up, Sigilkore
```

**댄스 & 리듬 트렌드:**
```
Jersey Club, Baltimore Club, 2-Step, Breakcore, UK Garage
```

**글로벌 & 힙합:**
```
Amapiano, Rage, Pluggnb, Jersey Drill, Latin Pop, Urbano
```

**분위기 & 미학:**
```
Bedroom Pop, Weirdcore, Dreamcore, Vaporwave
```

**사용 팁:**
- Drift Phonk: 자동차/드리프트 영상 배경음, 카우벨 강조
- Jersey Club: K-pop 아이돌곡에 많이 차용, 특유의 킥 패턴
- Amapiano: 로그 드럼 베이스 + 재즈 건반, 현재 글로벌 핫 장르

### 12.8 보컬 스타일 확장

**캐릭터/연극적 보컬:**
```
theatrical, persona-driven, animated, character voice
```

**특수 스타일:**
```
operatic, childlike, robotic, spoken word
```

### 12.9 구조 & 길이 제어 프롬프트

> 곡 구조와 길이를 조절하는 영어 프롬프트

**Intro/Outro 길이:**
```
Make the intro longer and more lyrical
Write a longer and more impactful outro
Let the outro fade slowly and emotionally
Strip the arrangement down in the outro
```

**구조 변형:**
```
Add a short instrumental break
Reduce density in the middle section
Build intensity gradually toward the end
```

**공간감 제어 (추가):**
```
Create a small jazz club atmosphere
Make the space feel intimate rather than wide
Let the sound feel close and personal
