# YouTube Metadata (SSOT)

Version: 2.0
Last Updated: 2026-03-04
Purpose: YouTube 제목/설명/태그 통합 규칙

> 장르 상세: `reference/GENRES.md`

---

## 1. 제목 구조

```
Playlist | {HH}:{MM} | {감정 훅 + 이모지} | {장르1} · {장르2} | {용도1} · {용도2} | Wavvy
```

| 순서 | 요소 | 예시 |
|------|------|------|
| 1 | 콘텐츠 타입 | `Playlist` (고정) |
| 2 | 시간 | `06:00` (24시간) |
| 3 | 감정 훅 + 이모지 | `잠든 몸을 깨우는 새벽 🌅` |
| 4 | 장르 (대문자) | `FAST LO-FI · CHILLHOP` |
| 5 | 용도 | `러닝 · 모닝루틴` |
| 6 | 브랜드 | `Wavvy` (고정) |

**구분자:** `|` (섹션), `·` (항목)

---

## 2. Context Mode (제목 생성 전 필수)

| Mode | 설명 | 허용 | 금지 |
|------|------|------|------|
| Settling | 가라앉힘 | 차분한, 느긋한 | 신나는 |
| Transition | 전환 | 부드러운, 가볍게 | 극단 표현 |
| Energizing | 에너지 | 신나는, 경쾌한 | - |
| Focusing | 집중 | 집중되는, 또렷한 | 고각성 |

---

## 3. 시간대별 이모지

| 시간 | 이모지 | 시간 | 이모지 |
|------|--------|------|--------|
| 04:00 | 🌙 | 14:00 | ☀️ |
| 06:00 | 🌅 | 16:00 | 🎸 |
| 10:00 | ☕ | 18:00 | 🚶 |
| 21:00 | 🌙 |  |  |

---

## 4. 제목 예시

```
Playlist | 06:00 | 잠든 몸을 깨우는 새벽 🌅 | FAST LO-FI · CHILLHOP | 러닝 · 모닝루틴 | Wavvy
Playlist | 10:00 | 오늘도 조용히 시작하는 중 ☕ | CHILLHOP · JAZZHOP | 집중 · 작업 | Wavvy
```

---

## 5. SEO 우선순위

| 순위 | 카테고리 | 예시 |
|------|---------|------|
| 1 | 영문 장르 | lofi, chillhop, rnb |
| 2 | 용도 Long-tail | study music, work music |
| 3 | 한글 장르 | 로파이, 칠홉, 알앤비 |
| 4 | 한글 용도 | 노동요, 집중음악 |
| 5 | 브랜드 | wavvy, 웨이비 |

---

## 6. 시리즈별 태그

| 시리즈 | 장르 | Studio 태그 | 해시태그 |
|--------|------|-------------|----------|
| 04-00 | Slow R&B | slow rnb, r&b, 슬로우알앤비, 새벽감성 | #slowrnb #알앤비 #새벽감성 |
| 06-00 | Fast Lo-fi | fast lofi, lofi, 패스트로파이, 노동요 | #fastlofi #로파이 #노동요 |
| 10-00 | Chillhop | chillhop, lofi, jazzhop, 칠홉, 노동요 | #chillhop #칠홉 #노동요 |
| 14-00 | Soft R&B | soft rnb, r&b, 소프트알앤비, 카페음악 | #softrnb #알앤비 #카페음악 |
| 16-00 | 감성 락 | korean rock, indie rock, 감성락 | #koreanrock #감성락 #드라이브 |
| 18-00 | Neo-Soul | neo soul, 네오소울, 퇴근길 | #neosoul #네오소울 #퇴근길 |
| 21-00 | 시티팝 | city pop, 시티팝, 뉴트로, 밤감성 | #citypop #시티팝 #밤감성 |

**공통:** `playlist, 플리, korean lyrics, 한국어가사, wavvy, 웨이비`

---

## 7. 설명 구조

```
{EMOJI} {HH}:{MM}, {TIME_HOOK_SHORT}
{BRAND_MESSAGE} - Wavvy

{EXTENDED_HOOK}
Wavvy는 우리말 가사로, 그 시간들의 감정을 기록합니다.
──────────────
Track List
{EMOJI} 00:00 - {TRACK_01}
{EMOJI} MM:SS - {TRACK_02}
...
──────────────
Music for your space, 24 hours a day.
All tracks feature Korean lyrics.

🎵 Music: wavvy
Copyright Ⓒ wavvy. All rights reserved.
──────────────
{해시태그}
```

> 첫 타임스탬프 `00:00` 필수 (YouTube 챕터 활성화)
> 60분 이상: `HH:MM:SS` 형식 필수 (예: `01:03:45`)
> 구분선: 14개 대시 (`─`)

---

## 8. 해시태그 Tier

| Tier | 목적 | 예시 |
|------|------|------|
| 장르 | 스타일 | #chillhop #lofi |
| 용도 | TPO | #노동요 #집중 |
| 발견 | 채널 | #playlist #플리 |
| 브랜드 | 고유 | #wavvy #웨이비 |
