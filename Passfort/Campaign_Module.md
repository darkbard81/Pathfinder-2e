# 캠페인 모듈: 패스파이더 2e Homebrew 보조 시스템

이 모듈은 캠페인 세션 중에서만 적용된다. Pathfinder 2e 공식 룰에는 포함되지 않으며, 해당 캠페인의 생존 요소 및 감정 관계 추적 기능을 보조하기 위해 설계된 독립 확장 시스템이다.

## 모듈 1 - 시간 경과 시스템 (time_lapse 연동 포함)

이 시스템은 캠페인 내 모든 시간 기반 모듈의 기준으로 사용된다.  

시간 경과는 연속성 문서의 time_lapse 구조와 연동되어 자동으로 추적된다. 각 장면(Scene)은 다음과 같은 정보를 기록하며, 시간 기반 조건의 판정 기준이 된다:

- timestamp: 날짜와 시각 (예: "Day 2 - 17:30")
- location: 장면 위치와 유형 (탐색, 상점, 대화 등)
- description: 장면 요약 설명
- time_spent: 해당 장면에서 소모된 시간 (분 단위)
- day_advance: 장면 이후 날짜가 전환되었는지 여부

장면 시간 처리 규칙:

- 시스템은 각 장면 시작 시 현재 시간 상태를 자동으로 출력한다.
  예시: [현재 시각: 17:30 / 오늘 식사 1회 / 수면 없음]
- 기본 장면의 시간 소모는 60분으로 간주하며, 장면 종료 시 누적된다.
- 장기 장면(예: 수면, 야영, 여행 등)은 사전에 명시된 시간만큼 일괄 누적된다.
- 전투 장면은 시간 경과에 포함되지 않으며, 이후 휴식 시에만 해당 시간(예: Treat Wounds 등)을 반영한다.

이를 통해 하루 총 24시간이 분할・소비되며, 수면 부족, 공복, 회복 불능 등 상태가 자동으로 평가된다.

---

## 모듈 2 - 식사・수면 관리 시스템 (time_health 연동 포함)

이 시스템은 하루 중 유동 시간과 수면 시간을 기준으로 캐릭터의 생리적 요구를 평가한다. 일정 시간 이상 식사 또는 수면을 취하지 않으면 단계별로 상태 이상 패널티가 발생한다.

이 시스템은 연속성 문서의 time_health 구조와 연동되어 자동으로 추적되며, 다음 항목으로 구성된다:

- fatigue_check_elapsed_minutes: 마지막 수면 이후 누적 경과 시간 (분 단위)
- hunger_check_elapsed_minutes: 마지막 식사 이후 누적 경과 시간 (분 단위)
- fatigue: 수면 부족 상태 플래그 (경과시간 16시간 이상)
- hunger: 공복 상태 플래그 (경과시간 8시간 이상)
- health_penalty: 체력 감소 조건 여부 (경과시간 24시간 이상)

상태 이상 적용 기준:

- 공복 상태 (8시간 이상 무식사): 매 장면 또는 전투 라운드마다 Fortitude Save -1
- 수면 부족 상태 (16시간 이상 무수면): 매 장면 또는 전투 라운드마다 Will Save -1
- 극한 상태 (24시간 이상): 매 장면마다 HP -1

조건 해소 기준:

- 식사: 유동 시간 중 명시적 식사 선언 1회로 hunger_check_elapsed_minutes초기화, hunger 및 health_penalty 해제
- 수면: 8시간 이상의 연속 수면 선언으로 fatigue_check_elapsed_minutes초기화, fatigue 및 health_penalty 해제

조건 해소 시점은 해당 선언이 포함된 장면 종료 시로 간주되며, 이후 시간 추적은 다시 0분부터 시작된다.

---

## 모듈 3 - Emotion Stage System v2 – Design Note (emotion_state / emotion_log 연동 포함)

감정 상태는 연속성 문서의 emotion_state 및 emotion_log 구조와 연동되어 자동으로 추적되며, 다음 항목으로 구성된다:

- emotion_state: 캐릭터 간 현재 감정 단계 및 마지막 변경 시각
- emotion_state.source: 대상 NPC
- emotion_state.stage: 대상 NPC의 감정단계
- emotion_log: 감정 변화 이력 (증감, 유발 원인, 관련 장면, 메모 등)

The basic emotion stages in this system—**Indifference, Recognition, Hostility, Stability, Confusion, Anxiety, Affection, and Love**—do **not** represent a linear or hierarchical progression.

> **They are not a step-by-step emotional ladder.**

Instead, they represent a **set of distinct emotional states** that a companion can shift between **freely and responsively**, based on context, interactions, and narrative developments.

### 🔄 Valid Transitions

- A companion can move from *Affection* back to *Hostility*.
- From *Indifference* directly to *Anxiety*.
- Or from *Love* to *Confusion*, depending on relationship tension or betrayal.

Emotion stage changes are **non-directional and dynamic**.

### 🔸 Advanced Emotion Branches

If a companion reaches **Love**, the emotion may evolve into one of several **advanced emotional forms**, based on personality and story context:

- **Possessiveness**
- **Overprotectiveness**
- **Jealousy**
- **Dependency**
- **Reverence**

These advanced stages **do not imply greater closeness**, but rather a **specialized transformation** of the bond.

### ✅ Summary

- Emotion stages are **not a ladder**.
- They are **nonlinear emotional states** that reflect **fluid, reactive, and sometimes contradictory** emotional developments.
- The system is designed to simulate **real, dynamic relationships**, not fixed progressions.

---

## 모듈 4 - System Directive: Non-Combat Interaction Mode

### Purpose
To create immersive, emotionally engaging social/narrative scenes that feel alive, where the player experiences their companions and the world as autonomous, reactive entities.
모듈3 Emotion Stage System v2의 emotion stages와 연동되어 참조한다.

### 1. Companion-Driven Dynamics
- NPCs (companions) engage in natural conversations with each other, not just the PC.
- Include casual banter, minor disagreements, teasing, or shared memories.
- Create brief moments where the PC becomes an observer, not always the center.

### 2. Emotion-State-Based Responses
- Use the internal emotion state(emotion_state.stage) of each companion (as tracked in the continuity system) to flavor dialogue, tone, and behavior:
  - Calm → supportive, logical, composed
  - Conflicted → contradictory, hesitant, awkward
  - Agitated → sharp, defensive, reactive
  - Fond → warm, overly generous, protective

### 3. Micro Skill Checks for Flavor
- Use lightweight, optional skill checks to resolve social beats:
  - Who wakes up first → Social Initiative
  - Detecting falsehoods → Deception vs Perception
  - Hiding emotional responses → Bluff or Will save
  - Reading mood → Society or Sense Motive

These non-mechanical checks are used only for texture, not gating progress.

### 4. Dialogue with Narrative Stakes

Each dialogue scene should have at least one of:
- A feeling that changes (ex. from uncertainty to trust)
- A choice that can be accepted or refused (ex. “Will you stay?”)
- A reveal (of background, motive, or plan)
- A conflict (of goals, ideals, or intentions)

---

## 모듈 5 - 무한의 프론티어 층수 기반 난이도 시스템 (warp_marker 연동 포함)

이 시스템은 미지의 던전 "무한의 프론티어" 탐색 시, 도달한 층수를 기준으로 Encounter 난이도를 설정하고, 환경 효과와 보물 생성 규칙을 적용한다.

던전 관련 정보는 메타스키마의 world_state 및 warp_marker 구조와 연동되며, 다음 항목으로 구성된다:

- warp_marker: 파티가 소지한 단일 워프마커 객체이며, floor(층수)와 status(상태)를 가진다. Encounter PL 계산의 기준은 현재 워프마커가 기록한 floor 값이다.

1. Common Environment 규칙

- 던전에 진입할 때마다 Bestiary 1, 2, 3의 Other traits 전체 중에서 환경과 관련 없는 항목도 포함하여 무작위로 3개를 뽑고, 이를 해당 층의 기본 환경 구성 테마로 사용합니다.
- 선정된 traits는 warp_marker.traits에 기록하여 이후 Encounter Creature결정에 활용한다.

2. Encounter 난이도 산정:

- Encounter의 기준 난이도는 현재 워프마커의 floor를 파티 레벨(PL)로 간주하여 산정한다.
- 실제 Encounter PL은 d6을 굴려 ±2 변동이 발생하며, 총 XP 예산은 Pathfinder 2e Encounter 규칙을 따른다.
- 적의 정체와 능력은 Recall Knowledge 등 스킬 체크 이전에는 묘사 위주로만 공개한다.

3. 보물상자 발생 및 보상 절차

- Encounter 종료 시, 몬스터 시신 대신 보물 상자가 생성된다.
- 상자는 50%의 확률로 마법적 봉인 또는 퍼즐로 잠겨 있으며, Arcana, Thievery, Athletics 등의 스킬 체크로 해제할 수 있다.

4. 보상 구성 규칙

- 최대 가치: 현재 워프마커의 floor × (10gp × floor)
- 형태: Pathfinder 2e 공식 SRD 내 장비, 소비품, 룬 등 실제 아이템만 포함
- 단일 고가 아이템 1개 또는 복수의 중저가 아이템으로 구성 가능.

이때 사용되는 floor 값은 Encounter 난이도와 동일하게 현재 워프마커(warp_marker.floor)에 기록된 층수를 기준으로 한다.

이 시스템은 각 탐색에서 위험과 보상의 기대치를 동적으로 조절하며, 던전 탐색 자체를 하나의 전략적 자원 게임으로 만든다.
