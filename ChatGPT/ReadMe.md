# ChatGPT를 사용한 TRPG

## 00. ChatGPT사용시 필요한 대화
- "규칙 리스트"
- "세션 줄거리"
- "퀘스트 설계 정의에 의해서 만들어봐. 실패/대실패에 의한 서사추가는 인과관계가 명확해야해 ,적대적 크리쳐는 monster core에서 발췌하고 변형이나 난이도 조정이 필요하면 따로 컨셉과 레벨만 표시해놔. 마크다운 문서로 작성해서 다운로드 링크까지 제공해야해. 참여 파티는 9레벨 3인파티야."
- "이번 인카운터는 Book of the Dead 몬스터로 XP Budget 기준 Moderate로 구성해줘.
우리 파티는 8레벨 3인 파티고, 테마는 오염된 숲이야.
몬스터는 Book of the Dead PDF 내 'CREATURE [숫자]' 표기를 기준으로 레벨 판단해서 찾아줘."

## Markdown문서와 Json문서의 msearch차이
- 마크다운 문서는 인용구나 볼드처리 같은 스타일이 들어가 있으면 파싱에 위협을 줌
- 아무리 세션단위로 나뉘어도 문장자체가 길어져버리면 chunk구성에 실패함
- 효과적인 구성은 json이며, 아래에서 더 자세히 다룬다.

## ChatGPT가 읽기 쉬운 Json문서 방침
- flat구조의 key list: deep구조로 해봐야 이해하지 않는다. 문장구조 및 keyword로 파악하기 때문
- 검색용 key값을 정의해 두는게 좋다. 여러 조건을 복합적으로 찾을 때, slug형식으로 "search_blob"이란 key에 값을 연결해 놓으면 용이하다.
- NDjson(Newline Delimited JSON) format이 객체별로 개행문자로 구별되어 용량 및 구분시 편리하지만 format자체가 지원안함
- NDjson으로 생성후 개행문자를 `"\n,"`로 변경하여 일반 json으로 만드는게 도움이 된다.

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
