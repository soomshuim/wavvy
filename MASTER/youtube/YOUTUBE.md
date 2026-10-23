# YouTube Metadata (SSOT)

Version: 2.4
Last Updated: 2026-10-23
Purpose: YouTube 제목/설명/태그 통합 규칙

> 장르 상세: `MASTER/reference/GENRES.md`

---

## 1. 제목 구조

```
Playlist | {감정 훅 + 이모지} | {장르1} · {장르2} | {음악에 맞는 용도들} | Wavvy | {HH}:{MM}
```

| 순서 | 요소 | 예시 |
|------|------|------|
| 1 | 콘텐츠 타입 | `Playlist` (고정) |
| 2 | 감정 훅 + 이모지 | `잠든 몸을 깨우는 새벽 🌅` |
| 3 | 장르 (대문자) | `FAST LO-FI · CHILLHOP` |
| 4 | 용도 | `카페 · 산책 · 작업 · 드라이브 · 노동요`처럼 음악에 맞는 여러 상황 |
| 5 | 브랜드 | `Wavvy` (고정) |
| 6 | 시리즈 시간 | `06:00` (24시간, 맨 끝) |

**구분자:** `|` (섹션), `·` (항목)

- 제목 앞부분은 클릭하기 전 듣는 이유와 음악의 성격을 알 수 있게 쓴다. 시간은 시리즈 식별 정보이므로 마지막에 둔다. `Wavvy 07:00`처럼 붙이지 않고 `Wavvy | 07:00`으로 구분한다.
- **기본 작성 방향:** 감정 훅은 해당 시리즈의 이미지·일상에서 떠오르는 구체적인 감각이나 비유와 실제 음악의 느낌을 짧고 자연스럽게 연결한다. `기분전환 · 드라이브` 같은 일반 용도 나열만으로 훅을 대신하지 않는다. 공개 레퍼런스는 표현 방식을 참고하되 문구를 그대로 복제하지 않는다. 아래 17:30의 `오렌지`는 그 시리즈에 맞는 예시이며 다른 시리즈에 고정하지 않는다.
- 용도 칸은 두 개로 제한하지 않는다. 음악과 맞는 상황만 고르고, 제목 길이가 허용하면 `카페 · 산책 · 작업 · 드라이브 · 노동요`처럼 폭넓게 보여준다. 각 시리즈의 실제 장르·분위기·사용 상황과 맞지 않는 항목은 넣지 않는다. 장르 칸도 확인된 음악 사실을 보존한다.
- 장르와 용도는 기본 제목 구조에서 유지한다. 기존 제목은 젠이 별도로 승인하지 않는 한 문구를 바꾸거나 장르·용도를 빼지 않고 시리즈 시간의 위치만 옮긴다.
- 젠이 승인한 개별 제목에는 다른 음악 정보를 사용할 수 있다. 07:00의 `180 BPM Running Mix · 2Hour`가 그 사례다. BPM·재생 시간은 해당 영상에 맞는 정보만 표기하며, 실제 길이와 다른 재생 시간 표기는 젠이 해당 제목을 승인했을 때만 쓴다.
- 여섯 구획은 **새 제목을 쓰는 기본형**이다. 이미 승인된 07:00의 다섯 구획 제목과 시간대가 없는 컴필레이션 제목은 그대로 유효하다. 기본형 도입만을 이유로 기존 승인 제목을 다시 작성하거나 게시된 영상을 수정하지 않는다.
- YouTube Studio의 100자 한도를 넘기지 않는다. 긴 설명이나 반복되는 키워드를 늘어놓기보다 한 번에 읽히는 훅과 핵심 정보로 줄인다.
- `verify-release`는 제목의 100자 한도, 빈 구획, `Playlist`·`Wavvy` 위치, 시간대 시리즈의 시각 일치만 기계 검사한다. 감각적 이미지와 음악의 연결, 장르의 사실성, 용도의 적합성은 `concept.md`와 실제 선택 음악을 보고 발행 전에 판단한다.
- 시간대가 없는 컴필레이션은 임의의 시각을 만들지 않는다. 별도의 시리즈 이름이 있으면 `Wavvy | {시리즈 이름}`으로 끝낼 수 있다.
- 기존 영상 제목을 수정할 때는 Studio의 현행 제목과 해당 시리즈의 `concept.md`를 먼저 확인하고, 영상별 **최종 제목 전체**를 젠에게 먼저 보여준다. 젠이 승인한 제목만 Studio에 저장한다. 일괄 수정은 전체 영상별 대응표를 먼저 보여주고 한 번에 승인받을 수 있다.

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

아래는 기존 시리즈의 참고 사례다. 새 제목의 이모지는 시간만으로 고정하지 않고 해당 시리즈의 감각적 이미지와 음악에 맞춰 고른다(17:30의 🍊, 07:00의 🏃처럼).

| 시간 | 이모지 | 시간 | 이모지 |
|------|--------|------|--------|
| 04:00 | 🌙 | 14:00 | ☀️ |
| 06:00 | 🌅 | 16:00 | 🎸 |
| 10:00 | ☕ | 18:00 | 🚶 |
| 11:00 | 🎯 | 21:00 | 🌙 |
| 12:00 | 🍽️ | 13:00 | 🌸 |
| 15:00 | 🕶️ | 20:00 | 💪 |
| 22:00 | 🌙 | | |

---

## 4. 제목 예시

**대표 베스트 사례 · 기본 작성 방향 (17:30, 젠이 전체 제목 승인):**

```
Playlist | 오렌지 한 입처럼 산뜻한 그루브 🍊 | MODERN R&B · NEO SOUL | 카페 · 산책 · 작업 · 드라이브 · 노동요 | Wavvy | 17:30
```

구체적 감각 비유와 음악 느낌을 훅으로 연결하고, 음악에 맞는 여러 용도를 100자 안에서 보여주는 사례다. 다른 시리즈에서는 그 시리즈의 이미지와 음악에 맞는 내용으로 새로 쓴다.

**기존 개별 제목 사례:**

```
Playlist | 상쾌하게 달릴 준비 됐나요?! 🏃 | 180 BPM Running Mix · 2Hour | Wavvy | 07:00
Playlist | 조용히 몰입하는 시간 ☕ | CHILLHOP · JAZZHOP | 집중 · 작업 | Wavvy | 10:00
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
| 11-00 | Classic Lo-fi | classic lofi, lofi hip hop, jazzhop, 클래식로파이, 딥워크 | #classiclofi #로파이 #딥워크 #몰입 |
| 12-00 | Korean Afrobeats | afrobeats, afropop, korean afrobeats, 아프로비츠, 점심플리 | #afrobeats #아프로비츠 #점심플리 |
| 13-00 | Feel Good R&B / Urban Neo-Soul | feel good rnb, urban neo soul, neo soul, r&b, 봄플리, 산책음악, 드라이브음악 | #feelgoodrnb #urbanneosoul #봄플리 #산책음악 |
| 14-00 | Soft R&B | soft rnb, r&b, 소프트알앤비, 카페음악 | #softrnb #알앤비 #카페음악 |
| 15-00 | Funky R&B / Urban Neo-Soul | funky rnb, urban neo soul, neo soul, drive music, 드라이브, 봄 | #funkyrnb #urbanneosoul #드라이브음악 #봄플리 |
| 16-00 | 감성 락 | korean rock, indie rock, 감성락 | #koreanrock #감성락 #드라이브 |
| 18-00 | Neo-Soul | neo soul, 네오소울, 퇴근길 | #neosoul #네오소울 #퇴근길 |
| 20-00 | Korean Hip-Hop / Trap / Rage / Drill | korean hip hop, korean trap, rage trap, k-drill, workout music, 운동bgm | #KoreanHipHop #Trap #RageTrap #KDrill #운동BGM |
| 21-00 | 시티팝 | city pop, 시티팝, 뉴트로, 밤감성 | #citypop #시티팝 #밤감성 |
| 22-00 | Chill R&B / Ambient Slow Jam | chill rnb, ambient slow jam, acoustic chill rnb, 수면음악, 릴랙스 | #chillrnb #slowjam #수면음악 #릴랙스 |

**공통:** `playlist, 플리, korean lyrics, 한국어가사, wavvy, 웨이비`

시리즈 `concept.md`에 명시된 YouTube Metadata가 있으면 그 섹션이 해당 시리즈의 최종 업로드 문안이다. 위 표는 새 Draft 작성과 장르 혼동 방지용 기본값이다.

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

🎵 Music: Wavvy
Copyright Ⓒ Wavvy. All rights reserved.
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

---

## 9. 메타데이터 생성 워크플로우

### 9.1 Phase 1: 시리즈 초기 생성 (Draft)

**시점:** 시리즈 폴더 + concept.md 최초 생성 시

**필수 요청 (유저에게):**
1. Context Mode (Settling/Transition/Energizing/Focusing)
2. 감정 훅 키워드 또는 방향
3. 고정 댓글 훅 아이디어

**작성 내용 (Track List 외 전부 초안):**
- 제목 (템플릿 기반, 장르/용도)
- 설명 인트로 (2줄 훅 + 확장 훅)
- 해시태그/태그 (시리즈 장르 매핑 참조)
- 고정 댓글 초안
- 아웃트로 (고정 템플릿)

**Track List:** `(트랙 완성 후 추가)` placeholder

**버전 태그:** `## YouTube Draft (v1 — 트랙 미완성)`

**⚠️ 유저 요청 없이 임의 생성 금지 — 필수 요청 항목 먼저 확인**

### 9.2 Phase 2: 시리즈 완성 (Final)

**시점:** 모든 트랙 PASS + 패키징 완료 시

**업데이트:**
1. Track List에 실제 타임스탬프 + 곡명 + 이모지
2. 버전 태그 변경: `(v1 — 트랙 미완성)` → `(v2.1)`
3. 해시태그/태그 최종 검토
4. 장르 태그 매핑 테이블 참조 (§6)
5. `python3 wavvy.py finalize-upload SERIES/[시리즈] --check` → PASS 후 `python3 wavvy.py finalize-upload SERIES/[시리즈]`

**⚠️ 설명 작성 전 필수: 기존 시리즈 설명 참조**
- 최소 2개 시리즈의 `concept.md > YouTube Metadata > 설명` 확인
- 톤/길이/구조 맞추기: 2줄 훅 + 장면 묘사 6-8줄 + Wavvy 클로징
- 장면 묘사는 해당 시간대의 구체적 행동/감각을 시간순으로 나열

**Final Track Sources:** 업로드 FINAL 단계에서는 `input/tracks/*.txt`의 제목/스타일/EXCLUDE/풀가사를 `concept.md > Final Track Sources`로 병합한다. 이 섹션이 완전해야 txt 삭제가 허용되며, 이후 자막/아카이브 작업은 concept.md의 Final Track Sources를 기준으로 한다.

### 9.3 장르 혼동 방지 체크

1. **concept.md 헤더**에서 장르 확인
2. §6 시리즈별 태그 매핑 참조
3. 제목/태그에 정확한 장르 반영

**⚠️ 장르 태그 매핑 확인 없이 메타데이터 작성 금지**
