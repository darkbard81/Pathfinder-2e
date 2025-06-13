# 캠페인 모듈: 패스파이더 2e Homebrew 보조 시스템 Part 3

이 모듈은 캠페인 세션 중에서만 적용된다. Pathfinder 2e 공식 룰에는 포함되지 않으며, 해당 캠페인의 생존 요소 및 감정 관계 추적 기능을 보조하기 위해 설계된 독립 확장 시스템이다.

## 모듈 6 - 무한의 프론티어 던전 Environment & Encounter 생성 규칙 (warp_marker 연동 포함)

이 규칙은 Pathfinder 2e 캠페인 내 "무한의 프론티어" 던전에 진입할 때마다 Environment & Encounter를 자동 생성하기 위한 절차입니다.

던전 관련 정보는 메타스키마의  warp_marker 구조와 연동되며, 다음 항목으로 구성되고 자동으로 추적된다:

- warp_marker.floor : 진입시 층수
- warp_marker.environment : Aquatic, Arctic, Desert, Forest, Jungle, Mountain, Plains, Swamp, Underground, Urban, Dungeon 중 하나로 진입시 갱신
- warp_marker.traits : 던전 진입시 몬스터에의해 갱신
- warp_makert.monsters_pool : 던전 진입시 갱신된 몬스터 일람 (ex. Phase Spider (Creature 7, Elite, Traits: Spider, Toxic) )
- warp_marker.status : 워프마커의 상태(Active,Detactive,Used,Broken), 하루에 한번 Active되고 사용하면 Used가 된다. 길드에서 탈퇴 시 Deactive. 파손인 경우 Broken

## 던전 진입시 시스템 절차

### 1. Encounter Level(EL) 설정
- **Encounter Level = 현재 던전 층수(warp_marker.floor) ± 2d4**
- 2d4는 진입 시점에 굴림
- Encounter PL에 영향을 줌 (파티 평균 레벨 기준 조정)

| 🎲 2d4 결과 | Encounter 변동치 (ΔEL) |
| --------- | ------------------- |
| 2         | –3                  |
| 3         | –2                  |
| 4         | -1                  |
| 5         | ±0                  |
| 6         | +1                  |
| 7         | +2                  |
| 8         | +3                  |


### 2. 몬스터 6개체 선택 (warp_makert.monsters_pool)
- **Encounter Level 기준으로 적합한 범위의 몬스터(Encounter Level ±1 또는 최대 ±2 이내)**만 선정합니다.
- bestiary1_creatures.json, bestiary2_creatures.json, bestiary3_creatures.json 파일에서 Level항목을 참조하여 선정합니다.
- 이 6개체는 **해당 층의 Encounter 풀(Pool)**로 등록된다.
- Encounter 설계 시, XP 예산에 맞춰 이 풀 중 일부만 실제 등장시킨다
- 잉여 개체는 이후 이벤트/재등장/서사용으로 보존할 수 있다.

#### 📌 몬스터 능력치 검색 방법
- 각 몬스터의 정식 능력치는 다음 형식으로 검색한다:
  - *Monster Name*: Creatures by Level 목록에 나온 이름 그대로
  - *X*: 해당 몬스터의 레벨 숫자

예시: `"Tiger CREATURE 4"`, `"Shae CREATURE 4"`

### 3. 몬스터 Traits 무작위 추첨 (warp_marker.traits)
- 2번에서 뽑은 6 마리의 Traits 필드를 모두 집계.
- 중복 제거 후, 무작위 3개 선택, 필요시 Alignment·Size·Rarity 등 기본 분류 Trait는 제외하고 기능·환경·키워드 Trait만 남긴다.
- 생성된 Trait은 이후 몬스터 능력 변화에 사용됨
- 선택된 3 개를 warp_marker.traits 배열에 기록.

  
### 4. XP 예산 정하기
- **XP 예산 = Core Rulebook p.488 "Encounter Budget by Party Level" 표** 사용

| EL – PL 차이 | Encounter 난이도 |
| ---------- | ------------- |
| –4 이하      | Trivial       |
| –3         | Low           |
| –2         | Low           |
| –1         | Moderate      |
| ±0         | Moderate      |
| +1         | Severe        |
| +2         | Severe        |
| +3 이상      | Extreme       |


| Encounter Level | XP Budget |
|------------------|------------|
| Trivial          | 40 XP     |
| Low              | 60 XP     |
| Moderate         | 80 XP     |
| Severe           | 120 XP    |
| Extreme          | 160 XP    |

### 5. 난이도 및 특성 조정

#### ✅ Elite / Weak 템플릿 적용 (필요시)
- **Elite**: AC, 공격, DC +2 / HP +30%
- **Weak**: AC, 공격, DC -2 / HP -30%

#### ✅ Trait 추가 / 삭제 (필요시)
- **warp_marker.traits**중 기능성 Trait을 추가하는 경우, 해당 룰 효과를 능력에 반영
  - 예: `incorporeal`, `swarm`, `mindless` 등
 
#### 난이도 및 특성 조정으로 인한 이름 변경은 접두사, 접미사만 허용한다.
 - Elite / Weak 예: Elite Drow Priestess, Weak Drow Priestess
 - Trait 추가 예: Mireborn Drow Priestess, Drow Priestess of Rot, Mireborn Drow Priestess of Decay

### 6. Encounter 확정 시점
- Encounter에 사용될 몬스터, 난이도, 테마 등은 **던전 진입 시점에 미리 확정**된다.
- 그러나 **전투의 발생 시점은 던전 내 서사, 탐색, 경로 등에 따라 자유롭게 배치**된다.
- 몬스터들은 해당 층의 **지속적 위협 존재로 간주**되며, 단일 전투뿐 아니라 복수 장면 또는 이벤트에서도 재활용 가능하다.

## 모듈 7 - 무한의 프론티어 던전 보물상자 발생 및 보상 절차

### 1. 보물상자 발생
- Encounter 종료 시, 몬스터 시신 대신 보물 상자가 생성된다.
- 상자는 50%의 확률로 마법적 봉인 또는 퍼즐로 잠겨 있으며, Arcana, Thievery, Athletics 등의 스킬 체크로 해제할 수 있다.

### 2. 보상 구성 규칙
- 최대 가치: 현재 워프마커의 floor × (10gp × floor)
- 형태: Treasure_Table.json 내 장비, 소비품, 룬 등 실제 아이템만 포함
- 단일 고가 아이템 1개 또는 복수의 중저가 아이템으로 구성 가능.

이때 사용되는 floor 값은 Encounter 난이도와 동일하게 현재 워프마커(warp_marker.floor)에 기록된 층수를 기준으로 한다.

---

>>이 시스템은 각 탐색에서 위험과 보상의 기대치를 동적으로 조절하며, 던전 탐색 자체를 하나의 전략적 자원 게임으로 만든다.
