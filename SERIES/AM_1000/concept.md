# AM_1000 — 업무시간

> **Korean Chillhop — Minimal Vocals, Loop-based**
>
> Version: 1.0
> Last Updated: 2026-02-26
> Status: 방향 전환 — 전 트랙 리워크

---

## Station Identity

| 항목 | 값 |
|------|-----|
| **시간** | 10:00 |
| **Station명** | 업무시간 |
| **감정톤** | 지속, 루틴, 차분 |
| **장르** | Korean Chillhop (minimal vocals, loop-based) |
| **용도** | 오전 업무/작업 중 배경음악 (집중 방해 X) |

---

## Direction

```
"한국어 미니멀 보컬 Chillhop. 루프 기반, 보컬은 텍스처."
```

- 인스트루멘탈 중심의 클래식 Chillhop 구조
- 보컬은 3가지 타입으로 최소화 (A/B/C)
- 루프 기반 전개: 레이어 추가/제거로 섹션 변화
- 듣는다기보다 깔아두는 음악
- Jazzy하고 세련된 분위기

---

## Sound Profile

| Slot | 값 |
|------|-----|
| **BPM** | 78-95 (Chillhop 표준, 업무용 하한 유지) |
| **Key Bucket** | Bucket 5 (Neutral: D minor / E minor) |
| **Lead Instrument** | Rhodes, Wurlitzer, Jazz Guitar (2개 이상 필수) |
| **Rhythm** | Crisp jazzy drums, swing feel, laid-back groove |
| **Bass** | Upright bass, warm but defined |
| **Texture** | **High-fidelity but warm** (NOT dusty/muffled) |
| **Optional** | Saxophone accents, vibraphone, subtle brass |

### Sound DNA (Lo-fi와 구분)

| ❌ 피할 것 (Lo-fi) | ✅ 지향할 것 (Chillhop) |
|-------------------|------------------------|
| Dusty, muffled | Crisp, polished |
| Heavy vinyl crackle | Subtle warm saturation |
| Underwater samples | Live-sounding instruments |
| Night mood | **Daylight mood** |

---

## Vocal Strategy (A/B/C 타입)

### 보컬 타입 시스템

| 타입 | 설명 | 배분 |
|------|------|------|
| **A** | 한 섹션만 보컬 (4-8줄), 나머지 인스트루멘탈 | 2 트랙 |
| **B** | 1-3줄 반복 (만트라/루프) | 7 트랙 |
| **C** | 거의 인스트루멘탈 + 허밍/스캣 텍스처 | 6 트랙 |

### 공통 규칙

| 항목 | 값 |
|------|-----|
| **Persona** | Female (Alto/Contralto) / Male (Baritone) 교대 |
| **Processing (A/B)** | Buried, low in mix, ambient reverb, soft |
| **Processing (C)** | 허밍/스캣도 악기처럼 처리, 텍스처 레벨 |
| **Articulation** | Clear Korean articulation (발음은 명확, 배치만 buried) |

### Vocal Mix 지시 (A/B 타입)

```
Vocals buried deep in mix, underneath instruments.
Heavy ambient reverb, far back in soundstage.
Vocal as background texture, not lead.
```

### Intro 제약 (전 타입 공통)

> **[Intro] 섹션에서 금지:**
> - ❌ Humming
> - ❌ Ad-libs
> - ❌ Scat
>
> **적용 방법:** Style Prompt의 Intro 섹션 지시에 명시 (Exclude 아님)
> ```
> Intro: Instrumental only, no vocal, no humming.
> ```
>
> **이유:** 업무 시작 시 집중 방해 요소 제거. Intro는 악기만으로 분위기 세팅.

---

## Structure Approach (루프 기반)

> 클래식 Chillhop은 Verse/Chorus 팝 구조가 아닌 **루프 기반 + 레이어 전개**가 표준.

### Type A (한 섹션 보컬)
```
[intro] → [loop A] → [vocal section] → [loop B] → [loop A'] → [outro]
```

### Type B (만트라)
```
[intro] → [loop A + mantra] → [loop B] → [loop A + mantra] → [outro]
```

### Type C (인스트루멘탈)
```
[intro] → [loop A] → [loop B] → [loop A'] → [bridge] → [outro]
```

**공통:**
- 섹션 전환은 레이어 추가/제거로 자연스럽게 (드라마틱 전환 금지)
- [interlude], [instrumental] 태그로 인스트루멘탈 구간 확보
- 목표 런타임: 3분 이상

---

## Exclude Strategy

```
Upbeat, Energetic, Bright, Dynamic shifts, Aggressive
Prominent vocals, Clear articulation, Forward vocals
Airy, Falsetto, Harmonized, Backing vocals, Whisper
```

**원칙:** 업무 방해 요소 차단 + 보컬 전면 배치 차단

**Style Prompt 권장:** `Minimal scat/humming if any, keep subtle and buried.`

---

## Cross-Series 겹침 검증

| 축 | 업무시간 (10:00) | 출근길 (08:30) | 오후햇살 (14:00) |
|---|---|---|---|
| **장소** | 책상, 모니터, 사무실 | 지하철, 버스, 거리 | 창가, 소파 |
| **감정** | 지속, 루틴, 차분 | 이동, 흐름, 몰입 | 나른, 따뜻, 멍 |
| **상황** | 업무 중, 집중 필요 | 출퇴근 이동 | 휴식, 여유 |

**결과:** 3축 중 0개 겹침 → PASS

---

## Track List (15곡)

| # | Title | Type | Vocal | BPM | Key | Lead Instruments | Status |
|---|-------|------|-------|-----|-----|-----------------|--------|
| 01 | 오전 | B | Female (Contralto) | 85 | Dm | Rhodes, Jazz Guitar | 완료 |
| 02 | 거울 | B | Male (Baritone) | 87 | Em | Wurlitzer, Rhodes | 완료 |
| 03 | 사진 | C | — (웃음소리 샘플) | 90 | D major | Jazz Guitar, Rhodes | 완료 |
| 04 | 모니터 | B | Male (Baritone) | 90 | Em | Rhodes, Wurlitzer | 완료 |
| 05 | 집중 | C | — | 78 | Dm | Wurlitzer, Jazz Guitar | 완료 |
| 06 | 알림 | B | Female (Alto) | 83 | Em | Rhodes, Jazz Guitar | 완료 |
| 07 | 잉크 | B | Male (Baritone) | 85 | E major | Jazz Guitar, Wurlitzer | 완료 |
| 08 | 타이핑 | B | Female (Alto) | 88 | Dm | Rhodes, Jazz Guitar | 완료 |
| 09 | 숨 | C | — | 85 | D major | Jazz Guitar, Wurlitzer | 완료 |
| 10 | 환기 | C | — | 80 | E major | Rhodes, Wurlitzer | 완료 |
| 11 | 회의 | B | Male (Baritone) | 87 | D major | Wurlitzer, Rhodes | 완료 |
| 12 | 다시 | C | — (finger snap) | 82 | E major | Rhodes, Wurlitzer | 완료 |
| 13 | Tab | A | Male (Baritone) | 85 | Dm | Wurlitzer, Rhodes | 완료 |
| 14 | Tick Tock | C | — (clock rhythm) | 80 | Em | Jazz Guitar, Rhodes | 완료 |
| 15 | Hunger | C | — (sparse) | 78 | E major | Jazz Guitar, Rhodes | 완료 |

### Type 배분
```
A (한 섹션 보컬): Track 13, 14
B (만트라/루프):  Track 01, 02, 04, 06, 07, 08, 11
C (인스트루멘탈): Track 03, 05, 09, 10, 12, 15
```

### BPM 아크
```
85 → 87 → 90 → 90 → 78 → 83 → 85 → 88 → 85 → 80 → 87 → 82 → 85 → 80 → 78
                      ↑              ↑                    ↑              ↑
                 Breathing       Recovery            2nd Wave        Wind Down
```

### 서사 아크 (오전 업무 동선)
```
오전(시작) → 거울(자리) → 사진(일상) → 모니터(몰입) → 집중(깊이)
→ 알림(중단) → 잉크(필기) → 타이핑(리듬) → 숨(쉼) → 환기(전환)
→ 회의(이동) → 다시(복귀) → Tab(정리) → Tick Tock(응시) → Hunger(끝)
```

---

## YouTube Metadata (초안)

### Title Format
```
10:00 playlist | 업무시간
```

### Description (초안)
```
[작성 예정]

---
#chillhop #업무용음악 #집중 #playlist #soomshuim

🎵 Music: soomshuim
Copyright Ⓒ soomshuim. All rights reserved.
```

### Pinned Comment
```
이 채널의 노래들은 모두 우리말 가사로 만들었어요.
지금 당신의 이 시간이 더 천천히, 더 깊게 닿기를 바랍니다.

오늘 하루, 무엇이 당신을 책상 앞에 앉게 했나요?
```

---

## Track 01: 오전

### Suno Parameters
- Style Influence: 70
- Weirdness: 30

### Lyrics
```
[intro]
(instrumental only, no vocals, no humming)

[instrumental]
(Rhodes melody, jazz guitar, upright bass, swing groove)

[verse]
(Contralto female buried deep, ambient reverb, no filler sounds)
물끄러미 앉아
볼펜이 굴러가

[instrumental]
(jazz guitar lead, Rhodes chords, upright bass groove)

[interlude]
(Rhodes pad, soft drums, breathing space)

[verse]
(buried vocal, ambient reverb)
물끄러미 앉아
볼펜이 굴러가

[outro]
(Rhodes restates motif, instruments fade gently)
```

### Style Prompt
```
Korean Chillhop, 85 BPM, D minor

Rhodes-led, jazz guitar accents. Upright bass warm defined. Crisp jazzy drums, swing feel, laid-back groove. High-fidelity but warm, subtle saturation. Daylight mood.

Contralto female vocal buried deep in mix, underneath instruments. Clear Korean articulation. Heavy ambient reverb, far back in soundstage. Vocal as background texture, not lead.

No filler sounds, no ad-libs. Clean vocal lines only.

Intro: Instrumental only, no vocals, no humming.
Instrumental sections: Rhodes melody, jazz guitar, full groove.
Verse: brief buried vocal, one mantra phrase, then instruments continue.
Outro: Rhodes restates motif, gentle fade.

Single vocal throughout. No harmony no backing no doubles.
Target runtime over 3 minutes.
```

### Exclude
```
Dusty, Muffled, Lo-fi hiss, Prominent vocals, Forward vocals, Airy, Falsetto, Harmonized```

## Track 02: 거울

### Suno Parameters
- Style Influence: 70
- Weirdness: 30

### Lyrics
```
[intro]
(instrumental only, no vocals, no humming)

[instrumental]
(Wurlitzer melody, Rhodes accents, upright bass, crisp jazzy drums)

[instrumental]
(jazz guitar enters, full arrangement, swing groove)

[verse]
(Baritone male buried deep, clear Korean articulation, ambient reverb, no filler sounds)
까만 거울 속에
내가 비쳐

[instrumental]
(Wurlitzer lead, Rhodes pad, upright bass groove)

[interlude]
(jazz guitar solo, soft drums, breathing space)

[verse]
(buried vocal, ambient reverb)
까만 거울 속에
내가 비쳐

[outro]
(Wurlitzer restates motif, instruments thin, gentle fade)
```

### Style Prompt
```
Korean Chillhop, 87 BPM, E minor

Wurlitzer-led, Rhodes accents. Upright bass warm defined. Crisp jazzy drums, swing feel, fresh groove. High-fidelity, polished. Daylight mood.

Baritone male vocal buried deep in mix, underneath instruments. Clear Korean articulation. Heavy ambient reverb, far back in soundstage. Vocal as background texture, not lead.

No filler sounds, no ad-libs. Clean vocal lines only.

Intro: Instrumental only, no vocals, no humming.
Instrumental sections: Wurlitzer melody, jazz guitar, full groove.
Verse: brief buried vocal mantra, two lines only, repeats.
Outro: Wurlitzer restates motif, gentle fade.

Single vocal throughout. No harmony no backing no doubles.
Target runtime over 3 minutes.
```

### Exclude
```
Dusty, Muffled, Lo-fi hiss, Prominent vocals, Forward vocals, Airy, Falsetto, Harmonized```

---

## Track 03: 사진

### Suno Parameters
- Style Influence: 75
- Weirdness: 25
- **Sample Upload**: 소예_반복20.wav (딸 웃음소리, 5초 × 20회, 홀수만 재생)

### Lyrics
```
[intro]
(girl laughter sample, then instruments fade in)

[instrumental]
(girl laughter sample brief, Jazz guitar melody, Rhodes pad, upright bass, swing groove)

[interlude]
(girl laughter sample, Rhodes chords, soft drums)

[instrumental]
(girl laughter sample brief, full arrangement, jazz guitar lead, warm groove)

[interlude]
(girl laughter sample, jazz guitar solo, breathing space)

[instrumental]
(girl laughter sample brief, Rhodes and jazz guitar together, upright bass groove)

[outro]
(girl laughter sample, Rhodes motif, gentle fade)
```

### Style Prompt
```
Korean Chillhop, 90 BPM, D major

Jazz guitar-led, Rhodes accents. Upright bass warm defined. Crisp jazzy drums, swing feel, playful groove. High-fidelity but warm, subtle saturation. Daylight mood, gentle smile. Warm major7 chords.

Purely instrumental with girl laughter sample as texture. Laughter sits in background, reverb-processed, blending into arrangement. Warm and familial tone.

No filler sounds, no ad-libs. No vocals, no humming.

Intro: Laughter sample into instruments.
Instrumental sections: jazz guitar melody, full groove, warm.
Interludes: laughter sample brief, breathing space.
Outro: laughter sample, Rhodes fade.

No vocal melody. No singing. Laughter as texture only.
Target runtime over 3 minutes.
```

### Exclude
```
Dusty, Muffled, Lo-fi hiss, Vocals, Singing, Airy, Falsetto, Harmonized
```

## Track 04: 모니터

### Suno Parameters
- Style Influence: 70
- Weirdness: 30

### Lyrics
```
[intro]
(instrumental only, no vocals, no humming)

[instrumental]
(Rhodes melody, Wurlitzer accents, upright bass, swing groove)

[instrumental]
(full arrangement, Rhodes lead, crisp jazzy drums)

[verse]
(Baritone male buried deep, clear Korean articulation, ambient reverb, no filler sounds)
모니터 픽셀 물결의 파동
점점 빠져가
헤엄쳐

[instrumental]
(Wurlitzer lead, Rhodes pad, upright bass groove)

[interlude]
(Rhodes chords, soft drums, breathing space)

[verse]
(buried vocal, ambient reverb)
모니터 픽셀 물결의 파동
점점 빠져가
헤엄쳐

[outro]
(Rhodes and Wurlitzer motif, gentle fade)
```

### Style Prompt
```
Korean Chillhop, 90 BPM, E minor

Rhodes-led, Wurlitzer accents. Upright bass warm defined. Crisp jazzy drums, swing feel, laid-back groove. High-fidelity but warm. Subtle vinyl warmth, light analog texture. NOT dusty or muffled. Daylight mood.

Baritone male vocal buried deep in mix, underneath instruments. Clear Korean articulation. Heavy ambient reverb, far back in soundstage. Vocal as background texture, not lead.

No filler sounds, no ad-libs. Clean vocal lines only.

Intro: Instrumental only, no vocals, no humming.
Instrumental sections: Rhodes melody, Wurlitzer, full groove.
Verse: brief buried vocal, mantra phrase, then instruments continue.
Outro: Rhodes and Wurlitzer motif, gentle fade.

Single vocal throughout. No harmony no backing no doubles.
Target runtime over 3 minutes.
```

### Exclude
```
Dusty, Muffled, Lo-fi hiss, Prominent vocals, Forward vocals, Airy, Falsetto, Harmonized```

---

## Track 05: 집중

### Suno Parameters
- Style Influence: 65
- Weirdness: 35

### Lyrics
```
[intro]
(instrumental only, no vocals, no humming)

[instrumental]
(Wurlitzer melody gentle, jazz guitar chords, upright bass, soft jazzy drums)

[instrumental]
(jazz guitar takes lead, Wurlitzer pad, upright bass groove, swing feel)

[interlude]
(Wurlitzer solo, minimal drums, breathing space)

[instrumental]
(Wurlitzer and jazz guitar together, full arrangement, warm groove)

[instrumental]
(jazz guitar solo, Wurlitzer accents, upright bass, subtle vibraphone)

[outro]
(Wurlitzer restates motif, instruments thin, gentle fade)
```

### Style Prompt
```
Korean Chillhop, 78 BPM, D minor

Wurlitzer-led, jazz guitar support. Upright bass warm defined. Crisp jazzy drums, swing feel, laid-back groove. High-fidelity but warm, subtle saturation. Deep focus mood, hypnotic. Minor7 and minor9 chord voicings.

Purely instrumental. No vocals, no humming, no scat.

No filler sounds, no ad-libs.

Intro: Wurlitzer melody, sparse.
Instrumental sections: Wurlitzer lead, jazz guitar weaving, warm groove builds gradually.
Interlude: Wurlitzer solo, breathing space.
Outro: Wurlitzer restates motif, gentle fade.

No vocal melody. No singing. Pure instruments only.
Target runtime over 3 minutes.
```

### Exclude
```
Dusty, Muffled, Lo-fi hiss, Vocals, Singing, Airy, Falsetto, Harmonized
```

---

## Track 06: 알림

### Suno Parameters
- Style Influence: 65
- Weirdness: 35

### Lyrics
```
[intro]
(instrumental only, no vocals, no humming)

[instrumental]
(Rhodes melody crisp, jazz guitar chords, upright bass, crisp jazzy drums, subtle bell chime accents)

[instrumental]
(jazz guitar takes lead, Rhodes accents, upright bass groove, swing feel, glockenspiel chime motif)

[verse]
(Alto female buried deep, clear Korean articulation, ambient reverb, no filler sounds)
고개를 들어
또 울린다

[instrumental]
(Rhodes lead, jazz guitar pad, upright bass groove)

[interlude]
(Rhodes chords, soft percussion, breathing space)

[verse]
(buried vocal, ambient reverb)
고개를 들어
또 울린다

[outro]
(Rhodes restates motif, instruments thin, gentle fade)
```

### Style Prompt
```
Korean Chillhop, 83 BPM, E minor

Rhodes-led, jazz guitar support. Upright bass warm defined. Crisp jazzy drums, swing feel, fresh groove. High-fidelity but warm, subtle saturation. Bright awareness mood. Minor7 chord voicings with occasional major lifts. Subtle bell chime and glockenspiel accents woven throughout, clean bright short tones evoking gentle notification sounds.

Alto female vocal buried deep in mix, underneath instruments. Clear Korean articulation. Heavy ambient reverb, far back in soundstage. Vocal as background texture, not lead.

No filler sounds, no ad-libs. Clean vocal lines only.

Intro: Instrumental only, no vocals, no humming.
Instrumental sections: Rhodes lead, jazz guitar weaving, groove with subtle energy.
Verse: brief buried vocal mantra, two lines only, repeats.
Outro: Rhodes restates motif, gentle fade.

Single vocal throughout. No harmony no backing no doubles.
Target runtime over 3 minutes.
```

### Exclude
```
Dusty, Muffled, Lo-fi hiss, Prominent vocals, Forward vocals, Airy, Falsetto, Harmonized```

---

## Track 07: 잉크

### Suno Parameters
- Style Influence: 65
- Weirdness: 35

### Lyrics
```
[intro]
(instrumental only, no vocals, no humming)

[instrumental]
(Jazz guitar melody, Wurlitzer chords, upright bass, crisp jazzy drums)

[instrumental]
(Wurlitzer takes lead, jazz guitar pad, fuller arrangement, swing groove)

[verse]
(Baritone male buried deep, clear Korean articulation, ambient reverb, no filler sounds)
번진 자국 위
마르지 않아

[instrumental]
(Jazz guitar lead, Wurlitzer accents, upright bass groove)

[interlude]
(jazz guitar solo, soft drums, breathing space)

[verse]
(buried vocal, ambient reverb)
번진 자국 위
마르지 않아

[instrumental]
(Jazz guitar and Wurlitzer together, full arrangement, warm groove)

[outro]
(Wurlitzer restates motif, instruments thin, gentle fade)
```

### Style Prompt
```
Korean Chillhop, 85 BPM, E major

Jazz guitar-led, Wurlitzer accents. Upright bass warm defined. Crisp jazzy drums, swing feel, laid-back groove. High-fidelity but warm, subtle saturation. Daylight mood, steady pulse.

Baritone male vocal buried deep in mix, underneath instruments. Clear Korean articulation. Heavy ambient reverb, far back in soundstage. Vocal as background texture, not lead.

No filler sounds, no ad-libs. Clean vocal lines only.

Intro: Instrumental only, no vocals, no humming.
Instrumental sections: Jazz guitar melody, Wurlitzer, full groove.
Verse: brief buried vocal mantra, two lines only, repeats.
Outro: Wurlitzer restates motif, gentle fade.

Single vocal throughout. No harmony no backing no doubles.
Target runtime over 3 minutes.
```

### Exclude
```
Dusty, Muffled, Lo-fi hiss, Prominent vocals, Forward vocals, Airy, Falsetto, Harmonized```

---

## Track 08: 타이핑

### Suno Parameters
- Style Influence: 65
- Weirdness: 35

### Lyrics
```
[intro]
(instrumental only, no vocals, no humming)

[instrumental]
(Rhodes melody, jazz guitar chords, upright bass, crisp jazzy drums)

[verse]
(Alto female buried deep, clear Korean articulation, ambient reverb, no filler sounds)
빽빽한 창문 마디 마디
쉼 없이 Knock knock
어깨는 down down

[instrumental]
(jazz guitar takes lead, Rhodes pad, fuller arrangement, swing groove)

[interlude]
(jazz guitar solo, soft drums, breathing space)

[verse]
(buried vocal, ambient reverb)
빽빽한 창문 마디 마디
쉼 없이 Knock knock
어깨는 down down

[instrumental]
(Rhodes and jazz guitar together, full arrangement, warm groove)

[outro]
(Rhodes restates motif, instruments thin, gentle fade)
```

### Style Prompt
```
Korean Chillhop, 88 BPM, D minor

Rhodes-led, jazz guitar support. Upright bass warm defined. Crisp jazzy drums, swing feel, rhythmic groove. High-fidelity but warm, subtle saturation. Daylight mood, gentle momentum.

Alto female vocal buried deep in mix, underneath instruments. Clear Korean articulation. Heavy ambient reverb, far back in soundstage. Vocal as background texture, not lead.

No filler sounds, no ad-libs. Clean vocal lines only.

Intro: Instrumental only, no vocals, no humming.
Instrumental sections: Rhodes melody, jazz guitar, full groove.
Verse: brief buried vocal mantra, three lines only, repeats.
Outro: Rhodes restates motif, gentle fade.

Single vocal throughout. No harmony no backing no doubles.
Target runtime over 3 minutes.
```

### Exclude
```
Dusty, Muffled, Lo-fi hiss, Prominent vocals, Forward vocals, Airy, Falsetto, Harmonized```

---

## Track 09: 숨

### Suno Parameters
- Style Influence: 65
- Weirdness: 35

### Lyrics
```
[intro]
(instrumental only, no vocals, no humming)

[instrumental]
(Jazz guitar melody gentle, Wurlitzer chords, upright bass, soft jazzy drums)

[instrumental]
(Wurlitzer takes lead, jazz guitar pad, upright bass groove, swing feel)

[interlude]
(Jazz guitar solo, minimal drums, breathing space)

[instrumental]
(Jazz guitar and Wurlitzer together, full arrangement, warm groove)

[instrumental]
(Wurlitzer solo, jazz guitar accents, upright bass, subtle vibraphone)

[outro]
(Jazz guitar restates motif, instruments thin, gentle fade)
```

### Style Prompt
```
Korean Chillhop, 85 BPM, D major

Jazz guitar-led, Wurlitzer accents. Upright bass warm defined. Crisp jazzy drums, swing feel, laid-back groove. High-fidelity but warm, subtle saturation. Daylight mood, gentle relief. Major7 chord voicings, warm open feel.

Purely instrumental. No vocals, no humming, no scat.

No filler sounds, no ad-libs.

Intro: Jazz guitar melody, sparse.
Instrumental sections: Jazz guitar lead, Wurlitzer weaving, warm groove builds gradually.
Interlude: Jazz guitar solo, breathing space.
Outro: Jazz guitar restates motif, gentle fade.

No vocal melody. No singing. Pure instruments only.
Target runtime over 3 minutes.
```

### Exclude
```
Dusty, Muffled, Lo-fi hiss, Vocals, Singing, Airy, Falsetto, Harmonized
```

---

## Track 10: 환기

### Suno Parameters
- Style Influence: 65
- Weirdness: 35

### Lyrics
```
[intro]
(instrumental only, no vocals, no humming)

[instrumental]
(Rhodes melody sparse and open, Wurlitzer chords, upright bass, soft jazzy drums)

[instrumental]
(Wurlitzer takes lead, Rhodes pad, upright bass groove, swing feel)

[interlude]
(Wurlitzer solo, minimal drums, breathing space)

[instrumental]
(Rhodes and Wurlitzer together, full arrangement, warm groove)

[instrumental]
(Rhodes solo, Wurlitzer accents, upright bass, spacious feel)

[outro]
(Rhodes restates motif, instruments thin, gentle fade)
```

### Style Prompt
```
Korean Chillhop, 80 BPM, E major

Rhodes-led, Wurlitzer accents. Upright bass warm defined. Crisp jazzy drums, swing feel, laid-back groove. High-fidelity but warm, subtle saturation. Daylight mood, open air feel. Major7 and add9 chord voicings, spacious and bright.

Purely instrumental. No vocals, no humming, no scat.

No filler sounds, no ad-libs.

Intro: Rhodes melody, sparse and open.
Instrumental sections: Rhodes lead, Wurlitzer weaving, warm groove builds gradually.
Interlude: Wurlitzer solo, breathing space.
Outro: Rhodes restates motif, gentle fade.

No vocal melody. No singing. Pure instruments only.
Target runtime over 3 minutes.
```

### Exclude
```
Dusty, Muffled, Lo-fi hiss, Vocals, Singing, Airy, Falsetto, Harmonized
```

---

## Track 11: 회의

### Suno Parameters
- Style Influence: 65
- Weirdness: 35

### Lyrics
```
[intro]
(instrumental only, no vocals, no humming)

[instrumental]
(Wurlitzer melody, Rhodes chords, upright bass, crisp jazzy drums)

[instrumental]
(Rhodes takes lead, Wurlitzer accents, fuller arrangement, swing groove)

[verse]
(Baritone male buried deep, clear Korean articulation, ambient reverb, no filler sounds)
핑퐁 핑퐁
삐걱 삐걱
핑퐁 핑퐁
삐걱 삐걱

[instrumental]
(Wurlitzer lead, Rhodes pad, upright bass groove)

[interlude]
(Wurlitzer solo, soft drums, breathing space)

[verse]
(buried vocal, ambient reverb)
핑퐁 핑퐁
삐걱 삐걱
핑퐁 핑퐁
삐걱 삐걱

[instrumental]
(Wurlitzer and Rhodes together, full arrangement, warm groove)

[outro]
(Wurlitzer restates motif, instruments thin, gentle fade)
```

### Style Prompt
```
Korean Chillhop, 87 BPM, D major

Wurlitzer-led, Rhodes accents. Upright bass warm defined. Crisp jazzy drums, swing feel, laid-back groove. High-fidelity but warm, subtle saturation. Daylight mood, meeting room rhythm.

Baritone male vocal buried deep in mix, underneath instruments. Clear Korean articulation. Heavy ambient reverb, far back in soundstage. Vocal as background texture, not lead.

No filler sounds, no ad-libs. Clean vocal lines only.

Intro: Instrumental only, no vocals, no humming.
Instrumental sections: Wurlitzer melody, Rhodes accents, full groove.
Verse: brief buried vocal mantra, four lines, repeats.
Outro: Wurlitzer restates motif, gentle fade.

Single vocal throughout. No harmony no backing no doubles.
Target runtime over 3 minutes.
```

### Exclude
```
Dusty, Muffled, Lo-fi hiss, Prominent vocals, Forward vocals, Airy, Falsetto, Harmonized```

---

## Track 12: 다시

### Suno Parameters
- Style Influence: 65
- Weirdness: 35

### Lyrics
```
[intro]
(instrumental only, no vocals, no humming, no scat)

[instrumental]
(Rhodes melody, Wurlitzer chords, upright bass, crisp jazzy drums, subtle finger snaps)

[instrumental]
(Wurlitzer takes lead, Rhodes pad, fuller arrangement, swing groove, finger snaps accent)

[interlude]
(Rhodes chords, soft drums, finger snaps, breathing space)

[instrumental]
(Rhodes and Wurlitzer together, full arrangement, warm groove, finger snaps continue)

[instrumental]
(Wurlitzer solo, Rhodes accents, upright bass groove, subtle finger snaps)

[outro]
(Rhodes restates motif, finger snaps fade, instruments thin, gentle fade)
```

### Style Prompt
```
Korean Chillhop, 82 BPM, E major

Rhodes-led, Wurlitzer accents. Upright bass warm defined. Crisp jazzy drums, swing feel, laid-back groove. High-fidelity but warm, subtle saturation. Daylight mood, return to focus.

Purely instrumental with finger snaps as rhythmic texture. Finger snaps subtle, woven into groove, not dominant. Snaps as gentle focus cue.

No vocals, no humming, no scat. No filler sounds.

Intro: Instrumental only.
Instrumental sections: Rhodes melody, Wurlitzer weaving, finger snaps accent on offbeats.
Interlude: breathing space, minimal.
Outro: Rhodes restates motif, gentle fade.

No vocal melody. No singing. Pure instruments with finger snap texture.
Target runtime over 3 minutes.
```

### Exclude
```
Dusty, Muffled, Lo-fi hiss, Vocals, Singing, Airy, Falsetto, Harmonized
```

---

## Track 13: Tab

### Suno Parameters
- Style Influence: 65
- Weirdness: 35

### Lyrics
```
[intro]
(instrumental only, no vocals, no humming)

[instrumental]
(Wurlitzer melody, Rhodes chords, upright bass, crisp jazzy drums)

[instrumental]
(Rhodes takes lead, Wurlitzer accents, fuller arrangement, swing groove)

[verse]
(Baritone male buried deep, clear Korean articulation, ambient reverb, no filler sounds)
열어둔 창들
하나씩 닫아
클릭 클릭

[instrumental]
(Wurlitzer lead, Rhodes pad, upright bass groove)

[interlude]
(Wurlitzer solo, soft drums, breathing space)

[instrumental]
(Rhodes and Wurlitzer together, full arrangement, warm groove)

[outro]
(Wurlitzer restates motif, instruments thin, gentle fade)
```

### Style Prompt
```
Korean Chillhop, 85 BPM, D minor

Wurlitzer-led, Rhodes accents. Upright bass warm defined. Crisp jazzy drums, swing feel, laid-back groove. High-fidelity but warm, subtle saturation. Daylight mood, quiet focus.

Baritone male vocal buried deep in mix, underneath instruments. Clear Korean articulation. Heavy ambient reverb, far back in soundstage. Vocal as background texture, not lead.

No filler sounds, no ad-libs. Clean vocal lines only. Minimal scat/humming if any, keep subtle and buried.

Intro: Instrumental only, no vocals, no humming.
Instrumental sections: Wurlitzer melody, Rhodes accents, full groove.
Verse: brief buried vocal, three lines only, appears once.
Outro: Wurlitzer restates motif, gentle fade.

Single vocal throughout. No harmony no backing no doubles.
Target runtime over 3 minutes.
```

### Exclude
```
Dusty, Muffled, Lo-fi hiss, Prominent vocals, Forward vocals, Airy, Falsetto, Harmonized
```

---

## Track 14: Tick Tock

### Suno Parameters
- Style Influence: 65
- Weirdness: 35

### Lyrics
```
[intro]
(instrumental only, no vocals, no humming, no scat, clock rhythm establishes)

[instrumental]
(Jazz guitar melody, Rhodes chords, upright bass, soft jazzy drums, tick-tock pulse)

[instrumental]
(Rhodes takes lead, jazz guitar accents, fuller arrangement, swing groove, tick-tock continues)

[interlude]
(Jazz guitar solo, soft drums, clock rhythm subtle, breathing space)

[instrumental]
(Rhodes and jazz guitar together, full arrangement, warm groove, tick-tock pulse)

[instrumental]
(Jazz guitar solo, Rhodes accents, upright bass groove, tick-tock steady)

[outro]
(Rhodes restates motif, instruments thin, clock fades last, gentle fade)
```

### Style Prompt
```
Korean Chillhop, 80 BPM, E minor

Jazz guitar-led, Rhodes accents, Upright bass warm defined, Crisp jazzy drums, swing feel, laid-back groove, High-fidelity but warm, subtle saturation, Daylight mood, time standing still, Clock-like rhythm throughout: wood block or rim click on every beat, steady tick-tock pulse woven into groove, Metronomic feel but organic, Purely instrumental, No vocals, no humming, no scat, No filler sounds, Intro: Instrumental only, clock rhythm establishes, Instrumental sections: Jazz guitar melody, Rhodes weaving, clock pulse continues, Interlude: Jazz guitar solo, clock rhythm subtle, Outro: Rhodes restates motif, clock fades last, No vocal melody, No singing, Pure instruments only, Target runtime over 3 minutes
```

### Exclude
```
Dusty, Muffled, Lo-fi hiss, Vocals, Singing, Airy, Falsetto, Harmonized
```

---

## Track 15: Hunger

### Suno Parameters
- Style Influence: 65
- Weirdness: 35

### Lyrics
```
[intro]
(instrumental only, no vocals, no humming, no scat, sparse and empty)

[instrumental]
(Jazz guitar melody sparse, Rhodes single notes, upright bass minimal, soft drums, lots of silence between notes)

[instrumental]
(Rhodes takes lead, jazz guitar accents, still sparse, breathing room)

[interlude]
(Jazz guitar solo, minimal drums, empty space, hunger in the gaps)

[instrumental]
(Rhodes and jazz guitar together, slightly fuller but still restrained)

[instrumental]
(Jazz guitar solo, Rhodes accents, upright bass groove, space between phrases)

[outro]
(Rhodes single notes, instruments thin to almost nothing, fade into silence)
```

### Style Prompt
```
Korean Chillhop, 78 BPM, E major

Jazz guitar-led, Rhodes accents. Upright bass warm defined. Soft jazzy drums, swing feel, laid-back groove. High-fidelity but warm, subtle saturation. Daylight mood, empty stomach feeling.

Sparse arrangement throughout. Lots of silence between notes. Empty space as texture. Notes floating in air. Minimalist, restrained, hungry. Less is more.

Purely instrumental. No vocals, no humming, no scat. No filler sounds.

Intro: Sparse, almost nothing.
Instrumental sections: Jazz guitar melody with gaps, Rhodes single notes, space between phrases.
Interlude: Minimal, breathing room.
Outro: Fade to near silence.

No vocal melody. No singing. Pure instruments only.
Target runtime over 3 minutes.
```

### Exclude
```
Dusty, Muffled, Lo-fi hiss, Vocals, Singing, Airy, Falsetto, Harmonized
```

---

## TODO

- [x] Track 01 가사/스타일 완료
- [x] Track 02 가사/스타일 완료
- [x] Track 03 스타일 완료 (딸 웃음소리 샘플 + D major)
- [x] Track 04 가사/스타일 완료 (바이닐 텍스처)
- [x] Track 05 스타일 완료 (pure instrumental, deep focus)
- [x] Track 06 가사/스타일 완료 (B타입 전환, bell chime 알림 컨셉)
- [x] Track 07 잉크 가사/스타일 완료 (B타입, E major)
- [x] Track 08 타이핑 가사/스타일 완료 (A→B타입 전환, 3줄 mantra)
- [x] Track 09 숨(Breathe) 스타일 완료 (B→C타입 전환, pure instrumental, D major)
- [x] Track 10 환기(Refresh) 스타일 완료 (C타입, pure instrumental, E major)
- [x] Track 11 회의 가사/스타일 완료 (B타입, 의성어 만트라)
- [x] Track 12 다시 스타일 완료 (C타입, finger snap texture)
- [x] Track 13 Tab 가사/스타일 완료 (A타입, 3줄 한 번)
- [x] Track 14 Tick Tock 스타일 완료 (C타입, clock rhythm)
- [x] Track 15 Hunger 스타일 완료 (C타입, sparse arrangement, E major)
- [x] CHILLHOP_RUBRIC.md 보컬 타입 대응 업데이트
- [ ] 썸네일 디자인 (10:00 시간 표기)
- [ ] Description 완성
- [ ] input/loop.mp4 준비
- [ ] input/thumb.jpg 준비
