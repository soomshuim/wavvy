# 시리즈 폴더 경로 이전 — 2026-10-22

젠의 “그리고 폴더 이름이 아직 06-30인데?”라는 지시에 따라 **`SERIES/06-30/` → `SERIES/17-30/`**으로 폴더 전체를 옮겼다. 시리즈 표시 시간은 17:30이다. Suno 작업 공간 이름 `[06:30]`과 곡 ID·제목·순서는 변경하지 않았다.

이동 직전 [984개 파일의 상대 경로·SHA-256 목록](validation/2026-10-22-folder-migration-before.json)을 저장했다(목록 파일 SHA-256 `3e8df01a725312a5c15e3124dd65b5ad381647896b00028ec55f26ea4aff5811`). 이동 직후 이 984개를 새 폴더의 동일 상대 경로에서 다시 읽어 **누락 0·바이트 변경 0**을 확인했다. 이 수에는 Git에서 무시되는 `input/loop.png`, 주방 시안 PNG, 수정 시안 v2, `input/artwork/thumb.psd`와 `.DS_Store`도 포함된다. 이후 문서의 현재 경로를 수정하고 새 이미지 생성 v3를 별도 추가했다.

과거 생성·화면 관찰의 원시 JSON, 텍스트 검사 출력, `input/source-history/` 아카이브에는 당시 `SERIES/06-30/` 경로가 남는다. 해당 값은 **관찰 당시 경로**이며 원시 바이트를 고치지 않았다. 파일을 읽을 때 경로 접두어만 위 대응대로 새 폴더로 해소한다. 현재 `input/...` 상대 경로는 `SERIES/17-30/` 아래에서 해소한다. 현행 문서 링크·현재 후보 JSON의 스크린샷 경로·`.ai/state.json`의 active series·`.gitignore` 이미지 규칙은 새 경로를 사용한다. 상태 파일은 공식 `wavvy.py state --write`로 revision 57을 기록했고 단계 `track_source_draft`와 로컬 오디오 0개를 유지했다.

이동 직후 젠이 “내가 직접 만들었어.”라며 `input/thumb.jpg`를 직접 제작한 이미지로 교체했다. 현재 [사용자 썸네일 기록](artwork/user-thumbnail-2026-10-22.md)의 SHA-256은 `634cbb9ff89b2c39cf89a240100368b310c0e22bfaee60a0463170f25912e025`다. 이동 전 합성본의 SHA-256 `aa875945206a48b7ba5fd24edb562e4544ff0a4673fdf53d3c9cc1b417705b4c`와 다른 것은 **사용자 제작 교체**이며 이동 손실이 아니다. 이전 합성본은 Git 이력에 남는다. `input/loop.png`는 이동 전후 SHA-256 `e27ade02cc17e58bceb7d9fbe6502e1ced62613cded357e59ffe58842dc68ca7`로 같다.

이동 후 젠의 별도 요청에 따라 미사용 썸네일 작업물 15개를 [삭제 목록](validation/2026-10-22-unused-thumbnail-deletion.json)에 상대 경로·크기·SHA로 기록하고 정확한 파일만 삭제했다. 이 삭제는 폴더 이동 시점의 984개 무결성 확인과 별개다. 사용자 `thumb.jpg`, 편집 원본 가능성이 있는 `artwork/thumb.psd`, 영상 배경 `loop.png`, 음악 원문·과거 생성 근거는 보존한다.
