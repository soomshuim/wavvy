# 승인된 Rubber Band 시간맵 제작

기존 atempo 실패 자료는 보존하며 새 경로는 Rubber Band4.0.0 CLI의 R3 offline engine이다. 일반 Homebrew 설치를 완료했다. 설치 로그와 `--full-help`는 `work/mix-170-20261026/`에 보존한다.

근거: [공식 CLI 도움말](https://www.breakfastquay.com/rubberband/usage.txt), [공식 API setKeyFrameMap/setExpectedInputDuration](https://www.breakfastquay.com/rubberband/code-doc/classRubberBand_1_1RubberBandStretcher.html). `--timemap`은 내부 입력→출력 sample frame 쌍이며, 전체 출력 길이는 별도 `--duration`으로 정한다. offline은 전체 입력 길이를 알고 처리한다. `-p0`으로 피치 변경을 지정하지 않는다. 피치 보존의 실제 근거는 대응 음역의 스펙트럼 검사로 별도 확인한다.

- 기존 독립 mid/high tempo로 가이드한 quarter path를 재사용한다. 몸체의 quarter를 누적170표본격자 `round(k*288000/17)`에 대응시킨다. sparse 도입과끝은 가장가까운본체16박평균속도로보간한다. 모든 순간에 audible beat가 있다는 뜻은 아니다.
- implicit원점0과 전체 source길이→정확한총출력길이를 사용한다. 양수인 내부 keyframe만map파일에쓴다. source0부터자연끝모든입력을CLI에전달한다. 파일sample수·처음/끝경계대응·예측에너지전개로보존을확인한다. 입력0→출력0의명시쌍을넣지않는이유는R3의0/0관련보고를피하고원점을implicit하게두기위함이다.
- 작은시험은 Goodbye본체60~100초, Warm Pixels후반150~190초, Dancing Tears140~180초다. 8ms 원파형이변환뒤그대로남는다는atempo검사는적용하지않는다.
- 변환에맞는검사: 정확출력sample수·finite/stereo/48k, 대응구간중고역onset에너지시간정렬, 독립출력mid/high반복주기, 대응주파수피크/스펙트럼이동검사. BeatThis추가검사는170/85family를분리하며170에맞추기위해모델half를강제해석하지않는다.
- 3시험통과후전곡20개를같은경로로제작하고독립출력검사를남긴다. 40진입/39연결은source전체를약1마디만겹치며첫시작/마지막끝을보존한다. 기존원본/분석/순서는변경하지않는다.
- 최종음량-14LUFS목표, AAC후≤-1.0dBTP를위해PCMceiling-1.5dBTP를둔다. 동일최종PCM을분기해WAV24/48kstereo와AAC-LC320k를한번인코딩한다. 실제최종값을검사한다.
- 기술검사만수행하며직접청음승인은없다. 공용180하네스/영상/source-final상태는사용하지않는다. 새방식에서반복문제발생시멈추고근거를보고한다.
