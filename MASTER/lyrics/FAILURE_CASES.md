# Lyrics Failure Case Archive

Version: 1.0
Last Updated: 2026-03-03
Purpose: 가사 작성 시 대표적인 실패 유형 아카이브

> SSOT는 `LYRICS.md`. 이 파일은 예시/참고용.

---

## Case 01: Metric 붕괴
- Verse 2에서 음절 수 증가/감소
- 결과: 멜로디 붕괴, AI 즉흥 변주 발생

## Case 02: Ending 불일치
- V1은 명사, V2는 의문문
- 결과: 후반 멜로디가 다른 곡처럼 들림

## Case 03: Bridge 설명조
- "~한 마음", "~한 감정"
- 결과: AI 특유의 내레이션 톤 발생

## Case 04: Meta Instruction Hallucination
- `(Scene: Wet breath)` 같은 문구 삽입
- 결과: 보컬이 이를 가사처럼 읽어버림

## Case 05: Vocabulary Overlap
- Track 03 제목이 "잔향"인데 Track 04에서 "잔향만 맴돌아" 사용
- 결과: 알고리즘이 "같은 곡 반복"으로 오인

## Case 06: Descriptive Hook
- "물안개 속에서 / 혼자 걷는 이 밤" (상황 설명)
- 결과: 훅 인지 속도 저하, 중독성 부족

## Case 07: Person-Dependent Thesis
- Bridge Thesis가 "너의 낮은 목소리"
- 결과: 트랙 간 테제 겹침, AI 과잉 해석

## Case 08: Flat V2
- V1과 V2 마지막 2행이 감정 강도 동일
- 결과: 곡 전체가 평탄하게 느껴짐

## Case 09: Abstract Word Density
- 4행 전체가 추상어(윤곽/경계/흐려/지워/사라져)로만 구성
- 결과: 이미지가 안 잡힘, "AI스러운 문장"

## Case 10: Ending 품사 불일치
- V1 "서 있어"(동사) vs V2 "차가워"(형용사)
- 결과: 멜로디 끝 처리가 다르게 재현됨

## Case 11: V1-V2 행 수 불일치
- V1은 4행인데 V2를 6행으로 시도
- 결과: Suno가 멜로디 억지로 얹으려다 붕괴 100%
- **교훈: "다른 컨셉"은 행 수가 아니라 단어 선택으로**

## Case 12: Chorus 과다 행
- Chorus를 6행으로 작성 (규칙: 3~4행)
- 결과: 훅이 너무 길어 리스너 피로감
- **교훈: Chorus는 무조건 3~4행**

## Case 13: Bridge Thesis 변경 + 키워드 충돌
- Bridge2 Thesis를 B1과 다르게 변경
- "윤곽"은 Track 02 제목 → Vocabulary Independence 위반
- **교훈: Bridge Thesis는 B1=B2 동일**
