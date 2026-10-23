# 06:30 1번 박자 지시 수정안 — 생성 전 검토용

- 상태: **젠 승인·Suno 생성 접수·새 후보 박자 측정 전**. 젠 원문 “박자 지시 수정안으로 재생성 (추천)”에 따라 [round4 별도 제출 원본](../../SERIES/06-30/input/retry-sources/track01-round4-tempo-explicit-2026-10-23.json)을 작성했다. 기존 20개 TXT와 packet은 수정하지 않았다. 승인 입력으로 Create를 한 번 눌렀고 [결과 UI](../../SERIES/06-30/input/bpm-audit/evidence/2026-10-23-track1-regeneration-round4-results-ui.json)에서 새 후보 2개·크레딧 1,776→1,766을 확인했다. 약 50초 동안 spinner였으나 재클릭하지 않았다. 최초 결과는 생성 중이므로 Play·30초 BPM은 확인 전이다. 범위 밖 후보의 휴지통 이동은 기존 사용자 지시로 이미 허용됐다. 1번의 3회 제출로 얻은 6후보가 각각 다른 30초 샘플에서 독립 검토상 175–177 BPM 밖이었다. 최초 두 후보는 3분 이상 길이에도 못 미쳤다. 자동 분석 `uncertain` 원시는 유지하며 독립 결과와 구분한다. 반복 실패의 원인은 확인되지 않았다.
- 고정: 가제 `첫 박부터`, Instrumental(무가사), E Minor, 하드코어 펑크 록, E5 → G5 → D5 → A5, 팜뮤트 기타·옥타브 기타·루트 베이스·강한 라이브 킥/스네어, 175 BPM 목표, 약 3:18 길이 목표. EXCLUDE 8항목과 LYRICS `[Instrumental]`도 원본 그대로 둔다.
- 변경: 박자를 **4분음표 기준 175회/분(한 박 약 0.343초)**으로 더 정확히 적고, 같은 박이 처음부터 끝까지 유지되며 스네어가 2·4박에 놓인다고 명시한다. 원본의 `fast eighth-note hats`를 같은 175 BPM 안의 `steady eighth-note hats`로 바꾼다. 실제 생성 박자가 교정된다는 보장은 없다.

## 기존 STYLE (동결 원문, 544자)

```text
Instrumental hardcore punk rock, fixed 175 BPM in E Minor, straight 4/4 from the first bar through the final hit. Strong punchy kick and cracking snare carry an unmistakable full-speed running step throughout. Palm-muted low E guitar drives E5 -> G5 -> D5 -> A5. Its tight three-note riff jumps upward on the last A5 while a second guitar opens into ringing octaves. Root-note bass and dry live kick-cracking snare push against fast eighth-note hats; the expanded hook doubles the upper guitar rather than relaxing the beat. Aim for about 3:18.
```

## 제안 STYLE (완전 문구, 664자)

```text
Instrumental hardcore punk rock, in E Minor, steady 4/4 with exactly 175 quarter-note beats per minute from the first bar through the final hit. Strong punchy kick and cracking snare lock the full-speed running step to that same 175 BPM pulse throughout; snare accents beats 2 and 4 without speeding up. Palm-muted low E guitar drives E5 -> G5 -> D5 -> A5. Its tight three-note riff jumps upward on the last A5 while a second guitar opens into ringing octaves. Root-note bass and dry live kick-cracking snare push against steady eighth-note hats within the 175 BPM grid; the expanded hook doubles the upper guitar rather than relaxing the beat. Aim for about 3:18.
```

## 실행 조건

젠이 이 **박자 지시 수정안**을 선택하면 새 입력을 별도 버전으로 기록하고 제출한다. 그 전에는 동결된 20개 TXT와 source packet을 바꾸지 않는다. 생성 후에도 새 후보의 유효 30초 녹음·실측·독립 판정 없이 175–177 BPM 성공으로 세지 않는다.

승인 조건은 충족됐다. 위 STYLE 문구를 그대로 담은 별도 JSON의 SHA-256은 `f624c1cdd9a881e93ac4f172deab84c64e3c3f9f8fbf48c6252a75da9a9e2b25`이다. 해당 JSON의 `submission_performed: false`는 작성 시점 입력 스냅샷이며 변경하지 않는다. 이후 실제 제출·신규 후보는 위 UI와 후보 manifest로 기록하고, 30초 판정은 아직 없다.
