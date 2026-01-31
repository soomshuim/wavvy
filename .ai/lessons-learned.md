# Lessons Learned - vibe-m

> 버그 패턴 및 해결책 기록
>
> Last updated: 2026-01-25

---

## 🎛️ Suno 파라미터 성공 패턴

### R&B 발라드 최적 파라미터

**날짜**: 2026-01-25

**장르**: Slow R&B Ballad, Lo-fi R&B, Soft R&B

**성공 파라미터**:
| 항목 | 값 | 효과 |
|------|-----|------|
| **Weirdness** | 35 | 가성 제거 + 진성 유지, 안정적 |
| **Style Influence** | 65 | Style Prompt 영향력 적절히 유지 |

**적용 사례**:
- AM_0400 (Slow R&B, 9곡) - 진성 보컬 안정적
- PM_1400 (Soft R&B, 10곡) - 담백한 톤 유지

**장르별 파라미터 가이드**:
| 장르 | Weirdness | Style Influence | 비고 |
|------|-----------|-----------------|------|
| **R&B 발라드** | **35** | **65** | 기본값, 안정적 |
| **공격적 (프롬프트 강화)** | 35 | 70 | Style Prompt 의존도 높일 때 |
| **실험적 (장르 변화 감수)** | 40 | 60 | 새로운 느낌 시도 시 |

**재발 방지**:
- R&B 발라드 계열은 W:35, I:65로 시작
- 문제 발생 시 Style Influence 먼저 조정 (±5)
- Weirdness는 가성/불안정 문제 시에만 조정

---

## 🎤 보컬 프롬프트 성공/실패 패턴

### Raw Vocal Baseline 성공 패턴 (Track 07)

**날짜**: 2026-01-19

**상황**: 가성 과다 + 더블링 코러스 + 힘없는 보컬 문제 해결

**이전 실패 증상**:
- 가성이 너무 많음
- 더블링/코러스 레이어 과다
- 힘있는 진성 보컬이 안 나옴

**실패 원인 분석**:

| 실패 키워드 | 문제 | Suno 해석 |
|------------|------|----------|
| `warm reflective tone` | 모호한 형용사 | Airy/Ethereal로 해석 → 가성 |
| `rich vibrato` | 결과 묘사 | 가성 비브라토 유발 |
| `Subtle R&B ad-libs` | 애드립 요청 | 더블링으로 해석 |

**성공 패턴 (3중 안전장치)**:

```
1) Style Prompt:
   Raw vocal, Powerful, Solid, Direct, Dry, Unprocessed
   Chest voice dominant. No falsetto. Strong vocal attack.

2) 가사 메타태그:
   [Direct vocal, No harmony] - Verse
   [Powerful belt, No backing vocals] - Chorus
   [Chest voice] - Bridge

3) Exclude:
   Airy, Falsetto, Harmonized, Backing vocals, Whisper, Auto-tune
```

**핵심 인사이트**:

| 원칙 | 설명 |
|------|------|
| 긍정형 > 부정형 | "Chest voice dominant" > "No falsetto" |
| 구체적 > 추상적 | "Raw, Powerful, Solid" > "warm reflective" |
| 3중 안전장치 | Style + 메타태그 + Exclude 동시 적용 |
| 피해야 할 단어 | Airy, Falsetto, Harmonized, Whisper, Ethereal, Opera |

**재발 방지 체크리스트**:
- [ ] Style에 `Raw, Powerful, Solid, Direct` 포함?
- [ ] `Chest voice dominant` 문장 있음?
- [ ] Exclude에 `Airy, Falsetto, Whisper` 포함?
- [ ] 가사에 `[Direct vocal]`, `[Powerful belt]` 메타태그 있음?
- [ ] `warm`, `reflective`, `rich vibrato` 같은 모호한 형용사 제거?

---

## FFmpeg 버그 패턴

### 필터 그래프 인덱싱 오류

**날짜**: 2026-01-18

**상황**: 3개 트랙 크로스페이드 병합 시도

**증상**:
```
Filter 'acrossfade:default' has output 1 (a01) unconnected
Error binding filtergraph inputs/outputs: Invalid argument
```

**원인**:
```python
# 잘못된 코드
for i in range(2, num_tracks):
    prev_label = f"a{str(i-2).zfill(2)}"  # i=2일 때 a00 (틀림)
    curr_label = f"a{str(i-1).zfill(2)}"  # i=2일 때 a01 (중복)
```

생성된 필터:
```
[0][1]acrossfade[a01];[a00][2]acrossfade[a01]  # 틀림
```

**해결**:
```python
# 올바른 코드
for i in range(2, num_tracks):
    prev_label = f"a{str(i-1).zfill(2)}"  # i=2일 때 a01
    curr_label = f"a{str(i).zfill(2)}"    # i=2일 때 a02

final_label = f"a{str(num_tracks-1).zfill(2)}"
```

생성된 필터:
```
[0][1]acrossfade[a01];[a01][2]acrossfade[a02]  # 맞음
```

**재발 방지**:
- 필터 그래프 수정 시 반드시 출력 로그로 확인
- 라벨 체인: `[0][1]→[a01]`, `[a01][2]→[a02]`, `[a02][3]→[a03]`

---

## ffmpeg-normalize 버그 패턴

### subtitles + drawtext 필터 충돌 (Shorts 자막)

**날짜**: 2026-01-21

**상황**: Shorts 영상에 SRT 자막(subtitles)과 훅 문구(drawtext)를 동시 적용

**증상**:
- `subtitles` 필터의 `force_style` 옵션 사용 시 자막이 렌더링되지 않음
- 훅 문구(drawtext)만 표시됨

**원인**:
- `force_style` 내부의 쉼표가 FFmpeg 필터 구분자로 해석됨
- 필터 체인이 깨져서 subtitles가 무시됨

**테스트 결과**:
```bash
# ✅ 성공: force_style 없이 단순 subtitles
-vf "crop=...,subtitles=/tmp/test.srt,drawtext=..."

# ❌ 실패: force_style 쉼표 문제
-vf "crop=...,subtitles=...:force_style='Fontname=X,Fontsize=28',drawtext=..."

# ✅ 성공: force_style 쉼표 이스케이프
-vf "crop=...,subtitles=...:force_style='Fontname=X\\,Fontsize=28',drawtext=..."
```

**해결 (진행 중)**:
1. `force_style` 내부 쉼표를 `\\,`로 이스케이프
2. 필터 순서: crop → subtitles → drawtext (subtitles가 drawtext보다 먼저)

**주의사항**:
- `ffmpeg` 기본 설치에는 subtitles/drawtext 필터 없음
- `ffmpeg-full` 필요 (`/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg`)

**재발 방지**:
- FFmpeg 필터 옵션 내부 쉼표는 항상 이스케이프
- 복잡한 필터 체인은 단계별로 테스트

---

### PATH 문제

**날짜**: 2026-01-18

**상황**: `pack` 커맨드에서 정규화 실행

**증상**:
```
ffmpeg-normalize not found. Install with: pip install ffmpeg-normalize
```

**원인**:
- pip 설치 시 CLI가 `~/Library/Python/3.9/bin/`에 설치됨
- 해당 경로가 시스템 PATH에 없음

**해결**:
```python
# 변경 전
cmd = ['ffmpeg-normalize', ...]

# 변경 후
cmd = [sys.executable, '-m', 'ffmpeg_normalize', ...]
```

**재발 방지**:
- Python CLI 도구는 `python -m` 방식으로 호출

---

### MP3 출력 형식 오류

**날짜**: 2026-01-18

**상황**: 정규화 후 MP3로 저장 시도

**증상**:
```
Output extension mp3 does not support PCM audio.
Please choose a suitable audio codec with the -c:a option.
```

**원인**:
- ffmpeg-normalize는 기본적으로 PCM 출력
- MP3는 PCM을 직접 담을 수 없음

**해결**:
```python
# 변경 전
norm_path = paths.norm_tracks_dir / f"norm_{track.path.name}"  # .mp3

# 변경 후
norm_path = paths.norm_tracks_dir / f"norm_{track.path.stem}.wav"  # .wav
```

**재발 방지**:
- 중간 파일은 WAV 형식 사용
- 최종 출력만 압축 포맷 (AAC/MP3) 적용

---

## 경로 버그 패턴

### 잘못된 경로 탐색

**날짜**: 2026-01-18

**상황**: `series/test_pilot/2026-01-18` 경로 검증 시도

**증상**:
- 존재하지 않는 경로로 validate 시도
- 실제 경로: `series/TestSeries/2026-01-18`

**원인**:
- 경로명 추측 (확인 없이 진행)

**해결**:
- `ls -laR` 또는 `find`로 실제 구조 확인 후 진행

**재발 방지**:
- 경로 작업 전 항상 실제 구조 확인
- 문서에 실제 예시 경로 명시

---

## 가사 작성 버그 패턴

### 괄호 주석 혼입

**날짜**: 2026-01-18

**상황**: Track 04 가사 초안 작성 시 설명용 괄호 포함

**증상**:
```
가로등이 번져가
젖은 바닥 위로
걸음을 멈춰도
발자국만 남아 (4행, 각 5-6음절)  ← 괄호 혼입
```

**원인**:
- 가사와 설명 주석을 같은 코드블록에 작성
- LYRICS.md 2.1 "괄호 속 지시어 금지" 규칙 위반

**리스크**:
- 사용자가 복사해서 Suno에 붙여넣으면 괄호 텍스트를 가사로 인식
- 보컬이 "(4행, 각 5-6음절)"을 읽어버림

**해결**:
```markdown
# 잘못된 방식 (가사 블록 내 주석)
[verse1]
가로등이 번져가 (스냅샷)

# 올바른 방식 (가사와 분석 분리)
## 가사
[verse1]
가로등이 번져가

## 분석
- V1 1행: 스냅샷 (명사+동사)
```

**재발 방지**:
- 가사 코드블록은 **순수 가사만** 포함
- 분석/설명은 별도 섹션으로 분리
- 가사 제시 후 체크리스트 테이블로 검증 결과 제시
- **의도한 효과(스냅샷 훅, V2 에스컬레이션 등)는 Style Prompt에서 지시**

---

## 체크리스트 요약

### Style Prompt 작성 시 (Raw Vocal Baseline)
- [ ] `Raw, Powerful, Solid, Direct, Dry` 포함?
- [ ] `Chest voice dominant` 문장 있음?
- [ ] `Strong vocal attack` 또는 `Belting` 포함?
- [ ] Exclude에 `Airy, Falsetto, Whisper, Harmonized` 포함?
- [ ] 모호한 형용사 제거? (`warm reflective`, `rich vibrato` 등)
- [ ] husky/airy 별도 요청 없으면 Raw Vocal Baseline 적용?
- [ ] **Articulation 포함?** (`Precise articulation, clear consonants`)
- [ ] **Reverb 포함?** (`Moderate reverb, room ambience` 등)
- [ ] **Sound Engineering 포함?** (`EQ balanced sound, clean mix`)

### 가사 메타태그 적용 시
- [ ] Verse에 `[Direct vocal, No harmony]` 있음?
- [ ] Chorus에 `[Powerful belt, No backing vocals]` 있음?
- [ ] Bridge에 `[Chest voice]` 있음?
- [ ] 메타태그는 구조 태그 바로 뒤 별도 행에 배치?

### FFmpeg 작업 전
- [ ] 필터 라벨 체인 로직 확인
- [ ] 디버그 로그로 생성된 필터 출력

### Python CLI 도구 사용 시
- [ ] `python -m` 방식 우선 사용
- [ ] 중간 파일은 무손실 포맷 (WAV)

### 경로 작업 전
- [ ] 실제 디렉토리 구조 확인
- [ ] 문서와 실제 구조 동기화

### 가사 작성 시
- [ ] 가사 코드블록에 괄호/주석 없음 확인
- [ ] 분석/설명은 별도 섹션으로 분리
- [ ] 복사해서 Suno에 바로 붙여넣기 가능한 상태인지 확인
- [ ] **V1-V2 행 수 동일 확인** (Case 11)
- [ ] **Chorus 3~4행 이내 확인** (Case 12)
- [ ] **Bridge Thesis B1=B2 동일 확인** (Case 13)
- [ ] **다른 트랙 제목 키워드 사용 금지** (Case 13)
- [ ] **보컬 제어 메타태그 포함 확인** (구조 태그만 있고 메타태그 없으면 FAIL)

### 시드곡 디자인 시 (레퍼런스 기반)
- [ ] **레퍼런스 DNA 체크리스트 먼저 작성?** (제목톤/가사톤/역설구조/훅형태/BPM/보컬성별)
- [ ] **제목 톤이 레퍼런스와 일치?** (밝음/어둠/중립)
- [ ] **역설 구조 보존?** (밝은 제목 + 어두운 가사 등)
- [ ] **훅 형태 일치?** (선언문/의문문/명령문)
- [ ] **BPM 및 체감 속도 일치?** (풀타임 vs 하프타임)
- [ ] **보컬 성별/구성 정확?** (보이밴드/걸그룹/혼성/솔로)
- [ ] **DNA 불일치 시 재설계?** (분석만 하고 적용 망각 방지)

---

## 가사 구조 버그 패턴 (Track 06 교정)

### "다른 컨셉" 시도 시 구조 붕괴

**날짜**: 2026-01-19

**상황**: Track 06 가사 작성 시 "이전 곡들과 다른 느낌"을 주려고 시도

**증상**:
- V1: 4행 (22음절)
- V2: 6행 (36음절)
- Chorus: 6행 (표준 3~4행 초과)

**원인**:
- "다른 컨셉 = 다른 구조"로 잘못 해석
- LYRICS.md 1.1 Metric Mirroring 규칙 망각

**리스크**:
- Suno가 V2를 V1 멜로디에 억지로 얹으려다 멜로디 붕괴
- Chorus가 너무 길어 리스너 피로감

**해결**:
```
❌ "다른 느낌" = 행 수 변경
✅ "다른 느낌" = 단어 선택, 감각 변경 (구조는 동일 유지)
```

**재발 방지 체크리스트**:
1. V1 작성 후, V2 작성 전에 V1 구조 메모
2. V2 작성 시 V1 구조 그대로 복사 후 단어만 변경
3. Chorus는 무조건 3~4행으로 제한
4. "다른 느낌"이 필요하면 → 단어/이미지 축 변경, 구조 변경 X

---

### Bridge Thesis 변경 + 키워드 충돌

**날짜**: 2026-01-19

**상황**: Track 06 Bridge2 Thesis를 B1과 다르게 작성

**증상**:
```
B1 Thesis: "적막이 더 깊어져"
B2 Thesis: "사라지는 윤곽뿐" ← 변경 + Track 02 제목 "윤곽" 사용
```

**원인**:
- Bridge Anchor Rule (1.4) "Thesis는 B1=B2 동일" 규칙 망각
- Vocabulary Independence (1.5) 규칙 망각

**해결**:
```
❌ B1 Thesis ≠ B2 Thesis
✅ B1 Thesis = B2 Thesis (항상 동일)

❌ 다른 트랙 제목 키워드 사용
✅ 현재 트랙의 컨셉 키워드만 사용
```

**재발 방지 체크리스트**:
1. Bridge 작성 전 Thesis 문장 먼저 확정
2. B1, B2 모두 동일한 Thesis 사용
3. Thesis 작성 시 기존 트랙 제목 목록 확인
4. 기존 제목과 겹치는 키워드 절대 금지

---

## 시드곡 디자인 버그 패턴

### 레퍼런스 DNA 미반영 (PM_1600 Track 01 실패)

**날짜**: 2026-01-30

**상황**: DAY6 "HAPPY" 레퍼런스 분석 후 시드곡 "시계" 설계

**증상**:
```
❌ 제목 "시계" = 중립적 단어 (HAPPY처럼 밝지 않음)
❌ Female vocal 설정 (DAY6는 보이밴드)
❌ 160 BPM 풀타임 (HAPPY는 80 하프타임 체감)
❌ 역설 구조 없음 (밝은 제목 + 어두운 가사)
```

**원인**:
- 레퍼런스 핵심 DNA 추출 후 **적용 검증 없이 설계 시작**
- "밴드락" 키워드에만 집중, 레퍼런스의 **정서 구조(역설)** 망각
- 보이밴드 vs 혼성그룹 구분 실패

**HAPPY DNA (핵심)**:
| 요소 | 설명 |
|------|------|
| 역설 구조 | 밝은 단어(HAPPY) + 어두운 가사("행복해도 되나요?") |
| 의문형 훅 | 선언 X, 질문 O ("May I be happy?") |
| 에너지 보류 | 160 BPM but 80 half-time feel ("뛰고 싶지만 못 뛰는") |
| 결론 없음 | 해결 X, 인정 O (질문으로 끝남) |

**해결 (재설계)**:
```
✅ 제목 "끝" = 해방/밝음을 연상시키는 단어 (역설 구조 가능)
✅ Male vocal, Boy band style
✅ 80 BPM half-time feel (체감 속도 일치)
✅ 의문형 훅 "끝나도 되나요" (HAPPY 구조 복제)
✅ 답 없이 질문으로 끝남
```

**재발 방지 체크리스트 (시드곡 설계 시 필수)**:

```
□ Step 0: 레퍼런스 DNA 체크리스트 작성
  - 제목 톤 (밝음/어둠/중립)
  - 가사 톤 (밝음/어둠/중립)
  - 역설 구조 유무
  - 훅 형태 (선언문/의문문/명령문)
  - BPM 및 체감 속도
  - 보컬 성별 및 구성

□ Step 1: 시드곡 초안 작성 후 DNA 대조
  - 제목 톤이 레퍼런스와 일치하는가?
  - 역설 구조가 보존되었는가?
  - 훅 형태가 동일한가?
  - BPM/체감이 일치하는가?
  - 보컬 성별/구성이 정확한가?

□ Step 2: 불일치 시 재설계
  - DNA 불일치 항목 명시
  - 해당 항목 수정 후 재검증
```

**핵심 인사이트**:
```
레퍼런스 분석 ≠ 레퍼런스 적용

분석만 하고 설계 시 망각하면 의미 없음
→ DNA 체크리스트를 설계 단계에서 강제 대조
→ "이 시드곡이 레퍼런스 DNA를 얼마나 복제했는가?" 질문 필수
```
