# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- **PM_0900 Track 06 "잠실대교" 베리에이션 디자인**
  - 장르: Korean Neo-Soul City Pop, 92 BPM, Eb Major, Female Alto
  - 컨셉: 택시 귀가, 알딸딸한 취기, 잠실대교 야경 감상
  - City Pop Rubric 82/100 PASS (초안 65점 FAIL → 재디자인)
  - Style: Rhodes + Juno pad + brass stabs + funky finger bass + plate reverb, 779자
- **PM_0900 Track 07 "공원" 베리에이션 디자인 (정류장→공원 장소 재설계)**
  - 장르: Korean City Pop Ballad, 68 BPM, Db Major, Female Contralto
  - 컨셉: 밤의 도시 공원, 강아지/커플/러너 관조
  - City Pop Rubric 84/100 PASS
  - Cross-Series 겹침: PM_0200 공원과 1/3 (장소만, PASS)

### Changed
- **CLAUDE.md v2.11.0 — Cross-Series Overlap Guard**
  - 가사 워크플로우 Step 0에 크로스시리즈 겹침 검증 추가
  - 체크리스트 1.12 Cross-Series Independence 항목 추가
  - 검증 출력 포맷 Section E 추가
  - Concept QC 체크리스트에 겹침 검증 항목 추가
- **PM_0900 concept.md 업데이트**
  - Track 05 제목: 수면 → 한강
  - Track 06 "잠실대교" 전체 디자인 반영 (가사/스타일/exclude)
  - Track 07 "막차" 전체 디자인 반영 (장소 재설계 대기)

### Removed
- PM_0900 Track 05 개별 txt 파일 3종 (제목 변경으로 삭제)

### Added
- **MASTER/CITYPOP_RUBRIC.md v1.0 — 시티팝 장르 루브릭**
  - 6개 팩터 100점 만점 (도시 서사/감정 절제/텐션 화성/리듬&베이스/사운드 팔레트/장르 정체성)
  - PASS ≥80, FAIL <80, CRITICAL FAIL: 개별 팩터 ≤5
  - BPM별 베이스 가이드, 7개 빈티지 사운드 요소, Dry vs Spacious 경고
- **PM_0900 Track 05 "수면" 시드 디자인**
  - 시드곡: Asoto Union "Think About Chu" DNA (Db Major, 88 BPM, one-loop 4-bar)
  - 시티팝 루브릭 84/100 PASS
  - Style: Juno-106/DX7/brass/plate reverb/tape warmth, 759자
  - seed05_think_about_chu_research.md 작성

### Changed
- **CLAUDE.md v2.10.0 — City Pop Rubric 워크플로우 통합**
  - 가사/Style Prompt 워크플로우에 장르 게이트 삽입
  - Auto Reference Rules, Quick Reference, Project Structure 업데이트
- **PM_0900 concept.md — Track 01-05 통합 완료**
  - Track 01-04 가사/스타일/exclude concept.md 반영, 상태 "완료"
  - Track 05 "수면" 시드 디자인 반영
  - Track 01-04 개별 txt 파일 삭제 (SSOT 정리)

### Changed
- **PM_0900 Track 02 "밤 산책" + Track 03 가사/스타일 전면 재작업**
  - Track 02: 담(골목)→밤 산책(거리), Female→Male, 네오소울→Korean City Pop
  - Track 03: 시티팝(108)→City Pop Ballad(90), 바라봐줘요 레퍼런스 기반
  - Track 03 가사: 거리 산책 + 그녀 기억 테마, 훅 "그렇게 다시 웃어줄래요"
  - Track 03 스타일: 신스 패드 리드 + 펑키 베이스 그루브 드라이브, Gb Major
  - LYRICS.md v2.2.0: [] 구조태그 전용, () 보컬+악기 단일행, QC F4/F5 추가
  - concept.md: Track 02 정보 업데이트 (보컬 배분 M6:F4)

- **PM_0900 Track 01 "문(Moon)" 최종 가사/스타일 반영**
  - 가사: V1 2-3행 수정 (편한 신발/손잡이), Pre-Chorus 전면 교체
  - 스타일: Articulation 선두 배치, 콤마 구분 단일 블록 포맷
  - concept.md: 키워드 축 열쇠→손잡이, 훅/상태 업데이트

### Added
- **museA Suno 가이드 통합 및 소괄호 메타태그 규칙 정립**
  - `Reference/museA_suno_guide.md` 생성 (Suno 실전 가이드 보존)
  - CLAUDE.md v2.9.0: 워크플로우에 museA 참조 단계 추가 (Step 0.5)
  - LYRICS.md v2.1.0: 소괄호 `()` 규칙 상세화 (위치/포함/금지/맥락 구분)
  - ROLES.md v1.8: Seed/Variation Designer에 Required References 추가
  - STYLE.md v2.6.4: Tag Bank 2026 트렌드 장르 + 구조/길이 제어 프롬프트 추가
  - lessons-learned.md: Cover 기능 활용법 추가
  - S18 Articulation 간소화: `Precise articulation, clear consonants` → `articulation`

### Added
- **PM_0900 "밤산책" 시리즈 시드곡 10곡 완성**
  - 테마: 밤산책의 경로를 따라가는 공간 중심 플레이리스트
  - 장르: 시티팝 베이스 (클래식 시티팝 + 시티팝풍 R&B 발라드 + 네오소울)
  - 레퍼런스: 죠지, 김현철, 유키카, 아소토유니온
  - 10곡: 문→담→불빛→벤치→물결→건넘→막차→창가→시야→집
  - 수미상관: Track 01 "문"(출발) ↔ Track 10 "집"(귀가), 둘 다 Db Major
  - Track 01 "문" 가사 v2: 문(門)=Moon 중의적 훅, 확장 구조
  - 파일: concept.md + 10트랙 lyrics/style/exclude txt (31개)
- **PM_0400 Track 09 "서랍" YouTube Shorts 제작 완료**
  - 구간: 0:50 ~ 1:50 (60초)
  - 출력: 1080x1920 (9:16), 62.4초, H.264+AAC
  - 타이틀 없음 (사용자 직접 삽입)
  - 출력 경로: `SERIES/PM_0400/output/shorts/short_서랍.mp4`
- **골목 숏츠 YouTube 메타데이터 문서화**
  - 골목_youtube.md에 Shorts 섹션 추가 (제목, 설명글, 고정댓글)
  - 시리즈 태그: PM 06:00 (#PM0600)
  - 풀 버전 링크: https://youtu.be/f-x7OkZ5Rgs

### Changed
- **시리즈 폴더 네이밍 24h→12h 통일**
  - PM_1400 → PM_0200 (오후 2시)
  - PM_1600 → PM_0400 (오후 4시)
  - PM_1800 → PM_0600 (오후 6시)
  - AM_0400 유지 (새벽 4시, 변경 불필요)
  - 폴더명 + 파일 내 참조 12개 파일 일괄 수정
  - CLAUDE.md 프로젝트 구조 섹션 업데이트

### Added
- **PM_0400 시리즈 패키징 및 업로드 준비 완료** `2a64214`
  - 9트랙 x 2회 반복 = 58.6분
  - description 최종 버전 (알고리즘 최적화 + 참여 유도)
  - 비공개 업로드 완료
- **PM_0400 Track 09 "서랍" 완성 - 시리즈 피날레** `87a853b`
  - 퍼소나: 모두 (시리즈 마무리)
  - 장르: Korean Pop Ballad, Pop-Rock
  - BPM: 108, Key: C Major
  - 보컬: Female, powerful chest voice, wide range
  - 시드곡: 다비치 타임캡슐 DNA 참조
  - 컨셉: 과거의 나에게 건네는 위로, 시간여행 감성
  - 훅: "시간이 조금만 천천히 가면 / 지금의 나를 한 번 더 안아 줄 텐데"
  - PM_0400 시리즈 9트랙 완성
- **PM_0400 Track 08 "컨펌" 완성** `ad80964`
  - 퍼소나: 프리랜서 (클라이언트 컨펌 대기)
  - 장르: Korean Indie Pop, Bright Bouncy Pop
  - BPM: 130, Key: A Major
  - 보컬: Male, light and playful, conversational
  - 컨셉: 통통 튀는 사운드 + 프리랜서 불안/자조
  - 훅: "컨펌 좀요 / 한 마디만요" + "제발 제발 제발요"
  - 엔딩: "이력서 안 쓰게요" (자조적 유머)
- **PM_0400 Track 07 "신호" 완성** `079a6c4`
  - 퍼소나: 배달기사 (오후 4시 반, 신호등 대기)
  - 장르: Korean Indie Pop, Bright Driving Pop
  - BPM: 126, Key: G Major
  - 보컬: Male, warm and relaxed, chest voice
  - 컨셉: 밝고 경쾌한 사운드 + 배달 일상의 고단함
  - 훅: "달리고 싶어 / 멈추기가 싫어" + "제발, 제발, 제발요"
  - 트랙 순서 변경: 07↔08 (배달기사↔프리랜서)
- **PM_0400 Track 06 "침묵" 완성** `37839cd`
  - 퍼소나: 취준생 (오후 4시, 탈락 통보 후 카페)
  - 제목 변경: 탈락 → 불합격 → 침묵
  - 장르: Korean Alternative Rock, Boy Band style Soft Pop-Rock
  - BPM: 160 half-time feel, Key: Eb Major
  - 보컬: K-pop idol boy band, bright and refreshing, sweet high notes
  - **컨셉: Bright instrumental vs sad anxious lyrics (대비)**
  - 훅: "닫힌 문 앞에 서 있어도" / "제발, 제발, 제발요"
  - 가사: 은유적 표현 (꺼지지 않게, 흐려지지 않게, 새벽이 오게)
  - txt 파일 전체 삭제 (concept.md SSOT 통합)
- **PM_0400 Track 05 "기다림" 완성** `43524a8`
  - 퍼소나: 주부 (오후 4시, 하원 전 고요한 시간)
  - 장르: Acoustic Band Rock, 95-102 BPM
  - 레퍼런스: 10cm 스토커 DNA + 밴드 어레인지
  - 훅: "이 순간 그대로 / 잠깐만 여기" + "조금 조금 조금요"
  - 감정: 고요한 자유 ↔ 기다림의 양면
  - 시리즈 훅 변형: "제발 제발 제발요" → "조금 조금 조금요" (부드러운 톤)
- **PM_0400 Track 04 "공강" 최종 완성** `8adfbc4`
  - 퍼소나: 대학생
  - 장르: Korean Indie Rock, Bright Pop Rock, 148 BPM, Bb Major
  - 특징: Jangly guitar, bouncy staccato picking, playful delivery
  - 훅: "그냥 여기 있고 싶어" / "공강 좀 늘려주세요"
- **PM_0400 Track 03 "7교시" 완성** `862ea43`
  - 퍼소나: 고등학생
  - 장르: Korean Alternative Rock, 84 BPM, Eb Major
  - 레퍼런스: DAY6 - 예뻤어
  - 특징: 베이스 중심 편곡, 슬픈 Verse + 폭발적 Chorus
- **PM_0400 "4시의 사람들" 시리즈 Track 01-02 완성** `7ba789e`
  - 시리즈 컨셉: 다양한 퍼소나들의 4시 (All Rock 장르)
  - 시그니처 훅: "제발, 제발, 제발요" (전 트랙 공통)
  - Track 01 "가도 되나요": Soft Pop-Rock, 160 BPM, Male (DAY6 HAPPY 레퍼런스)
  - Track 02 "눈치": J-Rock/Idol Rock, 160 BPM, Female (QWER 고민중독 레퍼런스)
  - 전체 10트랙 플레이리스트 구조 확정 (직장인/학생/주부/취준생/프리랜서/배달기사/퇴직자 등)
- **PM_0600 유튜브 업로드용 설명 추가** `d5d0e16`
  - draft_description.txt: 제목, 설명, 타임스탬프, 고정 댓글
  - .gitignore에 draft_description.txt 예외 추가
- **PM_0600 "퇴근길" 시리즈 9트랙 완성** `446051b`
  - Track 05 "쪽잠": 버스 안 쪽잠, 78 BPM, G minor, Female vocal (W:35/I:70)
  - Track 06 "전화": 퇴근길 전화 통화, 88 BPM, Db Major, Male vocal (W:35/I:70)
  - Track 07 "골목": 혼자 걷는 골목길, 67 BPM, Db Major, Male vocal (기존 싱글)
  - Track 08 "숨": 문 앞에서 숨 고르기, 70 BPM, Ab Major, Female vocal (W:40/I:60)
  - Track 09 "이름": 문 열림 이름 불려짐, 72 BPM, Ab Major, Male vocal (기존 싱글)
  - concept.md SSOT 통합: 개별 txt 파일 삭제, 전체 가사/스타일 concept.md에 기록
  - 10트랙 → 9트랙 확정 (Track 09 "이름"으로 Closing)
- **PM_0600 "퇴근길" 시리즈** `2805367` `0c6b49e` `216aee5` `6a1a4ba` `217fe40`
  - Track 01 "Exit": Uptown Funk 벤치마킹, 115 BPM, Eb Major, Korean Funk-Pop
  - Track 02 "약속": 자니 벤치마킹, 100 BPM, Db Major, Neo-soul R&B
  - Track 03 "정류장": 약속 커버 (글자수 완벽 매칭 기법), G minor 변주
  - Track 04 "차창밖": Verse-driven 구조, 85 BPM, G minor, Female vocal, Solo only, Blues R&B
  - concept.md 전체 구조 (10곡 플랜, 감정 아크, BPM 아크)
  - Reference/song/자니.pdf, uptown-funk.pdf 추가
- **LYRICS.md §2.3 메타태그 동작 원리** `2805367`
  - `[AA]` 대괄호: 구조 태그, 절대 낭독 안 됨
  - `(BB)` 소괄호: 100% 낭독 (가사) / ~30% 인식 (톤 지시)
  - 톤 지시는 반드시 단독 행에 배치
  - 감정/분위기 태그 → Style Prompt로 이동 규칙
- **CLAUDE.md v2.8.0 메타태그 검증 단계** `2805367`
  - 가사 생성 워크플로우 Step 4 추가

### Changed
- **Git LFS 설정** `06fff55`
  - *.mp4 파일 Git LFS 추적 설정
  - 히스토리 재작성으로 기존 대용량 파일 LFS 마이그레이션
  - GitHub 100MB 제한 해결

### Added
- **골목 싱글 (PM 07:00 퇴근길의 위로)** `6a538e4`
  - single.mp4: 0.5초 crossfade 루프 영상
  - 골목_youtube.md: 업로드 정보 (제목, 설명, 챕터, 해시태그)
  - PM 07:00 시리즈 첫 싱글 선공개

### Changed
- **SSOT 정리 5단계 완료** `f1b5ee5` `2d35cb6`
  1. MANAGER Pure Input → LYRICS §2 참조 (SSOT 통일)
  2. 글자수 제한 1000 → 800 통일 (전 문서)
  3. 보컬 메타태그 필수 규칙 LYRICS §2.2에 SSOT 승격
  4. STYLE에서 falsetto 트리거 단어 제거 (→ upper register)
  5. CLAUDE.md 역할 명확화 (사용 매뉴얼, 요약 표시)
  - MASTER/_INDEX.md SSOT 라우터 추가
  - 버전: MANAGER v1.3, STYLE v2.6.3, LYRICS v1.9.1, CLAUDE v2.7.0

- **바라봐줘요 seed 가사/스타일 업데이트** `c861208`
  - 기존 분석 문서를 트랙 생성용 가사+스타일로 교체
  - Suno Parameters: W:30 I:60

### Added
- **바라봐줘요 Seed Research + 골목 시드 트랙**
  - 레퍼런스 분석: 죠지 - 바라봐줘요 (67 BPM, Db Major, 확장 코드)
  - 시드 트랙 "골목" 가사 + Style Prompt + Exclude 완성
  - Synth piano-led, Minimal drums, Male vocal (Raw, Dry)
  - S1-S12 Validation Table 포함

### Changed
- **SSOT 슬롯 체계 통일** (CLAUDE.md v2.6.2, STYLE.md v2.6.2, ROLES.md v1.7)
  - CLAUDE.md를 슬롯 정의 SSOT로 지정 (S0-S20, 20개 슬롯)
  - STYLE.md "9-Slot Table" → CLAUDE.md 참조로 변경
  - ROLES.md S1-S12는 압축 검증용임을 명확화
  - S10-S12 (Articulation, Reverb, Sound Engineering) 필수 강제

### Added
- **PM_0200 vol1 플레이리스트 완성** `7c1155e`
  - 10곡 트랙 파일 추가, final.mp4 생성 (53.5분, x2 반복)
  - draft_description.txt 최종안 (피드백 반영, 해시태그 8개 최적화)
- **PM_0200 Track 10 "깸" 추가 - 수미상관 완성 (10곡 확정)**
  - Track 01 "멍" ↔ Track 10 "깸" 수미상관 구조
  - 같은 BPM(74)/Key(Eb)/Lead(Clean Electric Guitar)
  - 후렴 대칭: "멍때려요" ↔ "일어나요"
  - punchy bass guitar, bouncy groove 스타일
- **PM_0200 Track 07-09 추가**
  - Track 07 "온기" (Female, 70 BPM, Db Major)
  - Track 08 "그늘" → Track 07로 재배치 (Male, 72 BPM, Ab Major)
  - Track 09 "구름" → Track 08로 재배치 (Female, 76 BPM, F Major)
- **CLAUDE.md v2.6: 워크플로우 개선**
  - Suno 파라미터 가이드 (W:35/I:65 기본값)
  - Style Prompt + Exclude 세트 출력 규칙
  - 곡 길이 확장 규칙 (구조 태그로 확장, Verse 8행 금지)
  - 복사용 .txt 파일 저장 워크플로우
- **PM_0200 트랙 순서 재배치 (A안)**
  - 멍(01) → 얼음(02) → 산책(03) → 온기(04) → 돛(05) → 물결(06) → 그늘(07) → 구름(08) → 먼지(09)
  - 산책/물결/먼지 2트랙 이상 간격 확보 (운율 겹침 방지)

### Changed
- **AM_0400/PM_0200 실제 YouTube 제목/설명/고정댓글 기록** `f03ce6b`
  - AM 04:00: `[Playlist] [AM 04:00] soomshuim | 하루가 멈춘 시간, Slow R&B 보컬`
  - PM 02:00: `[Playlist] [PM 02:00] soomshuim | 햇살에 멍해지는 시간, Chilling R&B`
  - 고정 댓글 통일 (AI 협업 언급 추가)
- **AM_0400/PM_0200 디스크립션 포맷 통일**
  - 제목: `[시간대] 감성 키워드 | 상황 + 장르`
  - 해시태그 8개 최적화 (#AM04시/#PM02시 + #soomshuim)
- **SERIES 폴더 구조 단순화** (CLAUDE.md v2.6.1)
  - vol1 폴더 제거, 파일들 상위로 이동
  - `SERIES/AM_0400/vol1/` → `SERIES/AM_0400/`
  - `SERIES/PM_0200/vol1/` → `SERIES/PM_0200/`

- **PM_0200 vol1 트랙 리스트 확정 (6곡)**
  - Track 01 "산책", Track 02 "멍", Track 03 "물결", Track 04 "얼음", Track 05 "먼지", Track 06 "돛"
  - 그룹 A/B/C 교차 배치로 운율 반복 방지
  - Female vocal (얼음) 중간 배치로 다양성 확보
  - 4곡 추가 예정 (07~10)
- **PM_0200 Track 02 "물결"**: Boat 악보 분석 반영 (Final_v4)
  - Key: A Major (Boat 원곡 동일)
  - Chord: Neo-soul extended (M9, m7)
  - Melody: Narrow range, stepwise, speech-like rhythm
  - Lyrics: 직접적/담백한 Boat 스타일
  - QC Checklist: Speech-like 항목 추가
- **PM_0200 vol.2 시드 트랙**: Track 01 "먼지" 가사/스타일 확정
  - Reference: 죠지 - Boat (표류하는 느낌, R&B groove)
  - Male vocal, Vibraphone-led, 72 BPM, Eb Major
- **CLAUDE.md v2.2.0: Style Prompt QC 워크플로우**
  - S15 글자수 제한 (< 800자, wc -c 검증 필수)
  - S16 Lead Instrument Supportive 규칙
  - S17 Chorus Expansion Density 규칙
  - 검증 통과 전 유저 제안 금지
- **LYRICS.md v1.8: 가사 품질 규칙 추가**
  - 1.10 Image Density Management (V1=공간, V2=감각 분리)
  - 1.11 Chorus Tone Rule (관조 톤, 직접 호소 최소화)
- **vibem.py: 타이틀 자동 생성 (SSOT v1.5)**
  - draft_description.txt 상단에 제목 초안 자동 생성
  - concept.md에서 Title Meta 파싱 (Context Mode, Time, GENRE 등)
  - 메타 없으면 트랙 정보에서 자동 추론
- **vibem.py: shorts 커맨드 v2.0.0**
  - 입력 변경: `loop.mp4` → `shorts.mp4` (8~10초)
  - 짧은 영상을 음악 길이만큼 자동 루프
  - 출력: `output/shorts/short_[TrackName].mp4` (유지)
- **PLAYLIST_GUIDE.md v1.2: Playlist Title Generation Rules (SSOT v1.5)**
  - 타이틀 고정 구조: `[Playlist] [AM/PM HH:MM] soomshuim | {TIME_STATE_PHRASE}, {MODIFIER_PHRASE} {GENRE}`
  - Context Mode 필수 입력 (Settling/Transition/Energizing/Focusing)
  - TIME_STATE_PHRASE Type A/B 교대 규칙
  - GENRE 확장: R&B, Rock, Pop, Jazz 등
- **vibem.py: pack --repeat 옵션**
  - 플레이리스트 N회 반복 재생 (기본값 2회)
  - description에 회차 구분 없이 단일 타임스탬프 표시
- **vibem.py: draft_description.txt 자동 생성**
  - 시리즈/컨셉 기반 커스텀 인트로 문단
  - 📌 고정 댓글 섹션 (시간대별 인삿말)
  - Source/Derived 분리 원칙 (concept.md = SSOT)
- **/vibem 커맨드**: 프로젝트 재개용 컨텍스트 로더

### Changed
- **시리즈 디렉토리 변경**: `SERIES/잠들지_못한_새벽/` → `SERIES/AM_0400/`
- **첫 플레이리스트 제목/URL 변경**
  - 시리즈 컨셉: "[AM 04:00] 하루가 멈춘 시간"
  - YouTube 제목: "[Playlist] [AM 04:00] soomshuim | 하루가 멈춘 시간, Slow R&B 보컬"
  - 새 URL: https://youtu.be/i1GHmn1WZr4
- **CLAUDE.md v2.0.0: Shorts 워크플로우 업데이트**
  - 입력: shorts.mp4 (8~10초) 루프 방식
  - 프로젝트 구조에 shorts.mp4 추가
- **VIBE-M_Master_Plan.md: Shorts 커맨드 스펙 추가**
- **커맨드 체계 변경**: .claude/commands/ → 글로벌 커맨드로 통합
  - coach, record 삭제 → 글로벌 스킬로 이전
  - /vibem 신규 추가

- **LYRICS.md v1.7: Korean Lyric Positioning**
  - 한국어 가사 플레이리스트 차별점 공식화
  - 포지셔닝 원칙: 의미 있는 가사, 혼자 읽히는 언어, 소리가 먼저
  - 가사 설계 철학: 감정 직접 표출 금지, 사물/공간/현상 중심
  - K1-K3 한국어 검증 체크리스트 추가
  - 메타/브랜딩 적용 규칙
- **CLAUDE.md v1.6.0: Korean Positioning Workflow**
  - 가사 생성 Step 3에 Korean Positioning 검증 추가
  - 검증 출력 포맷에 Section C (K1-K3) 추가
- **24H_UNIVERSE.md v1.0: Master Project Bible**
  - 24H Universe 세계관 정의 (시간 기반 감정 스테이션)
  - 10개 Time Station 정의 (02:00~04:30)
  - 5개 Key/Mode Bucket 시스템
  - Production Templates 3종 (Track Brief, Style Skeleton, Lyrics Skeleton)
  - Station QC Checklist (Listen/Lyric/Style/Exclude 검증)
  - DNA Constants vs Variables 명세
- **PLAYLIST_GUIDE.md v1.1: Korean Lyric Positioning 3-Layer 전략**
  - Layer 1: 재생목록 설명 (자연스럽게)
  - Layer 2: 고정 댓글 (팬 메시지)
  - Layer 3: 채널 About (명확하게)
  - 템플릿 + DO/DON'T 규칙
- **vibem.py: description.txt 우리말 가사 문구 자동 추가**
  - "이 플레이리스트의 노래들은 모두 우리말 가사로 만들어졌습니다."
  - "*All tracks feature Korean lyrics.*"

- Track 09 "마음안": 수미상관 마지막 곡 (Track 01 "마음밖" 대응)
  - Male vocal + Powerful belt, 95 BPM, Db Major
  - 키워드 축: 여명/옥상/난간/지평선
  - 후렴: "마음 안으로 번져와 / 여명처럼 스며들어"
- Track 08 "빗줄기": Melancholic R&B, 85 BPM, F minor, Rhodes-led
  - 키워드 축: 빗줄기/아스팔트/골목/처마/우산
  - Raw Vocal + Chest Belt, Contralto female
  - 메타태그 포함 (Direct vocal, Chest voice, Powerful belt)
- **STYLE.md v1.7: Fail Fast Energy Check**
  - Chorus held note 정량화: "exactly 1 held note (longer sustain than any verse note)"
  - V2 → Chorus FAIL 조건 4개: register/intensity 미상승, 1 held note 부재, 레이어 의존
- ROLES.md v1.2: Automatic FAIL Conditions 추가
  - Chorus energy ≤ Verse2 → FAIL
  - Vocal intensity peak 부재 → FAIL
- 00_system.txt: Mandatory Slot Check 추가
  - 슬롯 누락 시 재생성 강제
  - Vocal Persona 누락 = INVALID
- 02/03_designer.txt: INVALID conditions 추가
- **STYLE.md v1.6: Energy Permission + Safety Separation**
  - 핵심 원칙: "금지는 레이어에만, 허용은 에너지에"
  - Verse2 에너지 상승 권한 명시적 부여 (encouraged/allowed/must)
  - 새 Harmony Guard: "Lead vocal remains single and dominant"
- ROLES.md v1.1: Energy Permission Principle 추가
  - Seed Designer에 에너지 허용 원칙 명문화
  - Sanity Check에 "Verse2 energy permission" 항목 추가
- 02_designer.txt: Safety Lines + Energy Permission 분리
- 03_variation.txt: Vocal Energy Risk Fail 조건 추가
  - Verse2 lacks lift → FAIL
  - Chorus sounds flat due to over-safety → FAIL
- PLAYLIST_GUIDE.md: 유튜브 감성 플레이리스트 인기 사례 분석 가이드
  - TPO 패턴, 제목 전략, 썸네일 가이드, 시리즈화 전략
  - Reference/ 디렉토리에 원본 PDF 추가
- Track 04 "물안개": 가사 + Style Prompt (Lo-fi R&B, Male vocal, 80 BPM)
- LYRICS.md v1.1: 새 규칙 4개 추가
  - 1.5 Vocabulary Independence (어휘 독립성)
  - 1.6 Snapshot Hook Rule (스냅샷 훅)
  - 1.7 Bridge Thesis Constraint (테제 제약)
  - 1.8 V2 Escalation Rule (2절 상승)
- Role System 문서화: ROLES.md + prompts/ 4종 + QUICK_REF.md
  - Seed Researcher / Seed Designer / Variation Designer 역할 분리
  - 사람용 운영 매뉴얼 (QUICK_REF.md) 별도 분리
- Test_Series concept.md: Track 01~04 가사/스타일 기록

### Changed
- **첫 플레이리스트 YouTube 업로드 완료** (2026-01-20 22:00 공개)
  - 제목: "[Playlist] [AM 04:00] soomshuim | 하루가 멈춘 시간, Slow R&B 보컬"
  - URL: https://youtu.be/i1GHmn1WZr4
  - 채널: soomshuim
  - 재생목록: "하루를 듣는 방법 | 24 Hours Playlist"
- **첫 플레이리스트 정식 출범**: Test_Series → "[AM 04:00] 하루가 멈춘 시간"
  - 디렉토리: `SERIES/Test_Series/2026-01-18/` → `SERIES/AM_0400/vol1/`
  - 9트랙 완성 (Track 01~09)
- **STYLE.md v1.5 → v1.6: Energy Permission + Safety Separation**
  - v1.5 문제: "금지 규칙이 에너지 규칙을 덮어버림" → 보컬이 무난해짐
  - v1.6 해결: "금지는 레이어에만, 허용은 에너지에" 분리
  - ❌ "vocals unchanged" → ✅ "lead vocal energy may increase, but no new vocal layers"
  - ❌ "Single lead vocal ONLY" → ✅ "Lead vocal remains single and dominant"
  - Verse2 에너지 상승: "encouraged", "allowed", "must" 권한 부여
- CLAUDE.md: 체크리스트 기반 워크플로우 강화
  - 가사/Style Prompt 생성 시 필수 검증 프로세스 명문화
  - 플레이리스트 컨셉 논의 시 PLAYLIST_GUIDE.md 자동 참조
- MANAGER.md v1.1: Phase 2 Track QC에 코러스 과다 Fail 기준 추가
- 02_designer.txt: Safety Lines 작성 규칙 제로 베이스라인으로 업데이트

### Fixed
- vibem.py preview: 각 트랙이 미리보기에 포함되도록 수정
  - 이전: 전체 병합 후 앞 N초 (Track 01만 포함)
  - 이후: 각 트랙 앞 N/트랙수 초씩 잘라서 병합
