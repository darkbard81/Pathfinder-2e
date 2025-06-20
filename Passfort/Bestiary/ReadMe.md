# 몬스터 도감

## 1. Bestiary 1,2,3권 몬스터 Index
- bestiary_creatures.json 구조
~~~json
  {
    "Creature": "Animated armor",
    "Level": 2,
    "Page": 20,
    "Book": "Bestiary1"
  }
~~~
- Level필드로 필터링하여 6개체 선정, Encounter 풀(Pool)로 등록
- 공식 PDF파일의 Parsing Method를 가르켜야함 ANIMATED ARMOR CREATURE 2 => MonsterName CREATURE N
- 위 내용이 지켜지면 몬스터의 상세 능력치를 가져올 수 있다.

---

## 2. Treasure Index
- Treasure_Table.json 구조
~~~json
  {
    "Level": 3,
    "Type": "Permanent Items",
    "Name": "Returning",
    "Grade": "N",
    "Category": "Rune",
    "Price": 55,
    "Page": "584"
  }
~~~
- 보상의 최대, 최저 가치를 설정하여 Price필드로 필터링이 가능
- Core Rulebook(CBR) PDF에서 제대로 못찾으면 추론하지 말고 /stop반응하도록 가르켜야함
- 공식 PDF자체가 이름과 상세 내용이 일치하지 않는 항목이 많음으로 중요한 아이템인 경우 수작업으로 확인이 필요하다.
