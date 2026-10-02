# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

- **17-00 Tracks 08·09 사용자 원문 교체 및 구간 태그 기준 수정** (2026-10-02) — 08은 「취향」으로 바꾸고 새 100 BPM acoustic-guitar STYLE과 남녀 파트가 구조 태그 옆에 표시된 가사를 원문대로 저장했다. 09는 같은 가사에 사용자가 준 indie acoustic rock STYLE을 적용했다. 이전 두 곡의 조성·템포·EXCLUDE는 새 원문으로 가져오지 않았다. Suno 공식 구조 라벨·보컬 태그 예시와 젠의 08 생성 경험을 구분해 `LYRICS.md`, `STYLE.md`, 작사 스킬/스펙, 근거 문서를 수정했다. Full-song 검사기는 `[Verse 1] [Female]` 같은 줄의 첫 구조 태그를 읽도록 고쳤다. 현재 txt 20개·state revision 41이며 08/09 새 원문에 별도 PASS나 로컬 음원 실측은 없다.
- **17-00 Tracks 08·09 사용자 재제작 예정** (2026-10-02) — 젠이 08 「네 취향」과 09 「한 곡만 더」를 다시 만들고 새 STYLE·LYRICS를 직접 알려주기로 했다. 새 원문은 아직 받지 않았으므로 기존 승인 소스는 보존하고, concept에 교체 대기 상태를 기록했다.
- **17-00 Track 12 제목 「서점」 변경** (2026-10-02) — 젠이 승인된 12번 제목을 「이런 데가 있었네」에서 「서점」으로 바꿨다. 현재 txt와 가사 기록의 제목·경로, concept 행과 참조 경로를 맞췄다. STYLE·빈 EXCLUDE·LYRICS 본문과 124 BPM/G Major·남성 단독 지시는 그대로다. 후렴의 `여기 이런 데가 있었네`도 가사이므로 유지했다. 음원은 없다.
- **17-00 Track 20 「오랜만이야」 사용자 PASS** (2026-10-02) — 젠이 20번 STYLE의 보컬이 여성인지 확인했고, 남성 단독임을 들은 뒤 현행 제목·전체 가사·02번 STYLE 원문·빈 EXCLUDE에 PASS했다. txt 승인 메타와 concept 승인 트랙 행을 현행화했다. STYLE·EXCLUDE·LYRICS 본문은 불변이다. STYLE 원문에는 BPM·조성이 없어 track-prompt는 그 두 항목에서 명시적 FAIL이며, 118 BPM·104마디·약 3:32는 편곡 계산일 뿐이다. 음원은 없다.
- **17-00 Track 20 「오랜만이야」 가사 전면 재작성** (2026-10-02) — 젠이 「여섯 층」의 뜻을 알기 어렵고 설정이 억지스럽다고 지적해, 승인 전 초안을 교체했다. 연락에 답을 미루던 화자가 오랜만에 친구를 만나 별다른 추궁 없이 대화를 이어 가는 새 가사다. 02번 「공강」 STYLE과 빈 EXCLUDE는 원문 그대로, 남성 단독 리드도 유지했다. 새 가사 SHA-256 `22af8bb45341ec338dbd3173d225c806c2f8a12da675f70aea05fc43fbfd10dd`; full-song·lyrics-review PASS, 현행 가사 독립 Codex Astra/xhigh 검토 CLEAN. 원본 STYLE에 BPM·조성이 없어 track-prompt는 명시적 FAIL. 104마디·4/4·계산용 118 BPM의 약 3:32는 편곡 추정이며 음원은 없다. State revision 39·txt 20개. 사용자 PASS 전이므로 concept 승인 표에는 20번이 없다.
- **17-00 Track 20 「여섯 층」 폐기된 검토용 초안** (2026-10-02) — 02번 「공강 (Accoustic Remix)」 STYLE과 빈 EXCLUDE를 그대로 재사용해, 승강기 고장으로 함께 계단을 오른 두 이웃이 다음 날 다시 인사하는 새 한국어 완곡 가사를 작성했다. 남성 단독 보컬은 원본 STYLE에서 이어받았다. 가사 SHA-256 `1288951b7068a59f3c79136461ff5bed036cd6a3b51a6f51049058c32c13b4eb`; full-song·lyrics-review PASS, 독립 Codex Astra/xhigh 검토 CLEAN. Track-prompt 게이트는 원본 STYLE의 BPM·조성 누락을 명시적으로 FAIL한다. 100마디·4/4·계산용 118 BPM의 약 3:23은 편곡 추정이며 실제 음원은 없다. State revision 38·txt 20개. 사용자 PASS 전이므로 concept 승인 목록에는 20번이 없다.
- **17-00 Track 19 「엄마」 사용자 PASS** (2026-10-02) — 젠이 제목 변경 뒤 현행 전체 가사에 PASS했다. txt 승인 메타를 먼저 바꾸고 concept에 19번을 등록했다. STYLE·빈 EXCLUDE·LYRICS 본문은 불변이며 가사 SHA-256 `8fe490db25285389172ac93358f08a52f84d88177739a13ebad93e57f28c3425`. Full-song·lyrics-review·state check PASS, 독립 Codex Astra/xhigh 검토 CLEAN. 11번에서 이어받은 STYLE에 BPM·조성이 없어 track-prompt는 명시적 FAIL. State revision 37·txt 19개·음원 0개. Final Track Sources 승격은 하지 않았다.
- **17-00 Track 19 제목 「엄마」 선택** (2026-10-02) — 젠이 초안 제목 「엄마가 고른 색」을 「엄마」로 바꿨다. 곡 소스와 가사 검토 기록의 이름·경로·제목 메타를 맞췄다. STYLE·EXCLUDE·LYRICS 본문은 불변이고 가사 SHA-256 `8fe490db25285389172ac93358f08a52f84d88177739a13ebad93e57f28c3425`. 새 경로의 full-song·lyrics-review·state check PASS. Track-prompt 게이트는 원본 STYLE에 BPM·조성이 없어 명시적 FAIL이다. State revision 36·txt 19개·음원 0개. 전체 가사는 사용자 검토 대기다.
- **17-00 Track 19 「엄마가 고른 색」 여성 리드·딸과 엄마 가사 초안** (2026-10-02) — 젠의 가사 전용 요청과 여성 보컬·딸과 엄마 소재 정정에 따라 새 한국어 완곡 가사를 썼다. 11번 「약속 (Acoustic Remix)」 STYLE은 `male`→`female` 보컬 한 단어 외에는 그대로, EXCLUDE는 빈칸이며 BPM·조성은 추가하지 않았다. 100 BPM은 92마디·약 3:41 길이 계산에만 쓴 가정이다. 가사 SHA-256 `8fe490db25285389172ac93358f08a52f84d88177739a13ebad93e57f28c3425`; full-song·lyrics-review·state check PASS, 독립 Astra/xhigh 검토 CLEAN. Track-prompt 게이트는 원본 STYLE에 BPM·조성이 없어 명시적 FAIL이다. State revision 35·txt 19개·음원 0개. 사용자 PASS 전이므로 concept 승인 목록에는 19번을 넣지 않았다.
- **17-00 Track 18 「흔들린 사진」 사용자 PASS** (2026-10-02) — 젠이 사진 부스 사랑 이야기의 제목·전체 가사, 07번 리믹스 사운드 기반 STYLE, 빈 EXCLUDE, 110 BPM/G Major, 여성 단독 진성 리드에 PASS했다. txt 승인 메타를 먼저 바꾸고 concept 승인 트랙 목록에 18번을 추가했다. STYLE SHA-256 `ea63a3c548c0987cbdc6efc91400566ed7ada84363efbc48f62665f7d676f1d0`·가사 SHA-256 `ae90881c8b66e23bffd06e4e20d3a6a48476b429796ac02df0bbb0245e66f26e`는 승인 전후 동일하다. Full-song·lyrics-review·track-prompt·state write/check·diff check PASS, 독립 Codex Astra/xhigh 검토 CLEAN. State revision 34·txt 18개·음원 0개. 100마디·약 3:38은 편곡 추정이며 실제 음원은 없다.
- **17-00 Track 18 여성 리드 선택** (2026-10-02) — 젠의 `여성으로` 선택에 따라 「흔들린 사진」의 보컬 지시만 남성 단독에서 여성 단독 진성 리드로 바꿨다. STYLE은 `male`→`female` 한 단어만 변경(680자, SHA-256 `ea63a3c548c0987cbdc6efc91400566ed7ada84363efbc48f62665f7d676f1d0`), 가사 SHA-256 `ae90881c8b66e23bffd06e4e20d3a6a48476b429796ac02df0bbb0245e66f26e`와 편곡·110 BPM/G Major·빈 EXCLUDE는 그대로다. Full-song·lyrics-review·track-prompt·state write/check·diff check PASS, 독립 Codex Astra/xhigh 검토 CLEAN. State revision 33·txt 18개·음원 0개. 18번 전체 초안은 사용자 PASS 전이므로 concept 승인 목록에는 없다.
- **17-00 Track 18 사랑 이야기로 전면 개작** (2026-10-02) — 젠의 `사랑 얘기로` 정정에 따라 승인 전 시장 소재·제목 「파장」을 「흔들린 사진」으로 교체했다. 두 연인이 사진 부스에서 가까이 앉으며 남긴 흔들린 한 장을 중심으로 새 한국어 완곡 가사를 썼다. 07번 리믹스 기반 STYLE·빈 EXCLUDE·제안 110 BPM/G Major/남성 단독 보컬과 100마디 편곡 계획은 유지했다. 가사 SHA-256 `ae90881c8b66e23bffd06e4e20d3a6a48476b429796ac02df0bbb0245e66f26e`. Full-song·lyrics-review·track-prompt·state write/check·diff check PASS, 현행 초안 독립 검토 CLEAN. State revision 32·txt 18개·음원 0개. 젠의 PASS 전이라 concept 승인 목록에는 18번을 넣지 않았다.
- **17-00 Track 17 「물결」 리믹스 소스·Track 18 「파장」 검토용 초안** (2026-10-02) — 젠이 17번의 어쿠스틱 리믹스 STYLE·전체 가사를 제공해 원문 그대로 저장했다. 14:00 원곡 「물결」의 가창 가사와 일치하고, 사용자 원문의 `[Instrumental]` 대문자 표기를 유지했다. 20곡 배분은 리믹스 7곡·신곡 13곡이다. 이어 07번 리믹스의 경쾌한 어쿠스틱 R&B 사운드로 18번 신곡 「파장」의 한국어 완곡 가사를 작성했다. 시장 파장 무렵 과일 가게에서 받은 작은 사과가 집 식탁에 남는 이야기다. 110 BPM/G Major/남성 단독 보컬은 제안값이고 젠의 PASS를 기다린다. 18번 STYLE 678/900자·빈 EXCLUDE, 100마디·약 3:38은 편곡 추정. Full-song·lyrics-review·track-prompt·state write/check·diff check PASS, 독립 검토 CLEAN. State revision 30·txt 18개·음원 0개. Concept에는 사용자 제공 17번만 반영하고 18번 승인 행은 넣지 않았다.
- **17-00 Track 16 「매듭」 사용자 PASS** (2026-10-02) — 젠이 제목을 고른 뒤 현행 전체 한국어 가사, 11번 「약속」 리믹스 사운드 기반 STYLE, 빈 EXCLUDE, 112 BPM/Bb Major, 남성 단독 진성 보컬 제안에 PASS했다. STYLE·EXCLUDE·LYRICS 본문은 승인 전후 동일하다. txt 승인 메타를 먼저 갱신하고 concept 승인 목록에 16번을 추가했다. Full-song·lyrics-review·track-prompt·state write/check·diff check PASS. State revision 29·txt 16개·`track_source_draft`; 102마디·약 3:39는 편곡 추정이며 음원은 없다.
- **17-00 Track 15 사용자 PASS·Track 16 「매듭」 검토용 초안** (2026-10-02) — 젠이 15번의 은유적 전체 가사, 01번 리믹스 사운드 기반 STYLE, 빈 EXCLUDE, 남성 단독 보컬, 110 BPM/C Major를 PASS했다. txt 승인 메타와 concept 트랙 목록을 현행화했다. 이어 11번 「약속」 리믹스의 핑거피킹 기타·업라이트 베이스·브러시 카혼 사운드에 새 수선 장면 가사를 쓴 16번 초안을 저장했다. 젠이 16번 제목을 「매듭」으로 정해 파일명과 가사 기록 경로를 변경했다. 가사·STYLE 본문은 변경하지 않았다. 16번의 112 BPM/Bb Major/남성 단독 보컬은 제안값이며 전체 초안은 사용자 PASS 전이다. STYLE 629/900자, EXCLUDE 공란. 4/4·102마디는 약 3:39 편곡 추정이다. 제목 변경 후 full-song·lyrics-review·track-prompt·state check PASS; 초안 독립 검토 CLEAN. State revision 28·txt 16개·음원 0개. Concept 승인 목록에는 16번을 넣지 않았다.
- **17-00 Track 15 「바람이 드는 쪽」 은유적 가사·남성 보컬·110 BPM 선택** (2026-10-02) — 젠이 첫 「맨 앞줄」 공연 응원 가사를 유치하다고 판단하고 컨셉 자체를 더 은유적·서정적으로 바꾸라고 했다. 공연 소재를 폐기하고 열린 창·움직이는 커튼과 종이·구분되어 들리는 거리 소리로 변화를 암시하는 새 한국어 가사와 제목을 저장했다. 01번 「서랍」 리믹스의 밝은 어쿠스틱 R&B 사운드는 유지했다. 이후 젠이 남성 리드와 110 BPM을 선택해 원본의 여성·125 BPM 지시를 바꿨고 가사는 그대로 뒀다. C Major는 제안 프롬프트 값이다. STYLE 880/900자·빈 EXCLUDE, 변경 없는 106마디는 110 BPM에서 약 3:51로 추정된다. 변경 후 full-song·lyrics-review·track-prompt·state check PASS; 기존 새 컨셉 독립 검토 CLEAN은 바뀌지 않은 가사에 관한 결과다. State revision 25·txt 15개·`track_source_draft`; 제목·전체 가사·나머지 STYLE의 사용자 PASS와 실제 음원 확인은 아직이다. Track 15는 concept 승인 목록에 넣지 않았다.
- **17-00 Track 14 「통화 (Acoustic Remix)」 사용자 제공 소스 기록** (2026-10-02) — 제공된 Korean Acoustic R&B STYLE과 전체 LYRICS를 14번 txt에 저장했다. 가사 원곡은 18-00 Track 06 「전화」로 확인했다. 새 STYLE의 88 BPM·남성 진성 리드는 프롬프트 값이며, 조성·EXCLUDE는 미제공으로 남겼다. 20곡 목표 배분을 리믹스 6곡·신곡 14곡으로 바꾸고 state revision 21·txt 14개를 기록했다. Source parser·state check·독립 검토 PASS. 실제 음원은 없다.
- **17-00 Track 13 「컵 두 개」 가사·STYLE 사용자 승인** (2026-10-02) — 04번 「낮꿈」 리믹스의 나일론 기타 중심 인디 어쿠스틱 R&B STYLE에 115 BPM·A Major를 더하고, 기존 화음 지시는 신곡의 여성 단독 진성 보컬로 바꿨다. 두 사람이 이사 전날 남겨 둔 컵을 새집에서 꺼내는 새 한국어 가사를 젠이 PASS했다. STYLE·EXCLUDE·LYRICS 본문은 승인 전후 동일하며 txt 승인 메타와 concept 트랙 목록을 현행화했다. Full-song·lyrics-review·track-prompt·state check PASS, 초안 독립 검토 CLEAN. State revision 20·txt 13개·`track_source_draft`; 96마디·약 3:20은 편곡 추정이며 음원은 없다.
- **17-00 Track 12 「이런 데가 있었네」 가사·STYLE 사용자 승인** (2026-10-02) — 02번 「공강」 리믹스의 밝은 어쿠스틱 인디 록 STYLE을 바탕으로 124 BPM·G Major만 더하고, 작은 책방을 우연히 찾는 새 한국어 가사를 작성했다. 젠이 전체 초안에 PASS해 txt 승인 상태와 concept 트랙 목록을 현행화했다. STYLE·EXCLUDE·LYRICS 본문은 승인 전후 동일하다. 전체곡 가사·프롬프트 검사와 독립 검토는 통과했다. state revision 18·txt 12개·`track_source_draft`; 음원은 없다.
- **17-00 Track 11 「약속 (Acoustic Remix)」 사용자 제공 소스 기록** (2026-10-02) — 제공된 acoustic neo-soul R&B STYLE와 전체 LYRICS를 11번 txt에 저장했다. 가사 원곡은 18-00 Track 02 「약속」으로 확인했고, 13-00의 동명 곡과 구분했다. 리믹스 프롬프트에 BPM·조성과 EXCLUDE가 없어 미제공으로 남겼다. 20곡 목표의 배분을 리믹스 5곡·신곡 15곡으로 바꾸고 state revision 16·txt 11개를 기록했다. 실제 음원은 저장소에 없다.
- **17-00 Track 10 「그때의 빛」 사용자 최종본 반영** (2026-10-02) — 젠이 제공한 104 BPM·F Major·여성 단독 acoustic neo-soul R&B STYLE, EXCLUDE 7개와 수정된 전체 가사를 txt 우선으로 저장했다. 기존 120 BPM 편곡과 100마디·3:20 추정은 과거 버전으로 돌리고, 기존 가사 검토 기록에도 과거본임을 표시했다. 현재 음원 파일은 없어 실제 길이·템포·조성·보컬·편곡은 확인하지 않았다. 시리즈는 `track_source_draft`이며 Final Track Sources는 승격하지 않았다.
- **17-00 Track 08 「네 취향」 완곡·혼성 보컬 사용자 승인** (2026-10-01) — 상대가 좋아하던 음식과 음악이 서로의 취향이 되는 한국어 가사, acoustic neo-soul STYLE/EXCLUDE를 txt에 저장하고 젠이 현재 원문을 PASS했다. 승인 배정은 1절 여성·2절 남성·3절 및 Bridge 여성, 모든 후렴 남녀 화음이다. 118 BPM·E Major·100마디 약 3:23은 프롬프트와 편곡 목표이고 실측 음원은 없다. 혼성 보컬을 헤더·STYLE 양쪽에서 올바르게 확인하도록 `track-prompt` 검사를 보정했다. 시리즈는 state revision 9·txt 8개·`track_source_draft`이며 Final Track Sources로 승격하지 않았다. full-song/track-prompt/state 검사 PASS; 기존 01–07은 보존했다.
- **17-00 Track 07 「봄비같은 너 (Accoustic Remix)」 사용자 제공 원문 기록** (2026-10-01) — 제공된 Acoustic R&B·110 BPM·남성 리드 STYLE과 전체 LYRICS를 txt에 저장하고 사용자 PASS를 concept에 반영했다. 13-00 Track 16 선례를 확인했지만 이번 제공 원문을 우선했다. 조성은 미제공, EXCLUDE는 빈칸이며 후렴의 airy stacked harmonies와 마지막 후렴 ad-libs는 07에 한정된 예외다. 시리즈 목표는 20곡 중 리믹스 4곡(01/02/04/07), 신곡 16곡(03/05/06/08–20)이다. state revision 8·txt 7개·`track_source_draft`; 실제 리믹스 음원은 없다.
- **17-00 Track 06 「그냥 좋아」 가사·STYLE 사용자 승인** (2026-10-01) — 별일 없는 하루에 혼자 있는 시간이 즐거운 전체 가사와 funky acoustic indie rock STYLE, `Folk`부터 시작하는 EXCLUDE 8개를 txt·full-song 기록에 저장하고 젠이 PASS했다. 남성 단독 중음·A Major·125 BPM은 확정 프롬프트 방향이다. 세 Verse 각 6행과 기타 응답 여백을 계획했고, 106마디는 약 3:24 편곡 추정치다. 승인 STYLE 807/900자·EXCLUDE 8/8개, 가사 해시는 초안과 동일하다. package/full-song/lyrics-review/track-prompt PASS, state revision 7·txt 6개. 초안의 독립 격리 검토 Critical/High 0. 실제 음원 확인은 남아 있다.
- **신규 완곡 가사 호흡·Verse 구조 검토** (2026-10-01) — 05 「한 정거장」의 음악 결과는 젠이 괜찮다고 판단해 원래 두-Verse 가사·STYLE을 승인했다. 다음 신곡부터 Verse 3개를 기본 출발점으로 삼고 곡별 구조 예외를 기록한다. `lyrics-review`는 Verse별 가창행 수, 가장 긴 가창행, 짧은 구절, 구절 뒤 쉼의 정확 인용·이유를 새 완곡 기록에 요구한다. 글자/행수 상한과 가사 총량 증가는 강제하지 않으며 실제 가창성은 오디오로 확인한다. 기존 승인 03·05는 기록 경로와 원문 해시가 모두 일치할 때만 새 증거에서 제외한다. 36 tests·py_compile·skill validation·03/05 full-song gate·diffcheck PASS; 독립 검토 Critical/High 0.
- **17-00 「너와」 완곡 초안·Style/가사 검사 현대화** (2026-09-30) — 사용자의 짧은 생성곡·누락된 Intro 피드백을 반영해 03의 가사를 55→67행으로 확장하고 `[Intro]`와 4/4·92마디 계획을 더했다. 약 3:20은 목표이며 106 BPM 기준 약 208.3초는 계획 추정치다. G Major·따뜻한 중저음 남성 보컬도 미승인 제안이며 STYLE은 822자, EXCLUDE는 6개다. `STYLE.md`·`ROLES.md`·`LYRICS.md`/작사 스킬을 고정 문구보다 음악적 의도·완곡 구조·출처 구분 중심으로 고치고, 실제 txt의 `track-prompt`와 `lyrics-review --draft-scope full-song` 검사를 분리했다. 독립 검토가 찾은 중복 STYLE/LYRICS와 BPM 헤더의 경로별 해석 차이는 공통 `wavvy_harness/source.py`에서 메타·구역을 함께 파싱하고 중복을 거부해 해결했다. 중복 BPM 106/125는 양쪽 gate와 아카이브에서 거부한다. 실제 03의 두 gate·lyric-skill, 01/02/04 파싱, 33 tests·py_compile·diffcheck PASS; 최종 fresh 격리 검토 `shared_parser_review`는 Critical/High 0·원칙 관찰 0으로 CLEAN. 사용자 가사·제안 프롬프트 검토와 실제 생성 음원 확인은 남아 있다. 이전 853자/8개 프롬프트와 55행 가사의 검토 결과는 현재 초안에 적용하지 않는다.

### Changed
- **17-00 03 신곡 초안·04 사용자 리믹스 소스 추가** (2026-09-30) — 03 「너와」의 오래된 친구 가사 초안과 제안 STYLE(어쿠스틱 네오소울·106 BPM)/EXCLUDE를 txt 및 작사 스킬 기록에 저장. 가사 본문 해시 검증과 `lyrics-skill` PASS를 받았으며 젠의 가사 검토는 남아 있다. 04 「낮꿈 (Accoustic Version)」의 사용자 제공 STYLE·혼합 언어 LYRICS를 그대로 저장하고, 해당 트랙만의 언어·보컬 예외를 concept에 기록했다. 04 원문 보존은 표현 품질 승인과 구분한다. 17-00 상태는 revision 5 `track_source_draft`, txt 4개이며 음원·최종 소스는 없다.
- **17-00 어쿠스틱 시리즈 초안·상태 전환** (2026-09-30) — 가을의 편안한 Acoustic R&B/Neo-Soul/Indie Rock 방향, 125 BPM 상한, 총 20곡 목표(01/02/04 어쿠스틱 버전 리믹스 3곡+03 및 05–20 신규 17곡)를 concept에 반영. 04의 원곡·제목·STYLE·LYRICS는 미제공 placeholder로 두고 03 신규 작업은 별도로 진행한다. 01 「서랍」과 02 「공강(Accoustic Remix)」의 사용자 제공 STYLE/LYRICS를 txt로 저장하고, 01의 잘린 `highly en`은 확인된 `high-energy`로만 보완했다. 이전 `올라가` 샘플과 구 콘셉트는 원본 바이트 그대로 보관하고 현 제작 후보에서 제외했다. 시리즈 전환 시 이전 `phase`/`next_action`이 넘어가던 state writer를 고쳐 17-00을 revision 4 `track_source_draft`로 기록했다. 테스트 23개 및 실제 state check PASS; 이 변경에 신규 곡 초안이나 음원은 포함하지 않았다.
- **Wavvy 작사 자연스러움 규칙·검토 근거 정렬** (2026-09-30) — 지정한 13곡의 가사 선례와 젠의 「낮꿈」 표현 기각을 반영해 문장 자체→앞뒤 연결→감정 흐름 순서로 `wavvy.md`/`LYRICS.md`/작사 스킬·스펙·선례를 개정. 직접 감정·설명·비유·시간어와 사물 개수에 대한 일괄 품질 규칙을 걷고, `lyrics-review`에 실제 가사 본문 해시·정확 인용·이유의 검토 기록을 연결. `review-only` Findings/Verdict, Suno Empty/Prompt/Structure, package-only `NOT_REVIEWED`, artifact 필수 CLI를 정합화하고 회귀테스트 20개 PASS. 자동 검사는 기록 형식·대상 일치·상태를 확인하며 문학적 의미·가창·작성 주체를 보증하지 않는다.
- **20-00 policy audit final concept sync** (2026-06-03) — `-director` read-only audit에서 확인된 20-00 최종 분포 충돌을 정리. `SERIES/20-00/concept.md`의 v0.4 과거 분포 문장을 현재 v0.5/v0.8 기준(A 3 / B 5 / C 5 / D 3 / E 2 / F 2, Hard 65%)으로 보정 표기하고, `MASTER/rubrics/HARD_HIPHOP_RUBRIC.md`를 v1.5로 갱신. `MASTER/scripts/check_series_gate.sh`는 pre-final txt source draft용 legacy validator로 명시하고 S1/S2/S3/S5를 current concept 기준으로 최소 동기화. 삭제/아카이브는 수행하지 않음.
- **20-00 series gate S2 safety correction** (2026-06-03) — reviewer 지적을 반영해 legacy `check_series_gate.sh`의 S2 BPM/체감 단계 정합을 ADVISORY로 출력하도록 보정. S2 판정 기준 SSOT는 `MASTER/rubrics/HARD_HIPHOP_RUBRIC.md` section `S2 Advisory Disposition`.

### Added
- **Wavvy `/write` / `-write` lyricist command shim** (2026-05-22) — `.claude/commands/write.md`를 추가해 Claude Code `/write`와 Codex `-write`를 Wavvy lyric-only thin alias로 연결. command는 가사 작성/리라이트/리뷰만 라우팅하고, 규칙은 `skills/wavvy-lyricist/SKILL.md`, `MASTER/lyrics/skills/WAVVY_LYRIC_SKILL_SPEC.md`, `MASTER/lyrics/LYRICS.md`, `wavvy.py lyrics-skill` 하네스에 위임. YouTube copy, concept/changelog/session, 일반 문서 작성은 범위 밖으로 명시.
- **`/write` lyricist routing team decision** (2026-05-22) — `-team` 논의로 Wavvy 작사가 호출 UX를 검토. 결론은 Claude Code에서는 `/write`, Codex에서는 `-write`를 Wavvy lyric-only thin alias로 두고, 실제 규칙은 `skills/wavvy-lyricist`와 `MASTER/lyrics/skills/WAVVY_LYRIC_SKILL_SPEC.md`에 유지하는 방향. 기록: `meetings/2026-05-22_write-command-lyricist-routing.md`.
- **Wavvy lyricist skill release docs** (2026-05-22) — `-play` worker run의 작사 스킬 산출물을 Wavvy SSOT/가사/브랜드 문서에 연결하고 release readiness를 기록. `MASTER/lyrics/skills/WAVVY_LYRIC_SKILL_SPEC.md`는 lyric skill output schema/self-gate/harness baseline owner로 등록하고, `MASTER/lyrics/LYRICS.md`와 `wavvy.md`는 `skills/wavvy-lyricist` 및 `lyrics-review` gate 진입점을 참조하도록 보강. 검증: lyric skill package/gate PASS, 기존 `doctor` peer script path와 17-00 source-final 상태는 별도 non-blocker로 유지.
- **17-00 Main POP R&B concept draft** (2026-05-21) — 다음 신규 시리즈를 `SERIES/17-00`으로 만들고, 사용자 결정 `기분 좋은 POP(Main) R&B`, `최소 120 BPM`, `무조건 Major Key`를 hard gate로 반영. 17:00은 18:00 퇴근길 위로와 겹치지 않게 `퇴근 전부터 기분을 먼저 올리는 시간`으로 포지셔닝. Style A Main Pop R&B / Style B Bright Contemporary R&B / Style C Light Funk Pop R&B, 18트랙 draft map, YouTube Draft, Next Steps를 작성.
- **17-00 Track 01 sample prompt** (2026-05-21) — 17-00 시리즈의 첫 Suno 테스트용 샘플을 `SERIES/17-00/input/tracks/01_올라가 (Up Again).txt`로 리디자인. 124 BPM, D Major, Female vocal, Main Pop R&B / Pop Neo-Soul. 목적은 `올라가` instant hook memory / mainstream polish / R&B verse pocket / no minor-dark drift 검증.
- **Time concept lyric policy** (2026-05-21) — 사용자 결정 반영: 시리즈 시간대는 가사 주제 강제가 아니라 BPM/Mood/Energy/Use Case 포지셔닝이다. 17:00도 퇴근/사무실 가사를 직접 다룰 필요 없이 퇴근 시간대 기분 전환에 도움이 되는 신나는 Pop R&B / Pop Neo-Soul이면 충분하다. `wavvy.md`, `MASTER/lyrics/LYRICS.md`, `SERIES/17-00/concept.md`에 정책을 추가하고 Track 01 샘플 가사에서 업무/퇴근 직전 소재를 제거.
- **RNB-BEST source-map compilation support** (2026-05-21) — Compilation/best-album 시리즈가 `input/tracks/`에 오디오를 복사하지 않아도 `concept.md`의 `## Track Selection` `Source` 경로를 오디오 SSOT로 사용하도록 `validate`, `pack`, `state`, `gate`를 보강. `Copied Filename`은 report/upload-facing filename으로 유지하고, thumb-only compilation은 static image mode로 검증 가능하게 처리. `SERIES/RNB-BEST` source map의 stale 13-00 norm track 경로 2건을 실제 존재 파일로 보정. 검증: `py_compile`, `unittest`, `validate SERIES/RNB-BEST`, `gate --stage source-final`, `git diff --check` PASS.
- **SSOT and harness hardening pass** (2026-05-02) — `-play` 절차로 프로젝트 전반 SSOT/문서 중복/하네스 설정을 점검하고 보강. `.ai/state.json`의 authoritative docs를 `MASTER/SSOT.md` conflict-owner 문서와 동기화하고, `doctor`에 SSOT 문서 존재/라우터 일관성/entrypoint stale pattern/state authoritative docs/tracked `.DS_Store` hygiene 체크를 추가. `upload-ready` gate는 업로드 전 준비 상태에서 실패성 `youtube_upload_completed` 체크를 표시하지 않고 `youtube_upload_status`로 상태를 보고하도록 수정. `uploaded` 추론은 명시적 Upload Status/YouTube URL/업로드 완료 문구만 인정하도록 강화. `WORKFLOWS`, `cli/SPEC`, `LYRICS`, `MANAGER`, `YOUTUBE`, `wavvy.md`의 vfade/image-mode/title/parentheses/문서 hierarchy drift를 정리. 검증: peer review PASS, plan review PASS, `py_compile`, `unittest`, `doctor`, `validate`, `state --check`, `gate upload-ready/uploaded` PASS.
- **Agent instruction minimalism refactor** (2026-05-02) — `AGENTS.md`를 canonical agent router로 추가하고 `CLAUDE.md`를 29줄 Claude overlay로 축소. 상세 hard constraints/media/approval 규칙은 `MASTER/ai/RUNTIME_RULES.md`로 분리하고 `MASTER/SSOT.md` Conflict Order priority 4에 등록. 사용자 확인 정책은 보존했고, video xfade는 image-mode/uploaded 상태에 무조건 적용되지 않도록 entrypoint에서 제거.
- **Wavvy harness engineering layer** (2026-05-02) — `/team` 분석 → Claude review PASS → plan → Claude plan PASS → `/director` 구현 흐름으로 `doctor/state/gate` CLI, `wavvy_harness/` helper package, `.ai/state.json`, `MASTER/SSOT.md`, 20-00 `uploaded` 상태 정리, harness unit tests, peer-review/plan artifacts를 추가. 업로드 완료 후 `final.mkv/upload.csv`를 용량 정리로 삭제한 상태를 `deleted_after_upload`로 구분. 검증: `py_compile`, `unittest`, `doctor --json`, `validate`, `state --check --json`, `gate --stage upload-ready --json`, `gate --stage uploaded --json` PASS.
- **20-00 Track 02 LLC 이전 버전 톤 고정** (2026-04-28) — `LLC (Low Light Code)` BPM 158 유지. aggressive/gym-crush 최종안 대신 melodic autotuned female vocal, workout-ready night trap pace, punchy tight 808 with controlled saturation, driving 1/16 hi-hats, polished glossy mix 기반 이전 버전 톤으로 고정. 번호 없는 파일명 정렬을 위해 `Order: 02` 추가.
- **20-00 draft verse 길이 보강** (2026-04-28) — 사용자 피드백 "3분이 안되네 좀 짧아" 반영. 신규/draft 실제 출력 최소 3:20 목표를 `concept.md` LYRICS 작성 가이드에 추가. `LLC (Low Light Code)` Length 3:45 + Verse 3 + Final Chorus 추가, `09_Block Signal` Length 3:45 + Verse 4 + 마지막 Refrain 추가, `12_Black Interval` Length 3:45 + Verse 3 + 반복 Final Chorus 지시 추가. `06_Overtime Flame`, `13_Dust Timer`에는 3분 미만 방지 길이 룰을 메타에 추가.
- **20-00 Night Rider PASS 파일명 반영** (2026-04-28) — 사용자 PASS 후 `Night Rider.txt`를 번호 없는 SSOT로 반영. 게이트 정렬을 위해 `Order: 01` 메타를 추가하고, `check_series_gate.sh`가 `Order:`를 파일명 번호보다 우선하도록 수정.
- **20-00 최종 20곡 체제 + 남성 14 / 여성 6 확정** (2026-04-27) — 사용자 정정에 따라 13곡은 현재 작업 세트로 두고 최종 시리즈를 **20곡**으로 복원. 최종 축 분포는 **A 3 / B 4 / C 5 / D 3 / E 2 / F 3 = 20곡**, Hard A+C+D+F = 14곡(70%). 최종 보컬 성별은 **남성 14곡 / 여성 6곡**. 현재 13곡 계획상 M9/F4이므로 추가 7곡은 M5/F2로 배정(14 B Male / 15 C Male / 16 A Male / 17 F Male / 18 D Female / 19 B Female / 20 E Male). 01/03/05/07/08/10 txt 헤더에 누락된 `Vocal: Male` 메타만 보강. `SERIES/20-00/concept.md` v0.4, `MASTER/rubrics/HARD_HIPHOP_RUBRIC.md` v1.4, `MASTER/scripts/check_series_gate.sh` v1.4 동기화. 시리즈 게이트에 S7 보컬 성별 분포 검사를 추가. 검증: lyric avoid PASS 13/13, series gate는 20곡 기준 expected FAIL(현재 13곡, M9/F4, 47:00).
- **20-00 변주 6곡 Suno draft + Track Map S6 정합화** (2026-04-27) — `SERIES/20-00/input/tracks/01_Night Rider.txt`, `02_LLC (Low Light Code).txt`, `06_Overtime Flame.txt`, `09_Block Signal.txt`, `12_Black Interval.txt`, `13_Dust Timer.txt` 생성. 각 파일은 `Status: DRAFT - Suno test pending`으로 표시한 Suno V5.5 작업용 txt이며, 아직 음원 PASS 메타가 아님. Track Map은 S6 마지막 멜로딕/보너스 조건 충족을 위해 E 붐뱁을 Track 13 최종 쿨다운으로 이동하고 D 변주를 Track 09로 이동. 검증: `check_series_gate.sh SERIES/20-00/` PASS 6/6 (draft 포함 13곡, 47:00), `check_lyric_avoid.sh SERIES/20-00/input/tracks` PASS 13/13. `.gitignore`는 `input/tracks` 미디어 무시를 유지하면서 txt 프롬프트는 추적되도록 보정.
- **20-00 최종 순서 정책 추가** (2026-04-27) — 현재 Track Map은 제작/검증용 임시 배치로 두고, 20곡 PASS 후 최종 순서는 **강-약-중-강-약** 흐름으로 다시 섞기로 결정.
- **20-00 보컬 성별 정책 정정** (2026-04-27) — 최종 20곡 성별 비중은 **남성 14 / 여성 6**으로 확정. 기존 PASS 트랙은 실제 음원 성별 우선이며 txt에서 임의 성별 재라벨링 금지.

- **20-00 RUBRIC v1.3 + concept v0.3 + 13곡 분포 + 7곡 PASS 메타 누적 + 5축 + F축 신설** (2026-04-26) — 사용자 7곡 일괄 검토 + /coach 옵션 2 채택. **7곡 PASS 사례 RUBRIC 후행 검증** (Rewrite D / Bottom to the Top C lazy / Fake C 디스 / Boomerang C 디스 / Paycheck A Rage Dry [매칭 정정] / Cold Stack F 신규 / Yang Gang C chant), v1.0/v1.1로는 0곡 통과였으나 v1.3 보정으로 7곡 모두 PASS. **RUBRIC v1.3 보정 7개 항목**: (1) H4 한국어 비중 룰 → 권장만 감점 X (코드스위치 한국 본가 표준), (2) 메타태그 [Bridge] [Pre-Chorus] [Chorus] [Final Chorus] 인정 (이전 금지 룰 폐지), (3) **F축 신설 — Faster Dark Trap 165-180 BPM hub** (Cold Stack 후행 인정), (4) C축 톤 분기 4가지 명시 (husky/distorted/muddy / lazy monotone deadpan / 디스 sarcastic / chant gang hook), (5) B축 introspective laid-back 변종 명시 (Travis Scott Astroworld 톤), (6) BPM 룰 확장 140-160 → 140-180, (7) 사운드 우선 정책 명문화 (가사 가중치 ↓, 사용자 결과물 정성 평가 우선). **concept v0.3**: 곡수 20곡 → 13곡 축소 (A 2 / B 2 / C 4 / D 2 / E 1 / F 2 = 13곡, Hard A+C+D+F = 10곡 77%, Hard 60% 정책 충족), 변주 6곡 슬롯 명시 (A 변주 1 / B 신규 2 / D 변주 1 / F 변주 1 / E 보너스 신규 1), Track Map 4막 × 13곡 스켈레톤 재작성, 5축 + 보너스 Style Templates 7곡 PASS Style Prompt 인용, EXCLUDE v4 (F축 추가), QA 체크리스트 사운드 우선. **자동화 스크립트 수정**: `check_series_gate.sh` 13곡 분포 + F축 추가 + Hard 60% minimum threshold + 시리즈 길이 40-65분 + S6 룰 완화 (마지막 1-2곡 중 하나는 B/E). **7곡 메타 파일 생성** (`SERIES/20-00/input/tracks/03~11_*.txt` Track Map v0.3 슬롯 정착). 산출물: `MASTER/rubrics/HARD_HIPHOP_RUBRIC.md` v1.3 + `SERIES/20-00/concept.md` v0.3 + 7곡 메타 + `MASTER/scripts/check_series_gate.sh` v1.3 + `meetings/2026-04-26_20-00-execution-coach.md` (구두 /coach 회의)

- **20-00 HARD_HIPHOP_RUBRIC v1.1 + 자동화 스크립트 2건 + Hard 60% 정책 반영** (2026-04-26) — /team Decision Meeting (실행 플랜) 만장 합의 후 즉시 실행. **사용자 정책 결정**: Hard 비중 60% (A Rage Dry + C Hardcore Trap + D K-Drill = 12곡 / B Tuned + 보너스 붐뱁 = 8곡, 20곡 확정). **산출물 4건**: (1) `MASTER/rubrics/HARD_HIPHOP_RUBRIC.md` v1.1 (225줄) — Hard Gates 8 + Style-Specific Gates 13 + 8-Factor Scoring 100점 + Series Gates 6, Hard 60% 정책 반영, 자동화 스크립트 인터페이스 예시 포함. (2) `MASTER/scripts/check_lyric_avoid.sh` — H8 가사 회피 자동 검사 (50 키워드 5카테고리: 폭력·살해/마약/혐오/자해·자살/노골적 성행위, K-Drill 본가 어휘 갱·크루·블록 보존). PASS/FAIL + 매칭 키워드 카테고리별 출력. (3) `MASTER/scripts/check_series_gate.sh` — S1-S6 시리즈 단위 자동 검증 (S1 곡수+Hard 60% / S2 BPM 4단계 분포 / S3 A·B 인접 회피 / S4 60-90분 / S5 Track 01 워밍업 B축 / S6 마지막 멜로딕). 트랙 메타 파일 헤더 파싱(Type/BPM/Length). (4) `SERIES/20-00/concept.md` v0.2 → v0.2.1 업데이트 — 곡수 분포 A 4 / B 5 / C 5 / D 3 / 보너스 3 = 20곡 확정 + Track Map 4막 × 20곡 스켈레톤 재작성 (Hard 12 / Non-Hard 8 + Track 19 A 추가로 Hard 60% 보강). 회의록 2건: `meetings/2026-04-26_20-00-genre-gate-rubric-design.md` + `meetings/2026-04-26_20-00-genre-gate-execution-plan.md`. 12-00 시리즈로 스크립트 작동 테스트 통과. Next: Suno V5.5 5곡 1차 테스트 (A/B/C/D/보너스 각 1) → 루브릭 v1.1 PASS/FAIL → v1.2 조정.

- **20-00 시리즈 장르 게이트(루브릭) v1.0 설계 — /team 합의** (2026-04-26) — Product Leader + Marketing Director + Engineering Lead Round 1 + QA Reviewer Round 2 만장 합의 (평균 94.6점, 모든 Gate 개별 PASS). 5개 안건 합의: (1) **Hard Gates 8개** (BPM·Drum·Bass·Vocal·Hook·EXCLUDE·Workout 사운드 정합·콘텐츠 회피, H6/H8 자동화 → 실질 수동 6개로 12-00 동등) (2) **Style-Specific Gates 13개** (A 3 + B 4 + C 2 + D 3 + E 2, A1 no autotune vs B1 autotune 필수가 시리즈 핵심 차별점, Section A.3.4 EXCLUDE 분리표 게이트화) (3) **8-Factor Scoring 100점** (F1 Trap Groove 15 / F2 808 10 / F3 Hook&Adlib 15 / F4 Korean Vocal 15 / F5 Energy 10 / F6 Workout BPM 단계 10 / F7 Production 15 / F8 장르 정체성 10, 판정 85+ PASS / 70-84 BORDERLINE / <70 FAIL) (4) **가사 자유 정책 게이트 반영** — F4 음성·발음·톤만, 가사 H8 회피 영역 자동 grep 50개 키워드 5카테고리(폭력·살해/마약/혐오/자해/노골적성), K-Drill 본가 어휘(갱·크루·블록) 보존, 라이리시즘은 보너스 붐뱁 E2만 (5) **Series Gates 6개** (S1 곡수 분포 / S2 BPM 분포 워밍업/메인/HIIT/쿨다운 / S3 A·B 인접 회피 / S4 60-90분 / S5 Track 01 워밍업 / S6 마지막 2-3곡 멜로딕). 충돌 해소 3건: MD H7 자동화 부담 → EL 자동 grep 비용 0 / EL F6 점수화 어려움 → PL BPM 단계 분류만 / EL Style Gate 16개 → PL 13개 축소 (C·D BPM Hard Gate 중복 제거). Next Actions: HARD_HIPHOP_RUBRIC.md v1.0 작성 + 자동화 스크립트 2건 + Suno 1차 5곡 테스트. 산출물: `meetings/2026-04-26_20-00-genre-gate-rubric-design.md`

- **20-00 `💪 AFTER HOURS WORKOUT` concept.md v0.2 + P0 갭 보충 리서치** (2026-04-26) — Workout Tuned-Rage 보충 리서치 2건 병렬(researcher × 2): Section A Korean Tuned Singing Rage Trap 정밀 + Suno V5/V5.5 키워드 분리표(Dry vs Tuned EXCLUDE 분리) + 글로벌 Dry vs Tuned 보컬 체인 비교 + Workout 적용 가설 검증 / Section B 한국 운동 BGM 트렌드(Bugs·Melon·Apple Music 7건 분석) + 25-35 직장인 운동 행태(헬스 30.9%·76.4% 저녁 운동·30대 매장 25.6%·러닝 +232%) + K-Drill Workout 정합성. 신뢰도 평균 72%. **시리즈 가설 CONDITIONAL PASS**: Korean Workout Hip-Hop 빈자리 = 글로벌 Apple Music Hip-Hop Workout 외산 트랩 우세, Korean rap 0%. concept.md v0.2 작성(497줄): 신 4축 + 보너스 (A Rage Dry 3-4 / B Rage Tuned 5 / C Hardcore Trap 5-6 / D K-Drill 액센트 3 / 보너스 빡센 붐뱁 2-3 = 18-21곡, A축 Section A·B 권장 절충안). Style Templates 5종(Section A.3 키워드 분리표 인용 + Paycheck v3 통합), EXCLUDE v3 축별 특화표, Workout 배치 룰(워밍업 100-120 → 메인 130-150 → HIIT 140-180 → 쿨다운 90-110), LYRICS 가이드, QA 체크리스트, YouTube Metadata v0.2 초안. 정정 사항: SMTM12 = 2026-04-02 결승 HAON 우승 (다음 달이라 후속작 평가 불가) / Loopy `MARNI` 메인 PD = SanityTooFye (Dayrick 잘못) / NOWIMYOUNG = electropop 비중 B축 단순 편입 부적합 / MOLLAK (Jvcki Wai × Vangdale 2025-07-04) = Female Korean Tuned Singing Rage 인접 신규 사례. **사용자 피드백 반영**: "가사까지 workout일 필요는 없어. 트랙 톤앤매너(BPM/에너지)만 workout스러우면 돼" → 가사 가이드 전반 수정 (D축 가사 리라이트 강제 제거 / Workout 어휘 강제 제거 / 회피 영역만 명시: 무차별 폭력·살해·총기·마약 직접 묘사). 메모리 저장: `feedback_wavvy-lyrics-vs-sound-separation.md` (시리즈 컨셉 정합 = 사운드 영역, 가사는 자유). 산출물: `SERIES/20-00/concept.md` v0.2 + `SERIES/20-00/report/2026-04-25_workout-tuned-rage-supplement.md`

### Removed
- **Historical artifact pruning** (2026-06-02) — 현재 하네스/스킬/에이전트 라우팅 참조를 확인한 뒤, 작동 경로에 연결되지 않은 과거 실행 기록과 회의/리뷰/레퍼런스 파일을 삭제. 삭제 범위는 `.ai/auto-handoff/`, `.ai/peer-review/runs/`, 미참조 `.ai/pipeline/runs/*`, `.ai/meetings/`, `reviews/`, `Reference/`, 미참조 `meetings/*.md`, 미참조 `report/*.md`, `.ai/lessons-learned.md`. 보존: `concept.md`, `.ai/state.json`, `.ai/HANDOFF.md`, `.ai/SESSION.md`, 현재 MASTER/스킬/하네스 문서, `skills/wavvy-lyricist`가 직접 참조하는 리서치 run, 20-00 루브릭/컨셉이 인용하는 리포트와 회의록.
- **Legacy markdown pruning** (2026-05-04) — `-team` 검토 기준으로 현재 SSOT/하네스 운영에 쓰이지 않는 legacy/superseded 문서만 삭제. 삭제: `.ai/plans/PLAN_wavvy_agent_instruction_minimalism.md`, `.ai/plans/PLAN_wavvy_harness_setting.md`, `meetings/2026-02-07_vibem-swot-analysis.md`, `meetings/2026-03-07_final-mp4-retrospective.md`, `reviews/2026-03-07_vibem-to-wavvy-rename.md`. 최신 `.ai/pipeline/*`, `.ai/peer-review/*`, `.ai/HANDOFF.md`, `.ai/SESSION.md`, 시리즈 concept/research, MASTER SSOT 문서는 보존.
- **20-00 시리즈 산출물 전면 리셋 — 차트·청자 검증 후 시상식 직반영 4축 안 폐기** — 사용자 의심 "진짜 Korean 2026 trend에 적합한가?" 검증 → 신규 리서치 결과 시상식 직반영 4축 안 **FAIL** (벅스 2025 힙합/R&B TOP30 Rage/Drill/Hyperpop 0-1곡 / 멜로딕 트랩·Trap-Soul 8-10곡 / KT지니 30대 1위 G-DRAGON `TOO BAD` / Effie "보수적 청자 싫어한다" 인용). 사용자 첫 직감("트렌디 트랩 비트 기반") 재확인. **삭제**: `SERIES/20-00/concept.md` v0.1(437줄), `test-prompts.md`(414줄), `input/tracks/` 가사 2건(Paycheck Rage / Rewrite K-Drill). **보존** (audit trail): 1162줄 딥리서치 + 미팅 노트 4건 + 차트 검증 리포트(`report/2026-04-25_chart-vs-awards-validation.md`). 새 방향은 사용자와 별도 논의 예정.

### Changed
- **YouTube metadata SSOT 하네스 보강** (2026-04-30) — `wavvy.py pack`이 더 이상 기본 제목/빈 description으로 `upload.csv`를 만들지 않도록 보정. `concept.md`의 `## YouTube Metadata` 또는 `## YouTube Draft` 섹션에서 `제목/설명/태그`(영문 heading도 허용)를 파싱해 `upload.csv`를 채우고, `validate` 단계에서 누락 시 warning을 출력한다. 20-00 metadata는 기존 Wavvy 포맷에 맞춰 이모지·구분선·트랙리스트·고정 댓글을 포함한 FINAL 섹션으로 갱신.
- **20-00 WAV 리네임 + YouTube 영상 패키징** (2026-04-30) — 다운로드된 20개 WAV를 `concept.md` v0.6 최종 러닝 오더 기준 `NN__Title__Style__Genre__BPM.wav`로 정리. 입력 파일에서 `17. Engine.wav`와 `18. Fake.wav`가 뒤바뀐 상태였으므로 제목 기준으로 `17 Fake / 18 Engine`으로 교정. `wavvy.py pack SERIES/20-00 -y` 자동모드로 -14 LUFS 정규화, 0.8초 크로스페이드, 20곡 x2 반복 머지(`work/merged.wav` 7,876.24s), `loop.png` 기반 최종 영상 `output/final.mkv` 생성. 초기 렌더 컨테이너 tail 61초를 remux-trim해 최종 duration 7,879s로 보정. `ffprobe`와 video/audio decode QA PASS.
- **20-00 `🌃 AFTER HOURS` 4축 재편 — /team 만장 합의 (2026 국힙 시상식 직반영)** — C축 모던 하드코어 붐뱁 Suno V5.5 생성 난이도 + 2025 H2 모멘텀 약화 객관화 + 글로벌 추천(Plugg 메인) K-rap 사례 부족 검증 → 새 4축 35/20/25/10+5 합의: A Rage 7곡(KC + EK 흡수 후보) / B K-Drill 4곡 / C Hardcore Trap 5곡(YUMDDA 추가) / D Hyperpop·Digicore Edge 2곡(Sion + Effie raged 한정) + 보너스 Modern Boom Bap 1-2곡. 폐기: PluggnB·Sexy Drill·Phonk(K-rap 사례 부족), 모던 붐뱁 메인 7곡 → 보너스 격하. 보존: 통과 가사 2건(Paycheck/Rewrite), Style Prompt 노하우, EXCLUDE v2 13종, After Hours 프레임 + Dark City 미학. Marketing/Product/Growth/Design 4역할 + QA Round 2 인라인 5/5 PASS. 산출물: `meetings/2026-04-25_20-00-4axis-realignment.md`
- **20-00 `🌃 AFTER HOURS` 시리즈 기획 착수 — 4축 딥리서치 + /team 결정** — Wavvy 첫 힙합 시리즈. 1차 서브장르 리서치(3축→4축 확장) + 2차 4축 음악적 특성 딥리서치(신뢰도 88%, 소스 180+, 10 parallel researcher agents). /team Trade-off Discussion(Marketing/Product/Growth/Design + QA) 5 안건 만장 합의: **`🌃 AFTER HOURS`** 하이브리드 포지셔닝(After Hours 프레임 + Dark City 미학), 20곡 배분 **4:5:7:4** (Rage/K-Drill/모던 하드코어 붐뱁/하드코어 트랩 젊은 씬), 썸네일 블루아워 도시 실루엣+네온 악센트, Suno V5.5 1,000자 Style 필드 활용. 리서치 오류 6건 교정(AMADU=2019 / Deepflow `Legacy` 미존재 / Loopy The Cohort·AOMG 미소속 / ZENE≠조광일 / KC=레이블(솔로X) / Jersey Drill 한국 미정립). 산출물: `SERIES/20-00/report/2026-04-24_hard-hiphop-4axis-musical-deep.md` + `meetings/2026-04-25_20-00-hard-hiphop-positioning.md`
- **Track 03 작사 프롬프트 + LYRICS.md 소괄호 금지** — Track 03 "볕 (Sunlit)" 작사 프롬프트 작성 (198자, 풀 구조+DNA 반영). LYRICS.md §1.2 소괄호 사용 금지 규칙 반영
- **리팩토링 후 잔존물 정리** — lessons-learned.md dead 가사 섹션 삭제(66줄) + 용어 업데이트(가사 작성→Suno 입력), SESSION.md stale 핸드오프 메모 3건 제거
- **워크플로우 리팩토링 — Suno 자체 작사 전환** — LYRICS.md v4.0 (§1 Lyric Prompt Guide), WORKFLOWS.md v2.0 (3단계), RUBRIC 가사→보컬 체크리스트 전환, LYRICS_DNA.md 역할 재정의, REFERENCE_SAMPLE/FAILURE_CASES 삭제. Track 01-04 제목 변경 + 가사 제거.
- **12-00 가사 DNA + RUBRIC 강화 + concept.md 재설계** — Afrobeats 가사 딥리서치(24개 소스) 기반 LYRICS_DNA.md 신규 생성, RUBRIC v1.1 (L15-L19 Afrobeats 특화 게이트), concept.md v3.0 (Style A/B/C 템플릿 + 15트랙 맵)
- **루브릭 SSOT 통합** — evidence 파일을 각 루브릭 본문으로 합침 (CHILLHOP, FAST_LOFI), evidence/ 폴더 제거

### Removed
- **중복 레퍼런스 정리** — `museA Suno 자료집.pdf` (MD 변환본 유지), `lofi-genre-research.md` (LOFI_RUBRIC에 흡수), `Reference/song/` 빈 폴더, `rubrics/evidence/` 폴더
- **레거시 정리** — `.pycache/` 삭제 (vibem 잔존), `04-00/input/template.psd` 제거 (미사용)

### Fixed
- **파일명 오타** — `shorts_orignal.mov` → `shorts_original.mov`
- **.gitignore** — VIBE-M 주석 → Wavvy, `.pycache/` 패턴 추가

### Changed
- **MASTER 문서 v3.2 — Writing Formula + 워크플로우 분리**
  - STYLE.md §1.5 Writing Formula 신설 (7요소 작성법)
  - TAG_BANK.md §2.5 Key/Mode 키워드 추가
  - LYRICS.md §2.5 Song Structure Patterns 추가
  - WORKFLOWS.md 정리 (215줄 → 113줄, FFmpeg/YouTube 분리)
  - CLI SPEC.md §6 영상 패키징 워크플로우 추가
  - YOUTUBE.md §9 메타데이터 워크플로우 추가
  - Reference 직접 참조 제거 (CLAUDE.md, ROLES.md)
- **wavvy.md 최신화** — 11-00 시리즈 추가, 영상 구성 규칙 업데이트 (인트로 없음 + 좌상단 로고), 브랜딩 문구 용도 변경 (썸네일용)
- **WORKFLOWS.md §4 레거시 참조 수정** — Wavvy_Master_Plan.md → cli/SPEC.md
- **vibem.py → wavvy.py 리네임** — CLI 파일명 프로젝트명 일치, 9개 파일 67곳 참조 업데이트
- **SESSION.md 슬림화** — 1,443줄 → 23줄 (98% 감소), 진행 중/다음 할 일/핸드오프 메모만 유지
- **wavvy.md §7 채널 브랜딩 추가** — SESSION.md에서 이동
- **11-00 YouTube Draft v2 완성** — 30트랙 타임스탬프, 이모지 🎯, 설명 문단 구분

### Removed
- **draft_description 잔존 코드 정리** — ProjectPaths, upload.csv 참조 제거
- **중복 handoff.md 삭제** — .ai/HANDOFF.md가 SSOT

### Added
- **wavvy.py vfade 자동 크롭 + 로고** — pillarbox 감지/제거 + 로고 오버레이 (50%)
  - `--crop/--no-crop`: 자동 pillarbox 크롭 (기본: 활성화)
  - `--logo/--no-logo`: 로고 오버레이 (기본: 활성화)
- **pack 인터랙티브 모드** — 4가지 설정 확인 후 진행
  - Video crossfade 사용 여부
  - Track repeat 횟수
  - Pillarbox 자동 크롭
  - Logo 오버레이
- **Seamless loop 워크플로우** — 끝-시작 xfade로 무한 반복 끊김 없음
  - WORKFLOWS.md §5.2 추가
  - lessons-learned.md 해결책 기록
- **wavvy.py vfade 명령어** — 비디오 크로스페이드 자동화
  - `--test`: 30초 테스트 영상 생성
  - `--fade 0.5`: xfade 전환 시간
  - 출력: input/loop_xfade.mp4
- **pack Pre-flight 체크** — loop_xfade.mp4 없으면 경고
  - `--use-xfade`: loop_xfade.mp4 사용 (권장)
  - `--force`: 확인 없이 진행

### Changed
- **CLAUDE.md 복잡한 작업 규칙 추가** — 10개+ 파일, 10분+ 미디어, 새 FFmpeg 필터 시 사용자 확인 필수

### Removed
- **draft_description.txt 생성 코드 제거** — YouTube 메타데이터는 concept.md를 SSOT로 사용
- **CLAUDE.md Hard Constraints #6, #7 추가**
  - Video Crossfade 필수
  - Pre-flight 체크
- **WORKFLOWS.md §5 영상 패키징 CLI 워크플로우로 단순화**
- **cli/SPEC.md vfade 명령어 문서화**
- **WORKFLOWS.md §5.0 필수 규칙 추가**
  - `--fade 0.5` (크로스페이드 0.5초)
  - `--repeat 2` (플레이리스트 2회 반복)
- **11-00 tracks 폴더 구조 통일**
  - tracks/ → input/tracks/ 이동 (다른 시리즈와 동일 구조)
  - wav 파일 네이밍 룰 적용: `{N}__{한글}__{영문}__{장르}__{BPM}.wav`
  - WORKFLOWS.md 경로 업데이트

### Added
- **11-00 input 폴더 + 썸네일/루프영상**
  - thumb.png: 고양이+헤드폰+모니터 응시
  - loop.mp4: 8초 원본 루프
  - 크로스페이드 0.5초 x3 테스트 PASS
- **11-00 Track 11-15 가사/스타일 txt + concept.md 반영**
  - Track 11 "어딘가": Rhodes, disoriented, F#m, 74 BPM
  - Track 12 "신호": Felt piano, awakening, D Major, 78 BPM
  - Track 13 "꼬르륵": Nylon guitar, organic, A Major, 82 BPM
  - Track 14 "고개": Neo-Jazzhop, sax, G Major, 85 BPM
  - Track 15 "벌써": Felt piano, present, C Major, 88 BPM
  - 11-00 시리즈 15/15 트랙 기획 완료
- **11-00 Track 02-06 가사/스타일 txt 완료**
  - Track 02 "멀어져": Ambient pad, dreamy, 80 BPM
  - Track 03 "리듬": Nylon guitar, warm, 78 BPM
  - Track 04 "에이전트": Felt piano, hypnotic, 76 BPM
  - Track 05 "초점": Wurlitzer, focused, 75 BPM
  - Track 06 "망각": Rhodes, hazy, 74 BPM
- **11-00 Style Variations 가이드 추가**
  - Track 08, 10: Kalimba-Keys Melancholia
  - Track 14: Neo-Jazzhop
  - Classic Lo-fi 80% + 변주 20% 배분

### Changed
- **WORKFLOWS.md v1.3 — txt 파일 우선 규칙 강화**
  - §0 절대 규칙 신설: txt 먼저 생성 → PASS → concept.md 반영
  - §2 Style Prompt 워크플로우 제거 (STYLE.md 참조로 대체)
  - txt 경로 통일: `SERIES/[시리즈]/tracks/{N}_{제목}.txt`

- **11-00 Track 01 "경계 (Threshold)" 가사/스타일 txt**
  - B타입 만트라, 82 BPM, Am
  - LOFI_RUBRIC Hard Gates PASS, 6-Factor 93점

### Fixed
- **Track 01 구조/스타일 수정**
  - Hook 4회→2회 (가사 반복 축소)
  - [interlude] 추가로 3분+ 구조 확장
  - 보컬 믹스 다운: "Vocal as texture, not lead"
  - Exclude: forward vocals, prominent vocals 추가

### Changed
- **WORKFLOWS.md v1.2 — Pre-condition + 루브릭 테스트 셀프 루프**
  - §1 가사, §2 스타일 워크플로우에 Pre-condition 추가 (LYRICS.md, STYLE.md, RUBRIC 필수 참조)
  - 루브릭 테스트 셀프 루프 추가: Hard Gates → 6-Factor → PASS까지 반복
  - 참조 없이 작성 시 FAIL 재작성 규칙 명시

- **전 시리즈 YouTube 메타데이터 v2 재생성**
  - 04-00, 14-00, 16-00, 18-00, 21-00 시리즈 v2 Final 재생성
  - 06-00 타임스탬프 형식 수정 (60분+ → HH:MM:SS)
  - 브랜드 통일 (soomshuim → Wavvy)
  - 제목 포맷 통일 (Playlist | HH:MM | 감정훅 + 이모지 | 장르 | 용도 | Wavvy)

- **10-00 YouTube 메타데이터 v2 재생성 + 타임스탬프 형식 규칙**
  - concept.md YouTube Draft v2 Final 재생성 (Wavvy 브랜드)
  - 중복 섹션 정리 (Tracklist, 해시태그, 저작권 → 설명에 통합)
  - YOUTUBE.md 60분 이상 타임스탬프 HH:MM:SS 형식 규칙 추가

- **YouTube 메타데이터 문서 통합 + 장르 마스터 분리**
  - youtube/ 3개 파일 → YOUTUBE.md 통합 (124줄)
  - reference/GENRES.md 신설 (장르 마스터 룩업)
  - TAG_BANK.md 압축 (장르 섹션 → GENRES.md 이동)
  - WORKFLOWS.md §7 Phase 1 유저 요청 항목 추가
  - 참조 링크 수정 (STYLE.md, LYRICS.md)

- **SSOT 문서 150줄 다이어트 + 폴더 구조 재편**
  - 모든 AI 규칙 문서 150줄 이하로 압축
  - 폴더 구조 재편: style/, lyrics/, roles/, rubrics/, youtube/, cli/
  - wavvy.md 신설 (프로젝트 정체성/브랜드)
  - CLAUDE.md 정리 (AI 실행 엔진 설정)
  - 삭제: _INDEX.md, 24H_UNIVERSE.md, PLAYLIST_GUIDE.md, QUICK_REF.md
  - 삭제: llm_loop 관련 파일, docs/planning/ 폴더
  - 루브릭 압축 + evidence/ 폴더로 근거 분리

### Added
- **AM_1000 완료 (15/15) + 영상 패키징 + Description 커스텀**
  - Track 11 "회의" (B타입, Male Baritone, 87 BPM, D major, 의성어 만트라)
  - Track 12 "다시" (C타입, finger snap texture, 82 BPM, E major)
  - Track 13 "Tab" (A타입, Male Baritone, 85 BPM, Dm, 3줄 한 번)
  - Track 14 "Tick Tock" (C타입, clock rhythm, 80 BPM, Em)
  - Track 15 "Hunger" (C타입, sparse arrangement, 78 BPM, E major)
  - 영상 패키징: final.mp4 (76.9분, 15트랙×2회, 0.5초 crossfade)
  - 압축 버전: final_compressed.mp4 (3.9GB→1.5GB, Canva 업로드용)
  - draft_description.txt 커스텀 (PLAYLIST_GUIDE 규칙 준수)
  - 해시태그 정리 (정체성/유입/맥락/브랜드 그룹화)
  - 고정 댓글 훅: "지금 열어둔 탭, 몇 개예요?"
  - txt 파일 정리 (concept.md SSOT 통합)

- **AM_1000 Track 05-10 완료 (10/15)**
  - Track 02 "거울" 리메이크 (A→B타입, 서랍→까만거울 컨셉)
  - Track 05 "집중" (C타입, pure instrumental, 78 BPM, Dm)
  - Track 06 "알림" (C→B타입 전환, bell chime/glockenspiel 알림 컨셉)
  - Track 07 "잉크" (B타입, Male Baritone, 85 BPM, E major)
  - Track 08 "타이핑" (A→B타입 전환, Female Alto, 88 BPM, Dm)
  - Track 09 "숨(Breathe)" (B→C타입 전환, pure instrumental, D major)
  - Track 10 "환기(Refresh)" (C타입, pure instrumental, E major)
  - 타이틀 정정: 루틴→사진, 흐름→모니터, 타자→타이핑
  - Major 키 확장: T07 E major, T09 D major, T10 E major (minor 11 / major 4)
  - T07↔T08 순서 스왑 (Alto→Alto 연속 보컬 해소)
  - 타입 배분: A(2) B(7) C(6)
  - Track 01-10 txt 파일 삭제 (concept.md SSOT 통합)

- **AM_1000 미니멀 보컬 Chillhop 방향 전환 + Track 01-04 완료**
  - 방향: 한국어 미니멀 보컬 Chillhop, 루프 기반 구조
  - 보컬 A/B/C 타입 시스템: A(4-8줄 한 섹션) / B(1-2줄 만트라) / C(인스트루멘탈+텍스처)
  - 10곡 → 15곡 확장 (Suno 출력 길이 대응)
  - concept.md v1.0 전면 재작성 (A×4/B×5/C×6 분배)
  - Track 01 "오전" (B, Contralto female, 85 BPM, Dm)
  - Track 02 "책상" (A, Baritone male, 87 BPM, Em)
  - Track 03 "루틴" (C, girl laughter sample, 90 BPM, D major)
  - Track 04 "흐름" (B, Baritone male, 90 BPM, Em, vinyl warmth)
  - 소예_반복20.wav (딸 웃음 20회 반복 WAV, Suno 업로드용)

- **CHILLHOP_RUBRIC.md v1.3**
  - v1.2 신설 (6-Factor 100점, Phase 0 Hard Gates 7개)
  - v1.3 A/B/C 보컬 타입별 채점 기준 추가
  - Lo-fi vs Chillhop 차이 명시 (dusty→crisp, 60-90→78-105 BPM)

- **RUBRICS_CREATION_PROCESS.md v1.1 신설**
  - Research-First 루브릭 생성 워크플로우 문서화
  - Phase 1-4: 리서치 → 팀협의 → 루브릭설계 → SSOT통합
  - Calibration Track 필수화 (Team 리뷰 반영)

### Changed
- **MANAGER.md v1.6 Phase 0.3 삽입**
  - New Genre Research 단계 추가 (기존 rubrics 없을 때 필수)
  - RUBRICS_CREATION_PROCESS.md를 SSOT로 지정

- **_INDEX.md v1.8 SSOT 매트릭스 확장**
  - Chillhop 장르 게이트 항목 추가
  - 새 장르 루브릭 생성 항목 추가

- **CLAUDE.md v2.14.0 Auto Reference Rules 확장**
  - Chillhop 트랙 QA → CHILLHOP_RUBRIC.md
  - 새 장르 루브릭 생성 → RUBRICS_CREATION_PROCESS.md

- **24H_UNIVERSE.md 10:00 Station 추가**
  - 업무시간 (Korean Chillhop, buried vocals)

- **AM_0600 업로드 메타/썸네일 에셋 미세 조정**
  - `SERIES/AM_0600/output/draft_description.txt` 생성 및 조회수 고려 문구(검색 키워드/CTA/해시태그) 보정
  - `SERIES/AM_0600/input/thumb.jpg`, `SERIES/AM_0600/input/thumb.psd` 최신본 반영
  - `SERIES/AM_0600/input/logo_soomshuim.png` 추가 및 `Reference/logo/playlist.png` 레퍼런스 반영
  - `SERIES/PM_0900/input/thumb.jpg`, `SERIES/PM_0900/input/thumb.psd` 최신본 동기화

- **AM_0600 패키징 사전 정리 및 영상 합성 준비**
  - `SERIES/AM_0600/input/` 구조 정리(`track/`, `loop.mp4`, `loop4.mp4`, 썸네일 소스)
  - 트랙 파일명 표준화: `NN__Title__Mood__Genre__BPM.wav` (01~10)
  - `SERIES/AM_0600/work/norm_tracks/` 생성 및 `norm_01..10` 정규화 산출
  - 1~10 트랙 2회 반복 플레이리스트 영상 생성(`output/final.mp4`, `final_youtube.mp4`)
  - 중간 산출물 정리: concat 목록/중간 WAV를 `work/`로 이동

- **AM_0600 Track 06-10 최종 정리 + 시각 컨셉 준비**
  - `SERIES/AM_0600/concept.md`를 Track 01-10 통합본으로 확정
  - Track 06 `Moving`, Track 07 `Wake Up`, Track 08 `Kitchen Light`, Track 09 `Unfold`, Track 10 `Settle Down` 상태/제목/본문 반영
  - Track 10 보컬 페르소나를 `male`로 통일(lyrics meta + style + exclude 정합)
  - Track 1~9 txt 작업본 정리 후 Track 10 txt(`lyrics/style/exclude`)만 유지
  - Fast Lo-fi 루브릭 v1.2에 웹 리서치 근거 섹션 추가 및 레퍼런스 링크 정리
  - YouTube 루프 제작 전 단계로 Freepik용 6AM 일러스트 컨셉/프롬프트 확정

### Added
- **GPT Loop Sidecar PRD 초안 작성 (기존 구조 불변)**
  - 문서: `docs/planning/PRD_GPT_LOOP_SIDECAR.md`
  - 범위: 가사/Style/Exclude 생성의 `generate -> validate -> revise` 옵션형 루프
  - 원칙: SSOT 문서/기존 승인 절차(`txt -> PASS -> concept`) 유지
  - 정책: `_llm` suffix + 자동 버전 증가(덮어쓰기 금지)
  - 리포트: 하드룰/소프트룰 분리 QC 문서 산출
- **GPT Loop Sidecar 구현 명세서 + 템플릿 위치 고정**
  - 문서: `docs/planning/IMPLEMENTATION_SPEC_GPT_LOOP_SIDECAR.md`
  - 범위: 파일별 책임, CLI 인자 계약, 환경변수, exit code, 리포팅 포맷
  - 프롬프트 경로: `MASTER/prompts/llm_loop/`
  - 템플릿 5종 추가:
    - `generate_lyrics.md`
    - `generate_style.md`
    - `generate_exclude.md`
    - `validate_soft.md`
    - `revise.md`
- **GPT Loop Sidecar M1 구현 (CLI 골격 + 버전 정책 + dry-run)**
  - 엔트리: `tools/llm_loop.py`
  - 모듈: `tools/llm_loop/config.py`, `tools/llm_loop/loader.py`, `tools/llm_loop/versioning.py`, `tools/llm_loop/reporter.py`
  - 기능:
    - `python tools/llm_loop.py run ...` 명령 골격
    - `_llm` 출력 파일 버전 자동 증가
    - 덮어쓰기 방지
    - `--dry-run` 실행 경로 및 요약 출력
  - 참고: 생성/검증 실제 LLM 루프는 M3에서 연결 예정
- **GPT Loop Sidecar M2/M3 1차 연결**
  - 모듈 추가:
    - `tools/llm_loop/rules_hard.py`
    - `tools/llm_loop/renderer.py`
    - `tools/llm_loop/llm_client.py`
    - `tools/llm_loop/rules_soft.py`
    - `tools/llm_loop/cross_series.py`
  - `tools/llm_loop.py` 확장:
    - 템플릿 변수 주입 (`MASTER/prompts/llm_loop/*.md`)
    - OpenAI 호출 기반 `generate -> hard-validate -> revise -> soft-validate` 루프
    - hard fail 시 최소수정 revise 재시도 (`max-iterations` 한도)
    - 최종 verdict 기준 종료 코드 반영 (`READY_FOR_REVIEW`/`NEEDS_REWRITE`)
  - 검증:
    - `python3 -m py_compile tools/llm_loop.py tools/llm_loop/*.py`
    - dry-run 성공
    - API 키 미설정 시 exit code `2` 확인

### Changed
- **AM_0600 Fast Lo-fi 시리즈 1차 운영 기준 정렬 + 루브릭 구조 확장**
  - 신규 시리즈 기준본 생성: `SERIES/AM_0600/concept.md` (concept 선행 생성 규칙 반영)
  - Track 01 산출물 정렬:
    - `track01_lyrics.txt` 구조 확장 (verse 3개 + intro/pre-chorus/interlude/bridge/instrumental/outro)
    - `track01_style.txt` 선두 `Articulation` 고정 + 3분 이상 전개 지시 반영
    - `track01_exclude.txt` 최종본 유지
  - 문서 규칙 보강:
    - `MASTER/LYRICS.md` v2.2.1: Hip-hop 조건부 H1-H5 게이트 추가
    - `MASTER/MANAGER.md`: 신규 시리즈 부트스트랩(Phase 0.4), 무버전 txt 정책 반영
  - 루브릭 체계 개편:
    - `MASTER/rubrics/` 폴더 신설
    - `CITYPOP_RUBRIC.md`, `FAST_LOFI_RUBRIC.md` 경로 이관
    - `FAST_LOFI_RUBRIC.md` v1.1: Track 01 PASS 캘리브레이션(87/100), Hard Gates, QC 템플릿 추가
  - 라우터/매뉴얼 경로 동기화:
    - `MASTER/_INDEX.md` v1.7
    - `CLAUDE.md` v2.13.3
- **GPT Loop 프롬프트 M1.1 하드게이트 정합성 강화 (SSOT 강제)**
  - 대상:
    - `MASTER/prompts/llm_loop/generate_lyrics.md`
    - `MASTER/prompts/llm_loop/generate_style.md`
    - `MASTER/prompts/llm_loop/validate_soft.md`
  - 반영:
    - 가사 템플릿: 구조 태그 직후 `()` 메타 1행 필수, K1-K3(2개 이상 No 시 재작성) 하드게이트화
    - 스타일 템플릿: Harmony Guard 2줄 + EDM 금지 1줄 + Energy Permission 블록 verbatim 강제
    - 검증 템플릿: S1-S12 테이블 누락/미통과 시 `NEEDS_REWRITE`, K1-K3 하드 판정 필드 추가
- **GPT Loop 템플릿 고도화 (Persona + 기존 역할 프롬프트 근간 반영)**
  - 대상: `MASTER/prompts/llm_loop/*.md` 5종
  - 반영:
    - 작사가 퍼소나 (가사/후크/언어 선명도)
    - 작곡가 퍼소나 (에너지 아크/보컬 설계)
    - 프로젝트 매니저 퍼소나 (게이트/최소수정/판정)
  - 근간:
    - Seed/Variation/Manager 역할 규칙 (`ROLES.md`, `MANAGER.md`)
    - 가사/스타일 SSOT (`LYRICS.md`, `STYLE.md`)
  - 개선: anti-pattern, hard requirement, recommendation 포맷 강화
- **GPT Loop M3.5 안정화**
  - `rules_soft.py` JSON 파싱 내구성 강화
    - fenced code block/중간 JSON 추출/fallback 처리
    - 비정상 응답 시 `NEEDS_REWRITE` 안전 기본값 적용
  - `rules_hard.py` 체크 확장
    - chorus 반복 섹션 확인
    - 한글 포함 여부 확인
    - vocal baseline marker(raw/direct/solid) 확인
    - exclude mandatory harmony guard 포함 여부 확인
- **SSOT 정책 및 문서 메타 포맷 정합성 정리**
  - `MASTER` 기준으로 SSOT 책임/우선순위/워크플로우 문구 충돌 해소
  - Style Prompt 길이 기준을 `900자 (공백 포함 문자)`로 통일
  - `CLAUDE.md`를 비-SSOT 실행 매뉴얼로 정렬하고 `MANAGER.md` 참조로 통일
  - 문서 헤더 메타(`Version`, `Last Updated`, `Purpose`) 포맷 통일 및 날짜 동기화
- **MASTER/_INDEX.md v1.3 갱신**
  - 비-SSOT 문서 참조에 GPT Sidecar PRD/구현 명세 추가
- **PRD/명세 문서 경로 분리 (MASTER → docs/planning)**
  - SSOT 운영 경계 유지 목적
  - `_INDEX`, `SESSION`, `CHANGELOG` 참조 경로 동기화

### Added
- **PM_0900 "밤산책" 시리즈 패키징 완료**
  - 최종 영상: 64분 (10트랙 x 2회 반복)
  - 왕복 루프 기법 적용 (forward + reverse = seamless 16초)
  - 썸네일: 신카이 스타일 일러스트 (Freepik AI + Veo 3.1)
  - 디스크립션: "서울의 밤을 걷는 뉴트로 시티팝" 브랜딩
  - PM_0400 포맷 정렬 (🎧 Tracklist 헤더, #PM0900 해시태그)

### Changed
- **wavvy.py: WAV 파일 지원 추가**
  - TRACK_PATTERN regex: `.mp3` → `.(?:mp3|wav)`
  - audio_files glob: MP3 + WAV 동시 검색
  - 에러 메시지 업데이트: "No MP3 files" → "No audio files (MP3/WAV)"

### Added
- **PM_0900 "밤산책" 시리즈 전곡 완료 (10/10 tracks)**
  - Track 04 "가로등": City Pop Ballad, 72 BPM, Female Mezzo, PASS
  - Track 08 "창가": Neo-Soul City Pop, 85 BPM, Male Baritone, PASS
  - Track 09 "시야": City Pop Funk, 105 BPM, Male Tenor, PASS (시리즈 피크)
  - Track 10 "방": City Pop R&B Ballad, 65 BPM, Female Alto, PASS
  - 수미상관 구조 완성: "문을 열면 moon" ↔ "No more moon, back in my room"
- **MASTER 문서 성공 패턴 반영 (PM_0900 회고)**
  - ROLES.md v1.9: Controlled Variation Pattern + Clean Slate Protocol
  - STYLE.md v2.7: Genre Mix Pattern 강화 (Spine + Color ≤ 2)
  - CLAUDE.md v2.12: Step 6.5 패턴 고착 검사
  - MANAGER.md v1.4: Phase 1.5 CV Enforcement
  - PLAYLIST_GUIDE.md v1.3: 수미상관 구조 (Bookend Pattern)

### Removed
- PM_0900 Track 04, 07, 08, 09, 10 txt 파일 18개 (concept.md SSOT로 정리)

### Added
- **PM_0900 하이브리드 전략 - Track 07 재설계 + Track 08-10 초안**
  - Track 07 "공원": City Pop Ballad → 80 BPM 신디 중심, City Pop Rubric 88/100 PASS
  - Track 08 "창가": City Pop + Lo-fi 크로스오버 초안 (74점 FAIL, 도시 서사 약함)
  - Track 09 "시야": City Pop + Funk 크로스오버 초안 (91점 PASS)
  - Track 10 "집": City Pop + Ambient 크로스오버 초안 (66점 FAIL, 수미상관 조정 필요)
  - Workflow Rules 추가: txt 먼저 → 컨펌 → concept.md (CLAUDE.md, MANAGER.md)
  - 구버전 txt 파일 18개 정리
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
- **wavvy.py: 타이틀 자동 생성 (SSOT v1.5)**
  - draft_description.txt 상단에 제목 초안 자동 생성
  - concept.md에서 Title Meta 파싱 (Context Mode, Time, GENRE 등)
  - 메타 없으면 트랙 정보에서 자동 추론
- **wavvy.py: shorts 커맨드 v2.0.0**
  - 입력 변경: `loop.mp4` → `shorts.mp4` (8~10초)
  - 짧은 영상을 음악 길이만큼 자동 루프
  - 출력: `output/shorts/short_[TrackName].mp4` (유지)
- **PLAYLIST_GUIDE.md v1.2: Playlist Title Generation Rules (SSOT v1.5)**
  - 타이틀 고정 구조: `[Playlist] [AM/PM HH:MM] soomshuim | {TIME_STATE_PHRASE}, {MODIFIER_PHRASE} {GENRE}`
  - Context Mode 필수 입력 (Settling/Transition/Energizing/Focusing)
  - TIME_STATE_PHRASE Type A/B 교대 규칙
  - GENRE 확장: R&B, Rock, Pop, Jazz 등
- **wavvy.py: pack --repeat 옵션**
  - 플레이리스트 N회 반복 재생 (기본값 2회)
  - description에 회차 구분 없이 단일 타임스탬프 표시
- **wavvy.py: draft_description.txt 자동 생성**
  - 시리즈/컨셉 기반 커스텀 인트로 문단
  - 📌 고정 댓글 섹션 (시간대별 인삿말)
  - Source/Derived 분리 원칙 (concept.md = SSOT)
- **/wavvy 커맨드**: 프로젝트 재개용 컨텍스트 로더

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
  - /wavvy 신규 추가

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
- **wavvy.py: description.txt 우리말 가사 문구 자동 추가**
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
- wavvy.py preview: 각 트랙이 미리보기에 포함되도록 수정
  - 이전: 전체 병합 후 앞 N초 (Track 01만 포함)
  - 이후: 각 트랙 앞 N/트랙수 초씩 잘라서 병합
