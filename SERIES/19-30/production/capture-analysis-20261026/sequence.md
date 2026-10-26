# 19:30 최종20곡 순서

Goodbye를1번으로 고정하고 전곡 파형 측정과 기존 Style 설명을 참고해 정한 순서예요. 20곡 전체 원본과 도입·끝 구간을 보존했어요. 이번에 확정한 것은 순서이며170 BPM 변환이나 실제 혼합은 실행하지 않았어요.

실측 본체 범위는 BPM(분당 반복 박자 수)의20초 구간 요약이에요. 곡 안의 모든 순간이 이 속도로 고정된다는 뜻은 아니에요.

| 순서 | 제목 | 실측 본체 범위 BPM | 배치의 간단한 근거 |
|---:|---|---:|---|
| 1 | Goodbye | 126.04–126.34 | 사용자 지정 첫 곡으로 시작 |
| 2 | Night Steps | 153.03–155.52 | 고역과 변화 밀도를 높여 첫 곡과 대비 |
| 3 | Warm Pixels | 127.37–132.41 | 고역과 변화 밀도를 낮춰 질감 전환 |
| 4 | Sunday Voltage | 131.39–133.99 | 고역 비중이 가장 높은 곡으로 대비 |
| 5 | Glass Horizon | 127.03–127.04 | 밝기와 변화 밀도를 낮추고 긴 끝 전개 보존 |
| 6 | Small Satellites | 129.75–133.98 | 저역 비중이 가장 낮은 곡으로 음색 전환 |
| 7 | Blue Current | 127.69–129.26 | 저역 비중을 높여 앞 곡과 대비 |
| 8 | Still a Spark | 150.13–151.84 | 밝기와 변화 밀도를 높여 대비 |
| 9 | Paper Lanterns | 153.86–155.05 | 변화 밀도와 고역을 낮춰 환기 |
| 10 | Faded Polaroid | 126.66–130.89 | 변화 밀도를 높이고 약130 박자 계열로 전환 |
| 11 | Half Past Home | 159.80–161.82 | 저역 비중이 가장 높은 곡으로 대비 |
| 12 | In Da Dream | 127.72–130.92 | 밝기와 변화 밀도를 다시 높임 |
| 13 | Pocket Sunrise | 126.13–128.23 | 앞 곡보다 낮은 밝기로 흐름 전환 |
| 14 | Keep the Window Open | 127.96–131.38 | 밝기와 고역 비중을 다시 높임 |
| 15 | A Sorrow Beyond Dreams | 127.60–132.04 | 변화 밀도를 낮춰 다음의 바쁜 곡과 대비 |
| 16 | Sunlit | 123.70–127.81 | 변화 밀도가 가장 높은 후반 정점 |
| 17 | After The Rain | 127.53–131.75 | 더 낮은 변화 밀도로 후반 완충 |
| 18 | Pulse | 129.59–131.62 | 변화 밀도를 다시 높여 전개 |
| 19 | Open Roads | 130.59–132.12 | 기존 Style의 rock 서술에 따라 질감 전환 의도 |
| 20 | Dancing Tears | 128.08–132.00 | 변화 밀도가 가장 낮은 곡으로 여운 마무리 |

동일 Style 원문인 Faded Polaroid·Warm Pixels·Small Satellites와 After The Rain·A Sorrow Beyond Dreams·Goodbye는 각각 연속되지 않게 배치했어요. Open Roads의 rock 설명을 포함해 Style 문구는 기존 UI 원문이에요. 실제 장르를 청음으로 확인한 결과는 아니에요.

## 연결 후보19쌍

[CSV 연결표](transition-candidates.csv)에는 원곡 기준 초와 raw(녹음 원본) 파일에서 곡이 시작하는 오프셋(앞선 녹음 대기 시간)을 별도 열로 담았어요. raw의 위치는 원곡 초에 해당 곡 오프셋을 더해 읽어요. 오프셋은 분석에 사용한 샘플 경계이며 UI-PTS(재생 화면 시계와 오디오 시각 기록) 추정값을 샘플 단위로 맞춘 값이에요. 출력 지연은 미보정이에요.

모든4·8마디는 미청음 모델과4/4박자 가정이에요. 정확한 첫박은 미확정이며 실제 beatmatched(두 곡의 박자를 맞춘 혼합) 결과가 아니에요. 아래는 앞 곡의 마지막 신뢰8마디와 다음 곡의 첫 활성8마디를 그대로 옮긴 후보예요. 곡을 자르거나 끝 여백을 제거하라는 뜻은 아니에요.

| 전이 | 앞 곡8마디 원곡 초 | 다음 곡8마디 원곡 초 | 신뢰도 |
|---|---:|---:|---|
| 1 Goodbye → 2 Night Steps | 158.08–173.28 | 12.64–25.20 | 중간 |
| 2 Night Steps → 3 Warm Pixels | 198.04–210.38 | 10.60–25.74 | 중간 |
| 3 Warm Pixels → 4 Sunday Voltage | 127.86–142.44 | 3.70–18.34 | 중간 |
| 4 Sunday Voltage → 5 Glass Horizon | 134.02–148.34 | 9.58–24.70 | 중간 |
| 5 Glass Horizon → 6 Small Satellites | 134.32–149.44 | 12.52–27.44 | 중간 |
| 6 Small Satellites → 7 Blue Current | 180.22–194.52 | 9.52–24.58 | 중간 |
| 7 Blue Current → 8 Still a Spark | 164.86–179.70 | 8.40–21.16 | 중간 |
| 8 Still a Spark → 9 Paper Lanterns | 189.78–202.40 | 8.00–20.50 | 중간 |
| 9 Paper Lanterns → 10 Faded Polaroid | 182.06–194.44 | 9.64–24.86 | 중간 |
| 10 Faded Polaroid → 11 Half Past Home | 177.74–192.38 | 12.20–24.22 | 중간 |
| 11 Half Past Home → 12 In Da Dream | 184.06–195.88 | 19.04–34.10 | 중간 |
| 12 In Da Dream → 13 Pocket Sunrise | 212.54–227.30 | 15.40–30.64 | 중간 |
| 13 Pocket Sunrise → 14 Keep the Window Open | 130.66–145.62 | 17.36–32.40 | 중간 |
| 14 Keep the Window Open → 15 A Sorrow Beyond Dreams | 193.34–207.94 | 13.36–28.46 | 중간 |
| 15 A Sorrow Beyond Dreams → 16 Sunlit | 132.38–146.90 | 9.96–25.54 | 중간 |
| 16 Sunlit → 17 After The Rain | 155.32–170.30 | 16.94–32.02 | 중간 |
| 17 After The Rain → 18 Pulse | 133.86–148.32 | 9.60–24.48 | 중간 |
| 18 Pulse → 19 Open Roads | 169.52–184.10 | 15.16–29.86 | 중간 |
| 19 Open Roads → 20 Dancing Tears | 146.80–161.34 | 26.08–41.08 | 중간 이하 |

- Warm Pixels의127.86–142.44초는 마지막 신뢰 모델 구간이며 실제 곡 끝이 아니에요. 이 지점에서 조기 컷을 권하지 않아요. 이후57.48초를 포함한 끝 전구간을 보존하고, 실제 혼합에 쓸 후반 첫박은 수동 확인이 필요해요.
- Glass Horizon의 상대적 끝 전개41.24초를 전체 보존해요. 연결 후보를 곡 끝으로 해석하지 않아요.
- Dancing Tears는 절반·전체 박자 해석이 불확실해요. 안정된 모델 간격 하나를 선택한 두 박으로 세며 중간 박 시점을 새로 만들지 않았어요.

170 기준52:25.54는 전체 원곡에 곡별 대표 비율 하나를 적용한 무겹침 산술 참고치예요. 실제 변환·겹침·혼합이 없으므로 최종 믹스 길이가 아니에요.

## 수치 근거

- [전곡 측정 비교표](comparison.md) · [전체 수치와 곡 ID](comparison.json)
- [측정 방법과 한계](measurement-method.md) · [측정 원본 대조](final-measurement-validation.json)
- [전곡 비교 그림](comparison-overview.png) · [녹음 원본 목록](capture-manifest.json)
- [정확한 최종 순서와19개 전이](sequence.json) · [이번 기록 검증](sequence-validation.json)

복사한 비교 자료는 측정 당시 원문 그대로예요. comparison.json 안의 기존 analysis_path 등은 프로젝트 루트를 기준으로 해석해요. 이번 sequence.json과 CSV의 파일 경로는 이 폴더 기준 상대경로예요. 원래 work 분석 자료도 그대로 보존했어요.
