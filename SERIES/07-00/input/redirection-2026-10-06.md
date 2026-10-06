# 07:00 source redirection — 2026-10-06

Status: 1차 교체 13곡의 A/B 26개 생성은 이력으로 보존한다. 젠은 그중 01·05·07·08·12·15·16·17·20에서 각 한 곡을 남겼고, 06·09·10·11은 다른 스타일로 재생성했다. 새 A/B 여덟 후보는 아직 선택 전이다. 보존 02·03·04·13·14·18·19의 옛 선택 ID는 불변이며 전체 실제 180 BPM 지속은 미측정이다. 아래 1차 4 jungle / 4 drill / 5 rock 표는 당시 승인된 생성 배치다. 1차 링크는 `redirection-review-2026-10-06.md`, 2차 링크는 `redirection-round2-review-2026-10-06.md`에 있다. 두 배치의 소스 키는 제안값이고 오디오 실측값이 아니다. 최종 채택은 전 구간 180 BPM 확인 뒤 한다.

선례: `remakes/13_호흡.txt` is the kept jazzy jungle source. Its historical synth bass and keyboard motif belong to that selected song; new jungle drafts borrow its fast broken drums and jazz color while choosing different acoustic leads. `remakes/03_첫 바퀴_round3.txt` shows why the step pulse must stay explicit. `MASTER/WORKFLOWS.md` §0, `MASTER/cli/SPEC.md` track-prompt gate, and the gate's observed path restriction require the new dated files directly in `input/remakes/`. Historical `input/tracks/`, remakes, selected IDs, and download records remain untouched.

## Current decision after the first batch

젠은 1차 후보 중 01·05·07·08·12·15·16·17·20을 번호당 한 곡씩 남겼다. 생존 ID는 `suno-redirection-2026-10-06.json`의 A/B와 UI에서 일치했다. 1차 06·09·10·11은 재생성으로 결정했고, 이 문서 아래의 1차 장르·소스 표는 생성 이력이다. 16은 선택된 상태이며 이번 재생성 대상이 아니다. 1차 10B는 2차 생성 전에도 작업공간에 있었으나 삭제하거나 현재 채택으로 간주하지 않았다.

2차 새 소스는 `remakes/*_redirection-round2-2026-10-06.txt` 네 개다. 06 빠른 개러지 록의 짧은 거친 기타 리프, 09 재지 정글의 클라리넷·피아노 선율과 쪼개진 드럼, 10 어쿠스틱 재즈의 트럼펫·피아노와 라이브 드럼, 11 펑크(funk) 록의 베이스·기타 응답을 각각 다르게 설계했다. 네 소스는 `track-prompt` PASS 후 각 한 번씩 생성됐고, 새 A/B 여덟 후보의 듣기 링크는 `redirection-round2-review-2026-10-06.md`, 생성 기록은 `suno-redirection-round2-2026-10-06.json`에 있다. 네 새 A/B는 아직 선택 전이다. STYLE 문구와 게이트는 실제 180 BPM 증거가 아니며, 최종 채택은 보존 7곡을 포함해 실제 음원의 전 구간 180 BPM 지속을 확인한 뒤 한다.

## Kept selected songs

The IDs below are the existing 2026-10-03 selections in `suno-selected.json`; they are unchanged. Numerical BPM has not been measured for these seven songs.

| Slot | Title | Selected ID |
|---|---|---|
| 02 | 파란불 | `ada71365-1fd0-45ca-b516-b17fe5a0146f` |
| 03 | 첫 바퀴 | `fad9fc49-9b35-4f10-aa76-f62ddd9cf10c` |
| 04 | 조금 일찍 | `91b7d5a3-eb05-4f30-9911-ae04252ac541` |
| 13 | 호흡 | `74a23cf8-aece-414a-bccc-33397c6ce050` |
| 14 | 하나씩 | `ccb46537-3f33-4577-80c2-dc70bbfa65e1` |
| 18 | 가까운 곳 | `4df43801-27cc-4592-a97e-8b6c38074240` |
| 19 | 괜찮은 날 | `6302ab31-3e9f-4db3-ae20-5efb65fa5860` |

## Replacement source proposals

| Slot | Lane / proposed key | Lead and melodic distinction | Source draft |
|---|---|---|---|
| 01 | Rock / G Major | 기타의 짧은 3음 상승 훅을 베이스가 낮은 옥타브로 받고, 후반에는 6음 상승으로 늘린다. | [01](remakes/01_문을%20열고_redirection-2026-10-06.txt) |
| 05 | Jazzy jungle / B Minor | 어쿠스틱 피아노의 5음 하강 계단을 뒤집어 상승시키고 한 옥타브 위에서 다시 낸다. | [05](remakes/05_길을%20바꿔_redirection-2026-10-06.txt) |
| 06 | Drill / C Minor | 트롬본의 짧은 2음 호출 뒤 큰 6도 도약이 나오고, 4마디마다 마지막 음이 바뀐다. | [06](remakes/06_정해%20둔%20건%20없어_redirection-2026-10-06.txt) |
| 07 | Rock / F# Minor | 두 마디의 엇박 기타 리프 뒤 길게 꺾는 음을 놓고, 두 기타가 반대 방향으로 이동한다. | [07](remakes/07_같은%20방향_redirection-2026-10-06.txt) |
| 08 | Jazzy jungle / E Minor | 테너 색소폰의 긴 반음계 하강을 짧은 상승 답변으로 쪼갠다. | [08](remakes/08_낮은%20비트_redirection-2026-10-06.txt) |
| 09 | Drill / A Minor | 저음 기타의 4음 하강에 높은 트럼펫 2음이 답하고, 중간에는 기타가 상승으로 뒤집힌다. | [09](remakes/09_숨을%20세어_redirection-2026-10-06.txt) |
| 10 | Rock / D Major | 거친 기타의 반복음 리프 위로 다른 기타가 벤딩 뒤 3음 하강을 들려준다. | [10](remakes/10_생각을%20놓고_redirection-2026-10-06.txt) |
| 11 | Drill / G Minor | 트롬본·트럼펫이 함께 높이 뛰고 작은 간격으로 내려오며, 끝에는 높은 음역으로 옮긴다. | [11](remakes/11_다시%20해볼게_redirection-2026-10-06.txt) |
| 12 | Jazzy jungle / B Major | 비브라폰의 3+3음 선율을 마디 앞에서 시작하고, 한 박 쉰 뒤 긴 하강으로 답한다. | [12](remakes/12_바람이%20바뀌어_redirection-2026-10-06.txt) |
| 15 | Rock / F Major | 높은 기타의 울퉁불퉁한 5음 훅을 낮은 지속음 위에 얹고, 끝에는 두 기타가 화음으로 친다. | [15](remakes/15_드럼%20위로_redirection-2026-10-06.txt) |
| 16 | Drill / C Minor | 저음 기타의 단3도 하강과 첼로의 긴 상승을 충돌시킨 뒤, 기타 리프를 높은 음역으로 옮긴다. | [16](remakes/16_비가%20갠%20뒤_redirection-2026-10-06.txt) |
| 17 | Jazzy jungle / G Major | 깨끗한 기타의 넓은 4음 질문에 피아노가 빠른 하강으로 답하고, 후반에는 음역을 낮춘다. | [17](remakes/17_이어지는%20소리_redirection-2026-10-06.txt) |
| 20 | Rock / F Major | 기타가 짧은 리프 대신 긴 고음을 둔 6음 선율을 내고, 마지막 후렴에서 화음이 바뀐다. | [20](remakes/20_집으로%20가는%20길_redirection-2026-10-06.txt) |

Arc proposal: 01 opens with rock; 02–04 stay selected; 05–12 alternate jungle, drill and rock to lift the stride; selected 13–14 anchor the peak; 15–16 hit rock/drill harder; 17 clears the texture without slowing; selected 18–19 lead into a strong rock finish at 20. This allocation governed the submitted candidates; final song choices and distribution remain subject to 젠's listening decision.
