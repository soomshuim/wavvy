# 07:00 — 아침 러닝 (제작 브리프)

Version: 0.1 draft · 2026-10-03
Status: 젠이 01–20 번호별로 한 곡씩 남기고 전곡을 청취 PASS했다. 2026-10-03 Suno `[07:00]`을 새로고침해 정확히 20곡을 확인하고, 각 번호를 검색해 선택 음원 ID·표시 길이를 `input/suno-selected.json`에 고정했다. 180 BPM 러닝감은 젠이 귀로 확인해 PASS했다. 수치 BPM은 측정하지 않았으며 확정값으로 쓰지 않는다. 02–07의 선택 음원 WAV 6개를 다운로드해 `input/tracks/`에 복사하고 `input/download-manifest.json`에 검증 결과를 기록했다. 01은 젠이 MP3/M4A로 받았고, 01 및 08–20의 WAV는 아직 없다.

## Series direction

- **Time and use:** 07:00, 젠이 실제로 운동하는 시간. 20곡을 이어 들으며 달리는 아침 플레이리스트.
- **Music:** Korean indie electronic and indie dance. Bright synth figures and quick, clearly defined drums lead. Some songs add firmer bass and a wider hook; the series keeps a morning brightness rather than a uniformly dark club sound.
- **Pulse:** 180 BPM target in 4/4 for each source, with an audible quarter-note running cadence. 젠이 최종 20곡을 귀로 확인해 러닝감 PASS로 결정했다. 이 청취 판정이 이번 시리즈의 채택 기준이다. 수치 BPM은 미측정이며 파일명·보고서에는 측정값처럼 180을 넣지 않는다.
- **Final vocal direction (2026-10-03 listening correction):** Instrumental. 젠 heard the initial vocal versions and chose to remove lyrics for the running playlist. The 20 lyric-bearing txt files and 40 initial candidate IDs remain as generation history; they are not final instrumental sources. 젠의 “2 완료” 신호 후 **03·05·07·08·11·12·15·16·18·20**의 생존 원본 ID를 확인하고 각각 Suno `... → Remix → Cover`에서 가사 칸을 `[Instrumental]` 한 줄로 바꿔 요청했다. 01은 이 Cover 요청에 포함되지 않았다. 젠은 이 10곡의 Cover 결과를 청취 PASS했으며, 기계적 무가사 분석은 하지 않았다.
- **Duration target:** about three minutes or longer per song. The selected 01 (2:41) and 03 (2:24) are shorter, but 젠이 청취 후 남긴 최종곡이다. 실제 WAV 길이는 수집 후 검사한다.
- **03 stronger remake:** After the 20-song cleanup, 젠 requested a more powerful 03 only. Its second A/B was judged “느려.” The third prompt added a continuous motorik drum pulse. 젠은 A (`fad9fc49-9b35-4f10-aa76-f62ddd9cf10c`, 화면 2:24)를 남기고 B를 삭제했다. The earlier 03 Cover and second remake remain historical.
- **Arc:** Tracks 01–04 open and establish the step; 05–10 settle into a steady stride; 11–16 raise bass and hook energy; 17–20 keep the beat while reducing density toward the return.
- **Remake variation:** Keep a bright morning identity. The first 02 remake used fast new-wave guitars; its second remake takes 10's motorik electroclash, angular guitar, clipped synths and relentless fast drum drive. The other directions are 04 piano breakbeats, 06 synth-punk, 09 liquid drum and bass, 10 motorik electroclash, 13 jazzy jungle, 14 a stronger bass-led breakbeat peak, 17 melodic electronic post-rock, and 19 light guitar-led breakbeats. All ten remake sources specify instrumental 180 BPM and continuous fast drums. Stronger sections sit mainly in the middle; the beginning and return remain lighter. The text is an instruction, not a measured tempo result.

## Precedent and explicit overrides

- `wavvy.md` labels 07:00 “기상 / 시작, 담담.” This series explicitly raises the tempo and energy for morning running because 젠 chose 180 BPM indie electronic for their exercise hour. The current instrumental direction overrides Wavvy's default of Korean lyrics and a lead vocal for this series.
- `SERIES/06-00/concept.md` is instrumental-first fast lo-fi at roughly 110–130 BPM; this series targets a much faster indie electronic pulse and is now also intended to be instrumental.
- `SERIES/20-00/concept.md` is hard after-hours workout hip-hop. This series uses bright indie electronic sounds and a lighter overall low end, with selected stronger sections.
- The instrumental decision applies to every final track. Initial vocal directions in the submitted txt files are historical and do not authorize vocals in the covers.

## Reference videos

- [Paw&Power — 180 BPM Running Music Mix 1Hour Metronome Synced 042026](https://youtu.be/A3psJJwkdSY): use the idea of a sustained, step-aligned 180 BPM pulse.
- [달리런 — Playlist 180BPM 러닝 플리](https://youtu.be/u2eyM-tS6QI): use the idea of a 20-track, continuously motivating running set, with firm bass and some broad hooks. Its YouTube description emphasizes a club setting; 젠 chose a brighter morning sound with medium-strength moments for this series.
- These directions come from the videos' published metadata and descriptions, checked 2026-10-03. Direct numerical BPM analysis was not performed; 젠의 청취 판정이 최종 채택 기준이다. Do not copy melody, distinctive arrangement, or lyrics from either reference.

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

The ten agent-created Covers are recorded separately from the initial 40 and later remakes. 젠은 01–20 전체를 번호별로 청취 PASS했고 Suno에는 각 번호 한 곡씩만 남겼다. `input/suno-selected.json`에 20개 최종 ID를 고정했다. 젠의 귀 판정으로 러닝 박자도 PASS이며 기술적 BPM 수치는 기록하지 않는다. 02–07 WAV 수집·검사는 완료했다. 나머지 선택 음원 WAV 수집 뒤 Final Track Sources로 진행한다.
