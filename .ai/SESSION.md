# Session State - vibe-m

> 현재 세션 상태 기록
>
> Last updated: 2026-01-29 (PM_1800 9트랙 완성)

## 완료된 작업

### 2026-01-29 - PM_1800 9트랙 시리즈 완성 `446051b`

- [x] **Track 08 "숨" 신규 제작**
  - 70 BPM, Ab Major, Female vocal
  - Rhodes-led, warm synth pad
  - Breakdown: 음악 멈추고 숨소리 "후..."
  - W:40 / I:60 Suno 파라미터

- [x] **Track 07 "골목" concept.md 추가** (기존 싱글)
  - 67 BPM, Db Major, Male vocal
  - Verse-heavy, Speech-like phrasing

- [x] **Track 09 "이름" concept.md 추가** (기존 싱글)
  - 72 BPM, Ab Major, Male vocal
  - Final Chorus chest belt climax

- [x] **시리즈 확정: 10트랙 → 9트랙**
  - Track 09 "이름"으로 Closing
  - concept.md SSOT 통합 (개별 txt 파일 삭제)

### 2026-01-29 - PM_1800 Track 05-06 완성

- [x] **Track 05 "쪽잠" 완성**
  - 78 BPM, G minor, Female vocal
  - Verse-driven 구조, Dreamy/Hazy texture
  - Track 04 "차창밖"과 같은 화자 (버스 안 연속 장면)
  - W:30 / I:65 Suno 파라미터

- [x] **Track 06 "전화" 완성**
  - 88 BPM, Db Major, Male vocal
  - 대화체 가사, 따뜻한 톤
  - Track 10 "귀환" 복선 (전화 통화 → 집 도착)
  - 독백/싱잉랩 방지: 추임새 제거 + EXCLUDE 강화
  - W:30 / I:65 Suno 파라미터

### 2026-01-29 - PM_1800 Track 04 차창밖 `217fe40` `4401d5a`

- [x] **Track 04 "차창밖" 완성**
  - 85 BPM, G minor, Female vocal
  - Verse-driven 구조 (No Chorus, Refrain만 사용)
  - Solo vocal 강제 (No harmonies, No doubles, No backing vocals)
  - Blues R&B 장르, Blues scale melody
  - Catchy singable topline, 3-4 chord loop
  - Intro에 vinyl crackle 추가
  - W:30 / I:65 Suno 파라미터

### 2026-01-28 - PM_1800 퇴근길 시리즈 `216aee5` `6a1a4ba`

- [x] **PM_1800 "퇴근길" 시리즈 추가**
  - Track 01 "Exit": Uptown Funk 벤치마킹, 115 BPM, Eb Major, Korean Funk-Pop
  - Track 02 "약속": 자니 벤치마킹, 100 BPM, Db Major
  - Track 03 "정류장": 약속 커버 (글자수 완벽 매칭), G minor
  - concept.md: 10곡 플랜, 감정 아크, BPM 아크, 가사 포함
  - W:30 / I:70 Suno 파라미터 (Track 01)

- [x] **LYRICS.md §2.3 메타태그 동작 원리 추가**
  - `[AA]` = 구조 태그 (낭독 X)
  - `(BB)` = 조건부 (가사 100%, 톤 지시 ~30%)
  - 톤 지시 단독 행 배치 규칙
  - 감정 태그 → Style로 이동

- [x] **Reference/song PDF 추가**
  - 자니.pdf, uptown-funk.pdf

### 2026-01-27 - Git LFS 설정 `06fff55`

- [x] **Git LFS 설정**
  - *.mp4 파일 Git LFS 추적 설정
  - 히스토리 재작성으로 기존 대용량 파일 LFS 마이그레이션
  - 11개 LFS 오브젝트 (418 MB) 업로드 완료

### 2026-01-26 - SSOT 정리 5단계 `f1b5ee5` `2d35cb6`

- [x] **SSOT 정리 5단계 완료** (GPT 피드백 기반)
  1. MANAGER Pure Input → LYRICS §2 참조 (SSOT 통일)
  2. 글자수 제한 1000 → 800 통일 (전 문서)
  3. 보컬 메타태그 필수 규칙 LYRICS §2.2에 SSOT 승격
  4. STYLE에서 falsetto 트리거 단어 제거 (→ upper register)
  5. CLAUDE.md 역할 명확화 (사용 매뉴얼, 요약 표시)
  - MASTER/_INDEX.md SSOT 라우터 추가
  - 버전: MANAGER v1.3, STYLE v2.6.3, LYRICS v1.9.1, CLAUDE v2.7.0

### 2026-01-26 - 골목 싱글 `6a538e4`

- [x] **골목 싱글 영상 제작 (PM 07:00 퇴근길의 위로)**
  - single.mp4: loop.mp4 0.5초 crossfade 루프 (2분 46초)
  - 골목_youtube.md: 제목, 설명, 챕터, 해시태그
  - PM 07:00 시리즈 첫 싱글 선공개

### 2026-01-25 (밤) - SSOT 리팩토링 `e97da74`

- [x] **바라봐줘요 seed 가사/스타일 업데이트** `c861208`
  - 기존 분석 문서 → 트랙 생성용 가사+스타일로 교체
  - Suno Parameters: W:30 I:60

- [x] **SSOT 슬롯 체계 통일 작업**
  - 문제: 문서별 슬롯 개수 불일치 (CLAUDE.md S0-S20, STYLE.md 9-Slot, ROLES.md S1-S12)
  - 해결: CLAUDE.md를 SSOT로 지정, 다른 문서는 참조로 연결

- [x] **STYLE.md v2.6.2 업데이트**
  - "9-Slot Table" → CLAUDE.md S0-S20 참조로 변경
  - 핵심 슬롯 요약 테이블 추가 (S18 Articulation, S19 Reverb, S20 Sound Engineering 포함)
  - 버전: v2.6 → v2.6.2

- [x] **CLAUDE.md v2.6.2 업데이트**
  - "S1-S9 Validation" → "S1-S12 Validation" 변경
  - S10-S12 (프로덕션 필수) 누락 시 FAIL 조건 추가
  - "17개 슬롯" → "20개 슬롯" 수정
  - "S0-S18" → "S0-S20" 수정

- [x] **ROLES.md v1.7 업데이트**
  - SSOT 관계 명시: CLAUDE.md가 전체 슬롯 정의, ROLES.md는 압축 검증용
  - "S1-S12 Validation Table (압축 검증용)" 명칭 변경
  - 버전: v1.6 → v1.7

- [x] **바라봐줘요 Seed Research + 골목 시드 트랙**
  - 레퍼런스 분석: 죠지 - 바라봐줘요 (67 BPM, Db Major)
  - 시드 트랙 "골목" 가사/Style Prompt/Exclude 완성
  - S1-S12 Validation Table 포함 (12/12 PASS)

### 2026-01-25 (저녁)

- [x] **프로젝트 폴더 이동: iCloud → ~/Project**
  - WDS, VIBE-M 폴더 로컬로 이동
  - vibe-m → VIBE-M 대문자 변경
  - SSH 키 신규 생성 및 GitHub 등록

- [x] **concept.md 타임스탬프 2회 반복 버전 업데이트**
  - AM_0400: 9곡 x2 (약 48분)
  - PM_1400: 10곡 x2 (약 54분)

- [x] **죠지 "바라봐줘요" Seed Research 분석**
  - 악보 분석 (Db Major, 67 BPM, 확장 코드)
  - 보컬 스타일: Chest voice, Raw, Dry, 기교 없음
  - 프로덕션: Rhodes piano-led, Minimal drums
  - 파일: `SERIES/바라봐줘요_seed_research.txt`

- [x] **시드 트랙 "골목" 가사 작성**
  - 컨셉: 혼자 걷는 저녁 산책
  - 키워드 축: 골목/가로등/그림자/발자국/저녁
  - 메타태그 적용: [Chest voice], [Powerful belt], [No harmony] 등
  - QC Validation PASS

### 2026-01-25 (오전)

- [x] **AM_0400/PM_1400 실제 YouTube 제목/설명/고정댓글 기록** `f03ce6b`
  - AM 04:00: `[Playlist] [AM 04:00] soomshuim | 하루가 멈춘 시간, Slow R&B 보컬`
  - PM 02:00: `[Playlist] [PM 02:00] soomshuim | 햇살에 멍해지는 시간, Chilling R&B`

- [x] **PM_1400 vol1 플레이리스트 완성** `7c1155e`
  - final.mp4 생성 (53.5분, x2 반복)
  - draft_description.txt 최종안, 해시태그 8개 최적화
  - AM_0400/PM_1400 디스크립션 포맷 통일

- [x] **PM_1400 Track 10 "깸" 추가 - 수미상관 완성 (10곡 확정)** `610ee73`
  - Track 01 "멍" ↔ Track 10 "깸" 수미상관 구조
  - 후렴 대칭: "멍때려요" ↔ "일어나요"
  - punchy bass guitar, bouncy groove 스타일

- [x] **PM_1400 Track 07-09 추가** `471d547`
  - Track 07 "온기" (Female, 70 BPM, Db Major)
  - Track 08 "그늘" → Track 07로 재배치 (Male, 72 BPM, Ab Major)
  - Track 09 "구름" → Track 08로 재배치 (Female, 76 BPM, F Major)

- [x] **PM_1400 트랙 순서 재배치 (A안)** `a01b253`
  - 기존: 산책(01)이 오프닝
  - 변경: 멍(01) → 컨셉 직결 ("햇살에 멍해지는 시간")
  - 최종 순서: 멍(01) → 얼음(02) → 산책(03) → 온기(04) → 돛(05) → 물결(06) → 그늘(07) → 구름(08) → 먼지(09)
  - 운율 겹침 방지: 산책/물결/먼지 2트랙 이상 간격 확보

- [x] **SERIES 폴더 구조 단순화** `a01b253`
  - vol1 폴더 제거, 파일들 상위로 이동
  - `SERIES/AM_0400/vol1/` → `SERIES/AM_0400/`
  - `SERIES/PM_1400/vol1/` → `SERIES/PM_1400/`
  - CLAUDE.md v2.6.1 업데이트

- [x] **CLAUDE.md v2.6 워크플로우 개선**
  - Suno 파라미터 가이드 (W:35/I:65 기본값)
  - Style Prompt + Exclude 세트 출력 규칙
  - 곡 길이 확장 규칙 (구조 태그로 확장, Verse 8행 금지)
  - 복사용 .txt 파일 저장 워크플로우
  - S18 Articulation 필수 규칙 추가

### 2026-01-24

- [x] **PM_1400 vol1 트랙 리스트 확정 (6곡)**
  - Track 01 "산책" (74 BPM, Male) - 나른한 오프닝
  - Track 02 "멍" (74 BPM, Male) - 컨셉 직결 "멍때려요"
  - Track 03 "물결" (74 BPM, Male) - Boat 스타일
  - Track 04 "얼음" (90 BPM, Female) - 분위기 전환
  - Track 05 "먼지" (72 BPM, Male) - 쉼표 역할
  - Track 06 "돛" (90 BPM, Male) - 에코 훅, 열린 마무리
  - 그룹 A/B/C 교차 배치로 운율 반복 방지

- [x] **Track 02 "물결" Boat 악보 분석 반영** (Final_v4)
  - Key: A Major (Boat 원곡), Neo-soul chords (M9, m7)
  - Melody: Narrow range, stepwise, speech-like rhythm
  - Lyrics: 직접적/담백한 Boat 스타일로 전면 수정
  - QC Checklist: Speech-like 항목 추가

- [x] **프로젝트 구조 SSOT 최적화**
  - concept 파일 통합: 루트 → SERIES/ 폴더 내로 이동
  - 아카이브.zip, MASTER/prompts/ 삭제
  - CLAUDE.md v2.4: Concept 파일 SSOT 규칙 추가

### 2026-01-23

- [x] **PM_1400 vol.2 시드 트랙 설계** `c6ffe3a`
  - Track 01 "먼지" 가사/스타일 확정
  - Reference: 죠지 - Boat
  - Male vocal, Vibraphone-led, 72 BPM, Eb Major

- [x] **CLAUDE.md v2.2.0: Style Prompt QC 워크플로우**
  - S15 글자수 제한 (< 800자)
  - S16 Lead Instrument Supportive 규칙
  - S17 Chorus Expansion Density 규칙

- [x] **LYRICS.md v1.8: 가사 품질 규칙 추가**
  - 1.10 Image Density Management
  - 1.11 Chorus Tone Rule

### 2026-01-18 (오전)

- [x] 프로젝트 초기 설정
  - `vibem.py` CLI 구현 (Click 기반)
  - `requirements.txt` 생성
  - FFmpeg 8.0.1 설치

- [x] 핵심 커맨드 구현
  - `validate` - 파일/오디오 검증
  - `preview` - 미리보기 생성
  - `pack` - 최종 패키징
  - `init` - 프로젝트 초기화
  - `clean` - 작업 폴더 정리

- [x] 버그 수정 3건
  - 필터 그래프 인덱싱 오류 수정
  - ffmpeg-normalize PATH 문제 해결
  - MP3 → WAV 출력 형식 변경

- [x] 테스트 완료
  - `SERIES/Test_Series/2026-01-18/` 테스트 프로젝트
  - preview 30초 미리보기 정상 확인

### 2026-01-18 (오후)

- [x] 프로젝트 구조 재정비
  - `series/` → `SERIES/` 대문자 변경
  - `MASTER/` 폴더 생성

- [x] MASTER 문서 3종 완성
  - `MANAGER.md` - 운영 마스터 플랜 (QC, Fail Fast)
  - `LYRICS.md` - 가사 공학 규칙 (Metric Mirroring 등)
  - `STYLE.md` - 사운드/스타일 가이드 (Playlist Profile)

- [x] `/coach` 커맨드 생성
  - `.claude/commands/coach.md`
  - 가사 검토, Style Prompt 검토, QC 체크리스트

- [x] GitHub 연동
  - Repository: https://github.com/soomshuim/vibe-m
  - Branch: master
  - Initial commit 완료

- [x] `/coach` 테스트
  - LYRICS.md Reference Example 검토 → PASS

## 현재 상태

- **프로젝트**: Production Ready (v2.6.2 - SSOT 슬롯 체계 통일)
- **GitHub**: https://github.com/soomshuim/vibe-m (master)
- **vol.1 (AM_0400)**: 완료, YouTube 게시됨
  - 제목: "[Playlist] [AM 04:00] soomshuim | 하루가 멈춘 시간, Slow R&B 보컬"
  - 작업 디렉토리: `SERIES/AM_0400/`
  - YouTube: https://youtu.be/i1GHmn1WZr4
- **vol.2 (PM_1400)**: 진행 중
  - 제목: "[Playlist] [PM 02:00] soomshuim | 햇살에 멍해지는 시간, 느긋하게 흐르는 Soft R&B 보컬"
  - **10곡 확정**: 멍(01) → 얼음(02) → 산책(03) → 온기(04) → 돛(05) → 물결(06) → 그늘(07) → 구름(08) → 먼지(09) → 깸(10)
  - **수미상관 완성**: 멍(01) ↔ 깸(10)
  - 작업 디렉토리: `SERIES/PM_1400/`
  - Suno 생성 대기
- **문서 버전**:
  - LYRICS.md v1.8
  - STYLE.md v2.6.2 (SSOT 슬롯 체계 통일)
  - CLAUDE.md v2.6.2 (SSOT 슬롯 체계 통일)
  - ROLES.md v1.7 (S1-S12 Validation + SSOT Alignment)

## 진행 중

- **바라봐줘요 스타일 테스트 트랙 제작**
  - Seed Research 완료
  - 시드 트랙 "골목" 가사 완료
  - 다음: Style Prompt 작성 → Suno 생성 테스트
- Shorts 제작 준비 (shorts.mp4 입력 대기)

## 2026-01-23 세션 완료

- [x] **vibem.py: 타이틀 자동 생성**
  - draft_description.txt 상단에 SSOT v1.5 기반 제목 초안
  - concept.md Title Meta 파싱 + 자동 추론 fallback
- [x] **vibem.py: shorts 커맨드 v2.0.0**
  - loop.mp4 → shorts.mp4 변경 (8~10초 루프)
- [x] **문서 업데이트**
  - CLAUDE.md v2.0.0: Shorts 워크플로우
  - VIBE-M_Master_Plan.md: Shorts 스펙 추가
- [x] **제목/URL 변경 반영**
  - 시리즈: "[AM 04:00] 하루가 멈춘 시간"
  - YouTube: https://youtu.be/i1GHmn1WZr4

## 완료된 추가 작업

### 2026-01-18 (저녁)

- [x] Role System 문서화 완료 (`6db9639`, `cabecb6`)
  - `MASTER/ROLES.md` 생성 (v1.0)
  - `MASTER/QUICK_REF.md` 생성 - 사람용 운영 매뉴얼
  - `MASTER/prompts/` 폴더 생성
    - `00_system.txt` - 공유 컨텍스트
    - `01_researcher.txt` - Seed Researcher 프롬프트
    - `02_designer.txt` - Seed Designer 프롬프트
    - `03_variation.txt` - Variation Designer 프롬프트
  - `CLAUDE.md` Quick Reference 업데이트
  - `CHANGELOG.md` 생성

- [x] STYLE.md 제로 베이스라인 진화 (`fcadb70` ~ `66a7a76`)
  - v1.1: Harmony Guard 추가
  - v1.2: Safety Lines + Exclude 재설계
  - v1.3: Safety Lines 강화 + Chorus 2 분리
  - v1.4: Safety Lines 압축 + 긍정 방향 가드
  - v1.5: 제로 베이스라인 - 코러스 완전 차단

- [x] MANAGER.md v1.1 (`66a7a76`)
  - Phase 2 Track QC에 코러스 과다 Fail 기준 추가

- [x] concept.md 기록 (`b5fce3d`)
  - Track 01~03 가사/스타일 기록

### 2026-01-18 (밤)

- [x] vibem.py preview 버그 수정
  - 이전: 전체 병합 후 앞 N초 자르기 (Track 01만 포함)
  - 이후: 각 트랙 앞 N/트랙수 초씩 잘라서 병합 (모든 트랙 포함)
  - 60초 preview = 3트랙 × 20.5초

- [x] Track 02 파일명 수정
  - `Sentimental_Acoustic-RnB` → `Sentimental__Acoustic-RnB` (언더스코어 2개)

- [x] 플레이리스트 주제 확정
  - "혼자 걷는 밤, 습기와 잔향"
  - 키워드: 습기, 잔향, 그림자, 번짐, 희미함, 혼자, 밤

- [x] Track 04-10 제작 플랜 수립
  - `.claude/plans/rippling-finding-lecun.md`

## 완료된 추가 작업

### 2026-01-19

- [x] Track 04 "물안개" 가사 + Style Prompt 완료 (`7cb2824`)
  - Lo-fi R&B, Male vocal, 80 BPM, Felt Piano
  - 가사 QC 9/9 PASS, Style Prompt 9/9 PASS
- [x] 워크플로우 강화
  - PLAYLIST_GUIDE.md 생성 (유튜브 인기 사례 분석)
  - LYRICS.md v1.1 (새 규칙 4개)
- [x] **STYLE.md v1.5: Single-Lead Explosion + Zero Exception** (`73800c6`)
  - Harmony Guard 예외 조항 완전 제거
  - "vocals unchanged" → "keep SINGLE lead (no layers)" 대체
  - Chorus/V2 Lift 정량화 (1 held note, 1 event)
  - Self-QC 3-Step 프로세스 강화
- [x] Track 04 "물안개" MP3 생성 완료 (Suno)
- [x] 4트랙 Preview 생성 완료 (60초)
- [x] **STYLE.md v1.6: Energy Permission + Safety Separation**
  - 핵심 원칙: "금지는 레이어에만, 허용은 에너지에"
  - "vocals unchanged" → "lead vocal energy may increase, but no new vocal layers"
  - "Single lead vocal ONLY" → "Lead vocal remains single and dominant"
  - Verse2 에너지 상승 권한 명시적 부여 (encouraged/allowed)
- [x] ROLES.md v1.1: Energy Permission Principle 추가
- [x] 02_designer.txt: Safety Lines + Energy Permission 분리
- [x] 03_variation.txt: Vocal Energy Risk Fail 조건 추가
  - Verse2 lacks lift → FAIL
  - Chorus sounds flat due to over-safety → FAIL
- [x] **STYLE.md v1.7: Fail Fast Energy Check**
  - Chorus held note 정량화: "exactly 1 held note"
  - V2 → Chorus FAIL 조건 4개 추가
- [x] ROLES.md v1.2: Automatic FAIL Conditions 추가
- [x] 00_system.txt: Mandatory Slot Check 추가
- [x] 02/03_designer.txt: INVALID conditions 추가

### 2026-01-19 (오후)

- [x] **Energy Permission 문서 일괄 강화** (무난함 방지)
  - 문제: "금지"만 강하고 "허용"이 흩어져서 AI가 평균값(무난함)으로 수렴
  - 해결: Safety Lines와 Energy Permission을 **항상 쌍으로** 배치
  - **STYLE.md v1.8**: Energy Permission (Mandatory) 섹션 추가
  - **02_designer.txt**: Seed-Level Energy Permission 블록 강화
  - **03_variation.txt**: PASS Criteria 추가 + "safe but unmemorable = FAIL"
  - **ROLES.md v1.3**: Team Philosophy 섹션 추가 ("무난함 = 실패" 문화 선언)

- [x] **Seed Energy Contract 헌법화** (마무리 보강)
  - **ROLES.md v1.4**: `Seed Energy Contract (Non-Negotiable)` 섹션 추가
    - "This contract overrides any safety or layer prohibition"
    - Canonical Sentence 전 문서 동일화 선언
  - **STYLE.md v1.9**: Canonical Sentence Unification
    - S8/S9 체크리스트 문장 통일 (ONLY 제거)
  - **02_designer.txt**: "safe/flat = INVALID" 조건 추가
  - **03_variation.txt**: Final Verdict Question 추가
    - "Does the Chorus feel more emotionally intense than Verse2 without adding layers?"

- [x] **100점 마무리 개선**
  - **04_ultra_compressed.txt**: 실행용 초압축 프롬프트 템플릿 생성
    - Canonical Blocks (A/B/C/D) 복붙 가능
    - ~750 chars 예시 포함
  - **"1 held note" 표현 통일**: 전 문서에 "longer sustain than any verse note" 고정
    - STYLE.md 4개소
    - 03_variation.txt 1개소
  - **Energy Reference 정량 기준 추가** (QC용, 프롬프트용 아님)
    - "Chorus peak note should sustain at least 1.5x longer than any Verse note"
    - STYLE.md + 03_variation.txt에 추가

- [x] **LYRICS.md v1.2 + STYLE.md v2.0 피드백 영구 반영**
  - **LYRICS.md v1.2:**
    - 1.2 Ending Mirroring 강화 (품사 불일치 = FAIL)
    - 1.9 Physical Object Anchor Rule (물성 오브젝트 앵커) 추가
    - Case 09: Abstract Word Density (추상어 과밀) 추가
    - Case 10: Ending 품사 불일치 추가
  - **STYLE.md v2.0:**
    - 4.4 Belt/Tempo Conflict Rule 추가 (Chill에서 belt 충돌)
    - Slot F: Mood Bucket 추가 (Chill/Hazy/Ethereal/Nocturne 등)
    - 6) Exclude 강화 (3그룹 최대, 과도한 Exclude 부작용 경고)

### 2026-01-20

- [x] **Suno Guide 2.0 시스템 병합 완료**
  - 외부 가이드 3종 분석 및 병합:
    - Reddit Style Prompt Guide 2.0
    - Section Tags 전체 목록
    - museA Suno 자료집 (한국어)
  - **LYRICS.md v1.4 → v1.5**
    - 구조 태그 10종 추가 ([pre-chorus], [breakdown], [hook], [big finish] 등)
    - Performance Cues 섹션 신규 추가 ((whispered), (belted), (soft) 등)
    - 가사 길이 가이드라인 추가 (100-120 단어 권장)
    - 구조 공식 옵션 추가 (Pop Standard, K-POP Standard, Storyteller)
  - **STYLE.md v2.4 → v2.5**
    - 0.4 Prompt Priority Rule: "핵심 앞에" (Genre/BPM 첫 5단어)
    - 0.5 Gravity Words: 중력 우물 단어 회피 (pop, beat, bass - 원치 않는 경우만)
    - 10) A/B Testing Rules: 한 번에 1개 변수만 변경
    - 11) Co-occurrence Hints: 장르 조합 가이드
    - 12) Tag Bank: 검증된 키워드 사전 (보컬/악기/프로덕션)
    - Raw Vocal Baseline 수정: **Powerful을 기본값에서 제거** → 요청 시 추가
  - **CLAUDE.md v1.3.0 → v1.4.0**
    - S0 "핵심 앞에" 체크 항목 추가
    - S1 Powerful 제거 반영
    - 2.4 가사 길이 가이드 추가
  - 충돌 해결:
    - "pop" 중력 우물: "원치 않는 경우에만 회피" (Pop 원하면 사용 OK)
    - 괄호 정책 분리: 설명형 금지 vs Performance Cues 허용
    - Powerful: 기본값 아닌 요청 시 추가 (airy, husky와 동일 레벨)

### 2026-01-20 (오후) — Guide 5종 검증 + GPT 피드백 통합

- [x] **레퍼런스 가이드 5종 전수 검증**
  - 유튜브 감성 플레이리스트 인기 사례 분석
  - museA Suno 자료집
  - Suno Style Prompt Guide 2.0
  - Section Tags 전체 목록
  - 커뮤니티/공식 자료 수렴 원리

- [x] **GPT 피드백 6개 포인트 통합**
  1. DEBUG/PROD 모드 분리 (1변수 디버깅)
  2. Pure Lyric Input 근거 명시
  3. Texture Lines 라이브러리 추가
  4. 태그 경계 명확화 (필수/옵션/주의)
  5. S1-S9 Validation 강제 출력
  6. Exclude 운영 규칙 강화

- [x] **문서 업데이트 완료**
  - **STYLE.md v2.5 → v2.6**
    - 0.6 Broad Genre Labels Rule
    - 6.1 Exclude 운영 규칙
    - 10.0 DEBUG/PROD 모드 추가
    - 10.4 DEBUG 기록 양식
    - 12.5 Texture Lines (믹스/공간 제어)
    - 12.6 FX/Production 키워드
  - **LYRICS.md v1.5 → v1.6**
    - 2.0 Pure Lyric Input 근거 명시 (가이드와 다른 이유)
    - 2.2 태그 경계 명확화 (필수/옵션/주의/고급)
  - **MANAGER.md v1.1 → v1.2**
    - Phase 2.5 A/B Testing Protocol
    - 보컬 타입 누락 방지 강제
  - **ROLES.md v1.5 → v1.6**
    - S1-S9 Validation Enforcement 섹션
    - 출력 필수 형식 정의
  - **prompts (02_designer, 03_variation)**
    - 🔴 MANDATORY OUTPUT FORMAT 추가
    - S1-S9 테이블 없으면 INVALID
  - **CLAUDE.md v1.4.0 → v1.5.0**
    - DEBUG/PROD 모드 안내
    - S1-S9 Validation 강제 안내

### 2026-01-20 (저녁)

- [x] **Track 09 "마음안" 완료** (`cb2543e`)
  - 수미상관 마지막 곡 (Track 01 "마음밖" 대응)
  - Male vocal + Powerful belt, 95 BPM, Db Major
  - 키워드 축: 여명/옥상/난간/지평선
  - 후렴: "마음 안으로 번져와 / 여명처럼 스며들어"
- [x] **Track 08 "빗줄기" 완료** (`286ceef`)
  - Melancholic R&B, 85 BPM, F minor, Rhodes-led
  - 키워드 축: 빗줄기/아스팔트/골목/처마/우산
  - Raw Vocal + Chest Belt, Contralto female
  - 메타태그: Direct vocal, Chest voice, Powerful belt
  - bridge2 가사 개선: 물방울/턱/입술 등 신체 감각 디테일
- [x] `/record` 커맨드 추가 (`.claude/commands/record.md`)
- [x] Reference 가이드 PDF 5종 추가
- [x] **첫 플레이리스트 정식 출범** (`c686ba6`)
  - 제목: "[AM 04:00] 하루가 멈춘 시간"
  - 디렉토리: `SERIES/Test_Series/2026-01-18/` → `SERIES/AM_0400/vol1/`
  - 9트랙 완성 (Track 01~09)
- [x] **YouTube 업로드 완료** (`6c199c7`)
  - URL: https://youtu.be/i1GHmn1WZr4
  - 채널: soomshuim
  - 재생목록: "하루를 듣는 방법 | 24 Hours Playlist"
  - 제목: "[Playlist] [AM 04:00] soomshuim | 하루가 멈춘 시간, Slow R&B 보컬"
  - 예약 공개: 2026-01-20 22:00

### 2026-01-20 (밤) — 문서 체계화

- [x] **Korean Lyric Positioning 공식화** (`f031be5`)
  - LYRICS.md v1.7: 한국어 가사 포지셔닝 원칙
  - K1-K3 검증 체크리스트 추가
  - CLAUDE.md 워크플로우에 Korean Positioning 검증 단계 추가
- [x] **24H UNIVERSE Master Project Bible** (`8828270`)
  - 10개 Time Station 정의 (02:00~04:30)
  - 5개 Key/Mode Bucket 시스템
  - Production Templates 3종
  - Station QC Checklist
- [x] **3-Layer Korean Positioning 전략** (`9add92d`)
  - PLAYLIST_GUIDE.md v1.1: 재생목록/고정댓글/채널About 전략
  - vibem.py: description.txt 우리말 가사 문구 자동 추가
- [x] **vol1 YouTube 정보 기록** (`2636a03`)
  - concept.md에 제목/설명란 전문 기록

### 2026-01-21 — Shorts 2-Layer 자막 시스템

- [x] **shorts 명령어 자막 기능 확장**
  - 위치 조정: 타이틀 45%, 가사 62.5% (하단 0-30% 금지 구역)
  - 폰트 분리: 훅=Pretendard Black, 가사=Pretendard Medium
  - `--title-font`, `--lyric-font` 옵션 추가
  - `get_pretendard_font_path()` 함수 추가

- [x] **SRT 자막 버그 수정**
  - 문제: `subtitles` + `drawtext` 필터 조합 시 자막 미표시
  - 원인: `force_style` 내부 쉼표가 FFmpeg 필터 구분자로 해석됨
  - 해결: `force_style` 제거, 단순 `subtitles=` 필터 사용
  - `ffmpeg-full` 필요 (subtitles/drawtext 필터 포함)

- [x] **CLAUDE.md v1.9.0 업데이트**
  - Shorts 자막 타이포그래피 스펙 (A/B/C 섹션)
  - D. 금지 구역 섹션 추가 (하단 0-30%, 우측 중앙)
  - Hook Copy Slot 필수 출력 형식
  - Shorts QC 체크리스트

- [x] **lessons-learned.md 업데이트**
  - subtitles + drawtext 필터 충돌 문제 기록

### 2026-01-23 — 타이틀 규칙 + Description 개선

- [x] **PLAYLIST_GUIDE.md v1.2: Title Rules SSOT v1.5**
  - 타이틀 고정 구조 정의
  - Context Mode 필수 입력
  - GENRE 확장 (R&B, Rock, Pop, Jazz)
- [x] **vibem.py: pack --repeat 옵션 추가** (`bd048d6`)
  - 플레이리스트 N회 반복 (기본 2회)
- [x] **vibem.py: draft_description.txt 자동 생성** (`fbd2f64`)
  - 커스텀 인트로 + 고정댓글 섹션
  - Source/Derived 분리 (concept.md = SSOT)
- [x] **CLAUDE.md v2.0.0**: 타이틀 규칙 참조 추가

## 다음 작업 (예정)

- [x] ~~Shorts force_style 문제 해결~~ → 제작 방식 변경으로 불필요
- [x] 공개 후 고정 댓글 작성 → 완료
- [x] Shorts 클립 업로드 → 완료
- [x] **vol.2 (PM_1400) 완성**
  - [x] Seed Researcher: 레퍼런스 분석 (죠지 - Boat)
  - [x] Time Station 선정: 오후햇살 (14:00)
  - [x] Seed Designer: Seed DNA 설계
  - [x] 6곡 트랙 리스트 확정 (산책, 멍, 물결, 얼음, 먼지, 돛)
  - [x] 3곡 추가 (07-09: 온기, 그늘, 구름)
  - [x] 트랙 순서 재배치 (A안: 멍 오프닝)
  - [x] **Track 10 "깸" 수미상관 완성** (멍 ↔ 깸)
  - [x] Suno 생성 및 pack 완료 (final.mp4)
  - [ ] YouTube 업로드
  - [ ] Shorts 제작

## 알려진 이슈

없음

## 참고 파일

| 파일 | 용도 |
|------|------|
| `MASTER/24H_UNIVERSE.md` | 24H Universe Bible (Time Station) |
| `MASTER/MANAGER.md` | 운영 마스터 플랜 |
| `MASTER/LYRICS.md` | 가사 공학 규칙 + Korean Positioning |
| `MASTER/STYLE.md` | 사운드/스타일 가이드 |
| `MASTER/PLAYLIST_GUIDE.md` | 플레이리스트 컨셉 + 3-Layer 전략 |
| `MASTER/ROLES.md` | 역할 분리 시스템 (SSOT) |
| `MASTER/QUICK_REF.md` | 사람용 운영 매뉴얼 |
| `MASTER/prompts/` | 역할별 프롬프트 템플릿 |
| `MASTER/VIBE-M_Master_Plan.md` | CLI 스펙 |
| `vibem.py` | 메인 CLI 코드 |
| `CLAUDE.md` | Claude 작업 지침 |
| `.claude/commands/coach.md` | /coach 커맨드 |
| `.ai/lessons-learned.md` | 버그 패턴 |
| `CHANGELOG.md` | 변경 이력 |
| `Reference/` | 참고 자료 (인기 사례 분석 PDF)
