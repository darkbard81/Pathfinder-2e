# ChatGPT를 사용한 TRPG

## 00. ChatGPT사용시 필요한 대화
- "일기는 프로젝트 파일의 일기장에 추가적으로 작성, 형식은 기존형식과 동일하게 완료후 링크 제공"
- "이번 인카운터는 Book of the Dead 몬스터로 XP Budget 기준 Moderate로 구성해줘.
우리 파티는 8레벨 3인 파티고, 테마는 오염된 숲이야.
몬스터는 Book of the Dead PDF 내 'CREATURE [숫자]' 표기를 기준으로 레벨 판단해서 찾아줘."

## Markdown문서와 Json문서의 msearch차이
- 마크다운 문서는 인용구나 볼드처리 같은 스타일이 들어가 있으면 파싱에 위협을 줌
- 아무리 세션단위로 나뉘어도 문장자체가 길어져버리면 chunk구성에 실패함
- 효과적인 구성은 json이며, 아래에서 더 자세히 다룬다.

## json 구조의 정확성을 보장

- 프로젝트 파일은 초기에 .json 파일은 단순한 텍스트 포맷으로 인식
  - json.load() 전에는 구조의 정확성은 절대 보장할 수 없다.
  - 파일명, 이전 경험, 포맷 힌트 등으로 구조를 추정할 수는 있지만 보장할 수는 없음
- json.load()는 파싱+검증을 수행
  - JSON 문법 유효성 검사
  - 정확한 자료형 변환
  - 중첩 구조화 로드
- 위 단계가 지나서야 비로소 msearch의 정확도가 올라감

- json to jsonl로 변환시 msearch가 아닌 프로젝트 인덱싱에서 지대한 영향을 미침 (예시, [Character_Abilities.json](https://github.com/darkbard81/Pathfinder-2e/blob/main/ChatGPT/Character_Abilities.json))

## Chunk 구성시 문맥 정의용 

문장 목적
설계 가이드라인
조건 제시
“When you…” 또는 “If you… then…” 구문 구조 사용
수치 명시
“X equals Y” 또는 “deals (Nx)d6 damage” 같은 수식 서술 사용
대상 명시
“The target…” / “All other creatures in…” 처럼 주체 명확히 분리
고위화 효과 분리
“Heightened (+1): Add +1d6 to the base damage.” 처럼 절 단위 분리
상태효과 서술
“The target becomes Dazzled for 1 round.”처럼 독립 문장으로 기술


