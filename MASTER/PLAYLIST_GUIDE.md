# Wavvy PLAYLIST_GUIDE.md
Version: 1.3
Last Updated: 2026-02-16
Purpose: 플레이리스트 컨셉 설계 시 참고하는 인기 사례 분석 가이드
Source: Reference/유튜브 감성 플레이리스트 인기 사례 분석.pdf

---

## 0. Playlist Title Generation Rules (SSOT v1.6) — Wavvy

> **이 섹션이 Wavvy 채널의 공식 타이틀 규칙이다. Section 1은 참고 패턴일 뿐.**

### Fixed Title Structure (DO NOT CHANGE ORDER)
```
[Playlist] [HH:MM] Wavvy | {TIME_STATE_PHRASE}, {MODIFIER_PHRASE} {GENRE}
```

---

### Fixed Tokens (Must be used exactly)
- `[Playlist]` must be included at the beginning.
- Channel name must be exactly: `Wavvy`
- Handle: `@wavvy24`
- Time must be formatted as:
  - `[HH:MM]` (24-hour clock, 00–23)
- Separator must be a vertical bar: `|`

---

### REQUIRED INPUT (Before Generation)

#### Context Mode (Mandatory)
Context Mode MUST be explicitly defined before title generation.
The model MUST NOT infer Context Mode implicitly.

Choose ONE:
- **Settling Mode** (가라앉힘 / 정리)
- **Transition Mode** (전환 / 이동)
- **Energizing Mode** (에너지 부여)
- **Focusing Mode** (집중)

Context Mode determines modifier and emotion/energy word allowance.

---

### Variable Slots & Rules

#### 0.1 {TIME_STATE_PHRASE} (Primary Subject — Mandatory)
- Describes a **time-based internal or perceptual state**.
- Time must always remain the **main subject** of the title.
- Must NOT describe tasks or genres directly.

Choose ONE type only:

**Type A — Poetic / Abstract**
- 하루가 멈춘 시간
- 잠들지 못한 시간
- 하루를 풀어내는 시간
- 다시 움직이기 전의 시간

**Type B — Perceptual / Observable**
- 소리가 낮아진 시간
- 움직임이 느려진 시간
- 주변이 바빠지기 전의 시간
- 빛이 바뀌는 시간

**Operational Rule:**
- Alternate Type A and Type B across consecutive uploads to avoid tonal repetition.

**Prohibited:**
- Task-only phrases (공부, 작업 단독 사용 금지)
- Emotion-only phrases (신나는, 설레는 단독 사용 금지)

---

#### 0.2 {MODIFIER_PHRASE} (Secondary Modifier)
- Supports the time state with flow, task context, or energy level.
- Must always follow {TIME_STATE_PHRASE}.

**A. Breathing / Flow (Always Allowed)**
- 조용히 숨 쉬는
- 천천히 흐르는
- 낮게 이어지는

**B. Task-related Words (Conditionally Allowed)**
- 공부, 작업, 일, 재택근무, 집중, 드라이빙

Rules:
1. Task words MUST NOT be the main subject.
2. Task words MUST appear only as contextual support.
3. Task words MUST align with Context Mode.

**C. Emotion / Energy Words (Context-Driven Only)**
- Emotion words describe **energy level or listening posture**, not feelings.
- Allowed strictly by Context Mode.

---

### Context Mode → Modifier Allowance

| Context Mode | Allowed | Blocked |
|--------------|---------|---------|
| **Settling** | 차분한, 느긋한, 가라앉은 | 신나는, 설레는 |
| **Transition** | 부드러운, 가볍게 풀리는 | Avoid extremes |
| **Energizing** | 신나는, 경쾌한, 리드미컬한 | - |
| **Focusing** | 집중되는, 또렷한, 안정적인 | Avoid high-arousal |

---

### Time-based Defaults (Fallback Only)
Use ONLY when Context Mode is missing or ambiguous.

| Time | Default |
|------|---------|
| 00:00 – 05:00 | Minimal / calm |
| 06:00 – 08:00 | Light / transitional |
| 09:00 – 17:00 | Functional |
| 18:00 – 21:00 | Energetic |
| 22:00 – 23:59 | Settling |

---

#### 0.3 {GENRE} (Mandatory, Targeting Signal)
- Genre MUST be explicitly stated.
- Genre exists to clarify **target listener and sound expectation**.
- Genre must NOT override time as the primary frame.

**Allowed GENRE values (expandable):**
- Slow R&B 보컬
- R&B 보컬
- 미디엄 템포 Rock
- Indie Rock
- Pop Rock
- 재즈 보컬
- Quiet Jazz Vocals
- Vocal Pop

**Rules:**
- Use ONE genre phrase only.
- Genre should reflect the **dominant sound texture**, not sub-influences.
- Avoid vague genre words (Chill, Mood, Vibes).

---

### Style & Output Constraints (Critical) — v1.6

**제목 (Title):**
- No emojis
- No hashtags

**설명 (Description):**
- 본문: No emojis, No hashtags
- 하단 (구분선 이후): 해시태그 허용 (SEO용)
- No keyword stuffing

**고정 댓글 (Pinned Comment):**
- 이모지 1개 이하 허용 (시간대 톤에 맞게)

**공통:**
- Optimized for long-form background listening
- Must be interpretable without visual context

---

### Canonical Examples

**Settling Mode:**
```
[Playlist] [04:00] Wavvy | 하루가 멈춘 시간, 새벽 Slow R&B 보컬
```

**Energizing Mode:**
```
[Playlist] [08:00] Wavvy | 하루를 밀어 올리는 시간, 경쾌하게 흐르는 미디엄 템포 Rock
```

**Transition Mode:**
```
[Playlist] [18:00] Wavvy | 다시 움직이기 전의 시간, 부드럽게 이어지는 Indie Rock
```

---

## 1. 제목 전략 (Title Strategy) — 참고 패턴

> ⚠️ **아래는 일반적인 유튜브 제목 패턴 참고용이다.**
> **Wavvy 채널의 공식 타이틀 규칙은 Section 0을 따른다.**

### 1.1 TPO 패턴 (시간/장소/상황)
> 음악이 필요한 순간을 정확히 포착

| 상황 | 예시 |
|------|------|
| 출퇴근/운전 | "드라이브할 때 듣는 노래" |
| 아침 시작 | "상쾌한 아침을 여는 플레이리스트" |
| 공부/집중 | "공부할 때 틀어두는 음악" |
| 감정 상태 | "울고 싶을 때", "이별하고 듣는 곡" |
| 여행 | "여행을 떠날 때" |

### 1.2 문학적/감성적 표현
> 시나 책 구절 인용 → 감성 자극

- "부끄럼 많은 생애를 보냈습니다" (오사무 다자이 인용, 328만 조회)
- "너에게 못다 한 말..."
- "오늘도 수고했어, 이제 울어도 돼"

### 1.3 포맷 패턴

| 패턴 | 예시 |
|------|------|
| 태그 + 제목 | [Playlist] 혼자 있고 싶은 밤 |
| 한글 + 영문 | "혼자 있고 싶은 밤 \| A lonely night playlist" |
| 시리즈 | Vol.1, Part 1, #1 |
| 미스터리 | 제목 비움 (페페 플레이리스트 전략) |

### 1.4 슬픔/고독 테마 키워드

직접 감정 표현:
- "슬픈 노래", "외로운 밤", "그리움 가득한 하루"
- "울고 싶을 때 듣는 노래"
- "마음이 지칠 때 위로가 되는 음악"

위로 메시지형:
- "오늘 힘들었죠? 이 음악들이 작은 위로가 되길"
- "오늘도 수고했어, 이제 울어도 돼"

---

## 2. 썸네일 전략 (Thumbnail Strategy)

### 2.1 색상/톤 가이드

| 테마 | 색상 | 분위기 |
|------|------|--------|
| 슬픔/고독 | 블루, 그레이 | 차분, 쓸쓸함 |
| 힐링/위로 | 파스텔톤, 노을빛 | 포근, 따뜻함 |
| 추억/회고 | 레트로 필름, 빈티지 | 향수, 그리움 |
| 밤/새벽 | 어두운 톤, 네온 | 고독, 몽환 |

### 2.2 이미지 요소

슬픔/고독 테마:
- 눈물, 빗방울
- 혼자 앉은 뒷모습
- 어두운 도시 거리
- 빈 방, 창문

힐링 테마:
- 자연 풍경
- 따뜻한 조명
- 커피/차

### 2.3 캐릭터/일러스트

- lofi girl 스타일: 애니메이션 풍 그림
- 밈 캐릭터: 페페 (감정 표현 직관적)
- 일관된 캐릭터 사용 → 시리즈 정체성

### 2.4 텍스트

- 최소화 권장 (키워드 1-2개 또는 로고만)
- 손글씨 느낌 필기체 또는 깔끔한 고딕체
- 이미지 분위기에 집중

---

## 3. 영상 구성 전략

### 3.1 최적 길이

| 유형 | 길이 | 목적 |
|------|------|------|
| 표준 | 30분~1시간 | 배경음악용, 몰입 감상 |
| 대용량 | 2~4시간 | 지속 재생, 알고리즘 극대화 |
| 미리보기 | 10~15분 | 첫 클릭 허들 낮춤 |

> 긴 영상 = 시청 유지시간 ↑ = 알고리즘 추천 유리

### 3.2 챕터/타임스탬프 전략

| 전략 | 장점 | 단점 |
|------|------|------|
| 공개 | 편의 제공, 신뢰도 ↑ | 이탈 가능성 |
| 비공개 | 궁금증 유발, 댓글 참여 ↑ | 불편함 |

**권장**: 고정 댓글로 곡 리스트 제공 + 본문 챕터 선택적

---

## 4. 조회수 상승 메커니즘

### 4.1 알고리즘 트리거

```
높은 CTR (클릭률)
    ↓
긴 시청 지속시간
    ↓
높은 참여도 (좋댓구알)
    ↓
추천 피드 노출
    ↓
조회수 폭발
```

### 4.2 핵심 지표

| 지표 | 높이는 방법 |
|------|------------|
| CTR | 공감 제목 + 감성 썸네일 |
| 시청시간 | 30분+ 길이 + 몰입 구성 |
| 참여도 | 댓글 유도, 커뮤니티화 |
| 재방문 | 시리즈화, 반복 소비 유도 |

### 4.3 외부 트리거

- SNS 입소문 (트위터, 커뮤니티)
- 인플루언서/셀럽 언급
- Shorts/TikTok 연계
- 트렌드 키워드 활용

---

## 5. 시리즈화 & 반복 소비 전략

### 5.1 시리즈 네이밍

```
[테마] + [번호]
예: "외로움의 감성 플레이리스트 Part 1, 2, 3..."
    "Sad Pop songs for late nights Vol.1, 2..."
```

### 5.2 브랜드 일관성

- 동일한 썸네일 템플릿
- 동일한 색상 톤
- 동일한 제목 포맷
- → "이번 편도 기대된다" 반응 유도

### 5.3 반복 소비 유도

> 우울/외로운 감정은 주기적으로 찾아옴 → 즐겨찾기 & 반복 재생

- 위로 메시지로 정서적 연결
- 댓글 커뮤니티화
- 연장선 콘텐츠 (명언, 시 구절)

---

## 6. 댓글 커뮤니티 전략

### 6.1 인기 댓글 유형

| 유형 | 예시 |
|------|------|
| 열성 팬 | "당신 때문에 유튜브 프리미엄 결제했습니다" |
| 썰풀이 | "약속 준비하다가 친구한테 못 나간다고 했다" |
| 상호 위로 | "여기 모인 분들 모두 행복해졌으면" |
| 정보 교환 | "이 노래 아시는 분?" → 답변 |

### 6.2 커뮤니티 형성 팁

- 고정 댓글로 따뜻한 인사
- 곡 정보 제공 (또는 의도적 숨김)
- 청자 간 상호작용 유도

---

## 7. Wavvy 적용 체크리스트

플레이리스트 컨셉 설계 시 확인:

| # | 항목 | 체크 |
|---|------|------|
| 1 | TPO 또는 감정 키워드 제목 | □ |
| 2 | 문학적/위로 표현 고려 | □ |
| 3 | 썸네일 색상/톤 테마 매칭 | □ |
| 4 | 시리즈 네이밍 전략 | □ |
| 5 | 최적 길이 (30분~1시간) | □ |
| 6 | 챕터/타임스탬프 전략 결정 | □ |
| 7 | 위로 메시지/고정 댓글 준비 | □ |

---

## 8. Korean Lyric Positioning (3-Layer 전략)

> **"우리말 가사"는 차별점이지만, 과시하지 않고 자연스럽게 반복 노출한다.**

### 8.1 3-Layer 노출 전략

| Layer | 위치 | 강도 | 목적 |
|-------|------|------|------|
| **Layer 1** | 재생목록 설명 | 자연스럽게 1줄 | 메인 메시지 |
| **Layer 2** | 고정 댓글 | 팬 메시지 톤 | 충성 청자용 |
| **Layer 3** | 채널 About | 명확하게 명시 | 브랜딩/협업용 |

### 8.2 적용 규칙

**✅ DO:**
- 재생목록 설명에 "우리말 가사" 한 문장 자연스럽게 삽입
- 고정 댓글에 팬 메시지로 언급
- 채널 About에 명확하게 정체성 명시
- 영문 한 줄 보조 (*All tracks feature Korean lyrics.*)

**❌ DON'T:**
- 제목에 "한국어/Korean" 직접 명시
- 썸네일에 "Korean Lyrics" 텍스트
- "영어 플리와 다르게" 같은 비교 문구
- "한국어 감성 플레이리스트" 같은 설명형 타이틀

### 8.3 템플릿

**재생목록 설명 (Layer 1):**
```
[감성 오프닝 문장]

Wavvy는 우리말 가사로, 그 시간들의 감정을 기록합니다.
[감각 이미지 묘사]

당신의 하루에 작은 쉼이 되길 바랍니다.
```

**고정 댓글 (Layer 2):**
```
이 채널의 노래들은 모두 우리말 가사로 만들어졌습니다.
익숙한 말들이 더 천천히, 더 깊게 닿기를 바랍니다.

오늘 하루 어땠나요? 💬
```

**채널 About (Layer 3):**
```
Wavvy는
우리말 가사로 하루의 시간들을 기록하는 음악 채널입니다.
말보다 먼저 닿는 소리를 모읍니다.
```

**영문 보조 (선택):**
```
*All tracks feature Korean lyrics.*
```

### 8.4 핵심 원칙

> **"설명하지 않아도 느껴지는 정체성"**

- 차별화는 분명하되, 과시하지 않는다
- 정보가 아닌 감성으로 전달한다
- 반복 노출로 자연스럽게 인지시킨다

---

## 9. 수미상관 구조 (Bookend Pattern)

> **시리즈 첫/끝 트랙이 서로 미러링되는 구조**

### 구조

| 위치 | 역할 | 예시 (21-00) |
|------|------|----------------|
| Track 01 | 시작 - 문 열림 | "문을 열면 moon" |
| Track 10 | 종결 - 문 닫힘 | "문을 닫으면 room" |

### 적용 규칙

1. **Hook 미러링**: 첫 트랙 핵심 키워드가 마지막 트랙에 변주로 등장
2. **감정 아크**: 시작(기대/설렘) → 종결(안정/귀환)
3. **사운드 미러링**: 유사한 악기 배치 또는 BPM

### 설계 시점

- **Track 01 확정 후** Track 10 방향 미리 스케치
- Track 10 작업 시 Track 01 반드시 참조

### 예시

| 시리즈 | Track 01 Hook | Track 10 Hook |
|--------|---------------|---------------|
| 21-00 밤산책 | "문을 열면 moon" | "문을 닫으면 room" |
| 04-00 새벽 | (TBD) | (TBD) |

---

## 참고 자료

- Source PDF: `Reference/유튜브 감성 플레이리스트 인기 사례 분석.pdf`
- 성공 사례: 때껄룩, 페페 플레이리스트, 코지팝, 채널 리플레이
- 핵심 성공 요인: **"공감"** - 제목으로 공감, 썸네일로 공감, 댓글로 공감
