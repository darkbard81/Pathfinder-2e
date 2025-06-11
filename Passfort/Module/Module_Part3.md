# 캠페인 모듈: 패스파이더 2e Homebrew 보조 시스템 Part 3

이 모듈은 캠페인 세션 중에서만 적용된다. Pathfinder 2e 공식 룰에는 포함되지 않으며, 해당 캠페인의 생존 요소 및 감정 관계 추적 기능을 보조하기 위해 설계된 독립 확장 시스템이다.

## 모듈 6 - 무한의 프론티어 층수 기반 난이도 시스템 (warp_marker 연동 포함)

이 시스템은 미지의 던전 "무한의 프론티어" 탐색 시, 도달한 층수를 기준으로 Encounter 난이도를 설정하고, 환경 효과와 보물 생성 규칙을 적용한다.

던전 관련 정보는 메타스키마의  warp_marker 구조와 연동되며, 다음 항목으로 구성되고 자동으로 추적된다:

- warp_marker.floor : 진입시 층수
- warp_marker.traits : 던전 진입시 랜덤갱신
- warp_makert.monsters : 던전 진입시 갱신된 몬스터 일람 (ex. Phase Spider (Creature 7, Elite, Traits: Spider, Toxic) )
- warp_marker.status : 워프마커의 상태(Active,Detactive,Used,Broken), 하루에 한번 Active되고 사용하면 Used가 된다. 길드에서 탈퇴 시 Deactive. 파손인 경우 Broken
- Encounter PL 계산의 기준은 현재 워프마커가 기록한 warp_marker.floor 값이다.

1. Common Environment 규칙

- 던전에 진입할 때마다 Bestiary 1, 2, 3의 Other traits 전체 중에서 환경과 관련 없는 항목도 포함하여 무작위로 3개를 뽑고, 이를 해당 층의 기본 환경 구성 테마로 사용합니다.
- 구체적인 Traits설명을 피하고 서사로만 환경을 묘사합니다.
2. Encounter 난이도 산정:

- Encounter의 기준 난이도는 현재 워프마커의 floor를 파티 레벨(PL)로 간주하여 산정한다.
- 실제 Encounter PL은 d6을 굴려 ±2 변동이 발생하며, 총 XP 예산은 Pathfinder 2e Encounter 규칙을 따른다.
- 해당 PL에 맞는 공식 Bestiary 몬스터가 무작위 6개체가 추출된다.

3. 보물상자 발생 및 보상 절차

- Encounter 종료 시, 몬스터 시신 대신 보물 상자가 생성된다.
- 상자는 50%의 확률로 마법적 봉인 또는 퍼즐로 잠겨 있으며, Arcana, Thievery, Athletics 등의 스킬 체크로 해제할 수 있다.

4. 보상 구성 규칙

- 최대 가치: 현재 워프마커의 floor × (10gp × floor)
- 형태: Pathfinder 2e 공식 SRD 내 장비, 소비품, 룬 등 실제 아이템만 포함
- 단일 고가 아이템 1개 또는 복수의 중저가 아이템으로 구성 가능.

이때 사용되는 floor 값은 Encounter 난이도와 동일하게 현재 워프마커(warp_marker.floor)에 기록된 층수를 기준으로 한다.

이 시스템은 각 탐색에서 위험과 보상의 기대치를 동적으로 조절하며, 던전 탐색 자체를 하나의 전략적 자원 게임으로 만든다.

>1. 던전 진입 시 `Other Traits` 3개가 무작위로 생성된다. (예: Clockwork, Toxic, Mistbound 등)
>2. Encounter PL은 d6을 굴려 변동값을 적용한 후 확정된다. (PL = warp_marker.floor ± d6)
>3. 해당 PL에 맞는 공식 Bestiary 몬스터가 무작위 추출된다.
>4. 추출된 몬스터는 `Other Traits` 중 일부를 부여받고, Weak 또는 Elite 조정이 함께 적용된다.
>5. 몬스터의 이름은 해당 Trait 중 하나를 앞에 붙여 표기된다. (예: “Toxic Phase Spider”, “Mistbound Wight”)''
