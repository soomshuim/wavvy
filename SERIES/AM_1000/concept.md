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
| **A** | 한 섹션만 보컬 (4-8줄), 나머지 인스트루멘탈 | 4 트랙 |
| **B** | 1-2줄 반복 (만트라/루프) | 5 트랙 |
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
| 02 | 책상 | A | Male (Baritone) | 87 | Em | Wurlitzer, Rhodes | 완료 |
| 03 | 루틴 | C | — (웃음소리 샘플) | 90 | D major | Jazz Guitar, Rhodes | 완료 |
| 04 | 흐름 | B | Male (Baritone) | 90 | Em | Rhodes, Wurlitzer | 완료 |
| 05 | 집중 | C | — | 78 | Dm | Wurlitzer, Jazz Guitar | 미정 |
| 06 | 알림 | C | — | 83 | Em | Rhodes, Jazz Guitar | 미정 |
| 07 | 타자 | A | Female (Alto) | 88 | Dm | Rhodes, Jazz Guitar | 미정 |
| 08 | 잉크 | B | Male (Baritone) | 85 | Em | Jazz Guitar, Wurlitzer | 미정 |
| 09 | 잠깐 | B | Female (Alto) | 85 | Dm | Jazz Guitar, Wurlitzer | 미정 |
| 10 | 환기 | C | — | 80 | Em | Rhodes, Wurlitzer | 미정 |
| 11 | 회의 | B | Male (Baritone) | 87 | Dm | Wurlitzer, Rhodes | 미정 |
| 12 | 다시 | C | — (스캣) | 82 | Em | Rhodes, Wurlitzer | 미정 |
| 13 | 정리 | A | Male (Baritone) | 85 | Dm | Wurlitzer, Rhodes | 미정 |
| 14 | 벽시계 | A | Female (Alto) | 80 | Em | Jazz Guitar, Rhodes | 미정 |
| 15 | 점심전 | C | — | 78 | Dm | Jazz Guitar, Rhodes | 미정 |

### Type 배분
```
A (한 섹션 보컬): Track 02, 07, 13, 14
B (만트라/루프):  Track 01, 04, 08, 09, 11
C (인스트루멘탈): Track 03, 05, 06, 10, 12, 15
```

### BPM 아크
```
85 → 87 → 90 → 90 → 78 → 83 → 88 → 85 → 85 → 80 → 87 → 82 → 85 → 80 → 78
                      ↑              ↑                    ↑              ↑
                 Breathing       Recovery            2nd Wave        Wind Down
```

### 서사 아크 (오전 업무 동선)
```
오전(시작) → 책상(자리) → 루틴(일상) → 흐름(몰입) → 집중(깊이)
→ 알림(중단) → 타자(리듬) → 잉크(필기) → 잠깐(쉼) → 환기(전환)
→ 회의(이동) → 다시(복귀) → 정리(마무리) → 벽시계(응시) → 점심전(끝)
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
Dusty, Muffled, Lo-fi hiss, Prominent vocals, Forward vocals, Airy, Falsetto, Harmonized
```

## Track 02: 책상

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
서랍이 안 닫혀
끼인 게 뭔지 몰라
꺼내지도 않고
그냥 밀어 넣어

[instrumental]
(Wurlitzer lead, Rhodes pad, upright bass groove)

[interlude]
(jazz guitar solo, soft drums, breathing space)

[instrumental]
(full arrangement, Wurlitzer and Rhodes together)

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
Verse: brief buried vocal, four lines only, then instruments continue.
Outro: Wurlitzer restates motif, gentle fade.

Single vocal throughout. No harmony no backing no doubles.
Target runtime over 3 minutes.
```

### Exclude
```
Dusty, Muffled, Lo-fi hiss, Prominent vocals, Forward vocals, Airy, Falsetto, Harmonized
```

---

## Track 03: 루틴

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

## Track 04: 흐름

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
Dusty, Muffled, Lo-fi hiss, Prominent vocals, Forward vocals, Airy, Falsetto, Harmonized
```

---

## TODO

- [x] Track 01 가사/스타일 완료
- [x] Track 02 가사/스타일 완료
- [x] Track 03 스타일 완료 (딸 웃음소리 샘플 + D major)
- [x] Track 04 가사/스타일 완료 (바이닐 텍스처)
- [ ] Track 05-15 가사/스타일 리디자인 (A/B/C 타입)
- [x] CHILLHOP_RUBRIC.md 보컬 타입 대응 업데이트
- [ ] 썸네일 디자인 (10:00 시간 표기)
- [ ] Description 완성
- [ ] input/loop.mp4 준비
- [ ] input/thumb.jpg 준비
