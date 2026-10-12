# 12:00 Korean Afrobeats

Version: 5.1
Last Updated: 2026-03-21

---

## Series DNA

- **정체성**: 한국어 가사 × Afrobeats 리듬/구조
- **시간대**: 정오(12:00) — 점심시간이라는 배경 설정
- **테마**: 제한 없음 — 사랑, 그리움, 후회, 이별, 여유, 축제 모든 감정 허용
- **톤**: 트랙별 자유. 점심시간 배경 연결 권장 (필수 아님)
- **가사**: Suno 자체 작사 (작사 프롬프트 또는 비움). Style에 보컬 지시 유지
- **보컬**: Female 60% / Male 37% / Inst 5% (F12:M7:Inst1), Chest voice
- **금지**: 시티팝 표현 문법 → `LYRICS_DNA.md` §6 (프롬프트 작성 시 참고)
- **20트랙 / 80분+**

---

## Style Templates

> 각 템플릿 900자 이하. `STYLE.md` Writing Formula 7요소 + Afrobeats 특화.
> Harmony Guard + Energy Permission 필수 포함.

### Style C — Minimal Afro

```
Articulation. Korean Afrobeats, minimal production, {BPM} BPM, {Key},
sparse arrangement, vocal-forward mix,
soft shaker, light congas, subtle cowbell, minimal hi-hat,
808 bass groove locked with kick, restrained low-end,
Female vocal: Raw, Intimate, Chest voice, Dry, articulation,
call-and-response chorus, 1-2 bar repeating hook,
intentional and restrained, wide stereo, open space,
moderate reverb, room ambience, EQ balanced sound, clean mix.
Lead vocal remains single and dominant throughout. No stacked or choir-like harmonies.
Vocal line may intensify dynamically (belt, higher register), but no additional vocal layers.
Chorus vocal may be delivered with stronger intensity or light belt.
Higher register emphasis is encouraged. Natural vocal strain allowed.
```

### Style D — Afropiano

```
Articulation. Korean Afrobeats, Afropiano, {BPM} BPM, {Key},
log drum groove, warm jazzy piano chords, rolling percussion,
trap hi-hats, shaker rhythm, rimshot snare,
808 bass groove locked with kick, deep low-end,
Female vocal: Raw, chant-style, Chest voice, Dry, articulation,
call-and-response chorus, repetitive hook chant,
moody spacious mix, wide stereo, deep groove,
moderate reverb, room ambience, EQ balanced sound, clean mix.
Lead vocal remains single and dominant throughout. No stacked or choir-like harmonies.
Vocal line may intensify dynamically (belt, higher register), but no additional vocal layers.
Chorus vocal may be delivered with stronger intensity or light belt.
Higher register emphasis is encouraged. Natural vocal strain allowed.
```

### Style E — Afro-Drill

```
Articulation. Korean Afrobeats, Afro-Drill, {BPM} BPM, {Key},
808 slide bass, snappy rimshot snare, trap hi-hat rolls,
syncopated African percussion, dark moody melody,
deep bass, shaker, minimal cowbell,
Female vocal: Raw, rhythmic chanting, Chest voice, Dry,
percussive articulation, repetitive hook,
aggressive cadence, wide stereo, dark spacious mix,
moderate reverb, room ambience, EQ balanced sound, clean mix.
Lead vocal remains single and dominant throughout. No stacked or choir-like harmonies.
Vocal line may intensify dynamically (belt, higher register), but no additional vocal layers.
Chorus vocal may be delivered with stronger intensity or light belt.
Higher register emphasis is encouraged. Natural vocal strain allowed.
```

### Exclude Template (공통)

```
autotune heavy, vocoder, EDM drops, big room,
choir, stacked harmonies, backing vocal layers, doubled vocals,
kalimba
```

---

## Track Map (20트랙)

| # | 제목 | Style | BPM | Key | Vocal | 상태 |
|---|------|-------|-----|-----|-------|------|
| 01 | 한낮 (Haze) | E | 105 | C Major | F | ✅ PASS |
| 02 | 먼지 (Dust) | E | 105 | C Major | F | ✅ PASS |
| 03 | 볕 (Sunlit) | D | 108 | D Major | M | ✅ PASS |
| 04 | 무음 (Mute) | D | 110 | F Minor | F | ✅ PASS |
| 05 | 갈증 (Thirst) | E | 104 | Ab Major | F | ✅ PASS |
| 06 | 낮 그림자 (Noon Shadow) | E | 107 | Bb Minor | M | ✅ PASS |
| 07 | 낮꿈 (Daydream) | E | 102 | Db Major | F | ✅ PASS |
| 08 | 차가워진 (Cold At Noon) | D | 112 | E Minor | M | ✅ PASS |
| 09 | 맥박 (Pulse) | E | 106 | F# Major | F | ✅ PASS |
| 10 | 잔상 (Afterimage) | E | 108 | A Minor | M | ✅ PASS |
| 11 | 그늘 (Shade) | E | 100 | B Major | Inst | ✅ PASS |
| 12 | 기다림 (Waiting) | D | 105 | D Minor | F | ✅ PASS |
| 13 | 정오의 균열 (Midday Crack) | E | 110 | Eb Minor | M | ✅ PASS |
| 14 | 설렘 (Flutter) | E | 104 | G Major | F | ✅ PASS |
| 15 | 온기 (Warmth) | E | 107 | A Major | F | ✅ PASS |
| 16 | 미열 (Low Fever) | D | 103 | F# Minor | F | ✅ PASS |
| 17 | 진동 (Vibration) | E | 109 | C Minor | M | ✅ PASS |
| 18 | 얼룩 (Stain) | E | 102 | Db Major | F | ✅ PASS |
| 19 | 폭발 (Burst) | E | 111 | B Minor | M | ✅ PASS |
| 20 | 고요 (Stillness) | D | 100 | F Major | Inst | ✅ PASS |

### 배분 규칙
- **BPM**: 100-112 (Hard Gate H1)
- **Key**: Major 11 : Minor 9 (55:45), 인접 트랙 같은 Key 금지
- **Style**: E 14 : D 6 (70:30)
- **Vocal**: Female 12 : Male 7 : Inst 1 (60:37:5)

---

## Song Structure

### 기본 구조 (V-P-C-V-C-B-C + Post-chorus)

```
[intro]
(프로듀서 태그 구간, 4-8마디)

[verse 1]
(Chest voice, Direct)

[pre-chorus]
(building energy)

[chorus]
(belt)

[post-chorus]
(chant, call-and-response ad-lib)

[verse 2]
(Chest voice, Direct)

[chorus]

[bridge]
(higher register, stronger dynamics)

[chorus]

[outro]
(instrumental fade)
```

> 가사는 Suno 자체 생성. 필요 시 LYRICS.md §1 Lyric Prompt Guide 참조하여 mood/theme 힌트 추가.

### 대안 구조 (C-V-C-V-C)

훅이 특별히 강한 트랙에 사용. 코러스 선행.

---

## Vocal Persona

| Style | 보컬 |
|-------|------|
| C (Minimal) | Female: Raw, Intimate, Chest voice |
| D (Afropiano) | Female: Raw, Chant-style, Chest voice |
| E (Afro-Drill) | Female: Raw, Rhythmic chanting, Chest voice |

---

## References

> 상세: `reference/` 폴더

### 레퍼런스 트랙 (BPM/Key 맵)

| 곡 | 아티스트 | BPM | Key | 참고 포인트 |
|---|---------|-----|-----|-----------|
| Calm Down | Rema | 107 | B Major | 글로벌 훅, 심플 코드 |
| Essence | Wizkid ft. Tems | 104 | C Major | 스무스 듀엣, 여름 바이브 |
| Rush | Ayra Starr | 100 | Db Major | 여성 보컬 파워 |
| FEEL | Davido | 112 | D Major | 밝은 에너지 |
| Love Nwantiti | CKay | 93 | G# Major | Afro-fusion 감성 *(범위 밖 — 훅 구조 참고용)* |
| Last Last | Burna Boy | 88 | Eb Minor | 감성 Afrobeats *(범위 밖 — 감성 톤 참고용)* |

### 리서치 소스
- `reference/00-synthesis.md` — 종합 (GPT + Agent + Lenny Team)
- `reference/01-gpt-deep-research.md` — 화성·멜로디·구성
- `reference/02-agent-deep-research.md` — 리듬·악기·가사·트렌드·Suno
- `LYRICS_DNA.md` — 작사 프롬프트 DNA (리서치 증류본)
- `report/2026-03-13_afrobeats-lyrics-deep-research.md` — 가사 딥리서치 원본

---

## YouTube Metadata (v2.1)

### 제목
```
Playlist | 4K 리듬 맛집 🍽️ | KOREAN AFROBEATS · AFRO-DRILL | 점심플리 · 작업 | Wavvy | 12:00
```

### Context Mode
Energizing — 점심시간 에너지 전환, 리듬 기반 각성

### 설명
```
🍽️ 12:00, 오늘의 메뉴는 아프로비츠.
점심시간 리듬 맛집 - Wavvy

자리에서 일어나 엘리베이터를 타고,
밖으로 나서면 햇볕이 얼굴을 때리고,
이어폰을 끼는 순간 발걸음에 리듬이 붙어요.
줄 서서 기다리는 동안에도, 숟가락을 내려놓은 뒤에도,
다시 사무실로 돌아가는 길에도,
점심시간이 끝나지 않은 것처럼.

Wavvy는 우리말 가사로, 그 시간들의 감정을 기록합니다.
──────────────
Track List
🎵 00:00 - 한낮 (Haze)
🎵 01:59 - 먼지 (Dust)
🎵 04:00 - 볕 (Sunlit)
🎵 06:39 - 무음 (Mute)
🎵 09:23 - 갈증 (Thirst)
🎵 11:00 - 낮 그림자 (Noon Shadow)
🎵 14:07 - 낮꿈 (Daydream)
🎵 17:37 - 차가워진 (Cold At Noon)
🎵 20:53 - 맥박 (Pulse)
🎵 23:19 - 잔상 (Afterimage)
🎵 26:24 - 그늘 (Shade)
🎵 28:00 - 기다림 (Waiting)
🎵 30:47 - 정오의 균열 (Midday Crack)
🎵 33:30 - 설렘 (Flutter)
🎵 36:00 - 온기 (Warmth)
🎵 38:18 - 미열 (Low Fever)
🎵 40:48 - 진동 (Vibration)
🎵 43:22 - 얼룩 (Stain)
🎵 46:08 - 폭발 (Burst)
🎵 48:34 - 고요 (Stillness)
──────────────
Music for your space, 24 hours a day.
All tracks feature Korean lyrics.

🎵 Music: wavvy
Copyright Ⓒ wavvy. All rights reserved.
──────────────
#afrobeats #아프로비츠 #점심플리 #koreanafrobeats #playlist #플리 #노동요 #집중음악 #wavvy #웨이비
```

### 태그
```
afrobeats, afropop, korean afrobeats, afro-drill, afropiano, 아프로비츠, 점심플리, 점심음악, 노동요, 집중음악, playlist, 플리, korean lyrics, 한국어가사, wavvy, 웨이비
```

### 고정 댓글
```
오늘 점심, 뭐 드셨어요? 🍽️
리듬이랑 같이 소화시키는 중 🎵
```

### Pack 정보
- **Duration**: 102.7분 (20곡 x2)
- **Video**: 팔린드롬 루프 (밀림 젬베 + god rays)
- **Audio**: -14 LUFS, 0.8s acrossfade
- **Status**: ✅ PACK COMPLETE (2026-03-21)
