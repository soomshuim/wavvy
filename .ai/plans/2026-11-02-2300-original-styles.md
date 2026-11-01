# 23:00 재생성 9곡 — 원곡 스타일 수집과 새 STYLE 조립안

- 만든 날: 2026-11-02 · 브리프: `.ai/plans/2026-11-02-2300-original-styles-brief.md` · 같은 내용의 기계 판독본: `.ai/plans/2026-11-02-2300-original-styles.json`
- 상태: **조립안만 있다.** 원고(`SERIES/23-00/input/tracks/*`)·concept·`suno-candidates.json`은 건드리지 않았고 브라우저·생성·커밋도 하지 않았다. 아래 값은 오케스트레이터가 고르기 전의 후보다.

## 젠 원문 (2026-11-02)

- 「스타일도 수정하자」
- 「공통 스타일은 Lo-fi Remix만 쓰고 23:00버전이 아닌 원곡 스타일에 Lo-fi Remix만 남기자 얼터너티브나 모던 알앤비는 제외」
- 템포: 「원곡 BPM 그대로」

## 조립 규칙 (브리프 그대로)

1. 새 STYLE = `Lo-fi Remix, ` + 원곡 STYLE 원문 (줄바꿈 그대로).
2. 원곡 STYLE에서 `alternative / Alt / 얼터너티브`, `Modern R&B / 모던 알앤비` **낱말만** 뺀다. 그 밖의 단어·순서·BPM은 바꾸지 않는다.
3. STYLE 안에서 `‑`/`-`로 시작하는 제외 항목이 있으면 EXCLUDE로 옮긴다 — 이 8개 원곡에는 그런 항목이 **0건**이다(스크립트가 assert로 확인).
4. 글자 수는 Unicode 코드포인트 수이며 공백·줄바꿈(`\n` 1자)을 센다. BPM·Key·성별 낱말은 `wavvy_harness/gate.py`의 정규식(`STYLE_BPM_RE` · `KEY_MODE_RE` · `VOCAL_GENDER_RE`)을 그대로 불러와 쟀다. "gate 재현" 열은 gate의 논리를 같은 함수로 계산한 것이며 실제 gate 실행이 아니다(txt를 만들지 않았다).

## 1. 곡별 요약표

| 새 곡 | 타입 | 원곡 STYLE 위치 (`SERIES/` 아래) | 원곡 BPM | 원곡 Key | 원곡 성별 / 설계 | Suno 파라미터 |
|---|---|---|---|---|---|---|
| 11 라디오 | 먼지 | `14-00/concept.md` 1040-1062행 (### Track 09: 먼지) | 72 | Eb Major | male / male | W20 / I80 |
| 12 스웨터 | 마음밖 | `04-00/concept.md` 135-135행 (## Track 01 (Seed)) | 90 | A♭ (Major/Minor 표기 없음) | female / female | 미기록 |
| 13 편지 | 작은 빛 | `22-00/concept.md` 1095-1106행 (### 10. 작은 손 (Tiny Hand)) | 72 | Db Major | male / male | 미기록 |
| 14 기타 | 산책 | `14-00/concept.md` 423-449행 (### Track 03: 산책) | 74 | Eb Major | male / male | W25 / I75 |
| 15 노을 | 물결 | `14-00/concept.md` 735-735행 (### Track 06: 물결) | 74 | A Major | male / male | W20 / I80 |
| 16 여름밤 | 물안개 | `04-00/concept.md` 349-356행 (## Track 04) | 80 | Eb Major | male / female | 미기록 |
| 17 막차 | 골목 | `18-00/concept.md` 1091-1110행 (## 10. Track 07 "골목" — 혼자 걷는 골목길 (기존 싱글)) | 67 | Db Major | male / male | `기존 싱글` (숫자 없음) |
| 18 벚꽃 | 이름 | `18-00/concept.md` 1393-1413행 (## 12. Track 09 "이름" — 문 열림, 이름 불려짐 (기존 싱글)) | 72 | Ab Major | male / female | `기존 싱글` (숫자 없음) |
| 19 그네 | 이름 | `18-00/concept.md` 1393-1413행 (## 12. Track 09 "이름" — 문 열림, 이름 불려짐 (기존 싱글)) | 72 | Ab Major | male / female | `기존 싱글` (숫자 없음) |

## 2. 뺀 말 · 조립안 글자 수 · EXCLUDE 수

| 새 곡 | 뺀 말 | 원곡 STYLE 글자 수 | 조립안 글자 수 | 줄 수 | STYLE 안 BPM 숫자 | STYLE 안 Key | STYLE 안 성별 낱말 | EXCLUDE 수 (주 조립안) | 인라인 EXCLUDE를 옮긴 대안 | gate 재현에서 걸리는 항목 |
|---|---|---|---|---|---|---|---|---|---|---|
| 11 라디오 | 없음 | 705 | **718** | 23 | [72] | Eb Major | Male | 10 | STYLE 624자 · EXCLUDE 10개 | EXCLUDE 8개 |
| 12 스웨터 | 없음 | 707 | **720** | 1 | [96, 106] | 없음 | Female | 0 | 해당 없음 | BPM, Key |
| 13 편지 | 없음 | 809 | **822** | 12 | [72] | Db Major | Male | 0 | 해당 없음 | 없음 |
| 14 기타 | `Alt` (`…⏎Korean Indie [Alt] R&B, 74 BP…`) | 946 | **955** | 27 | [74] | Eb Major | Male | 14 | 해당 없음 | 900자, EXCLUDE 8개 |
| 15 노을 | `Alt` (`…Korean Indie [Alt] R&B, 74 BP…`) | 627 | **636** | 1 | [74] | A Major | Male | 13 | 해당 없음 | EXCLUDE 8개(물결 예외 적용 가능) |
| 16 여름밤 | 없음 | 753 | **766** | 8 | [80] | Eb Major | Male | 18 | 해당 없음 | EXCLUDE 8개, 성별 |
| 17 막차 | 없음 | 731 | **744** | 20 | [67] | Db Major | Male | 0 | STYLE 598자 · EXCLUDE 15개 | 없음 |
| 18 벚꽃 | 없음 | 843 | **856** | 21 | [72] | Ab Major | Male | 0 | STYLE 737자 · EXCLUDE 11개 | 성별 |
| 19 그네 | 없음 | 843 | **856** | 21 | [72] | Ab Major | Male | 0 | STYLE 737자 · EXCLUDE 11개 | 성별 |

- 18 벚꽃과 19 그네는 같은 원곡(이름)을 쓰므로 조립안이 글자 단위로 같다(sha256 동일).
- 글자 수 = 원곡 글자 수 + 13(`Lo-fi Remix, `) − 뺀 말(`Alt ` 4자, 14 기타·15 노을만). 독립 재계산(`sed | wc -m`)과 원곡 글자 수 8건이 모두 일치했다.

## 3. 설계와 부딪히는 점 (표시만 — 고치지 않았다)

설계 보컬: 11 남 · 12 여 · 13 남 · 14 남 · 15 남 · 16 여 · 17 남 · 18 여 · 19 여 (브리프 4항). 심각도 열: `gate 걸림`은 위 "gate 재현"이 FAIL인 것, `결정 필요`는 오케스트레이터 선택이 갈리는 것, `정보`는 값 차이만 적은 것.

### 11 라디오 (먼지)

- **EXCLUDE 8개 초과** [gate 걸림] — 별도 EXCLUDE 블록이 10개 (한도 8).
- **인라인 EXCLUDE 줄** [결정 필요] — STYLE 안 14-00/concept.md:1062에 `Exclude Style:` 줄이 있다(8개 항목). 브리프 규칙 2는 `-` 시작 항목만 EXCLUDE로 옮기라고 했으므로 주 조립안은 이 줄을 STYLE에 그대로 둔다. 옮기면 STYLE 624자 · EXCLUDE 10개(8개 초과) — alt_inline_exclude_moved 참조. MASTER/style/STYLE.md:35는 피하고 싶은 요소를 가능하면 별도 Exclude에 적도록 한다. 어느 쪽으로 할지는 오케스트레이터 결정.
- **여러 줄 STYLE** [표시] — STYLE이 23줄이다(빈 줄 포함; 줄바꿈 22개를 글자 수에 1자씩 셈). `Lo-fi Remix, `는 첫 줄 맨 앞에 붙는다. 한 줄 STYLE이던 23:00 방식과 모양이 다르다.
- **설계 BPM ≠ 원곡 BPM** [정보] — new-song-styles.json 설계 BPM 70 ≠ 원곡 BPM 72. 젠 「원곡 BPM 그대로」를 따르면 설계값이 원곡값으로 바뀐다.
- **설계 Key ≠ 원곡 Key** [정보] — new-song-styles.json 설계 Key F Major ≠ 원곡 Key Eb Major. 젠은 Key에 대해 말한 적이 없다(미확정).

### 12 스웨터 (마음밖)

- **BPM 불일치** [gate 걸림] — STYLE의 BPM 숫자(gate 정규식 [106], 범위 표기 포함 [96, 106])는 원곡 BPM 90(파일명 기준)과 다르다. 브리프: STYLE 숫자는 바꾸지 않는다. gate 재현: FAIL STYLE=[106] 원곡=90.
- **Key가 STYLE에 없음** [gate 걸림] — 조립안 STYLE에 `X Major|Minor` 형식 Key가 없다 (원문: `A♭ (Major/Minor 표기 없음)`). gate `key_metadata_matches_style`은 이 형식을 요구한다.
- **STYLE 문구 ↔ 가사 기준** [표시] — STYLE에 `Melody understated (no big leaps, no catchy hook)`(04-00/concept.md:135)가 있다. 23-00/concept.md:34 새 곡 가사 기준(젠 「후렴이 중독성이 약하네」 → 후렴 훅 반복·한 번에 따라 부르기)과 방향이 반대다.
- **설계 BPM ≠ 원곡 BPM** [정보] — new-song-styles.json 설계 BPM 72 ≠ 원곡 BPM 90. 젠 「원곡 BPM 그대로」를 따르면 설계값이 원곡값으로 바뀐다.

### 13 편지 (작은 빛)

- **여러 줄 STYLE** [표시] — STYLE이 12줄이다(빈 줄 포함; 줄바꿈 11개를 글자 수에 1자씩 셈). `Lo-fi Remix, `는 첫 줄 맨 앞에 붙는다. 한 줄 STYLE이던 23:00 방식과 모양이 다르다.

### 14 기타 (산책)

- **900자 초과** [gate 걸림] — 조립안 955자 > 900자 (원곡 STYLE 946자 + 앞붙임 13자 − 뺀 말 4자 = 955). 초과 55자. 뺀 말을 안 빼도 959자라 앞붙임만으로 이미 초과.
- **EXCLUDE 8개 초과** [gate 걸림] — 별도 EXCLUDE 블록이 14개 (한도 8).
- **여러 줄 STYLE** [표시] — STYLE이 27줄이다(빈 줄 포함; 줄바꿈 26개를 글자 수에 1자씩 셈). `Lo-fi Remix, `는 첫 줄 맨 앞에 붙는다. 한 줄 STYLE이던 23:00 방식과 모양이 다르다.

### 15 노을 (물결)

- **EXCLUDE 8개 초과** [표시(기존 예외 적용 가능)] — 별도 EXCLUDE 블록이 13개 (한도 8). 23-00/concept.md:31·210에 물결 타입 한정 13개 예외가 이미 있다(txt 머리말 `Style Type: 물결` + `Exclude Source: user-supplied type style` + 항목·순서 일치 시에만 통과). 14-00 원곡의 13개와 그 예외 줄이 항목·순서까지 같다(물결_cross_check).

### 16 여름밤 (물안개)

- **성별** [gate 걸림] — 설계 보컬 female인데 원곡 보컬은 male이다 (concept 표기 male, 원곡 STYLE 성별 낱말 `Male`). 조립안 STYLE에도 `Male`가 그대로 남는다. gate 재현: FAIL STYLE=male 설계=female.
- **EXCLUDE 8개 초과** [gate 걸림] — 별도 EXCLUDE 블록이 18개 (한도 8).
- **여러 줄 STYLE** [표시] — STYLE이 8줄이다(빈 줄 포함; 줄바꿈 7개를 글자 수에 1자씩 셈). `Lo-fi Remix, `는 첫 줄 맨 앞에 붙는다. 한 줄 STYLE이던 23:00 방식과 모양이 다르다.
- **설계 BPM ≠ 원곡 BPM** [정보] — new-song-styles.json 설계 BPM 76 ≠ 원곡 BPM 80. 젠 「원곡 BPM 그대로」를 따르면 설계값이 원곡값으로 바뀐다.
- **설계 Key ≠ 원곡 Key** [정보] — new-song-styles.json 설계 Key G Major ≠ 원곡 Key Eb Major. 젠은 Key에 대해 말한 적이 없다(미확정).

### 17 막차 (골목)

- **인라인 EXCLUDE 줄** [결정 필요] — STYLE 안 18-00/concept.md:1110에 `EXCLUDE:` 줄이 있다(15개 항목). 브리프 규칙 2는 `-` 시작 항목만 EXCLUDE로 옮기라고 했으므로 주 조립안은 이 줄을 STYLE에 그대로 둔다. 옮기면 STYLE 598자 · EXCLUDE 15개(8개 초과) — alt_inline_exclude_moved 참조. MASTER/style/STYLE.md:35는 피하고 싶은 요소를 가능하면 별도 Exclude에 적도록 한다. 어느 쪽으로 할지는 오케스트레이터 결정.
- **여러 줄 STYLE** [표시] — STYLE이 20줄이다(빈 줄 포함; 줄바꿈 19개를 글자 수에 1자씩 셈). `Lo-fi Remix, `는 첫 줄 맨 앞에 붙는다. 한 줄 STYLE이던 23:00 방식과 모양이 다르다.
- **설계 BPM ≠ 원곡 BPM** [정보] — new-song-styles.json 설계 BPM 80 ≠ 원곡 BPM 67. 젠 「원곡 BPM 그대로」를 따르면 설계값이 원곡값으로 바뀐다.
- **설계 Key ≠ 원곡 Key** [정보] — new-song-styles.json 설계 Key E Major ≠ 원곡 Key Db Major. 젠은 Key에 대해 말한 적이 없다(미확정).

### 18 벚꽃 (이름)

- **성별** [gate 걸림] — 설계 보컬 female인데 원곡 보컬은 male이다 (concept 표기 male, 원곡 STYLE 성별 낱말 `Male`). 조립안 STYLE에도 `Male`가 그대로 남는다. gate 재현: FAIL STYLE=male 설계=female.
- **인라인 EXCLUDE 줄** [결정 필요] — STYLE 안 18-00/concept.md:1413에 `EXCLUDE:` 줄이 있다(11개 항목). 브리프 규칙 2는 `-` 시작 항목만 EXCLUDE로 옮기라고 했으므로 주 조립안은 이 줄을 STYLE에 그대로 둔다. 옮기면 STYLE 737자 · EXCLUDE 11개(8개 초과) — alt_inline_exclude_moved 참조. MASTER/style/STYLE.md:35는 피하고 싶은 요소를 가능하면 별도 Exclude에 적도록 한다. 어느 쪽으로 할지는 오케스트레이터 결정.
- **여러 줄 STYLE** [표시] — STYLE이 21줄이다(빈 줄 포함; 줄바꿈 20개를 글자 수에 1자씩 셈). `Lo-fi Remix, `는 첫 줄 맨 앞에 붙는다. 한 줄 STYLE이던 23:00 방식과 모양이 다르다.
- **원곡 가사·구조에 묶인 문구** [표시] — STYLE에 `Bridge3: sparse, tension rising…`(18-00/concept.md:1405)와 `Last "괜찮아": longest sustain in entire track, This single note defines the emotional peak`(1407)가 있다. 새 곡 18 벚꽃·19 그네 가사에 `괜찮아`가 있는지·브리지가 3개인지는 이번에 확인하지 않았다(원고 미열람).
- **설계 BPM ≠ 원곡 BPM** [정보] — new-song-styles.json 설계 BPM 78 ≠ 원곡 BPM 72. 젠 「원곡 BPM 그대로」를 따르면 설계값이 원곡값으로 바뀐다.
- **설계 Key ≠ 원곡 Key** [정보] — new-song-styles.json 설계 Key C Major ≠ 원곡 Key Ab Major. 젠은 Key에 대해 말한 적이 없다(미확정).

### 19 그네 (이름)

- **성별** [gate 걸림] — 설계 보컬 female인데 원곡 보컬은 male이다 (concept 표기 male, 원곡 STYLE 성별 낱말 `Male`). 조립안 STYLE에도 `Male`가 그대로 남는다. gate 재현: FAIL STYLE=male 설계=female.
- **인라인 EXCLUDE 줄** [결정 필요] — STYLE 안 18-00/concept.md:1413에 `EXCLUDE:` 줄이 있다(11개 항목). 브리프 규칙 2는 `-` 시작 항목만 EXCLUDE로 옮기라고 했으므로 주 조립안은 이 줄을 STYLE에 그대로 둔다. 옮기면 STYLE 737자 · EXCLUDE 11개(8개 초과) — alt_inline_exclude_moved 참조. MASTER/style/STYLE.md:35는 피하고 싶은 요소를 가능하면 별도 Exclude에 적도록 한다. 어느 쪽으로 할지는 오케스트레이터 결정.
- **여러 줄 STYLE** [표시] — STYLE이 21줄이다(빈 줄 포함; 줄바꿈 20개를 글자 수에 1자씩 셈). `Lo-fi Remix, `는 첫 줄 맨 앞에 붙는다. 한 줄 STYLE이던 23:00 방식과 모양이 다르다.
- **원곡 가사·구조에 묶인 문구** [표시] — STYLE에 `Bridge3: sparse, tension rising…`(18-00/concept.md:1405)와 `Last "괜찮아": longest sustain in entire track, This single note defines the emotional peak`(1407)가 있다. 새 곡 18 벚꽃·19 그네 가사에 `괜찮아`가 있는지·브리지가 3개인지는 이번에 확인하지 않았다(원고 미열람).
- **설계 BPM ≠ 원곡 BPM** [정보] — new-song-styles.json 설계 BPM 70 ≠ 원곡 BPM 72. 젠 「원곡 BPM 그대로」를 따르면 설계값이 원곡값으로 바뀐다.
- **설계 Key ≠ 원곡 Key** [정보] — new-song-styles.json 설계 Key E Minor ≠ 원곡 Key Ab Major. 젠은 Key에 대해 말한 적이 없다(미확정).

### 한눈에 보는 묶음

- EXCLUDE 8개 초과: 11 라디오, 14 기타, 15 노을, 16 여름밤
- 인라인 EXCLUDE 줄: 11 라디오, 17 막차, 18 벚꽃, 19 그네
- 여러 줄 STYLE: 11 라디오, 13 편지, 14 기타, 16 여름밤, 17 막차, 18 벚꽃, 19 그네
- 설계 BPM ≠ 원곡 BPM: 11 라디오, 12 스웨터, 16 여름밤, 17 막차, 18 벚꽃, 19 그네
- 설계 Key ≠ 원곡 Key: 11 라디오, 16 여름밤, 17 막차, 18 벚꽃, 19 그네
- BPM 불일치: 12 스웨터
- Key가 STYLE에 없음: 12 스웨터
- STYLE 문구 ↔ 가사 기준: 12 스웨터
- 900자 초과: 14 기타
- 성별: 16 여름밤, 18 벚꽃, 19 그네
- 원곡 가사·구조에 묶인 문구: 18 벚꽃, 19 그네

## 4. 곡별 상세 — 조립안 전문

### 11 라디오 ← 먼지

- 출처: `SERIES/14-00/concept.md` — `### Track 09: 먼지` (제목줄 968행) · STYLE 본문 1040-1062행 · 별도 EXCLUDE 1067-1067행 · 파일명 970행 `09__먼지__Warm__Soft-RnB__72.mp3`
- 고른 판: 14-00 concept 트랙 절에 Style Prompt가 1개뿐(판 선택 불필요). 같은 절 안에 Style Prompt 속 `Exclude Style:` 줄(8개)과 별도 `Exclude Style:` 블록(10개)이 둘 다 있고 내용이 다르다.
- BPM 72 ← 14-00/concept.md:970 파일명 `09__먼지__Warm__Soft-RnB__72.mp3` · 14-00/concept.md:1188 트랙 리스트 BPM 72 · SERIES/RNB-BEST/concept.md:278 파일명 ...72.mp3
- Key Eb Major ← 14-00/concept.md:1040 STYLE `Eb Major` · 14-00/concept.md:1188 트랙 리스트 Key Eb Major
- 성별 male ← 14-00/concept.md:1188 트랙 리스트 Vocal Male · 14-00/concept.md:1045 STYLE `Male vocal.`
- Suno 파라미터: W20 / I80 — 14-00/concept.md:976-980
- 별도 EXCLUDE 블록(별도 Exclude Style 블록 14-00/concept.md:1067): Airy, Falsetto, Whisper, Harmonized, Backing vocals, Choir, Cold, Dark, Intense, Dramatic — 10개
- STYLE 안 인라인 EXCLUDE 줄(14-00:1062, 8개): Airy, Falsetto, Whisper, Harmonized, Backing vocals, Choir, Intense, Dramatic
- 뺀 말: 없음
- 조립안: 718자 · 23줄 · sha256 `57b675f6564a5e9a…` · EXCLUDE 10개

조립안 STYLE (주):

```text
Lo-fi Remix, Korean Soft R&B, 72 BPM, Eb Major

Vibraphone-led, supportive R&B groove,
laid-back brush rhythm, warm afternoon texture.

Male vocal. Natural, intimate.
Raw, Solid, Direct, Dry.
Chest voice dominant. No falsetto. Minimal vibrato.

Verse1: vibraphone melody, sparse drums, drifting feel.
Verse2: soft kick enters, groove locks in.
Lift through rhythm, not volume.

Chorus: kick and snare present, melodic bass,
pad widens gently.

Bridge: vibraphone and voice only, gentle build.
Outro: gradual fade, vibraphone restates motif softly.

Single lead vocal throughout.
Chorus expansion by arrangement density only.

Exclude Style: Airy, Falsetto, Whisper, Harmonized, Backing vocals, Choir, Intense, Dramatic
```

조립안 EXCLUDE (주): Airy, Falsetto, Whisper, Harmonized, Backing vocals, Choir, Cold, Dark, Intense, Dramatic

대안 — 인라인 EXCLUDE 줄을 STYLE에서 빼 EXCLUDE로 옮긴 경우: STYLE 624자 · EXCLUDE 10개 (전문은 json `alt_inline_exclude_moved`)

참고:
- 원곡 절 내부 불일치: 같은 14-00 Track 09 절 안에서 Style Prompt 속 `Exclude Style:` 줄은 8개(1062행), 별도 `Exclude Style:` 블록은 10개(1067행, `Cold, Dark` 추가)로 서로 다르다. 어느 쪽이 Suno에 실제로 들어갔는지는 concept만으로 알 수 없다.

### 12 스웨터 ← 마음밖

- 출처: `SERIES/04-00/concept.md` — `## Track 01 (Seed)` (제목줄 77행) · STYLE 본문 135-135행 · 별도 EXCLUDE 140-140행 · 파일명 80행 `01__마음밖__Sentimental__RnB-Ballad__90.mp3`
- 고른 판: 04-00 concept `## Track 01 (Seed)`에 Style Prompt 1개뿐(판 선택 불필요). 제목줄에 곡명이 없고 파일명(80행)에 `마음밖`이 있다.
- BPM 90 ← 04-00/concept.md:80 파일명 `01__마음밖__Sentimental__RnB-Ballad__90.mp3` · 04-00/output/provenance.md 표 01 파일명 ...90.mp3 · SERIES/RNB-BEST/concept.md:297 파일명 ...90.mp3
- Key A♭ (Major/Minor 표기 없음) ← 04-00/concept.md:135 STYLE `key color like A♭`
- 성별 female ← 04-00/concept.md:766 메모 `Female vocal` · 04-00/concept.md:135 STYLE `Female vocal very forward…`
- Suno 파라미터: 미기록 — 04-00/concept.md 전체 grep `Weirdness|Style Influence|Suno Param` 결과 0건
- 별도 EXCLUDE 블록(별도 Exclude Style 블록 `(없음)`): 없음 — 0개
- 뺀 말: 없음
- 조립안: 720자 · 1줄 · sha256 `56729ee045a4b12a…` · EXCLUDE 0개

조립안 STYLE (주):

```text
Lo-fi Remix, articulation, Korean R&B/pop ballad, 96–106 BPM, key color like A♭, Piano/Rhodes-led, cinematic but restrained, Warm keys upfront, soft supportive bass, tight understated kick (present, not huge), rim/snare light, simple hats, no rolls, Subtle strings/pads in choruses only, never dramatic, Verse intimate and sparse; chorus opens slightly wider with more harmony, not more rhythm, Final chorus adds a gentle "major-color" lift via chords/strings, not belting, Female vocal very forward and dry/close-mic: warm husky tone, clear Korean diction, conversational phrasing, controlled vibrato, natural breaths, minimal pitch correction, Melody understated (no big leaps, no catchy hook), Outro instrumental fade
```

조립안 EXCLUDE (주): (없음)

참고:
- 설계 Key 비교: new-song-styles.json 설계 Key Ab Major vs 원곡 STYLE `key color like A♭`: 음 이름은 같고 Major/Minor 표기만 원곡에 없다.
- Suno 파라미터 미기록: 해당 concept에 Weirdness·Style Influence 기록이 없다.
- 선행 단어: STYLE이 소문자 `articulation,`로 시작한다. 바꾸지 않았다.
- STYLE 특수문자: STYLE에 `–`(en dash)와 `♭`가 있다 (`96–106 BPM`, `A♭`). 그대로 두었다.

### 13 편지 ← 작은 빛

- 출처: `SERIES/22-00/concept.md` — `### 10. 작은 손 (Tiny Hand)` (제목줄 1091행) · STYLE 본문 1095-1106행
- 고른 판: 22-00 concept에 STYLE이 트랙 10 절에 1개뿐(판 선택 불필요). 제목 불일치: Track Map(118행)은 `10 작은 빛 (Little Light)`, 트랙 상세 제목줄(1091행)은 `10. 작은 손 (Tiny Hand)`. 발매 파일명(RNB-BEST 272행)은 `작은 빛`이라 곡 제목은 작은 빛. 같은 파일 84-92행에 시리즈 공통 `Exclude Template`이 있으나 트랙 10 절에는 EXCLUDE 줄이 없다.
- BPM 72 ← 22-00/concept.md:118 Track Map `10 | 작은 빛 (Little Light) | B | 72 | Db Major | M` · 22-00/concept.md:1095 STYLE `72 BPM` · SERIES/RNB-BEST/concept.md:272 파일명 `10__작은 빛__Little Light__Chill R&B__72.wav`
- Key Db Major ← 22-00/concept.md:118 Track Map Db Major · 22-00/concept.md:1095 STYLE `Db Major`
- 성별 male ← 22-00/concept.md:118 Track Map Vocal M · 22-00/concept.md:1098 STYLE `Male vocal:`
- Suno 파라미터: 미기록 — 22-00/concept.md 전체 grep `Weirdness|Style Influence|Suno Param` 결과 0건
- 별도 EXCLUDE 블록(없음 (이 곡 절에 EXCLUDE 없음)): 없음 — 0개
- 뺀 말: 없음
- 조립안: 822자 · 12줄 · sha256 `84370501a8cd3c29…` · EXCLUDE 0개

조립안 STYLE (주):

```text
Lo-fi Remix, Articulation. Korean Chill R&B, 72 BPM, Db Major,
felt piano-led, warm Rhodes chords, soft brush kit,
rim-click, warm bass groove, subtle strings in chorus,
Male vocal: Warm, Intimate, Chest voice, Dry, articulation,
warm baritone, conversational phrasing, gentle sustained chorus hook,
chorus builds with emotional swell, tender vocal intensity, aching warmth,
cozy intimate mix, wide stereo, warm low-end,
moderate reverb, intimate ambience, EQ balanced sound, clean mix.
Lead vocal remains single and dominant throughout. No stacked or choir-like harmonies.
Vocal line may intensify dynamically (gentle lift, higher register), but no additional vocal layers.
Chorus vocal may be delivered with tender intensity or gentle sustained note.
Higher register emphasis is allowed. Natural vocal warmth encouraged.
```

조립안 EXCLUDE (주): (없음)

참고:
- Suno 파라미터 미기록: 해당 concept에 Weirdness·Style Influence 기록이 없다.
- 제목 불일치: 22-00 Track Map(118행)은 `10 작은 빛 (Little Light)`, 트랙 상세 제목줄(1091행)은 `10. 작은 손 (Tiny Hand)`. STYLE 본문은 한 곳뿐이고 발매 파일명(RNB-BEST/concept.md:272)이 `작은 빛`이라 같은 곡으로 봤다.
- 공통 EXCLUDE 템플릿: 22-00/concept.md:84-92 `Exclude Template (공통)`(18개 항목)이 있으나 트랙 10 절에는 EXCLUDE 줄이 없다. 이 곡에 적용됐는지 미확정이라 original_exclude를 비워 두었다.

### 14 기타 ← 산책

- 출처: `SERIES/14-00/concept.md` — `### Track 03: 산책` (제목줄 353행) · STYLE 본문 423-449행 · 별도 EXCLUDE 454-454행 · 파일명 355행 `03__산책__Chill__Alt-RnB__74.mp3`
- 고른 판: 14-00 concept 트랙 절에 Style Prompt가 1개뿐(판 선택 불필요). 23-00 concept `### 산책`의 (a)는 Suno 작업공간의 Lo-Fi Remix 곡 표시 문구라 원곡 STYLE이 아니다(`Lo-Fi Remix, Modern R&B, clear voice, precise articulation, laidback, …`로 시작).
- BPM 74 ← 14-00/concept.md:355 파일명 `03__산책__Chill__Alt-RnB__74.mp3` · 14-00/concept.md:424 STYLE `74 BPM` · 14-00/concept.md:1182 트랙 리스트 BPM 74
- Key Eb Major ← 14-00/concept.md:424 STYLE `Eb Major` · 14-00/concept.md:1182 트랙 리스트 Key Eb Major
- 성별 male ← 14-00/concept.md:1182 트랙 리스트 Vocal Male · 14-00/concept.md:428 STYLE `Male vocal:`
- Suno 파라미터: W25 / I75 — 14-00/concept.md:361-365
- 별도 EXCLUDE 블록(별도 Exclude Style 블록 14-00/concept.md:454): Falsetto, Airy, Whisper, Breathiness, Growl, Vibrato, Opera, Dramatic, High-pitched belting, Harmonized, Backing vocals, Choir, Intense, Mumbled — 14개
- 뺀 말: `Alt` (`…⏎Korean Indie [Alt] R&B, 74 BP…`)
- 조립안: 955자 · 27줄 · sha256 `a1990eaaa31063df…` · EXCLUDE 14개

조립안 STYLE (주):

```text
Lo-fi Remix, Articulation.
Korean Indie R&B, 74 BPM, Eb Major.
Clean Electric Guitar-led, supportive R&B groove,
rim-click, warm afternoon texture, subtle vinyl crackle.

Male vocal: Solid, Direct, Raw, Dry.
Chest voice dominant. No falsetto.
Straight tone only. No vibrato, no ad-libs.
High register chest voice preferred over falsetto.
Tone is nonchalant and effortless, never dramatic.

Vocal articulation is critical:
clear consonant attack, precise syllable separation,
no slurring, no breathy phrasing.

Verse2 builds clear tension.
Chorus contains a single, unavoidable high-note focal point:
short, decisive high register chest note,
straight tone, not sustained belting.
If the chorus does not reach a high register chest note,
the emotional intent is considered failed.

Chorus hook-first, repeated identically.
Later choruses grow only by arrangement density.
Bridge builds every bar.
Outro guitar fades.
Lead vocal remains single and dominant.
```

조립안 EXCLUDE (주): Falsetto, Airy, Whisper, Breathiness, Growl, Vibrato, Opera, Dramatic, High-pitched belting, Harmonized, Backing vocals, Choir, Intense, Mumbled

참고:
- 선행 단어: STYLE 첫 줄이 `Articulation.`이다. 바꾸지 않았다.

### 15 노을 ← 물결

- 출처: `SERIES/14-00/concept.md` — `### Track 06: 물결` (제목줄 660행) · STYLE 본문 735-735행 · 별도 EXCLUDE 740-740행 · 파일명 662행 `06__물결__Chill__Alt-RnB__74.mp3`
- 고른 판: 14-00 concept 트랙 절에 Style Prompt가 1개뿐(판 선택 불필요). 23-00 concept `### 물결` (a)와 대조: (a) = 이 원곡 STYLE + `, Modern Indie R&B, Lo-fi Remastered, Articulation`(젠이 붙이라고 한 3개 구절). 이번 조립안은 그 3개 구절을 쓰지 않는다(젠 11-02 「23:00버전이 아닌 원곡 스타일」).
- BPM 74 ← 14-00/concept.md:662 파일명 `06__물결__Chill__Alt-RnB__74.mp3` · 14-00/concept.md:735 STYLE `74 BPM` · 14-00/concept.md:1185 트랙 리스트 BPM 74
- Key A Major ← 14-00/concept.md:735 STYLE `A Major` · 14-00/concept.md:1185 트랙 리스트 Key A Major
- 성별 male ← 14-00/concept.md:1185 트랙 리스트 Vocal Male · 14-00/concept.md:735 STYLE `Male vocal:`
- Suno 파라미터: W20 / I80 — 14-00/concept.md:673-677 — 23-00/concept.md:307 작업공간 Cover 곡 표시 Weirdness 20% · Style Influence 80%와 일치
- 별도 EXCLUDE 블록(별도 Exclude Style 블록 14-00/concept.md:740): Falsetto, Airy, Whisper, Breathiness, Growl, Vibrato, Opera, Dramatic, Harmonized, Backing vocals, Choir, Intense, Mumbled — 13개
- 뺀 말: `Alt` (`…Korean Indie [Alt] R&B, 74 BP…`)
- 조립안: 636자 · 1줄 · sha256 `3926d154576a0f1e…` · EXCLUDE 13개

조립안 STYLE (주):

```text
Lo-fi Remix, Korean Indie R&B, 74 BPM, A Major, Neo-soul chords (M9, m7), Clean Electric Guitar-led supportive groove, rim-click, warm texture, subtle vinyl crackle, Male vocal: Solid, Direct, Raw, Dry, Chest dominant, No falsetto, Straight tone, No vibrato, no ad-libs, Narrow range, stepwise melody, speech-like rhythm, High chest voice over falsetto, Nonchalant tone, never dramatic, Articulation: clear consonants, precise syllables, no slurring, Verse2 tension builds, Chorus hook-first, high-note focal: short chest note, straight, not sustained, Choruses grow by density only, Bridge sparse, Outro guitar fades, Single lead vocal
```

조립안 EXCLUDE (주): Falsetto, Airy, Whisper, Breathiness, Growl, Vibrato, Opera, Dramatic, Harmonized, Backing vocals, Choir, Intense, Mumbled

참고:
- 23:00 구절 미사용: 23-00/concept.md `### 물결` (a)의 끝 `, Modern Indie R&B, Lo-fi Remastered, Articulation`은 이번 조립안에 넣지 않았다(젠 「23:00버전이 아닌 원곡 스타일」). 맨 앞 `Lo-fi Remix, `만 붙었다.

### 16 여름밤 ← 물안개

- 출처: `SERIES/04-00/concept.md` — `## Track 04` (제목줄 291행) · STYLE 본문 349-356행 · 별도 EXCLUDE 361-361행 · 파일명 294행 `04__물안개__Hazy__Lo-fi-RnB__80.mp3`
- 고른 판: 04-00 concept 트랙 절에 Style Prompt가 1개뿐(판 선택 불필요). 소제목이 `Style Prompt (제로 베이스라인 v2)`(347행)이고 Track 03의 `제로 베이스라인 최종`은 다른 곡이다. 04-00 메모(769행)에는 이 곡의 보컬 성별 언급이 없다.
- BPM 80 ← 04-00/concept.md:294 파일명 `04__물안개__Hazy__Lo-fi-RnB__80.mp3` · 04-00/concept.md:349 STYLE `80 BPM` · SERIES/RNB-BEST/concept.md:279 파일명 ...80.mp3
- Key Eb Major ← 04-00/concept.md:349 STYLE `key Eb Major`
- 성별 male ← 04-00/concept.md:350 STYLE `Male vocal:`
- Suno 파라미터: 미기록 — 04-00/concept.md 전체 grep `Weirdness|Style Influence|Suno Param` 결과 0건
- 별도 EXCLUDE 블록(별도 Exclude Style 블록 04-00/concept.md:361): choir, gospel choir, stacked harmonies, vocal harmonies, harmony stack, ensemble vocals, doubled vocals, vocoder, vocal chop, hard tune, pitchy EDM lead, hyperpop vocal, autotune heavy, EDM drops, big room, festival, supersaw lead, sidechain pumping — 18개
- 뺀 말: 없음
- 조립안: 766자 · 8줄 · sha256 `15de4017908364fd…` · EXCLUDE 18개

조립안 STYLE (주):

```text
Lo-fi Remix, articulation, Korean Lo-fi R&B, 80 BPM, key Eb Major, Felt Piano-led, soft shaker, hazy ambient pad, cinematic but restrained.
Male vocal: warm soulful tone, dry close-mic, slightly breathy, straight delivery, minimal vibrato, minimal autotune.
No backing vocals, no harmonies, no doubles, no choir.
Lead vocal only throughout; absolutely no vocal layers in chorus (no doubles, no unison, no octaves).
Chorus hook-first, repeat identical; Chorus2 bigger only by arrangement density and stereo width, vocals unchanged.
Verse2 same melodic contour as verse1; last 2 lines stronger dynamics and slightly higher register, minimal runs.
Bridge builds every bar with instrumental layers; no energy drop into chorus.
Outro felt piano notes fading into silence.
```

조립안 EXCLUDE (주): choir, gospel choir, stacked harmonies, vocal harmonies, harmony stack, ensemble vocals, doubled vocals, vocoder, vocal chop, hard tune, pitchy EDM lead, hyperpop vocal, autotune heavy, EDM drops, big room, festival, supersaw lead, sidechain pumping

참고:
- Suno 파라미터 미기록: 해당 concept에 Weirdness·Style Influence 기록이 없다.
- 선행 단어: STYLE이 소문자 `articulation,`로 시작한다. 조립안은 `Lo-fi Remix, articulation, Korean Lo-fi R&B, …` 순서. 바꾸지 않았다.

### 17 막차 ← 골목

- 출처: `SERIES/18-00/concept.md` — `## 10. Track 07 "골목" — 혼자 걷는 골목길 (기존 싱글)` (제목줄 1000행) · STYLE 본문 1091-1110행
- 고른 판: 18-00 concept에 STYLE 1개뿐(판 선택 불필요). `기존 싱글`(18-00/concept.md:1000, 1117-1118)로 표시된 곡. SERIES/Single/골목_youtube.md에는 STYLE이 없고 BPM 67·Key Db Major·장르 `Korean Slow R&B Ballad`만 있어 18-00 값과 일치한다.
- BPM 67 ← 18-00/concept.md:1011 구조 표 BPM 67 · 18-00/concept.md:1091 STYLE `67 BPM` · SERIES/Single/골목_youtube.md:13 BPM 67 · SERIES/RNB-BEST/concept.md:303 파일명 ...67.mp3
- Key Db Major ← 18-00/concept.md:1012 구조 표 Key Db Major · 18-00/concept.md:1091 STYLE `Db Major` · SERIES/Single/골목_youtube.md:14 Key Db Major
- 성별 male ← 18-00/concept.md:1013 구조 표 Vocal Male, Solo only · 18-00/concept.md:1093 STYLE `Male vocal`
- Suno 파라미터: `기존 싱글` (숫자 없음) — 18-00/concept.md:1113-1118
- 별도 EXCLUDE 블록(STYLE 안 인라인 `EXCLUDE:` 줄 18-00/concept.md:1110 (별도 블록 없음)): 없음 — 0개
- STYLE 안 인라인 EXCLUDE 줄(18-00:1110, 15개): Rap, Hip-hop, Spoken word, Harmonies, Backing vocals, Doubles, Choir, Ad-libs, Runs, Melisma, Falsetto, Bright, Upbeat, Energetic, Fast
- 뺀 말: 없음
- 조립안: 744자 · 20줄 · sha256 `8aaa4af0085da44c…` · EXCLUDE 0개

조립안 STYLE (주):

```text
Lo-fi Remix, Korean Slow R&B Ballad, 67 BPM, Db Major

Male vocal, Raw, Dry, Unprocessed, Chest voice dominant
No falsetto, No runs, No melisma
Speech-like phrasing, Narrow melodic range
Precise articulation, clear consonants

supportive, warm pad texture
Minimal drums or drumless verses
Soft bass, low presence
Moderate reverb, EQ balanced sound, clean mix

Verse2 subtle intensity increase by vocal weight only
Chorus: longer sustain on hook phrase, no belt
Bridge: single guitar line, no solo flourish

No harmony, no backing vocals, no doubles
Lead vocal remains single and dominant throughout

EXCLUDE: Rap, Hip-hop, Spoken word, Harmonies, Backing vocals, Doubles, Choir, Ad-libs, Runs, Melisma, Falsetto, Bright, Upbeat, Energetic, Fast
```

조립안 EXCLUDE (주): (없음)

대안 — 인라인 EXCLUDE 줄을 STYLE에서 빼 EXCLUDE로 옮긴 경우: STYLE 598자 · EXCLUDE 15개 (전문은 json `alt_inline_exclude_moved`)

참고:
- Suno 파라미터 숫자 없음: Weirdness·Style Influence가 `기존 싱글`로만 적혀 숫자가 없다.

### 18 벚꽃 ← 이름

- 출처: `SERIES/18-00/concept.md` — `## 12. Track 09 "이름" — 문 열림, 이름 불려짐 (기존 싱글)` (제목줄 1292행) · STYLE 본문 1393-1413행
- 고른 판: 18-00 concept에 STYLE 1개뿐(판 선택 불필요). `기존 싱글`(18-00/concept.md:1292, 1420-1421)로 표시된 곡이며 Closing 트랙.
- BPM 72 ← 18-00/concept.md:1303 구조 표 BPM 72 · 18-00/concept.md:1393 STYLE `72 BPM` · SERIES/RNB-BEST/concept.md:301 파일명 `09__이름__Homecoming__Soft-RnB__72.mp3`
- Key Ab Major ← 18-00/concept.md:1304 구조 표 Key Ab Major · 18-00/concept.md:1393 STYLE `Ab Major`
- 성별 male ← 18-00/concept.md:1305 구조 표 Vocal Male, Solo only · 18-00/concept.md:1397 STYLE `Male vocal:`
- Suno 파라미터: `기존 싱글` (숫자 없음) — 18-00/concept.md:1416-1421
- 별도 EXCLUDE 블록(STYLE 안 인라인 `EXCLUDE:` 줄 18-00/concept.md:1413 (별도 블록 없음)): 없음 — 0개
- STYLE 안 인라인 EXCLUDE 줄(18-00:1413, 11개): Falsetto, Airy, Whisper, Breathiness, Vibrato, Harmonized, Backing vocals, Choir, Intense, Dramatic, Mumbled
- 뺀 말: 없음
- 조립안: 856자 · 21줄 · sha256 `0fdae5b5fb9adffb…` · EXCLUDE 0개

조립안 STYLE (주):

```text
Lo-fi Remix, Korean Soft R&B, 72 BPM, Ab Major

Soft Synth Pad-led, supportive groove, gentle pulse, warm shade texture

Male vocal: Natural, laid-back, Raw, Solid, Direct, Dry
Chest voice dominant, No falsetto, Straight tone, No vibrato, no ad-libs
Precise articulation, clear consonants

Verse1: synth pad, sparse drums, drifting
Verse2: kick steady, groove deepens
Verse2 last 2 lines: higher register, tighter rhythm, vocal push
Bridge1/2: pad and voice, intimate
Bridge3: sparse, tension rising, emotional commitment
Final Chorus: chest belt pushed, high register climax
Last "괜찮아": longest sustain in entire track, This single note defines the emotional peak
Outro: short fade, pad sustain

Single lead vocal
Density expansion only

EXCLUDE: Falsetto, Airy, Whisper, Breathiness, Vibrato, Harmonized, Backing vocals, Choir, Intense, Dramatic, Mumbled
```

조립안 EXCLUDE (주): (없음)

대안 — 인라인 EXCLUDE 줄을 STYLE에서 빼 EXCLUDE로 옮긴 경우: STYLE 737자 · EXCLUDE 11개 (전문은 json `alt_inline_exclude_moved`)

참고:
- Suno 파라미터 숫자 없음: Weirdness·Style Influence가 `기존 싱글`로만 적혀 숫자가 없다.

### 19 그네 ← 이름

- 출처: `SERIES/18-00/concept.md` — `## 12. Track 09 "이름" — 문 열림, 이름 불려짐 (기존 싱글)` (제목줄 1292행) · STYLE 본문 1393-1413행
- 고른 판: 18-00 concept에 STYLE 1개뿐(판 선택 불필요). `기존 싱글`(18-00/concept.md:1292, 1420-1421)로 표시된 곡이며 Closing 트랙.
- BPM 72 ← 18-00/concept.md:1303 구조 표 BPM 72 · 18-00/concept.md:1393 STYLE `72 BPM` · SERIES/RNB-BEST/concept.md:301 파일명 `09__이름__Homecoming__Soft-RnB__72.mp3`
- Key Ab Major ← 18-00/concept.md:1304 구조 표 Key Ab Major · 18-00/concept.md:1393 STYLE `Ab Major`
- 성별 male ← 18-00/concept.md:1305 구조 표 Vocal Male, Solo only · 18-00/concept.md:1397 STYLE `Male vocal:`
- Suno 파라미터: `기존 싱글` (숫자 없음) — 18-00/concept.md:1416-1421
- 별도 EXCLUDE 블록(STYLE 안 인라인 `EXCLUDE:` 줄 18-00/concept.md:1413 (별도 블록 없음)): 없음 — 0개
- STYLE 안 인라인 EXCLUDE 줄(18-00:1413, 11개): Falsetto, Airy, Whisper, Breathiness, Vibrato, Harmonized, Backing vocals, Choir, Intense, Dramatic, Mumbled
- 뺀 말: 없음
- 조립안: 856자 · 21줄 · sha256 `0fdae5b5fb9adffb…` · EXCLUDE 0개

조립안 STYLE (주):

```text
Lo-fi Remix, Korean Soft R&B, 72 BPM, Ab Major

Soft Synth Pad-led, supportive groove, gentle pulse, warm shade texture

Male vocal: Natural, laid-back, Raw, Solid, Direct, Dry
Chest voice dominant, No falsetto, Straight tone, No vibrato, no ad-libs
Precise articulation, clear consonants

Verse1: synth pad, sparse drums, drifting
Verse2: kick steady, groove deepens
Verse2 last 2 lines: higher register, tighter rhythm, vocal push
Bridge1/2: pad and voice, intimate
Bridge3: sparse, tension rising, emotional commitment
Final Chorus: chest belt pushed, high register climax
Last "괜찮아": longest sustain in entire track, This single note defines the emotional peak
Outro: short fade, pad sustain

Single lead vocal
Density expansion only

EXCLUDE: Falsetto, Airy, Whisper, Breathiness, Vibrato, Harmonized, Backing vocals, Choir, Intense, Dramatic, Mumbled
```

조립안 EXCLUDE (주): (없음)

대안 — 인라인 EXCLUDE 줄을 STYLE에서 빼 EXCLUDE로 옮긴 경우: STYLE 737자 · EXCLUDE 11개 (전문은 json `alt_inline_exclude_moved`)

참고:
- Suno 파라미터 숫자 없음: Weirdness·Style Influence가 `기존 싱글`로만 적혀 숫자가 없다.

## 5. 대조·검증 기록

- 물결 대조(브리프 표 15행): `23-00/concept.md` `### 물결` (a)(677자) = 14-00 원곡 STYLE(627자) + `, Modern Indie R&B, Lo-fi Remastered, Articulation` → **일치**. 14-00 원곡 EXCLUDE 13개 = 23-00 물결 `- EXCLUDE:` 줄 → **일치** (항목·순서). 따라서 젠이 채팅에 준 원본 = 14-00 Track 06 Style Prompt로 본다.
- 이 조립안의 물결(15 노을)에는 23:00에서 더한 `Modern Indie R&B, Lo-fi Remastered, Articulation`을 넣지 않았다(젠 「23:00버전이 아닌 원곡 스타일」).
- 8개 원곡 STYLE 모두 `‑`/`-`로 시작하는 제외 항목 0건, `lo-fi remix` 중복 0건, `alt`/`modern` 낱말은 산책·물결의 `Alt` 각 1건뿐(전체 부분문자열 검색으로 확인).
- 원곡 STYLE 모두 줄 끝 공백 0건. 특수문자: 마음밖 `–`·`♭`, 이름 한글 `괜찮아`.
- 골목 보조 자료 `SERIES/Single/골목_youtube.md`에는 STYLE이 없고 BPM 67 · Key Db Major · `Korean Slow R&B Ballad`만 있어 18-00 값과 일치한다. `SERIES/RNB-BEST/concept.md` 발매 파일명 BPM(산책 74 · 먼지 72 · 물안개 80 · 물결 74 · 마음밖 90 · 이름 72 · 골목 67 · 작은 빛 72)도 모두 일치한다.

## 6. 미확정 · 미확인

1. **인라인 EXCLUDE 줄 처리(먼지 · 골목 · 이름)** — 원곡 STYLE 마지막에 `Exclude Style:`/`EXCLUDE:` 줄이 들어 있다. 브리프 규칙 2는 `-` 시작 항목만 옮기라고 했으므로 주 조립안은 STYLE에 그대로 뒀다. STYLE에서 빼 EXCLUDE로 옮길지, 그대로 둘지는 결정이 필요하다(대안 값은 json `alt_inline_exclude_moved`와 2번 표).
2. **먼지의 EXCLUDE 원본** — 같은 절에서 STYLE 속 `Exclude Style:` 줄(8개)과 별도 블록(10개)이 다르다. 어느 쪽이 실제 입력이었는지 concept만으로는 알 수 없다. 주 조립안은 별도 블록 10개를 EXCLUDE로 둔다.
3. **마음밖 BPM** — STYLE은 `96–106 BPM`, 발매 파일명·RNB-BEST는 90. 브리프(젠 「원곡 BPM 그대로」)의 90은 파일명 기준이다. STYLE 숫자를 바꿀지(바꾸면 규칙 2의 "BPM은 바꾸지 않는다"와 부딪힘), 설계 BPM만 90으로 둘지 결정이 필요하다. 마음밖 Key는 `key color like A♭`로 Major/Minor가 없어 gate의 Key 검사 형식에 맞지 않는다.
4. **성별이 설계와 다른 곳** — 16 여름밤(물안개 원곡 남) · 18 벚꽃 · 19 그네(이름 원곡 남). STYLE의 `Male`을 그대로 쓰면 설계(여)와 어긋나고, 바꾸면 "낱말 외에는 바꾸지 않는다"와 부딪힌다. 처리는 오케스트레이터/젠 결정.
5. **산책(14 기타) 900자 초과** — 조립안 955자. 앞붙임만으로도 959자라 `Alt` 제거와 무관하게 초과한다. 줄일 방법(어떤 문장을 뺄지)은 이번 범위 밖이라 손대지 않았다.
6. **Suno 파라미터** — 마음밖 · 물안개 · 작은 빛은 concept에 기록이 없고, 골목 · 이름은 `기존 싱글`로만 적혀 숫자가 없다. 실제 값은 이 저장소에서 확인할 수 없었다(원곡이 있는 Suno 작업공간 화면은 열어 보지 않았다).
7. **작은 빛 제목** — 22-00은 Track Map에 `작은 빛`, 트랙 상세 제목줄에 `작은 손 (Tiny Hand)`이라 적혀 있다. STYLE은 상세 절 한 곳뿐이라 같은 곡으로 보았다. 시리즈 공통 `Exclude Template`(18개)이 이 곡에 쓰였는지는 알 수 없어 EXCLUDE를 비워 뒀다.
8. **설계 BPM·Key** — `.ai/plans/2026-11-01-2300-new-song-styles.json`의 설계 BPM은 11·12·16·17·18·19가 원곡과 다르고(11 라디오 70 vs 72, 12 스웨터 72 vs 90, 16 여름밤 76 vs 80, 17 막차 80 vs 67, 18 벚꽃 78 vs 72, 19 그네 70 vs 72) 13·14·15는 같다. 설계 Key는 11·16·17·18·19가 원곡과 다르고 12(Ab vs `A♭`, 음 이름 같음)·13·14·15는 같다. 젠이 정한 것은 BPM(원곡 그대로)뿐이고 Key는 정한 적이 없다.
9. **원곡 가사·구조에 묶인 문구** — 이름 STYLE의 `Bridge3`·`Last "괜찮아"`, 마음밖 STYLE의 `no catchy hook`(23-00 가사 기준 "후렴 중독성"과 반대 방향). 새 곡 원고는 열어 보지 않아 실제로 충돌하는지는 확인하지 못했다.
10. **여러 줄 STYLE** — 먼지 · 산책 · 물안개 · 작은 빛 · 골목 · 이름은 여러 줄이다(23:00 방식은 한 줄). 줄바꿈을 유지했고 글자 수에 1자씩 셌다. Suno 입력창에서 줄바꿈이 어떻게 처리되는지는 이번에 확인하지 않았다.

## 재현

- 이 두 파일은 `SERIES/04-00` · `14-00` · `18-00` · `22-00` `concept.md`의 지정 행을 프로그램으로 읽어(다시 타이핑하지 않음) 만들었다. 스크립트: `/private/tmp/claude-501/-Users-zenkim-office-Project-wavvy/b2585a9e-89e5-48a0-b2cb-d35470aebd29/scratchpad/build_original_styles.py` 와 `build_md.py` (저장소 밖, 커밋 대상 아님).
