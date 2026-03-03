# YouTube Title Rules (SSOT v2.1)

Version: 2.1
Last Updated: 2026-03-03
Purpose: Wavvy 채널 공식 타이틀 규칙

---

## 1. Fixed Title Structure (v2.1 - 24H Universe)

**구조:**
```
Playlist | {HH}:{MM} | {감정 훅 + 이모지} | {장르1} · {장르2} | {용도1} · {용도2} | Wavvy
```

**구분자:** `|` (섹션 간), `·` (항목 간)

| 순서 | 요소 | 개수 | 예시 |
|------|------|------|------|
| 1 | 콘텐츠 타입 | 고정 | `Playlist` |
| 2 | 시간 | `HH:MM` | `06:00` |
| 3 | 감정 훅 + 이모지 | 1문장 + 1이모지 | `잠든 몸을 깨우는 새벽 🌅` |
| 4 | 장르 | 2개 (대문자) | `FAST LO-FI · CHILLHOP` |
| 5 | 용도 | 2개 | `러닝 · 모닝루틴` |
| 6 | 브랜드 | 고정 | `Wavvy` |

---

## 2. Fixed Tokens

- `Playlist` - 시작 고정
- `Wavvy` - 채널명 고정
- `@wavvy24` - 핸들
- 시간: `HH:MM` (24시간)
- 구분자: `|`

---

## 3. Context Mode (필수 입력)

제목 생성 전 반드시 명시:
- **Settling Mode** (가라앉힘/정리)
- **Transition Mode** (전환/이동)
- **Energizing Mode** (에너지 부여)
- **Focusing Mode** (집중)

### Context Mode → Modifier Allowance

| Mode | Allowed | Blocked |
|------|---------|---------|
| Settling | 차분한, 느긋한 | 신나는, 설레는 |
| Transition | 부드러운, 가볍게 | 극단적 표현 |
| Energizing | 신나는, 경쾌한 | - |
| Focusing | 집중되는, 또렷한 | 고각성 표현 |

---

## 4. Variable Slots

### 4.1 {TIME_STATE_PHRASE}
시간 기반 내면/지각 상태. **시간이 주어**여야 함.

**Type A (시적):** 하루가 멈춘 시간, 잠들지 못한 시간
**Type B (지각적):** 소리가 낮아진 시간, 움직임이 느려진 시간

> 연속 업로드 시 Type A/B 교차 사용

### 4.2 {MODIFIER_PHRASE}
시간 상태를 보조. 항상 TIME_STATE_PHRASE 뒤에.

- **Flow (항상 허용):** 조용히 숨 쉬는, 천천히 흐르는
- **Task (조건부):** 공부, 작업, 집중 (보조 역할만)
- **Emotion (Context 기반):** 에너지 레벨 표현

### 4.3 {GENRE}
명시적 장르. 타겟 청자 신호.
- 1개 장르만 사용
- Chill, Mood, Vibes 같은 모호한 표현 금지

---

## 5. 시간대별 이모지

| 시간대 | 이모지 | 키워드 |
|--------|--------|--------|
| 04:00 | 🌙/🌃 | 새벽 |
| 06:00 | 🌅 | 아침 |
| 10:00 | ☕ | 오전 업무 |
| 14:00 | ☀️ | 오후 |
| 16:00 | 🎸 | 늦은 오후 |
| 18:00 | 🚶 | 퇴근길 |
| 21:00 | 🌙 | 밤 |

---

## 6. Style & Output Constraints

**제목:**
- 이모지 1개 (감정 훅 끝)
- 장르 대문자 (예: `CHILLHOP`)
- No hashtags

**설명:** → `youtube/DESCRIPTION.md` 참조

---

## 7. 제목 예시

```
Playlist | 06:00 | 잠든 몸을 깨우는 새벽 🌅 | FAST LO-FI · CHILLHOP | 러닝 · 모닝루틴 | Wavvy
Playlist | 10:00 | 오늘도 조용히 시작하는 중 ☕ | CHILLHOP · JAZZHOP | 집중 · 작업 | Wavvy
Playlist | 21:00 | 하루를 내려놓는 밤 🌙 | SLOW R&B · NEO-SOUL | 힐링 · 휴식 | Wavvy
```
