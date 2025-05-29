# LastOrigin Continuity Schema v2.0

이 문서는 `LastOrigin` 캠페인의 연속성 관리 파일 구조를 정의한 최신 버전 스키마다. 기존 `LastOrigin_Continuity_schema.md`를 기반으로 실제 사용 사례와 자동화 적용을 고려해 다음 항목들이 추가되었다:

---

## 🧭 캠페인 정보
```json
"campaign": "string",          // 캠페인 식별자 또는 제목
"location": "string"           // 현재 진행 지역 (던전/도시 등)
```

## 🧑‍🤝‍🧑 파티 정보

### party (object)

| 필드명 | 타입 | 설명 |
|--------|------|------|
| leader | string | 파티 리더 이름 |
| members | array[object] | 파티 구성원 목록 |

### members[i] (object)

| 필드명 | 타입 | 설명 |
|--------|------|------|
| name | string | 캐릭터 이름 |
| level | number | 현재 레벨 |
| gear | object | 장비 정보. 아래 gear 참조 |
| spells | object | 주문 슬롯 정보. 아래 spells 참조 |

### gear (object)

| 필드명 | 타입 | 설명 |
|--------|------|------|
| weapon | string | 주요 무기 이름 |
| armor | string | 착용 방어구 이름 |

※ 기타 장비는 `inventory.character_items`로 이동

### spells (object)

| 필드명 | 타입 | 설명 |
|--------|------|------|
| 1 | object | 1레벨 주문 슬롯 (슬롯 수, 사용 수, 준비 주문 포함) |
| 2 | object | 2레벨 주문 슬롯 |
| focus_points | number | 집중 포인트 보유량 |

### spells[1 or 2] (object)

| 필드명 | 타입 | 설명 |
|--------|------|------|
| slots_total | number | 총 슬롯 수 |
| slots_used | number | 사용된 슬롯 수 |
| prepared | array[string] | 준비된 주문 목록 |
```json
"party": {
  "leader": "string",          // 파티 리더 이름
  "members": [
    {
      "name": "string",
      "level": number,
      "gear": {
        "weapon": "string",
        "armor": "string"
      },
      "spells": {
        "1": { "slots_total": number, "slots_used": number, "prepared": ["string"] },
        "2": { "slots_total": number, "slots_used": number, "prepared": ["string"] },
        "focus_points": number
      }
    }
  ]
}
```

## ⏰ 시간 기록

### time (object)

| 필드명 | 타입 | 설명 |
|--------|------|------|
| current_day | number | 현재 날짜 (1일부터 시작) |
| clock | string (HH:MM) | 현재 시각 |
| activity_hours | number | 활동 시간 누적 |
| utility_hours | number | 유동 시간 누적 (식사, 정비 등) |
| sleep_hours | number | 수면 시간 누적 |
| last_meal | string | 마지막 식사 시각 |
| last_sleep | string | 마지막 수면 시각 |

### time (object)

| 필드명 | 타입 | 설명 |
|--------|------|------|
| current_day |
```json
"time": {
  "current_day": number,
  "clock": "HH:MM",          // 현재 시각
  "activity_hours": number,   // 활동 시간 누적
  "utility_hours": number,    // 식사/기도/정비 시간 누적
  "sleep_hours": number,      // 수면 시간 누적
  "last_meal": "HH:MM",
  "last_sleep": "HH:MM"
}
```

## 🌍 세계 상태

### world_state (object)

| 필드명 | 타입 | 설명 |
|--------|------|------|
| dungeon_floor | number | 현재 탐색 중인 던전 층수 |
| frontier_warp_marker | boolean | 워프마커 발급 여부 |
| passport_events | array[string] | 패스포트에서 발생한 이벤트 로그 |
| last_checkpoint | string | 마지막 체크포인트 요약 |
| last_checkpoint_desc | string | 마지막 위치의 상세 설명 |
```json
"world_state": {
  "dungeon_floor": number,
  "frontier_warp_marker": boolean,
  "passport_events": ["string"],
  "last_checkpoint": "string",
  "last_checkpoint_desc": "string"
}
```

## ❤️ 감정 관계

### relationships (object)

| 필드명 | 타입 | 설명 |
|--------|------|------|
| 캐릭터이름 | object | 해당 캐릭터 기준 감정 대상 목록 |
| └ 상대이름 | number (0~5) | 감정 단계 (0=무관심 ~ 5=소유) |
```json
"relationships": {
  "캐릭터이름": {
    "상대이름": 감정단계(0~5)
  }
}
```

## 🎬 장면 로그

### scene_log (array[object])

| 필드명 | 타입 | 설명 |
|--------|------|------|
| timestamp | string | 장면 시작 시각 (예: Day 1 - 08:00) |
| location | string | 장면 발생 장소 |
| description | string | 간략한 요약 또는 사건 설명 |
| time_spent | string | 소비된 시간 (예: "1시간") |
```json
"scene_log": [
  {
    "timestamp": "Day N - HH:MM",
    "location": "string",
    "description": "string",
    "time_spent": "string"
  }
]
```

## 🎒 인벤토리

### inventory (object)

| 필드명 | 타입 | 설명 |
|--------|------|------|
| shared_items | array[object] | 파티 전체가 공유하는 아이템 목록 |
| └ name | string | 아이템 이름 |
| └ quantity | number | 수량 |
| party_gold | number | 현재 파티가 보유한 금화량 |
| character_items | array[object] | 캐릭터별 개별 소지품 목록 |
| └ owner | string | 아이템 소지 캐릭터 이름 |
| └ name | string | 아이템 이름 |
| └ quantity | number | 수량 |

```json
"inventory": {
  "shared_items": [
    { "name": "string", "quantity": number }
  ],
  "party_gold": number,
  "character_items": [
    { "owner": "string", "name": "string", "quantity": number }
  ]
}
```

## 💞 감정 로그

### emotion_log (array[object])

| 필드명 | 타입 | 설명 |
|--------|------|------|
| log_id | number | 고유 로그 식별자 |
| timestamp | string | 시점 (예: Day 1 - 08:00) |
| scene_id | number | 연관된 장면 번호 |
| from | string | 감정을 유발한 캐릭터 |
| to | string | 감정을 느낀 대상 |
| change | string | 변화량 (+1 / -1) |
| new_stage | number | 변경 후 감정 단계 (0~5) |
| trigger | string | 변화 원인 요약 |
| note | string | 추가 설명 또는 메모 |
```json
"emotion_log": [
  {
    "log_id": number,
    "timestamp": "Day N - HH:MM",
    "scene_id": number,
    "from": "string",
    "to": "string",
    "change": "+1" 또는 "-1",
    "new_stage": number,
    "trigger": "string",
    "note": "string"
  }
]
```

## 🆙 레벨업 로그

### levelup_log (array[object])

| 필드명 | 타입 | 설명 |
|--------|------|------|
| character | string | 레벨업한 캐릭터 이름 |
| level | number | 새로운 레벨 값 |
| status | string | "planned" 또는 "confirmed" 상태 구분 |
| timestamp | string | 적용 시점 |
| changes | object | 변경 사항 묶음 |
| └ hp_increase | number | 증가한 HP 양 |
| └ trained_skills_added | array[string] | 새로 훈련한 스킬 목록 |
| └ class_feat_gained | string | 획득한 클래스 특기 |
| └ general_feat_gained | string | 획득한 일반 특기 |
| └ skill_increases | array[string] | 스킬 상승 목록 |
| └ spells_added | array[string] | 새로 얻은 주문 목록 |
| └ notes | string | 기타 기록 사항 |
```json
"levelup_log": [
  {
    "character": "string",
    "level": number,
    "status": "planned" | "confirmed",
    "timestamp": "Day N - HH:MM",
    "changes": {
      "hp_increase": number,
      "trained_skills_added": ["string"],
      "class_feat_gained": "string",
      "general_feat_gained": "string",
      "skill_increases": ["string"],
      "spells_added": ["string"],
      "notes": "string"
    }
  }
]
```

---

> 본 스키마는 `LastOrigin` 캠페인의 연속성과 자동화를 보장하기 위해 v2.0으로 확장되었으며,
> 이전 버전(`LastOrigin_Continuity_schema.md`)과 호환되지 않는 구조 변경을 포함합니다.
