# 07:00 러닝 썸네일 조사·제작 — 2026-10-12

## 조회수와 실제 썸네일

Aside CLI의 YouTube 기능으로 `running music 180 BPM` 관련 영상을 조회했다. 아래 조회수는 2026-10-12 시점의 표시값이다. 조회수가 높다는 사실만으로 썸네일 디자인의 효과를 입증할 수는 없다.

| 영상 | 확인 당시 조회수 | 보이는 특징 |
|---|---:|---|
| [Workout Music Source — 180 BPM Running Workout Mix Vol. 2](https://www.youtube.com/watch?v=8z6GKCwHZuE) | 5,067,258 | 오른쪽의 큰 러너와 왼쪽의 매우 큰 `180`; 어두운 배경에 흰 글자. |
| [네이처 레이브 — 180 케이던스 TECHNO #5](https://www.youtube.com/watch?v=39jA8zIBZpQ) | 717,986 | 실제 단체 러닝 사진과 큰 `180 케이던스` 글자. |
| [Hard EDM Workout — Running Music Motivation 180 BPM](https://www.youtube.com/watch?v=1GntgYdEUYU) | 475,397 | 강한 대각선 달리기 자세, 초록 배경, 큰 흰 글자. |
| [Workout Music Source — 180 BPM Running Workout Mix Vol. 9](https://www.youtube.com/watch?v=5TziMYg7UeM) | 337,235 | 달리는 인물을 크게 배치하고 제목을 밝게 표시. |
| [StridePulse — 180 BPM Running Music](https://www.youtube.com/watch?v=yv22TpNNXWI) | 259,763 | 큰 제목과 조명 효과. 젠이 원치 않는 인공적인 표현의 예로만 기록. |

## 젠의 최신 시각 방향

- 시각을 정확히 07:00처럼 표현할 필요는 없다.
- 나이키 러닝 광고처럼 자연스러운 일상 러닝 사진을 쓰되 작가가 찍은 듯한 구도로 만든다. 형광 라임 도형 제안은 이후 젠의 `도형은 없고` 지시로 대체됐다.
- 인공지능 생성 러닝 사진·이전 `RUNNING MUSIC` 글자·밝은 강변 단체 러닝 시안을 젠이 거절했다. 젠이 제공한 야간 러닝 사진은 인물의 움직임·직접 플래시·가까운 카메라 구도의 참고로 삼는다. 원본 픽셀 복사는 금지했다. 완전한 밤 대신 해가 막 뜨는 새벽으로 바꾼다.
- `-taste`는 설치된 Taste 플러그인의 `entry-taste`와 프로젝트 `skills/wavvy-thumbnail/references/taste-adaptation.md`를 적용했다. 웹 전용 동작 규칙 대신 실제 사진, 짧은 글자, 분명한 크기 차이, 휴대폰 크기 확인을 적용했다.
- 젠의 두 번째 참고 사진에서 NRC 글자 구조를 지정했다. 젠이 시간 폰트 패밀리 오류를 지적해 `SERIES/06-00/input/thumb.psd`와 `SERIES/15-00/input/thumb.psd`의 시간 레이어에서 `Pacifico-Regular`를 확인했다. 젠은 한때 현재 시안의 `07:00`을 제거했다가, 다시 Wavvy 로고 오른쪽에 배치하라고 했다. 업로드된 17:00은 건드리지 않았다. NRC 글자는 결과에 쓰지 않았고, 메인 러너 가슴의 Nike 스우시는 젠의 별도 요청으로 새로 생성했다. `Cadance`는 젠의 입력 철자였고 현재 표기는 `Cadence`다. `180 BPM`은 러닝 케이던스 목표값을 나타내며 모든 음원이 정확히 180 BPM으로 측정됐다는 주장은 아니다.
- 추가 참고 사진 `~/Downloads/nike-run-club-app.avif`의 왼쪽 아래 글자 구도를 적용했다. 젠의 최종 수정에 따라 `Cadence`는 작고 얇게 `180 BPM` 왼쪽 위에 정렬하고, `180 BPM`은 매우 두껍게 표시한다. 기존 가로선과 CADENCE의 강제 폭 맞춤은 제거하고, 마지막 `e` 옆에서 헤드라인 `M` 오른쪽 끝까지 1px 선을 넣었다.

## 생성 사진과 현재 시안

- 젠이 제공한 `/Users/zenkim_office/Documents/images.jpeg`(407×491)는 구도·달리기 순간·직접 플래시 참고다. 이를 프로젝트로 복사하고 왼쪽을 확장한 첫 시안은 젠의 `역분석 후 프롬프트로 재생성` 정정에 따라 폐기하고, 프로젝트의 복사본·확장본·합성본을 삭제했다. Documents의 원본은 보존했다.
- 새 `thumb-scene-dawn-2026-10-12.png`(1672×941, SHA-256 `57619ab694ee2f4128db2c9bf7574fc6dbc6353f366bcc94b24d4f2ac1a68df7`)는 참고 사진 픽셀을 입력하지 않고 문장 프롬프트만으로 만든 새벽 장면을 후속 편집한 결과다. 세 명의 러너, 낮은 광각 시점, 직접 플래시, 강변 난간과 붉은 도로를 유지했다. 하늘과 그림자에 은은한 보랏빛을 더했고, 메인 러너는 블랙 러닝복·라임 양말·흰색 바탕에 작은 라임 포인트가 있는 신발을 신었다. 검은 나시의 가슴에는 작은 형광 라임색 Nike 스우시를 넣었다. 메인 러너가 카메라를 살짝 내려다본다. 중간 생성본은 이미지 생성 도구의 저장 위치에 남아 있다.
- 실제 `brand/logo_wavvy.png`를 왼쪽 위 x=65px에 표시 너비 264px로 뒀다. `07:00`은 Pacifico-Regular 58pt로 로고 오른쪽 x=345px, y=120px에 배치했다. 처음 65pt로 만들었으나 젠이 제공한 06:00·11:00 썸네일을 같은 폭으로 비교해 로고 대비 시간 글자의 크기·간격을 줄였다. 왼쪽 아래에는 SF Pro Display Thin 50pt `Cadence`(180×37px, x=65px, y=700px)를, 그 아래에는 Helvetica Neue Condensed Black 155pt `180 BPM`(536×113px, x=65px, y=755px)을 정렬했다. 1px 선은 x=261–600px, y=718px이며 끝 x=600px은 헤드라인의 `M` 오른쪽 끝과 같다. 다른 장식 도형은 없다.
- 젠이 승인한 `thumb.jpg`는 1672×941, SHA-256 `cb623c2811ce2cfe9bf003629516c4e36554fe89f05e6b2eea34e27d1659de30`이다. 전체 크기와 320×180에서 글자·인물·여백을 확인했다.
- 승인한 장면을 Lanczos 방식으로 확대해 영상용 최종 배경 `loop.png`(3840×2160, SHA-256 `75dac23e65f3908a126c5fa19bd01d854ef5ef1767585e23de3139634d346e89`)를 만들고 육안으로 확인했다. 원본 장면은 1672×941이며 원생 4K가 아니다. 첫 강변 생성 초안 `art-draft-2026-10-12.png`는 이력으로 보존한다.
