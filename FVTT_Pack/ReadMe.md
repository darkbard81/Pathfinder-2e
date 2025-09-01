# A system implementation of Pathfinder Second Edition for Foundry VTT
> [Link](https://github.com/foundryvtt/pf2e)

## Global Conversion Rule
- Flat key list
- HTML to Plaintext
- Create key "search_blob"

# Pathfinder2e Feats Conversion From FVTT

## 변환 규칙
- **보존 필드**
  - `id` ← `_id`
  - `name`
  - `type`
  - `actionType` ← `system.actionType.value`
  - `actionCost` ← `system.actions.value`  
    - 숫자면 `"1 action"`, `"2 actions"` 문자열로 변환
  - `level` ← `system.level.value`
  - `traits`
    - `rarity` ← `system.traits.rarity`
    - `values` ← `system.traits.value[]`
  - `prerequisites` ← `system.prerequisites.value[].value`
  - `source` ← `system.publication.title`
  - `description` ← `system.description.value` (HTML → plaintext 변환)

---

## description 변환 규칙
1. **UUID 치환**
   - `@UUID[...] {텍스트}` → `텍스트`
   - `@UUID[...]` → 제거
2. **강조 태그 치환**
   - `<strong>…</strong>`, `<b>…</b>` → **대문자 + 콜론** (`TRIGGER:`)
3. **HTML 제거**
   - `<p>`, `<div>` 등 블록 태그 → 줄바꿈 추가
   - `<br>` → 줄바꿈
   - `<hr>` → `---`
   - 나머지 태그는 제거
4. **공백 정리**
   - 연속 공백/개행 축소
   - 텍스트 앞뒤 공백 제거

---

## 출력 예시
입력:
```html
<p><strong>Trigger</strong> You succeed at a saving throw to disbelieve an illusion.</p>
<hr />
<p>You can cut through illusions …</p>
