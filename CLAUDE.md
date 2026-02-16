# Claude Code Instructions - vibe-m

Version: 2.13.3
Last Updated: 2026-02-16
Purpose: YouTube Music Playlist Generator CLI 실행 매뉴얼 (비-SSOT 요약)

## ⚠️ SSOT 경고

> **이 문서는 "사용 매뉴얼"입니다. 규칙의 SSOT가 아닙니다.**
>
> | 규칙 유형 | SSOT 문서 |
> |----------|----------|
> | 가사 규칙 | `MASTER/LYRICS.md` |
> | Style Prompt 규칙 | `MASTER/STYLE.md` |
> | QC/운영 규칙 | `MASTER/MANAGER.md` |
> | 역할 분리 | `MASTER/ROLES.md` |
>
> **아래 체크리스트는 "요약"입니다. 충돌 시 MASTER 문서가 우선합니다.**

## Quick Reference

| 용도 | 파일 |
|------|------|
| **24H Universe Bible** | `MASTER/24H_UNIVERSE.md` |
| **운영 마스터 플랜** | `MASTER/MANAGER.md` |
| **가사 공학 규칙** | `MASTER/LYRICS.md` |
| **사운드/스타일 가이드** | `MASTER/STYLE.md` |
| **플레이리스트 컨셉 가이드** | `MASTER/PLAYLIST_GUIDE.md` |
| **타이틀 생성 규칙 (SSOT)** | `MASTER/PLAYLIST_GUIDE.md` §0 |
| **역할 분리 시스템** | `MASTER/ROLES.md` |
| **사람용 운영 매뉴얼** | `MASTER/QUICK_REF.md` |
| **역할별 프롬프트** | `MASTER/ROLES.md` 내 정의 |
| CLI 스펙 | `MASTER/VIBE-M_Master_Plan.md` |
| CLI 코드 | `vibem.py` |
| 버그 패턴 | `.ai/lessons-learned.md` |
| 현재 상태 | `.ai/SESSION.md` |
| 인기 사례 분석 PDF | `Reference/유튜브 감성 플레이리스트 인기 사례 분석.pdf` |
| **Suno 실전 가이드 (필수)** | `Reference/museA_suno_guide.md` |
| **시티팝 장르 루브릭** | `MASTER/rubrics/CITYPOP_RUBRIC.md` |
| **Fast Lo-fi 장르 루브릭** | `MASTER/rubrics/FAST_LOFI_RUBRIC.md` |

## Hard Constraints (절대 제약)

> 출처: `MASTER/MANAGER.md` Phase 0

1. **NO Pydub** - 메모리 누수 방지
2. **Pure FFmpeg** - `ffmpeg-python` 또는 `subprocess`만 사용
3. **Sequential Acrossfade** - 단순 concat 금지
4. **Fail Fast** - 입력 검증 실패 시 즉시 종료
5. **Pure Input Principle** - Suno 가사란에 가사 + 구조 태그 + 구조 직후 1행 `()` 메타만 (설명형 지시어 금지)

## Auto Reference Rules

| 요청 유형 | 참조 문서 | 읽을 범위 |
|----------|----------|----------|
| **24H Universe 트랙 생성** | `MASTER/24H_UNIVERSE.md` | 전체 (필수) |
| **플레이리스트 컨셉 논의/시작** | `MASTER/PLAYLIST_GUIDE.md` | 전체 (필수) |
| **플레이리스트 타이틀 생성** | `MASTER/PLAYLIST_GUIDE.md` | Section 0 (SSOT) |
| **가사 작성/수정** | `MASTER/LYRICS.md` + `Reference/museA_suno_guide.md` | 전체 + §3-4 |
| **Style Prompt 작성** | `MASTER/STYLE.md` + `Reference/museA_suno_guide.md` | 전체 + §2,6 |
| 플레이리스트 프로파일 | `MASTER/STYLE.md` | Section 3 |
| QC/Fail Fast 기준 | `MASTER/MANAGER.md` | Section 1, 3 |
| 역할 분리/AI 작업 | `MASTER/ROLES.md` | 전체 |
| FFmpeg 필터 작업 | `.ai/lessons-learned.md` | "필터 그래프 버그" 섹션 |
| 정규화 작업 | `.ai/lessons-learned.md` | "ffmpeg-normalize 버그" 섹션 |
| 새 커맨드 추가 | `MASTER/VIBE-M_Master_Plan.md` | CLI 커맨드 명세 |
| **곡 발음 수정** | `Reference/museA_suno_guide.md` | §7 Cover 기능 |
| **City Pop 트랙 QA** | `MASTER/rubrics/CITYPOP_RUBRIC.md` | 전체 (필수) |
| **Fast Lo-fi 트랙 QA** | `MASTER/rubrics/FAST_LOFI_RUBRIC.md` | 전체 (필수) |

## Workflow Checklists

### 가사/Style Prompt 제안 워크플로우 (필수)

**원칙**: 체크리스트 기반 출력 + 누락 검증 강제
> "자유 생성"이 아니라 **"이걸 다 포함했는지 증명해라"**가 핵심

**가사 생성 요청 시:**
```
Step 0. LYRICS.md + 이전 트랙 키워드 확인
        + 크로스시리즈 컨셉 겹침 검증 (v2.11 NEW):
          SERIES/ 내 모든 concept.md 트랙리스트 스캔
          장소(location) + 감정(emotion) + 상황(situation) 3축 비교
          → 3축 중 2개 이상 겹침 = FAIL → 장소/컨셉 변경 후 재설계 (유저 제안 금지)
Step 0.5. museA 가이드 참조 (v2.9 NEW):
         - §3 구조 공식 (Pop Standard/K-POP Standard 등) 선택
         - §4 메타태그 규칙 ([AA] 절대 안 읽음, (BB) 조건부)
Step 1. Generate 가사 초안
Step 2. Run self-QC against checklist (10개 항목)
Step 3. Korean Positioning 검증 (K1-K3)
Step 4. 메타태그 검증 (v2.8 NEW):
        - [AA] 대괄호: 구조/보컬 메타만 (감정/분위기 태그 금지)
        - (BB) 소괄호 톤지시: 반드시 단독 행에 배치
        - 감정/분위기 태그 발견 시 → Style로 이동
Step 5. 장르 게이트 (v2.10 NEW):
        IF genre = City Pop → rubrics/CITYPOP_RUBRIC.md 실행
        → 총점 ≥ 80 AND 개별 팩터 > 5 → PASS
        → 미달 시 재디자인 (유저 제안 금지)
        IF genre = Fast Lo-fi → rubrics/FAST_LOFI_RUBRIC.md 실행
        → 총점 ≥ 80 AND 개별 팩터 > 5 → PASS
        → 미달 시 재디자인 (유저 제안 금지)
        IF genre includes Hip-hop/Rap → LYRICS.md §1.12 H1-H5 실행
        → H1-H5 중 2개 이상 FAIL 시 재디자인 (유저 제안 금지)
Step 6. If all pass → output with QC 테이블
        If any fail → 재작성 후 Step 2 반복
        (통과할 때까지 유저에게 제안하지 않음)
Step 6.5. 패턴 고착 검사 (v2.12 NEW):
         - 이전 트랙들과 톤앤매너/서술 방식 비교
         - "~하고 / ~해" 같은 패턴 반복 감지 시 → FAIL
         - 3회 수정 후에도 유사 시 → Clean Slate Protocol 발동
           (ROLES.md § Clean Slate Protocol 참조)
```

**Style Prompt 생성 요청 시:**
```
Step 0. STYLE.md Required Slots 확인
Step 0.5. museA 가이드 참조 (v2.9 NEW):
         - §2 조합 공식: "핵심을 앞에" (Genre/BPM 첫 3-5단어)
         - §6 공간감/다이내믹 프롬프트 1-2개 선택
         - §1 Tag Bank에서 장르/악기/보컬 키워드 선택
Step 1. Generate Style Prompt (압축 버전)
Step 2. Run self-QC against checklist (20개 슬롯)
Step 3. 글자수 검증 (공백 포함 문자 수 기준, <= 900자 확인)
Step 4. 장르 게이트 (v2.10 NEW):
        IF genre = City Pop → rubrics/CITYPOP_RUBRIC.md 실행
        → 총점 ≥ 80 AND 개별 팩터 > 5 → PASS
        → 미달 시 재디자인 (유저 제안 금지)
        IF genre = Fast Lo-fi → rubrics/FAST_LOFI_RUBRIC.md 실행
        → 총점 ≥ 80 AND 개별 팩터 > 5 → PASS
        → 미달 시 재디자인 (유저 제안 금지)
Step 5. If all pass → QC 테이블 + 글자수와 함께 output
        If any fail → 수정 후 Step 2 반복
        (검증 통과 전 유저에게 제안 금지)
Step 6. .txt 파일 저장 + pbcopy ← v2.5 NEW
        (채팅 UI 공백 문제 우회)
Step 7. Style Prompt + Exclude 반드시 세트로 출력 ← v2.6 NEW
        (Exclude 누락 방지)
```

**곡 길이 확장 규칙 (v2.6 NEW):**
```
문제: 긴 곡 필요 시 가사를 과하게 늘리면 반복감 증가

해결: 가사 행 수는 유지하고, 구조 태그로 길이 확보
     → [interlude], [instrumental], [bridge] 추가
     → Verse 8행 이상 금지 (4행 권장)
     → Chorus 반복 횟수로 길이 조절

예시 (3분 → 4분 확장):
❌ Verse1 4행 → 8행 (가사 2배)
⭕ Verse1 4행 유지 + [interlude] 추가 + Chorus 3회 반복
```

**Style Prompt + Exclude 세트 출력 규칙 (v2.6 NEW):**
```
원칙: Style Prompt 출력 시 반드시 Exclude Style도 함께 출력

출력 형식:
### Style Prompt
```(코드블록)
...
```(닫기)

### Exclude Style
```(코드블록)
Falsetto, Airy, Whisper, ...
```(닫기)

→ 둘 중 하나만 출력 = INVALID
→ txt 파일도 style.txt + exclude 포함 또는 별도 파일
```

---

### 가사 필수 슬롯 체크리스트 (요약)
> **SSOT: `MASTER/LYRICS.md`** — 충돌 시 원본 우선
> **원칙: 하나라도 누락 시 FAIL → 재작성 후 통과 시 제안**

| # | 규칙 | 체크 내용 |
|---|------|----------|
| 1.1 | Metric Mirroring | V1-V2 음절 수 동일 |
| 1.2 | Ending Mirroring | **행 끝 품사 엄격 일치** (동사↔동사, 형용사↔형용사) |
| 1.3 | Chorus Static | 3~4행, 100% 동일 반복 |
| 1.4 | Bridge Anchor | Thesis 1라인 고정 + Scene 2~3라인 변주 |
| 1.5 | Vocabulary Independence | 이전 트랙과 핵심 키워드 겹침 없음 |
| 1.6 | Snapshot Hook | Chorus 1-2행 명사+동사 |
| 1.7 | Bridge Thesis | 현상 기반 (사람 의존 X) |
| 1.8 | V2 Escalation | 마지막 2행 신체 반응/감정 상승 |
| 1.9 | Physical Object Anchor | **각 섹션에 물성 오브젝트 1개 이상** (추상어 과밀 금지) |
| **1.10** | **Image Density** | **V1=공간, V2=감각 분리 (핵심 이미지 2개 이상 겹침 금지)** |
| **1.11** | **Chorus Tone** | **직접 호소/명령형 최대 1개, 나머지 관조 톤** |
| **1.12** | **Cross-Series Independence** | **다른 시리즈 concept.md와 장소+감정+상황 3축 중 2개 이상 겹침 없음** |
| **H1-H5** | **Hip-hop Flow/Rhyme Gate** | **Hip-hop/Rap일 때만 적용: flow 길이/강세/라임/훅 분리 QC** |
| 2.1 | Pure Input | 설명형 괄호 금지, 구조 직후 1행 `()` 메타 허용 (Performance Cue 포함) |
| **2.3** | **메타태그 동작** | **`[AA]`=구조(낭독X), `(BB)`=조건부(톤지시 단독행), 감정태그→Style** |
| **2.2** | **메타태그 필수** | **LYRICS.md §2.2 SSOT 참조** (구조 태그 + 보컬 메타태그 세트 필수) |
| 2.4 | Length Guide | **전체 100-120 단어, 섹션당 4-6행** |
| **K1** | **Korean Only** | **한국어여야만 성립하는 가사인가?** |
| **K2** | **Translation Loss** | **영어 번역 시 힘 빠지는 지점 있는가?** |
| **K3** | **Dual Satisfaction** | **배경음악 OK + 읽으면 문장으로 남는가?** |

**검증 출력 포맷:**
```
Section A: 가사 (전문)
Section B: QC Validation (각 항목 ✓/✗)
Section C: Korean Positioning (K1-K3 ✓/✗) ← v1.7 NEW
Section D: 키워드 축 요약 (이전 트랙과 비교)
Section E: Cross-Series 겹침 검증 (v2.11 NEW) ← SERIES/ 전체 concept.md 대조
Section F: Hip-hop Flow/Rhyme (H1-H5 ✓/✗, Hip-hop/Rap일 때만) ← v2.13.1 NEW
```

---

### Style Prompt 필수 슬롯 체크리스트 (요약)
> **SSOT: `MASTER/STYLE.md`** — 충돌 시 원본 우선
> **원칙: 하나라도 누락 시 FAIL 선언 → 출력 금지**

| # | 슬롯 | 체크 내용 | 예시 |
|---|------|----------|------|
| S0 | **핵심 앞에** | Genre/BPM이 첫 5단어 내 | "Korean Lo-fi R&B, 80 BPM, ..." |
| S1 | **Raw Vocal Baseline** | `Raw, Solid, Direct, Dry` | 기본값 (powerful/husky/airy 요청 시 추가) |
| S2 | Vocal Persona | gender + 발성 타입 | "Contralto female" 또는 "Deep male vocal" |
| S3 | **Chest Voice 강제** | `Chest voice dominant` 문장 | 진성 보컬 확보 |
| S4 | Vocal Processing | dry/close-mic 여부 | "dry close-mic, Unprocessed" |
| S5 | Lead Instrument | 메인 악기 | "Felt Piano-led" |
| S6 | Rhythm Source | 리듬 요소 | "soft brush kit, layback groove" |
| S7 | BPM | 템포 | "82 BPM" |
| S8 | Key | 조성 | "Eb Major" |
| S9 | Musicality Matrix | V2/Chorus/Bridge/Outro 지시 | "Verse2 stronger dynamics..." |
| S10 | Harmony Guard | 레이어 금지 명시 | "No harmony, no backing vocals, no doubles" |
| S11 | Chorus Layer Block | 코러스 레이어 완전 차단 | "Lead vocal remains single and dominant" |
| S12 | Exclude 필수 항목 | **Airy, Falsetto, Whisper, Harmonized** | 얇은 보컬 유발 단어 차단 |
| S13 | Exclude 제한 | **최대 3그룹, 8키워드** (기본 1줄 권장) | 과도한 Exclude = 부작용 |
| S14 | **모호 형용사 제거** | warm reflective, rich vibrato 등 제거 | 가성 유발 방지 |
| **S15** | **글자수 제한** | **<= 900자 (공백 포함 문자)** | 출력 전 문자수 검증 |
| **S16** | **Lead Instrument Supportive** | **`[악기]-led, supportive` 형태** | 악기 과도한 존재감 방지 |
| **S17** | **Chorus Expansion Density** | **`arrangement density only` 명시** | 스테레오/볼륨 해석 방지 |
| **S18** | **Articulation (필수)** | **`articulation`** | 발음 명확성 확보, 웅얼거림 방지 |
| **S19** | **Reverb (필수)** | **`Moderate reverb, room ambience`** | 공간감 제어 |
| **S20** | **Sound Engineering (필수)** | **`EQ balanced sound, clean mix`** | 믹스 품질 확보 |

**검증 프로세스:**
```
Step 0. powerful/husky/airy 별도 요청 있는지 확인
Step 1. 없으면 Raw Vocal Baseline 적용
Step 2. Run self-QC against checklist (20개 슬롯) ← v2.6.2 UPDATE
Step 3. 글자수 검증 (공백 포함 문자 수 <= 900) ← v2.2 NEW
Step 4. If all pass → QC 테이블과 함께 output
        If any fail → STOP + 수정 후 Step 2 반복
        (검증 통과 전 유저에게 제안 금지)
```

**Raw Vocal Baseline (기본값):**
```
Raw vocal, Solid, Direct, Dry, Unprocessed
Chest voice dominant. No falsetto.
```

**요청 시 추가:**
- `powerful` 요청 → Powerful, Strong attack 추가
- `husky` 요청 → Raspy, Grit 추가
- `airy` 요청 → Airy, Breathy 허용

**Exclude 필수 항목:**
```
Airy, Falsetto, Harmonized, Backing vocals, Whisper, Auto-tune
```

**피해야 할 모호한 형용사:**
- ❌ `warm reflective tone` → Airy/Ethereal로 해석됨
- ❌ `rich vibrato` → 가성 비브라토 유발
- ❌ `Subtle R&B ad-libs` → 더블링으로 해석됨
- ✅ `Raw, Powerful, Solid, Direct` → 구체적 발성 키워드

---

### Style Prompt Suno 최적화 규칙 (v2.2 NEW)

**글자수 제한:**
```
- Suno Style Prompt 제한: <= 900자 (공백 포함 문자 기준)
- 출력 전 반드시 문자수로 검증
- 검증 없이 유저에게 제안 금지
```

**Lead Instrument Supportive 규칙:**
```
❌ Vibraphone-led (악기 과시 리스크)
⭕ Vibraphone-led, supportive (보조 역할 명시)

→ "supportive" 하나로 "주인공 아님" 각인
→ 재즈화/솔로 과시 방지
```

**Chorus Expansion Density 규칙:**
```
❌ Chorus expansion by arrangement only (모호)
⭕ Chorus expansion by arrangement density only (명확)

→ 스테레오/볼륨 해석 여지 차단
→ 보컬 스택 방지 강화
```

**Outro Motif Restate 규칙:**
```
❌ vibraphone solo (연주 과시 느낌)
⭕ vibraphone restates motif softly (정리 느낌)

→ 재즈 솔로 치우침 방지
→ 플레이리스트 반복 재생 안정성 확보
```

**Style Prompt QC 출력 포맷:**
```
| 항목 | 상태 |
|------|------|
| 글자수 | [N]자 ✓/✗ (<= 900, 공백 포함 문자) |
| S0-S20 | ✓/✗ |

→ 모든 항목 ✓ 시에만 유저에게 제안
```

**복사용 파일 저장 규칙 (v2.5 NEW):**
```
문제: 채팅 UI 렌더링 시 공백이 대량 추가됨
     → 복사-붙여넣기 시 글자수 5000자+ 초과 발생

해결: Style Prompt / 가사 완성 시 .txt 파일로 저장 + pbcopy
     → SERIES/[시리즈]/track[NN]_style.txt
     → SERIES/[시리즈]/track[NN]_lyrics.txt

워크플로우:
Step 1. 텍스트 완성 → .txt 파일로 Write
Step 2. 공백 포함 문자 수로 글자수 검증
Step 3. cat [파일] | pbcopy 로 클립보드 복사
Step 4. 유저에게 "Cmd+V로 붙여넣기" 안내
```

---

### Suno Parameters 필수 기록 (v2.4 NEW)

> **트랙 생성 시 반드시 Weirdness/Style Influence 제안 및 기록**

**기본값 (VIBE-M 권장):**
| 항목 | 값 | 설명 |
|------|-----|------|
| **Weirdness** | 35 | 가성 제거 + 진성 하이라이트 최적 |
| **Style Influence** | 65 | Style Prompt 영향력 유지 |

**적용 규칙:**
```
Step 1. 트랙 생산 지시서 작성 시 Suno Parameters 제안
Step 2. concept.md에 트랙별 파라미터 기록
Step 3. 결과 QC 후 파라미터 조정 필요 시 기록
```

**조정 가이드:**
| 상황 | Weirdness | Style Influence |
|------|-----------|-----------------|
| **안정적 (기본)** | **35** | **65** |
| **공격적 (프롬프트 강화)** | **35** | **70** |
| **실험적 (장르 변화 감수)** | **40** | **60** |

---

### Concept 파일 최종 QC 체크리스트 (v2.3 NEW)

> **린터 대체용 — concept 작성 완료 후 30초 검증**

```
□ Lyrics에 편곡 지시 없음 (Kick in, Groove locks in 등 → Style Prompt)
□ Style Prompt에 보컬/편곡 지시 집중
□ Style Prompt <= 900자 (공백 포함 문자)
□ Title에 이모지/해시태그 없음
□ Description 해시태그는 구분선(---) 아래에만
□ Pinned comment 이모지 ≤ 1개
□ SSOT version 명시됨
□ Cross-Series 겹침 없음 (SERIES/ 전체 concept.md 장소+감정+상황 3축 대조) ← v2.11 NEW
```

**FAIL 시:** 해당 항목 수정 후 재검증

---

### QC 체크 시 (3-Point Fail Fast)
> 상세: `MASTER/MANAGER.md` Phase 2

- [ ] Intro (0:00~0:20): 발음 뭉개짐/웅얼거림 → Fail
- [ ] Chorus: 훅이 10초 내 잡지 못함 → 보류
- [ ] Outro: 끊김/클릭 노이즈 → Fail

### DEBUG vs PROD 모드 (v1.5.0 NEW)
> 상세: `MASTER/STYLE.md` §10 + `MASTER/MANAGER.md` Phase 2.5

| 모드 | 상황 | 규칙 |
|------|------|------|
| **PROD** | 정상 트랙 제작 | 최소 2개 슬롯 변주 |
| **DEBUG** | 같은 문제 2회 재발 | **1개 변수만 변경** |

- 하모니/가성/EDM 보컬 문제 재발 시 → DEBUG 모드 전환
- DEBUG A/B 비교로 원인 특정 → PROD 복귀

### S1-S12 Validation 강제 (v2.6.2 UPDATE)
> 상세: `MASTER/ROLES.md` S1-S12 Validation Enforcement

- Style Prompt/Variation 출력 시 **반드시 S1-S12 테이블 포함**
- S1 (Vocal Persona) 비어있음 = **즉시 FAIL, 재생성**
- S10-S12 (Articulation, Reverb, Sound Engineering) 누락 = **즉시 FAIL**
- 테이블 없는 출력 = **자동 INVALID**

### FFmpeg 필터 그래프 작업 시
- [ ] Sequential acrossfade 패턴 준수
- [ ] 라벨 인덱싱: `[0][1]→[a01]`, `[a01][2]→[a02]`
- [ ] `final_label = a{num_tracks-1}` 확인

> 근거: `.ai/lessons-learned.md#필터-그래프-인덱싱-오류`

### 정규화 작업 시
- [ ] `sys.executable -m ffmpeg_normalize` 사용
- [ ] 출력 형식: WAV (MP3는 PCM 미지원)
- [ ] 원본 파일 덮어쓰기 금지

> 근거: `.ai/lessons-learned.md#ffmpeg-normalize-path-문제`

### 새 시리즈 프로젝트 생성 시
- [ ] 디렉토리 구조: `SERIES/[Series_Name]/[YYYY-MM-DD]/`
- [ ] `SERIES/[Series_Name]/concept.md` 먼저 생성 (시리즈 기준본)
- [ ] 필수 파일: `input/tracks/*.mp3`, `input/loop.mp4`, `input/thumb.jpg`
- [ ] 파일명 형식: `NN__Title__Mood__Genre__BPM.mp3`

### Shorts 생성 요청 시 (v2.0.0)
> **원칙: 반드시 사용자에게 확인 후 생성**

**입력 파일:**
- `input/shorts.mp4` (8~10초 짧은 영상) - 사용자가 준비
- 이 영상이 음악 구간 길이만큼 자동 루프됨

**"숏츠 만들어줘" 요청 시 필수 질문:**
```
Step 0. shorts.mp4 확인: input/shorts.mp4 존재 여부 체크
Step 1. 시리즈 확인: SERIES/ 내 폴더 목록 보여주고 선택 요청
Step 2. 트랙 번호 확인: 해당 시리즈의 트랙 목록 보여주고 선택 요청
Step 3. 구간 확인: "어느 구간으로 할까요? (예: 00:45 ~ 01:15)"
Step 4. 확인 후 실행: python vibem.py shorts [TRACK_PATH] --start [MM:SS] --duration [SEC]
```

**⚠️ 절대 규칙: 시작/종료 시간 수정 금지**
```
- 사용자가 "01:35 ~ 02:15" 라고 하면 → --start 01:35 --duration 40
- 버퍼/여유 시간 임의 추가 금지
- 반올림/보정 금지
- duration = 종료시간 - 시작시간 (정확히 계산)
```

**실행 전 검증 체크리스트 (필수):**
```
□ --start 값이 사용자 지정 시작 시간과 정확히 일치하는가?
□ --duration 값이 (종료시간 - 시작시간)과 정확히 일치하는가?
□ 임의로 버퍼/여유 시간을 추가하지 않았는가?

→ 하나라도 미준수 시: 명령어 수정 후 재실행
→ 실행 후 출력 duration 확인: 오차 ±2초 초과 시 원인 파악
```

**질문 예시:**
```
숏츠를 만들기 전에 확인이 필요합니다:

1. 어떤 시리즈인가요?
   - AM_0400
   - PM_0200
   - (기타 시리즈...)

2. 몇 번 트랙인가요?
   - 01. 마음밖
   - 02. 윤곽
   - ...

3. 어느 구간인가요? (시작 MM:SS ~ 끝 MM:SS)
```

**출력 경로:** `output/shorts/short_[TrackName].mp4`

### Shorts 2-Layer 텍스트 시스템 (v1.9.0)

**레이어 구조:**
```
Layer 1 (Title): 중앙 후킹 문구 - 0~2초만 표시, 빠르게 퇴장
Layer 2 (Lyric): 하단 가사 - 4초 이후 등장, 끝까지 유지
```

---

### Shorts Hook Copy Slot (필수)

> 쇼츠 계획 시 **반드시** 후킹 문구 제안 필요

**출력 형식:**
```
HOOK_TITLES (3-7 단어, 5개 제안):
1) ...
2) ...
3) ...
4) ...
5) ...

HOOK_SUBTITLES (6-12 단어, 3개 제안, 선택):
1) ...
2) ...
3) ...
```

**규칙:**
- ❌ 가사 라인 그대로 사용 금지
- ⭕ 상황/감정 선언문 (화면 타이틀용)
- ⭕ 시리즈 컨셉/시간대 포지셔닝과 일치

---

### Shorts QC 체크리스트 (필수)

```
□ Hook Title 있음? (Y/N)
□ Bottom Lyric 있음? (Y/N)
□ 역할 분리 유지? (Title: 0-2초만, Lyric: 4초 이후 하단) (Y/N)
□ Title이 가사가 아닌 선언문인가? (Y/N)

→ 하나라도 N이면 수정 후 재생성
```

---

### Shorts 자막 타이포그래피 스펙 (필수)

#### A. 공통 원칙 (가독성 3종 세트)

| 항목 | 값 | 비고 |
|------|-----|------|
| Fill (글자색) | White / Off-white | 고정 |
| Shadow | 부드럽고 넓게 | 필수 |
| Backplate | 반투명 바 | 배경 밝거나 복잡할 때만 |
| Stroke (외곽선) | **금지** | 촌스러움 방지 |

#### B. 하단 가사 스펙 (지속 레이어)

| 항목 | 값 |
|------|-----|
| **위치** | 세로 35-40% (화면 중앙보다 약간 아래) |
| **정렬** | Center |
| **폰트** | 산세리프 (얇게~보통) |
| **크기** | 화면 높이의 4.5-5.5% |
| **자간** | +1 ~ +3 |
| **행간** | 1.0 ~ 1.1 |
| **페이드** | In/Out 6-8프레임 (컷점프 금지) |

**드랍쉐도우 (하단 가사):**
| 항목 | 값 |
|------|-----|
| Opacity | 55-70% |
| Blur | 12-18 |
| Distance Y | 6-10 |
| Distance X | 0 |
| Color | Black |

**백플레이트 (옵션):**
| 항목 | 값 |
|------|-----|
| Shape | Rounded rectangle |
| Opacity | 18-28% |
| Blur | 0 (단색) |
| Padding | 좌우 24-36px, 상하 12-16px |

#### C. 중앙 타이틀 스펙 (0-2초만)

| 항목 | 값 |
|------|-----|
| **위치** | 세로 45% (화면 중앙보다 살짝 위) |
| **폰트 두께** | Medium ~ Semibold |
| **크기** | 화면 높이의 7-9% |
| **줄 수** | 1줄 권장, 최대 2줄 (행간 0.95) |
| **등장/퇴장** | 0.2초 이내 (강한 타이틀 느낌) |

**드랍쉐도우 (중앙 타이틀):**
| 항목 | 값 |
|------|-----|
| Opacity | 60-80% |
| Blur | 20-28 |
| Distance Y | 10-16 |
| Distance X | 0 |
| Color | Black |

#### D. 금지 구역

| 구역 | 규칙 |
|------|------|
| 하단 0-30% | ❌ 절대 침범 금지 (YouTube UI 영역) |
| 우측 중앙 | ❌ 텍스트 길게 금지 (좋아요/댓글 버튼) |

> ⚠️ 하단 30%에 텍스트 배치 시 YouTube UI에 가려짐

---

### Shorts CLI 옵션

```bash
python vibem.py shorts [TRACK_PATH] \
  --start 01:35 --duration 40 \
  --title "잠들지 못한 새벽" \
  --srt lyrics.srt \
  --title-font /path/to/heavy.otf \
  --lyric-font /path/to/medium.otf
```

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--title` | None | 중앙 타이틀 (훅 문구) |
| `--title-duration` | 4 | 타이틀 표시 시간 (초) |
| `--lyric` | None | 하단 고정 가사 (static) |
| `--srt` | None | 동적 가사 SRT 파일 (dynamic) |
| `--lyric-delay` | 1 | 가사 페이드인 시작 (초) |
| `--title-font` | Pretendard Black | 타이틀(훅) 폰트 |
| `--lyric-font` | Pretendard Medium | 가사 폰트 |

**기본 폰트:**
- 훅 문구: `Pretendard-Black.otf` (Heavy)
- 가사: `Pretendard-Medium.otf`

**의존성:** 텍스트 옵션 사용 시 `ffmpeg-full` 필요
```bash
brew install ffmpeg-full
```

---

### Concept 파일 위치 규칙 (요약)

> **concept.md는 반드시 SERIES 폴더 내에만 존재**

**기준 위치 (MASTER 정책 요약):**
```
SERIES/[시리즈명]/concept.md
```

**예시:**
- `SERIES/AM_0400/concept.md` ← AM 04:00 시리즈 기준 파일
- `SERIES/PM_0200/concept.md` ← PM 02:00 시리즈 기준 파일
- `SERIES/PM_0400/concept.md` ← PM 04:00 시리즈 기준 파일
- `SERIES/PM_0600/concept.md` ← PM 06:00 시리즈 기준 파일

**금지:**
- ❌ 루트에 `concept_vol.*.md` 생성 금지
- ❌ 같은 시리즈의 concept을 여러 위치에 복사 금지

**작업 시:**
```
Step 1. SERIES/[시리즈]/concept.md 직접 편집
Step 2. 루트에 임시 파일 생성하지 않음
Step 3. 편집 완료 후 Last updated 날짜 갱신
```

**이유:**
- SSOT 위반 시 어느 파일이 최신인지 혼란
- 트랙 추가/수정 시 누락 위험
- 시리즈별 독립성 보장

---

## Project Structure

```
vibe-m/
├── MASTER/                 # 프로젝트 헌법
│   ├── 24H_UNIVERSE.md     # 24시간 세계관 Bible
│   ├── PLAYLIST_GUIDE.md   # 플레이리스트 컨셉 가이드
│   ├── LYRICS.md           # 가사 공학 규칙
│   ├── STYLE.md            # 사운드/스타일 가이드
│   ├── MANAGER.md          # 운영 마스터 플랜 (Phase 0~6)
│   ├── ROLES.md            # 역할 분리 시스템
│   ├── QUICK_REF.md        # 사람용 운영 매뉴얼
│   ├── rubrics/
│   │   ├── CITYPOP_RUBRIC.md   # 시티팝 장르 루브릭 (≥80점 PASS)
│   │   └── FAST_LOFI_RUBRIC.md # Fast Lo-fi 장르 루브릭 (≥80점 PASS)
│   └── VIBE-M_Master_Plan.md # CLI 스펙
│
├── SERIES/                 # 시리즈별 프로젝트 (concept.md 기준 위치)
│   ├── AM_0400/            # 새벽 4시 시리즈
│   │   ├── concept.md      # 컨셉 문서 (기준본)
│   │   └── input/
│   │       ├── tracks/     # MP3 파일
│   │       ├── loop.mp4
│   │       └── thumb.jpg
│   ├── PM_0200/            # 오후 2시 시리즈
│   │   ├── concept.md
│   │   └── input/
│   ├── PM_0400/            # 오후 4시 시리즈
│   │   ├── concept.md
│   │   └── input/
│   ├── PM_0600/            # 오후 6시 시리즈
│   │   ├── concept.md
│   │   └── input/
│   └── Single/             # 싱글 트랙
│
├── vibem.py                # CLI 메인 코드
├── requirements.txt        # Python 의존성
├── CLAUDE.md               # 이 파일
└── .ai/                    # AI 전용 메모리
    ├── SESSION.md          # 세션 상태
    └── lessons-learned.md  # 버그 패턴
```

## Quick Commands

| 명령 | 설명 |
|------|------|
| `python3 vibem.py validate <path>` | 파일 검증 |
| `python3 vibem.py preview <path> --sec 30` | 미리보기 생성 |
| `python3 vibem.py pack <path>` | 최종 패키징 |
| `python3 vibem.py shorts <track_path> --start MM:SS --duration SEC [--title "..."] [--lyric "..."]` | 숏츠 생성 (9:16, 텍스트 옵션) |
| `python3 vibem.py clean <path>` | 작업 폴더 정리 |

## Token Saving

### DO
- `MASTER/` 문서 링크로 규칙 참조
- 필요한 파일만 읽기
- 에러 메시지 전문 확인 후 수정

### DON'T
- 전체 코드 다시 작성
- 추측으로 버그 수정 (로그 확인 먼저)
- 불필요한 파일 탐색

## Context Management

> 토큰 90% 초과 시

1. `.ai/SESSION.md` 업데이트
2. `/compact` 제안
3. 다음 작업 명시

## Workflow Rules

### 가사/스타일/Exclude 수정 워크플로우 (요약)

> **SSOT: `MASTER/MANAGER.md` Phase 0.5**  
> 아래는 실행 요약이다.

**절차:**

1. **txt 파일 먼저 수정**
   - `SERIES/[시리즈]/trackNN_lyrics.txt`
   - `SERIES/[시리즈]/trackNN_style.txt`
   - `SERIES/[시리즈]/trackNN_exclude.txt`
   - 이전 버전 파일은 남기지 않고 최종본 1세트만 유지

2. **사용자 컨펌 PASS 받음**
   - QC 검증 완료
   - 사용자가 "좋아" / "PASS" 확인

3. **그 다음 concept.md에 반영**
   - `SERIES/[시리즈]/concept.md` 업데이트
   - txt 파일 내용 동기화

**이유:**
- txt = 작업 중 기준본 (수정/검증 단계)
- concept.md = 최종 확정본 (컨펌 완료 후)
- 수정 중인 내용과 확정된 내용 분리로 혼란 방지

**금지:**
- ❌ concept.md 먼저 수정하고 txt는 나중에
- ❌ 컨펌 전에 concept.md 업데이트
- ❌ txt와 concept.md 동시 수정
