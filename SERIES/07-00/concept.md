# 07:00 — 아침 러닝 (제작 브리프)

Version: 0.1 draft · 2026-10-03
Status (2026-10-06): 기존 선택 02·03·04·13·14·18·19 일곱 곡과 1차 교체 생존 01·05·07·08·12·15·16·17·20 아홉 곡은 유지한다. 2차 06·09·10·11의 A/B 생성 뒤 젠은 11만 남기고 06·09·10을 다른 곡 스타일로 직접 다시 만들었다. 11은 `[07:00]`에 남은 2차 B 한 곡(ID `ee96c338-2a08-4248-827d-82fc44da3de6`)으로 확인했다. 새 06·09·10은 Suno 기본 `My Workspace`에 각각 한 곡씩 있으며 `[07:00]`에는 아직 없다. 세 새 후보의 채택은 미정이고 정확한 링크·화면 표시 길이는 `input/user-remakes-review-2026-10-06.md`에 있다. 이전 20곡 선택 기록 `input/suno-selected.json`과 1·2차 생성 기록은 이력으로 보존한다. 02–07 WAV 여섯 개는 물리적으로 남아 있지만 현재 유지 번호의 WAV는 02·03·04 세 개다. 보존곡과 새 후보의 실제 180 BPM 지속은 미측정이다. Phase는 `track_source_draft`다.

젠의 2026-10-06 결정: 다운로드부터 이후 제작은 다운로드 한도 회복과 젠의 재개 요청 전까지 보류한다. 재개 시 현행 선택 ID와 새 06·09·10 후보의 위치·채택부터 대조한다. Final Track Sources·편집/렌더·업로드/릴리스는 아직 수행하지 않았으며 업로드는 별도 명시적 `-wavvy-release`에서 진행한다.

## Series direction

- **Time and use:** 07:00, 젠이 실제로 운동하는 시간. 20곡을 이어 들으며 달리는 아침 플레이리스트.
- **Music (current source direction):** 보존 7곡과 젠이 하나씩 남긴 1차 후보 9곡, 2차 11B를 현재 보존 선택으로 기록한다. 1차의 4 jungle / 4 drill / 5 rock과 2차 06·09·10의 장르는 생성 당시 이력이다. 젠의 직접 재제작 06은 기존 20과 같은 화면 스타일 설명의 기타 록, 09는 기존 17과 같은 기타 중심 재지 정글, 10은 보존 04와 같은 피아노 중심 인디 브레이크비트다. 새 세 곡의 STYLE 입력 원문과 채택은 확인하지 않았다. 16은 젠이 남긴 선택이며 이번 재생성 대상이 아니다.
- **Pulse and acceptance:** 교체곡 STYLE의 첫 문장부터 180 BPM 지속과 명확한 4분음표 러닝 박자를 지시한다. 최종 채택 기준은 보존 7곡을 포함해 실제 음원이 전 구간 180 BPM의 러닝 박자를 유지하는지 확인하는 것이다. 템포가 바뀌거나 90 BPM 하프타임으로 느껴지는 후보는 채택하지 않는다. 프롬프트는 실제 음원의 BPM 증거가 아니며, 미측정 상태를 수치 PASS로 기록하지 않는다. 보존 7곡을 남기겠다는 젠의 선택은 확정되었지만 그 일곱 음원의 수치 템포 확인은 아직 미완료다. 2026-10-03 당시 전곡 청취 PASS도 현재 재구성의 오디오 판정으로 소급하지 않는다.
- **Final vocal direction (2026-10-03 listening correction):** Instrumental. 젠 heard the initial vocal versions and chose to remove lyrics for the running playlist. The 20 lyric-bearing txt files and 40 initial candidate IDs remain as generation history; they are not final instrumental sources. 젠의 “2 완료” 신호 후 **03·05·07·08·11·12·15·16·18·20**의 생존 원본 ID를 확인하고 각각 Suno `... → Remix → Cover`에서 가사 칸을 `[Instrumental]` 한 줄로 바꿔 요청했다. 01은 이 Cover 요청에 포함되지 않았다. 젠은 이 10곡의 Cover 결과를 청취 PASS했으며, 기계적 무가사 분석은 하지 않았다.
- **Duration target:** about three minutes or longer per song. 현재 보존된 03은 2:24 표시/약 2:23.72 WAV로 이 목표보다 짧지만 젠이 남기기로 정했다. 2026-10-03 선택됐던 옛 01의 표시 길이 2:41은 역사 기록이고, 새 01 후보 두 개는 UI에 각각 2:59로 표시된다. 1차 후보 26개의 UI 표시 길이는 `input/redirection-review-2026-10-06.md`, 2차 후보 8개는 `input/redirection-round2-review-2026-10-06.md`에 기록했다. 2차 11A는 3:00 입력에도 2:59로 표시됐고, 현재 남은 11B는 3:00이다. 젠의 직접 재제작 06·09·10은 각각 화면상 2:04·3:22·2:25다. 길이 목표는 전곡 통과로 판정하지 않는다.
- **03 stronger remake:** After the 20-song cleanup, 젠 requested a more powerful 03 only. Its second A/B was judged “느려.” The third prompt added a continuous motorik drum pulse. 젠은 A (`fad9fc49-9b35-4f10-aa76-f62ddd9cf10c`, 화면 2:24)를 남기고 B를 삭제했다. The earlier 03 Cover and second remake remain historical.
- **Arc proposal (earlier 2nd-round direction):** 01 록으로 출발하고 02–04 보존곡을 지난다. 05–12에 06 개러지 록·09 재지 정글·10 어쿠스틱 재즈·11 펑크(funk) 록을 끼운 구상은 2차 생성 당시 안이다. 젠이 06·09·10을 새로 만든 뒤의 최종 흐름은 세 새 후보를 듣고 정한다. 13–14 보존곡을 중심점으로, 15–16은 더 강하게, 17은 밀도만 덜어낸다. 18–19 보존곡 뒤 20은 박자를 늦추지 않는 록으로 닫는다. 번호별 과거 근거는 `input/redirection-2026-10-06.md`에 있다.
- **2026-10-03 remake history:** 당시 02의 두 차례 기타/일렉트로클래시 방향, 04 피아노 브레이크비트, 06 신스펑크, 09 드럼 앤 베이스, 10 일렉트로클래시, 13 jazzy jungle, 14 베이스 브레이크비트, 17 일렉트로닉 포스트록, 19 기타 브레이크비트를 사용했다. 이 중 지금 보존된 13의 실제 소스에는 신스 베이스와 키보드 선율이 있다. 보존곡 원문은 바꾸지 않고 새 jungle은 재즈 화성과 쪼개진 드럼만 선례로 쓴다.

## Precedent and explicit overrides

- `wavvy.md` labels 07:00 “기상 / 시작, 담담.” This series explicitly raises the tempo and energy for morning running because 젠 chose 180 BPM indie electronic for their exercise hour. The current instrumental direction overrides Wavvy's default of Korean lyrics and a lead vocal for this series.
- `SERIES/06-00/concept.md` is instrumental-first fast lo-fi at roughly 110–130 BPM; this series targets a much faster indie electronic pulse and is now also intended to be instrumental.
- `SERIES/20-00/concept.md` is hard after-hours workout hip-hop. This series keeps a morning running purpose and uninterrupted step pulse even as its proposed drill and rock sources grow stronger.
- The instrumental decision applies to every final track. Initial vocal directions in the submitted txt files are historical and do not authorize vocals in the covers.

## Reference videos

- [Paw&Power — 180 BPM Running Music Mix 1Hour Metronome Synced 042026](https://youtu.be/A3psJJwkdSY): use the idea of a sustained, step-aligned 180 BPM pulse.
- [달리런 — Playlist 180BPM 러닝 플리](https://youtu.be/u2eyM-tS6QI): use the idea of a 20-track, continuously motivating running set, with firm bass and some broad hooks. Its YouTube description emphasizes a club setting; 젠 chose a brighter morning sound with medium-strength moments for this series.
- These directions come from the videos' published metadata and descriptions, checked 2026-10-03. Direct numerical BPM analysis was not performed. 2026-10-03 당시 젠의 청취 판정은 역사 기록이며, 현행 교체 후보와 보존곡의 180 BPM 지속 여부는 새로 확인해야 한다. Do not copy melody, distinctive arrangement, or lyrics from either reference.

## Initial vocal source arc (historical)

The following titles and lanes describe the initial submissions. The lyric angles and proposed leads are historical; they do not apply to the instrumental covers and are not approved Final Track Sources.

| # | Working title | Energy role | Main musical variation | Initial lyric angle | Initial lead |
|---|---|---|---|---|---|
| 01 | 문을 열고 | open | bright synth pluck, dry live-feel drums | air and first beat | Female |
| 02 | 파란불 | open | muted guitar rhythm and synth bass | step into the beat | Male |
| 03 | 첫 바퀴 | open | arpeggiator and crisp kick | settling breath | Female |
| 04 | 조금 일찍 | open | warm keys and light breakbeat | waking through movement | Male |
| 05 | 길을 바꿔 | stride | guitar chop with electronic drums | same pulse, new route | Female |
| 06 | 정해 둔 건 없어 | stride | rubbery bass and short synth replies | leave the distance counter aside | Male |
| 07 | 같은 방향 | stride | layered guitar and pad | own pace | Female |
| 08 | 낮은 비트 | stride | percussive keys and restrained 808 sub-bass | low end and light steps | Male |
| 09 | 숨을 세어 | stride | shimmering sequencer | breathing and counting | Female |
| 10 | 생각을 놓고 | stride | clipped synth chords | release mental noise | Male |
| 11 | 다시 해볼게 | push | heavier live kick and bass synth | recover the pace | Female |
| 12 | 바람이 바뀌어 | push | syncopated synth lead | adjust to a changing breeze | Male |
| 13 | 호흡 | push | sharp drums and warm counter-melody | comfortable breath | Female |
| 14 | 하나씩 | push | bass-led indie dance | one step at a time | Male |
| 15 | 드럼 위로 | push | wide chorus guitar and synth | voice riding the drums | Female |
| 16 | 비가 갠 뒤 | push | driving drum break and lifted chords | air after rain | Male |
| 17 | 이어지는 소리 | return | light piano over steady drums | hold the pulse lightly | Female |
| 18 | 가까운 곳 | return | soft plucked synth, defined bass | focus on the next stretch | Male |
| 19 | 괜찮은 날 | return | open guitar and brushed synth | keep a sustainable pace | Female |
| 20 | 집으로 가는 길 | return | simple repeating synth figure | return without slowing the beat | Male |

## Production status

Initial vocal txt: 20/20, with track-prompt and full-song lyric-record gates PASS. These apply to the first generation only. Instrumental remake txt: 12/12 in `input/remakes/`, with track-prompt gates PASS. First-pass, remake, and Cover IDs remain in their historical manifests. 젠이 20곡을 한 번호당 한 곡으로 정리한 뒤 Suno `[07:00]`을 새로고침해 20곡과 고유 ID를 대조했다. `input/suno-selected.json` is the selected-song map, including 01·02 Covers made outside this agent's recorded submissions. 젠의 전곡 청취 및 180 BPM 체감 PASS는 기록했다. Numerical BPM and automated no-vocal checks were not performed.

The Suno download dialog displayed 7 remaining Pro downloads on 2026-10-03 before this download pass. 젠이 01을 MP3/M4A로 받았고, Codex가 선택 ID를 대조해 02–07을 WAV로 다운로드했다. 각 파일은 48 kHz·16-bit PCM·stereo WAV이며 Downloads의 원본과 `input/tracks/` 복사본 SHA-256이 일치한다. Suno's [download policy](https://help.suno.com/en/articles/13926209) counts each distinct song once, regardless of format. A browser-stream pulse probe of an earlier 20B candidate at 30–42 seconds suggested a roughly 92–94 BPM low-frequency pulse; that short window was inconclusive and the candidate is not the selected 20. Automated tempo probing stopped after two Aside navigation/context failures. 젠은 최종 20곡의 러닝 박자를 귀로 확인하고 채택했다. 기술적으로 측정한 BPM 값은 없다.

The ten agent-created Covers are recorded separately from the initial 40 and later remakes. 2026-10-03 젠은 당시 01–20 전체를 번호별로 청취 PASS했고 Suno에는 각 번호 한 곡씩만 남겼다. 그날의 20개 ID는 `input/suno-selected.json`에 고정한 역사 기록이다. 당시 청취 러닝감 PASS는 수치 BPM 측정이 아니다. 2026-10-06 재구성 뒤 현행 보존 번호는 02·03·04·13·14·18·19이고, 새로 남긴 선택은 1차 아홉 곡 및 2차 11B다. 05·06·07의 WAV는 물리적으로 존재하지만 기존 선택 음원 이력이다. 젠이 기본 `My Workspace`에 직접 만든 06·09·10은 현재 각각 새 후보 한 곡씩이며 아직 채택 미정이다. 실제 180 BPM 확인과 최종 선택 전에는 Final Track Sources로 올리지 않는다.
