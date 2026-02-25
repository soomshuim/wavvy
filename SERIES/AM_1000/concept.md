# AM_1000 — 업무시간

> **Korean Chillhop with Buried Vocals**
>
> Version: 0.4
> Last Updated: 2026-02-25
> Status: Track 01-02 완료

---

## Station Identity

| 항목 | 값 |
|------|-----|
| **시간** | 10:00 |
| **Station명** | 업무시간 |
| **감정톤** | 지속, 루틴, 차분 |
| **장르** | Korean Chillhop (buried vocals) |
| **용도** | 오전 업무/작업 중 배경음악 (집중 방해 X) |

---

## Direction

```
"한국어 가사 Chillhop, 보컬이 묻혀서 배경처럼 깔리는 업무용 음악"
```

- 가사가 있지만 악기 속에 묻혀서 텍스처처럼 작용
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

## Vocal Strategy (배경화 처리)

| 항목 | 값 |
|------|-----|
| **Persona 교대** | 홀수 트랙: Female (Alto) / 짝수 트랙: Male (Baritone) |
| **Processing** | Low in mix, buried, ambient reverb, soft |
| **가사 스타일** | 반복적, 단순, 명상적 (인지 부하 최소화) |
| **Articulation** | Soft, relaxed (명확한 발음 X → 배경화) |

### Vocal Mix 특수 지시

```
Vocals sit low in the mix, almost buried.
Soft, relaxed delivery. No clear articulation.
Ambient reverb, blending into instrumental texture.
Listener should feel vocals as texture, not foreground.
```

### Intro 제약 (시리즈 공통)

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

## Track List

| # | Title | Vocal | BPM | Key | Lead Instruments | Status |
|---|-------|-------|-----|-----|------------------|--------|
| 01 | 오전 | Female (Contralto) | 85 | D minor | Rhodes, Jazz Guitar | 완료 |
| 02 | 책상 | Male (Baritone) | 87 | E minor | Wurlitzer, Rhodes | 완료 |
| 03 | 루틴 | Female (Alto) | 90 | D minor | Jazz Guitar, Rhodes | 미정 |
| 04 | 흐름 | Male (Baritone) | 90 | E minor | Rhodes, Wurlitzer | 미정 |
| 05 | 집중 | Female (Alto) | 78 | D minor | Wurlitzer, Jazz Guitar | 미정 |
| 06 | 타자 | Male (Baritone) | 88 | E minor | Rhodes, Jazz Guitar | 미정 |
| 07 | 잠깐 | Female (Alto) | 85 | D minor | Jazz Guitar, Wurlitzer | 미정 |
| 08 | 다시 | Male (Baritone) | 82 | E minor | Rhodes, Wurlitzer | 미정 |
| 09 | 정리 | Female (Alto) | 85 | D minor | Wurlitzer, Rhodes | 미정 |
| 10 | 점심전 | Male (Baritone) | 78 | E minor | Jazz Guitar, Rhodes | 미정 |

### BPM 아크
```
85 → 87 → 90 → 90 → 78 → 88 → 85 → 82 → 85 → 78
                     ↑                         ↑
              Breathing Point              Release
```

---

## Track 01: 오전

### Lyrics
```
[intro]
(instrumental only, no vocals)
(Rhodes pad, soft jazzy drums fade in)

[verse1]
(buried vocal, low mix)
창문 너머 햇살이 비춰와
커피잔 위로 김이 흩어져
키보드 위 손끝이 멈춰도
시간은 계속 흘러

[chorus]
(soft, blending into instruments)
오전은 늘 이렇게
조용히 지나가
여기 앉아 있으면
그것만으로 돼

[interlude]
(Rhodes solo, upright bass groove)

[verse2]
(buried vocal, low mix)
모니터 빛이 얼굴에 닿아
마시던 커피 천천히 식어
의자에 기대 숨을 내쉬어도
하루는 계속 흘러

[chorus]

[bridge]
(minimal, almost whisper)
할 일은 쌓여 있고
손은 멈춰 있어
그래도 괜찮아
여기 있으니까

[chorus]

[outro]
(Rhodes restates motif softly, upright bass, fade out)
```

### Style Prompt
```
Korean Chillhop, 85 BPM, D minor

Rhodes-led, supportive. Jazz guitar accents. Upright bass, warm and defined. Crisp jazzy drums, swing feel, laid-back groove. High-fidelity but warm, subtle saturation.

Contralto female vocal. Soft, distant, recessed. Vocals buried deep in mix, underneath instruments. Heavy ambient reverb, far back in soundstage. Vocal as background texture, not lead.

Intro: Pure instrumental, absolutely no vocals, no humming, no vocalizations. Rhodes and drums only.
Verse: Rhodes carries melody, minimal accompaniment, soft vocal sits behind instruments.
Verse2: slight dynamic lift, natural breath, vocal remains buried.
Chorus: arrangement density increases, upright bass melodic, drums fill out. Vocal stays low in mix.
Bridge: stripped to Rhodes and bass, vocal almost whisper.
Outro: Rhodes restates motif softly, gentle fade.

Lead vocal remains single throughout. No harmony, no backing vocals, no doubles.
Chorus expansion by arrangement density only.

Target runtime over 3 minutes.
```

### Exclude
```
Dusty, Muffled, Lo-fi hiss, Prominent vocals, Forward vocals, Clear articulation, Airy, Falsetto, Harmonized, Backing vocals, Whisper, Auto-tune
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
#lofi #업무용음악 #집중 #playlist #soomshuim

🎵 Music: soomshuim
Copyright Ⓒ soomshuim. All rights reserved.

All tracks feature Korean lyrics.
```

### Pinned Comment
```
이 채널의 노래들은 모두 우리말 가사로 만들었어요.
지금 당신의 이 시간이 더 천천히, 더 깊게 닿기를 바랍니다.

오늘 하루, 무엇이 당신을 책상 앞에 앉게 했나요?
```

---

## Track 02: 책상

### Lyrics
```
[intro]
(instrumental only, no vocals, no humming, no ad-libs)
(Wurlitzer pad, Rhodes accents, crisp jazzy drums fade in)

[verse1]
(buried vocal, low mix, no filler sounds)
의자를 당겨 앉아
모니터 불빛 켜져
마우스 위에 손을 올려
하루가 시작돼

커피 향이 번지고
창문 너머 햇살이
책상 위를 비춰와
오늘도 여기서

[chorus]
(blending into instruments, no ad-libs)
여기 내 자리야
매일 앉는 곳
손끝이 기억해
이 책상 위를

[interlude]
(Wurlitzer solo, upright bass groove, 8 bars)

[instrumental]
(Rhodes pad, drums groove, 8 bars)

[verse2]
(buried vocal, low mix, no filler sounds)
키보드 소리 울려
화면이 밝아지고
펜을 하나 집어서
오늘 할 일 적어

포스트잇 한 장 붙여
달력을 한 번 보고
시간은 천천히
앞으로 흘러가

[chorus]

[bridge]
(minimal, no ad-libs, no humming)
창밖은 여전하고
시간은 흘러가
그래도 여기 있어
이 자리 위에

[chorus]

[outro]
(Wurlitzer restates motif, scat vocal allowed here only, gentle fade)
```

### Style Prompt
```
Korean Chillhop, 87 BPM, E minor

Wurlitzer-led, Rhodes accents. Upright bass warm defined. Crisp jazzy drums, swing feel, fresh groove. High-fidelity, polished. Morning energy.

Baritone male vocal buried deep in mix, underneath instruments. Heavy ambient reverb, far back. Vocal as texture, not lead.

CRITICAL: No filler sounds, no "eh" "uh" "hm" ad-libs. No humming no scat except outro. Clean lines only.

Intro: Instrumental only, no vocals. Wurlitzer drums only.
Verse: Wurlitzer melody, vocal behind instruments. No fillers.
Interlude: Wurlitzer solo 8 bars, bass groove.
Instrumental: Rhodes pad drums 8 bars.
Chorus: density increases, bass melodic. Vocal low. No embellishments.
Bridge: Wurlitzer bass only, vocal minimal.
Outro: Wurlitzer motif, scat allowed here only, fade.

Single vocal throughout. No harmony no backing no doubles.
Target runtime over 3 minutes 30 seconds.
```

### Exclude
```
Dusty, Muffled, Lo-fi hiss, Prominent vocals, Forward vocals, Clear articulation, Airy, Falsetto, Harmonized, Backing vocals, Whisper, Auto-tune, Filler sounds, Ad-libs, Humming, Scat, Vocal runs, Melisma, Drowsy, Sleepy, Lazy
```

---

## TODO

- [x] Track 01 가사/스타일 완료
- [x] Track 02 가사/스타일 완료
- [ ] Track 03-10 가사/스타일 기획
- [ ] 썸네일 디자인 (10:00 시간 표기)
- [ ] Description 완성
- [ ] input/loop.mp4 준비
- [ ] input/thumb.jpg 준비
