# Korean Afrobeats Rubric

Version: 2.0
Last Updated: 2026-03-14
Purpose: Korean Afrobeats 장르 게이트 (12-00 시리즈)

> Based on: `SERIES/12-00/reference/00-synthesis.md` + concept.md

---

## Hard Gates (1개라도 FAIL = 재작성)

| # | Gate | 기준 |
|---|------|------|
| H1 | BPM | 100-112 범위 |
| H2 | Rhythm | 3-2 Son Clave 기반 싱코페이션 퍼커션 존재 |
| H3 | Percussion | Shaker/Congas/Cowbell/Hi-hat 중 2개+ |
| H4 | Bass | 808 또는 synth bass, 킥과 동기화된 그루브 |
| H5 | Vocal | 한국어 보컬 + Chest voice + 단독 리드 (Harmony Guard) |
| H6 | Hook | 1-2마디 반복 훅 존재, 3-8음절 |
| H7 | Exclude | EDM drop / falsetto / stacked harmonies 없음 |

---

## Style-Specific Gates (Style C/D/E)

### Style C — Minimal Afro
| # | Gate | 기준 |
|---|------|------|
| C1 | Sparse | 악기 밀도 낮음, 공간감 넓음 |
| C2 | Vocal-forward | 보컬이 믹스의 중심 |
| C3 | Intentional | 과잉 프로덕션 없음, 절제된 편곡 |

### Style D — Afropiano
| # | Gate | 기준 |
|---|------|------|
| D1 | Log Drum / Piano | 로그 드럼 또는 재즈 피아노 그루브 존재 |
| D2 | Rolling Percussion | 트랩 하이햇 + 셰이커 리듬 조합 |
| D3 | Moody Groove | 무디하고 공간감 있는 그루브 |

### Style E — Afro-Drill
| # | Gate | 기준 |
|---|------|------|
| E1 | 808 Slide Bass | 슬라이드 베이스 존재 |
| E2 | Drill Pattern | 림샷 스네어 + 트랩 하이햇 롤 패턴 |
| E3 | Dark Energy | 다크하고 무디한 멜로디/에너지 |

---

## 8-Factor Scoring (100점)

| # | Factor | 배점 | 기준 | 레퍼런스 |
|---|--------|------|------|---------|
| F1 | Afro Groove | 15 | 3-2 clave 기반 리듬감, 싱코페이션, 폴리리듬 레이어링 | Calm Down, Essence |
| F2 | Percussion | 10 | 퍼커션 레이어링 완성도 (스타일별 조합) | 리서치 §1.3 |
| F3 | Melody/Hook | 15 | 1-2마디 반복, 링 프레이즈, 챈트감 | 리서치 §4 |
| F4 | 한국어 보컬 | 15 | Suno 생성 보컬/가사 자연스러움, 한국어 발음 명료도, 장르 적합성, 훅 중독성 | 청취 QC |
| F5 | Bass & Low-end | 10 | 808 싱코페이션, 킥과 locked-in, 과하지 않은 움직임 | 리서치 §2.3 |
| F6 | 에너지 아크 | 10 | V→V2→C 상승, Chorus belt/higher register, Bridge 에너지 유지 | STYLE.md §3-4 |
| F7 | 프로덕션 | 15 | 악기 공간 분리(EQ), 보컬 포워드, 리버브 절제, Filler 없음, Harmony Guard | STYLE.md §1-2 |
| F8 | 장르 정체성 | 10 | Afrobeats로 인식되는가? (팝/R&B/EDM으로 이탈하지 않았는가) | 종합 판단 |

---

## 판정

| 점수 | 판정 | 액션 |
|------|------|------|
| 85+ | **PASS** | 진행 |
| 70-84 | **BORDERLINE** | 문제 Factor 수정 후 재평가 |
| <70 | **FAIL** | 재작성 |

**CRITICAL FAIL:** 개별 Factor ≤ 배점의 30% = 즉시 FAIL
- F1 ≤4, F2 ≤3, F3 ≤4, F4 ≤4, F5 ≤3, F6 ≤3, F7 ≤4, F8 ≤3

---

## Style Checklist

| # | 항목 | C | D | E | 체크 |
|---|------|---|---|---|------|
| S1 | BPM 100-112 | ● | ● | ● | ☐ |
| S2 | Syncopated African percussion | ● | ● | ● | ☐ |
| S3 | 808 bass groove | ● | ● | ● | ☐ |
| S4 | Sparse/vocal-forward | ● | | | ☐ |
| S5 | Log drum / jazzy piano | | ● | | ☐ |
| S6 | Rolling percussion + trap hi-hats | | ● | ● | ☐ |
| S7 | 808 slide bass | | | ● | ☐ |
| S8 | Rimshot snare + drill pattern | | | ● | ☐ |
| S9 | Chest voice + raw/direct | ● | ● | ● | ☐ |
| S10 | No filler sounds | ● | ● | ● | ☐ |
| S11 | Harmony Guard (단독 리드) | ● | ● | ● | ☐ |
| S12 | Articulation 포함 | ● | ● | ● | ☐ |
| S13 | Exclude 키워드 준수 | ● | ● | ● | ☐ |

---

## 보컬 Checklist (Suno 결과물 청취 QC)

| # | 항목 | 체크 |
|---|------|------|
| V1 | 한국어 발음 명료 (뭉개짐 없음) | ☐ |
| V2 | 훅 존재 + 중독성 (반복 시 각인) | ☐ |
| V3 | 보컬 톤이 장르에 적합 (Afrobeats 감성) | ☐ |
| V4 | 단독 리드 보컬 (합창/스택 없음) | ☐ |
| V5 | 가사 자연스러움 (AI스러운 어색함 없음) | ☐ |

---

## QC Template

```
## Afrobeats QC — Track {N} "{제목}"

### Hard Gates
| Gate | 결과 | 비고 |
|------|------|------|
| H1 BPM | | {N} BPM |
| H2 Rhythm | | |
| H3 Percussion | | |
| H4 Bass | | |
| H5 Vocal | | |
| H6 Hook | | |
| H7 Exclude | | |

### Style {C/D/E} Gates
| Gate | 결과 |
|------|------|
| {X}1 | |
| {X}2 | |
| {X}3 | |

### 8-Factor Scoring
| Factor | 점수 | 비고 |
|--------|------|------|
| F1 Afro Groove | /15 | |
| F2 Percussion | /10 | |
| F3 Melody/Hook | /15 | |
| F4 한국어 보컬 | /15 | |
| F5 Bass & Low-end | /10 | |
| F6 에너지 아크 | /10 | |
| F7 프로덕션 | /15 | |
| F8 장르 정체성 | /10 | |
| **Total** | **/100** | |

### Style Checklist: S1-S13
### 보컬 Checklist: V1-V5

### 판정: PASS / BORDERLINE / FAIL
### 수정 사항: (BORDERLINE/FAIL 시)
```
