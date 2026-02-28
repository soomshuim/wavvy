# Claude Code Instructions - vibe-m

Version: 2.14.0
Last Updated: 2026-02-24
Purpose: YouTube Music Playlist Generator CLI 실행 매뉴얼 (비-SSOT 요약)

## SSOT 경고

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
| **Chillhop 장르 루브릭** | `MASTER/rubrics/CHILLHOP_RUBRIC.md` |
| **루브릭 생성 프로세스** | `MASTER/RUBRICS_CREATION_PROCESS.md` |

## Hard Constraints (절대 제약)

> 출처: `MASTER/MANAGER.md` Phase 0

1. **NO Pydub** - 메모리 누수 방지, Pure FFmpeg만 사용
2. **Sequential Acrossfade** - 단순 concat 금지
3. **Fail Fast** - 입력 검증 실패 시 즉시 종료
4. **Pure Input Principle** - Suno 가사란에 가사 + 구조 태그 + 구조 직후 1행 `()` 메타만 (설명형 지시어 금지)
5. **크로스페이드 구분 필수** - 오디오 vs 비디오 반드시 구분. "크로스페이드" 요청 시 어느 쪽인지 확인

## Auto Reference Rules

| 요청 유형 | 참조 문서 | 읽을 범위 |
|----------|----------|----------|
| **24H Universe 트랙 생성** | `MASTER/24H_UNIVERSE.md` | 전체 |
| **플레이리스트 컨셉 논의/시작** | `MASTER/PLAYLIST_GUIDE.md` | 전체 |
| **플레이리스트 타이틀 생성** | `MASTER/PLAYLIST_GUIDE.md` | §0 |
| **가사 작성/수정** | `MASTER/LYRICS.md` + `Reference/museA_suno_guide.md` | 전체 + §3-4 |
| **Style Prompt 작성** | `MASTER/STYLE.md` + `Reference/museA_suno_guide.md` | 전체 + §2,6 |
| 플레이리스트 프로파일 | `MASTER/STYLE.md` | §3 |
| QC/Fail Fast 기준 | `MASTER/MANAGER.md` | §1, §3 |
| 역할 분리/AI 작업 | `MASTER/ROLES.md` | 전체 |
| FFmpeg 필터 작업 | `.ai/lessons-learned.md` | "필터 그래프 버그" 섹션 |
| 정규화 작업 | `.ai/lessons-learned.md` | "ffmpeg-normalize 버그" 섹션 |
| 새 커맨드 추가 | `MASTER/VIBE-M_Master_Plan.md` | CLI 커맨드 명세 |
| **곡 발음 수정** | `Reference/museA_suno_guide.md` | §7 Cover 기능 |
| **장르별 트랙 QA** | `MASTER/rubrics/[GENRE]_RUBRIC.md` | 전체 (총점 >= 80 AND 개별 > 5 = PASS) |
| **새 장르 루브릭 생성** | `MASTER/RUBRICS_CREATION_PROCESS.md` | 전체 |

## Workflow Rules

### 가사 생성 워크플로우
> **SSOT: `MASTER/LYRICS.md` (체크리스트) + `MASTER/MANAGER.md` Phase 0.5 (수정 절차)**

1. `LYRICS.md` + 이전 트랙 키워드 확인 + 크로스시리즈 겹침 검증 (3축 중 2개 이상 겹침 = FAIL)
2. `Reference/museA_suno_guide.md` §3-4 참조 (구조 공식, 메타태그 규칙)
3. 초안 생성 -> self-QC (LYRICS.md 전항목) -> Korean Positioning (K1-K3) -> 메타태그 검증 -> 장르 게이트 (루브릭) -> 패턴 고착 검사
4. 전부 PASS시 QC 테이블과 함께 출력 (통과 전 유저 제안 금지)
5. .txt 파일 저장 + pbcopy -> 유저 컨펌 후 concept.md 반영

### Style Prompt 생성 워크플로우
> **SSOT: `MASTER/STYLE.md` (S0-S20 슬롯) + `MASTER/ROLES.md` (S1-S12 Validation)**

1. `STYLE.md` Required Slots + `Reference/museA_suno_guide.md` §1,2,6 참조
2. 초안 생성 -> self-QC (S0-S20) -> 글자수 검증 (<= 900자, 공백 포함) -> 장르 게이트
3. 전부 PASS시 QC 테이블 + 글자수와 함께 출력 (Style + Exclude 반드시 세트 출력)
4. .txt 파일 저장 + pbcopy -> 유저 컨펌 후 concept.md 반영

### 가사/스타일 수정 절차
> **SSOT: `MASTER/MANAGER.md` Phase 0.5**

txt 먼저 수정 -> 유저 컨펌 -> concept.md 반영 (역순 금지, 동시 수정 금지)

### Concept 파일 최종 QC
> **SSOT: `MASTER/MANAGER.md`**

concept 작성 완료 후 검증: 편곡지시 분리, 글자수, 타이틀/Description 포맷, Cross-Series 겹침, 저작권 표기, SSOT version

### Shorts 생성
> **SSOT: `MASTER/VIBE-M_Master_Plan.md` (CLI 스펙)**

- 반드시 시리즈/트랙/구간 확인 후 생성. 시작/종료 시간 임의 수정 절대 금지
- Hook Title (선언문, 가사 그대로 사용 금지) + Bottom Lyric (하단 가사) 2-Layer 구조
- 타이포: Shadow 필수, Stroke 금지, 하단 30% 침범 금지 (YouTube UI 영역)
- CLI: `python3 vibem.py shorts <track> --start MM:SS --duration SEC [--title "..."] [--srt file.srt]`

### 영상 패키징 워크플로우
> **⚠️ 크로스페이드 = 오디오 + 비디오 둘 다 필요**

**1. 크로스페이드 종류 구분:**

| 종류 | 도구 | 설명 |
|------|------|------|
| **오디오 크로스페이드** | `vibem.py pack --fade` | 트랙 간 오디오 전환 (acrossfade) |
| **비디오 크로스페이드** | FFmpeg `xfade` 필터 | 루프 영상 자연스러운 반복 |

**2. vibem.py pack 한계:**
- 오디오 크로스페이드만 적용
- 비디오는 `-stream_loop -1`로 단순 반복 (끊김 발생)

**3. 비디오 크로스페이드 필요 시:**
```bash
# Step 1: loop.mp4를 xfade로 N번 반복 (테스트 먼저)
ffmpeg -i loop.mp4 -i loop.mp4 -i loop.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=7.5[v1];[v1][2:v]xfade=transition=fade:duration=0.5:offset=15[v2]" \
  -map "[v2]" -c:v libx264 -an loop_xfade.mp4

# Step 2: 오디오와 합치기
ffmpeg -i loop_xfade_long.mp4 -i audio.m4a -c:v copy -c:a copy -shortest final.mp4
```

**4. 워크플로우:**
1. 사용자가 테스트용 비디오 크로스페이드 영상 제작
2. Claude가 **명시적으로 PASS 여부 확인** ("이 크로스페이드 PASS인가요?")
3. PASS 시 해당 옵션(duration 등)으로 유튜브용 영상 자동 제작 (오디오 + 비디오 크로스페이드)
4. 압축 (2GB 미만 등)

**⚠️ PASS 확인 없이 본 작업 진행 금지**

## Project-Specific Gotchas

- **FFmpeg 필터 그래프**: Sequential acrossfade 패턴 준수, 라벨 `[a{N}]` 인덱싱 확인 (`.ai/lessons-learned.md`)
- **정규화**: `sys.executable -m ffmpeg_normalize`, 출력 WAV만, 원본 덮어쓰기 금지
- **Concept 파일 위치**: `SERIES/[시리즈명]/concept.md`에만 존재. 루트에 임시 파일 금지
- **DEBUG vs PROD**: 같은 문제 2회 재발 시 DEBUG 모드 (1개 변수만 변경). 상세: `MASTER/STYLE.md` §10
- **Suno Parameters 기본값**: Weirdness 35, Style Influence 65. concept.md에 트랙별 기록
- **곡 길이 확장**: 가사 늘리지 말고 구조 태그로 ([interlude], [instrumental]). Verse 8행 이상 금지

## Quick Commands

| 명령 | 설명 |
|------|------|
| `python3 vibem.py validate <path>` | 파일 검증 |
| `python3 vibem.py preview <path> --sec 30` | 미리보기 생성 |
| `python3 vibem.py pack <path>` | 최종 패키징 |
| `python3 vibem.py shorts <track> --start MM:SS --duration SEC` | 숏츠 생성 |
| `python3 vibem.py clean <path>` | 작업 폴더 정리 |

## Token Saving

- `MASTER/` 문서 링크로 규칙 참조, 필요한 파일만 읽기
- 전체 코드 재작성 금지, 추측 수정 금지 (로그 확인 먼저)
- 토큰 90% 초과 시: `.ai/SESSION.md` 업데이트 -> `/compact` 제안
