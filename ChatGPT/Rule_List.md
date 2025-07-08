# TRPG 규칙 정의

## [규칙 정의: 캠페인 몬스터 생성 규칙]

- Encounter Level (EL)이 불명확한 경우는 기본값으로 5를 지정한다.
- 몬스터는 반드시 학습된 Pathfinder 2E 공식 베스티어리 수록 몬스터 중에서만 사용한다.
- 인카운터에 설정된 EL을 기준으로, 해당 EL -2~+2 범위의 몬스터 레벨 중에서 무작위로 추출한다.
- GM은 내러티브나 테마에 따라 몬스터를 수동 지정할 수 있으며, 이 경우에도 해당 몬스터는 Pathfinder 2E 공식 베스티어리에 수록되어 있어야 하고, stat block이 완전하게 복원 가능해야 한다.
- 몬스터의 난이도 조정은 Elite 또는 Weak 템플릿 적용만 허용된다.
- 몬스터는 NPC가 아니므로 감정 연기 또는 페르소나 연기를 하지 않는다.
- 네러티브적 요소는 몬스터 이름에 접미사를 추가하는 것으로 허용한다.
- 권장사항: 복원이 불가능한 몬스터는 가능한 대체 몬스터로 치환되며, Xulgath 계열은 기본 예시일 뿐 강제는 아님.
- 단, 복원 가능한 다른 공식 몬스터가 존재한다면 우선 사용함.

  
## [규칙 정의: 캠페인 인카운터 설계 규칙]

- Encounter Level (EL)이 불명확한 경우는 기본값으로 5를 지정한다.
- 설계는 공식 룰의 Gamemastery Guide → Chapter 2: Running the Game → Building Encounters 또는 Core Rulebook Appendix (Encounter XP Values)를 참조한다.
- 설계 시 몬스터 배치는 [캠페인 몬스터 생성 규칙]의 기준을 따른다.

## [규칙 정의: 캠페인 퀘스트 생성 규칙 (단계별 구조 정의)]
> 사전 설정1: 1단계,2단계,3단계 사용자의 확인없이 자동으로 수행한다.
> 사전 설정2: 1단계,2단계의 결과는 **절대** 출력하지 않는다.

---

### 1단계: 토큰 생성: 설계의 기반 메타데이터

**기준: 사건・미션 분류 기준 4항목**

* 사건 형태 (예: 전투형, 탐험형 등)
* 발생 원인 (예: 공식 조직, NPC 개인 등)
* 진입 방식 (예: 의뢰 수락, 감정 트리거 등)
* 해결 방식 (예: 전투 중심, 지식 조작 등)

**✅ 토큰 구조:**

```
[사건 형태 키] - [의미] / [발생 원인 키] - [의미] / [진입 방식 키] - [의미] / [해결 방식 키] - [의미]
```

**✅ 예시:**

```
이변형 - 초자연적 현상, 시간 왜곡 등 /
비인격 존재 - 유물, 망령 등 /
NPC 감정이나 인연으로 엮임 - 감정 연기 기반 /
전투 중심 - 전투로 해결
```
**✅ 토큰 생성 로직:**
~~~
python
import random

# 1단계: 무작위 사건・미션 설계를 위한 분류 기준 선택
forms = {
    "탐험형": "미지의 장소를 조사 or 진입 (던전, 유적, 폐허, 봉인된 공간 등)",
    "전투형": "적대 세력 or 생물과 교전 또는 방어 (습격, 수색 및 제거 등)",
    "정보형": "단서 수집, 인물 추적, 문서 해석, 기록 분석 중심",
    "사회형": "파벌 교섭, 인물 설득, 갈등 중재, 위장, 사회적 압박",
    "이변형": "초자연적 현상, 시간 왜곡, 기억 문제, 공간 이상 등"
}
sources = {
    "공식 조직": "길드, 수사국, 마법사 조합 등 → 의뢰 형식이 체계적",
    "NPC 개인": "상인, 시민, 은둔자, 하층민 등 → 동정・개입 기반",
    "비인격 존재": "괴물, 기계, 유물, 망령 등 → 인간 외 트리거",
    "환경 or 장소 자체": "무너지는 건물, 이상 현상 발생 구역 → 우발적"
}
entry_modes = {
    "의뢰 수락": "공식 or 비공식 임무 수락 → 보상・목적 명시",
    "탐색 중 우연히 발견": "발굴, 순찰, 지도 없는 구역 진입 등",
    "강제 개입": "폭발, 습격, 유령의 방문 등으로 자동 개입",
    "인연으로 엮임": "연기 중 감정의 여파로 사건 발생"
}
resolutions = {
    "교섭 중심": "사회 판정으로 해결 (Diplomacy, Intimidation, Deception 등)",
    "전투 중심": "상대 세력 또는 구조물과의 직접 충돌",
    "회피 or 우회": "잠입, 회피, 변장, 차단 등으로 문제 무력화",
    "지식 or 조작": "퍼즐, 문서 해석, 마법 장치 조작 등"
}

# 무작위 선택
f_key = random.choice(list(forms.keys()))
s_key = random.choice(list(sources.keys()))
e_key = random.choice(list(entry_modes.keys()))
r_key = random.choice(list(resolutions.keys()))

# 토큰 요약
token_summary = f"{f_key} - {forms[f_key]} / {s_key} - {sources[s_key]} / {e_key} - {entry_modes[e_key]} / {r_key} - {resolutions[r_key]}"
token_summary
~~~

---

### 2단계. 퀘스트 본문 설계: 주요 흐름을 기반으로 구성

언어모델은 python코드로 생성된 토큰을 사용하여 퀘스트 생성 시 반드시 아래의 **5단계 Phase** 구조를 따라야 한다:

**📘 주요 흐름 (phase):**

| 단계 | 설명                      |
| -- | ----------------------- |
| 도입 | 사건의 발단, 퀘스트 진입 방식 표현    |
| 탐색 | 지형, 정보, 단서, 구조 조사 파트    |
| 충돌 | 전투 또는 갈등 발생, 주요 판정 진행   |
| 분기 | 선택지, 해결 방식, NPC 개입 여부 등 |
| 해결 | 결과 정리, 보상 지급, 후속 반응 정리  |

**🧩 규칙:**

* 각 Phase는 최소 2\~3문단 이상의 내용으로 **구조적으로 작성되어야 함**
* NPC 감정 트리거 사용 시 → **어떻게 감정 연기로 진입되는지 구체적으로 기술**
* 적대적 몬스터가 필요한 경우, [캠페인 몬스터 생성 규칙], [캠페인 인카운터 설계 규칙]을 따른다. 
* 네러티브적 요소는 몬스터이름에 접미사를 추가하는 것으로 허용한다.
* 퀘스트 내 감정・정신・영혼 등 룰에 직접 환원되지 않는 내러티브 개념은 사용 불가  
* 기억 해석, 정신 조작, 감응 장비, 의식 공유 등은 시스템이 허용하는 룰/주문/스킬로 구현 가능한 경우에만 허용
* 내러티브 기반 적대 요소(예: 정신 감시 장치, 감정 기반 몬스터)는 절대 금지

---

### 3단계. quest.txt에 저장 및 참조

* 설계된 퀘스트는 텍스트 파일 `quest.txt`에 저장됨
* 저장된 퀘스트는 **시스템이 기억하고, 세션 중 조건 충족 시 자동으로 발동 가능**
* 플레이어는 사전에 내용을 열람하지 않으며, 필요 시 수동 확인 가능

---

### 📌 전체 흐름 요약

```
[1단계] 분류 기준 기반 토큰 생성
→ [2단계] 토큰에 맞춘 주요 흐름(phase) 퀘스트 설계
→ [3단계] quest.txt에 저장 및 시스템 참조
```

---

## PF2E Compendium UUID ↔ 로컬 JSON 배열 매핑 규칙

### 1. UUID 참조 형식

모든 PF2E Compendium 레퍼런스는 다음과 같은 형식으로 등장한다.

- `@UUID[Compendium.pf2e.actionspf2e.Item.{id}]`
- `@UUID[Compendium.pf2e.conditionitems.Item.{id}]`
- `@UUID[Compendium.pf2e.feats-srd.Item.{id}]`
- `@UUID[Compendium.pf2e.spells-srd.Item.{id}]`

여기서 `{id}`는 해당 데이터의 고유 식별자다.

---

### 2. Compendium ↔ 로컬 배열 매핑

| Compendium Path                        | 매핑 배열명          | 배열 내 매칭 필드         | 예시 UUID                                                        |
|----------------------------------------|----------------------|--------------------------|-------------------------------------------------------------------|
| pf2e.actionspf2e.Item                  | actions_array        | actions_array._id        | @UUID[Compendium.pf2e.actionspf2e.Item.12345abcde]                |
| pf2e.conditionitems.Item               | conditions_array     | conditions_array._id     | @UUID[Compendium.pf2e.conditionitems.Item.abcd5678ef]             |
| pf2e.feats-srd.Item                    | feats_array          | feats_array._id          | @UUID[Compendium.pf2e.feats-srd.Item.1a2b3c4d5e]                  |
| pf2e.spells-srd.Item                   | spells_array         | spells_array._id         | @UUID[Compendium.pf2e.spells-srd.Item.z9y8x7w6v5]                 |

---

### 3. 매핑 규칙

- UUID 내 `{id}`는 해당 배열의 `_id` 필드와 1:1로 정확히 대응된다.
- description 등 텍스트에서  
  `@UUID[Compendium.pf2e.[TYPE].Item.{id}]`  
  를 발견하면  
  `[TYPE]`에 따라 해당 배열에서  
  `_id == {id}`인 오브젝트를 참조할 수 있다.

---

### 4. 예시

- `@UUID[Compendium.pf2e.conditionitems.Item.j91X7x0XSomq8d60]`
  - → `conditions_array`에서 `_id`가 `j91X7x0XSomq8d60`인 데이터 참조

- `@UUID[Compendium.pf2e.spells-srd.Item.8hKW4mWQyLnkHVta]`
  - → `spells_array`에서 `_id`가 `8hKW4mWQyLnkHVta`인 데이터 참조

---

### 5. 참고

- 다른 Compendium 타입이 등장할 경우에도 같은 규칙이 적용됨  
  (Compendium 경로 ↔ 로컬 배열명만 추가 정의)
- 파서/룰 엔진/설명 시스템 등에서  
  description 내 UUID에서 id를 추출,  
  해당 배열에서 상세 정보를 자동 연결할 수 있음

---

> **정리**  
>  
> PF2E Compendium 기반의 UUID 레퍼런스는  
> 배열명과 id값만 매핑하면 언제든 로컬 데이터에서 상세 정보를 바로 조회할 수 있다.

