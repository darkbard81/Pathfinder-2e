
# NDJSON Conversion Specification for Pathfinder Monsters (Extended with Attacks)

This document defines the transformation rules for converting Pathfinder creature JSON data
into a **flattened, search-friendly NDJSON format**.

## Input Scope
Only the following fields from the original JSON are used:
- `_id`
- `name`
- `system.traits`
- `system.attributes{ac, allSaves, hp, resistances, speed, weaknesses, immunities}`
- `system.details{level, publicNotes, languages}`
- `system.saves`
- `system.perception`
- `items` (for extracting one attack)

## Output Schema (NDJSON, one object per line)

```jsonc
{
  "id": "<_id>",
  "name": "<name>",

  "rarity": "<system.traits.rarity>",
  "size": "<system.traits.size.value>",
  "traits": ["<system.traits.value[]>"],

  "level": <system.details.level.value>,

  "languages": {
    "list": ["<system.details.languages.value[]>"],
    "details": "<system.details.languages.details>"
  },

  "defenses": {
    "ac": <system.attributes.ac.value>,
    "hp": { "max": <system.attributes.hp.max>, "details": "<system.attributes.hp.details>" },
    "saves": { 
      "fort": <system.saves.fortitude.value>, 
      "save_reflex": <system.saves.reflex.value>, 
      "will": <system.saves.will.value> 
    },
    "immunities": ["<system.attributes.immunities[]>"],
    "resistances": ["<system.attributes.resistances[]>"],
    "weaknesses": ["<system.attributes.weaknesses[]>"],
    "notes": "<system.attributes.allSaves.value>"
  },

  "perception": {
    "mod": <system.perception.mod>,
    "senses": ["<system.perception.senses[]>"]
  },

  "speed": {
    "land": <system.attributes.speed.value>,
    "other": ["<system.attributes.speed.otherSpeeds[]>"]
  },

  "attacks": {
    "melee": {    // if melee exists
      "name": "<item.name>",
      "bonus": <item.system.bonus.value>,
      "damage": "<item.system.damageRolls[0].damage>",
      "damageType": "<item.system.damageRolls[0].damageType>",
      "traits": ["<item.system.traits.value[]>"]
    },
    "range": {    // if no melee exists, use items[0]
      "name": "<item.name>",
      "bonus": <item.system.bonus.value>,
      "damage": "<item.system.damageRolls[0].damage>",
      "damageType": "<item.system.damageRolls[0].damageType>",
      "traits": ["<item.system.traits.value[]>"]
    }
  },

  "publicNotes_text": "<system.details.publicNotes converted to plain text, max length 1200 characters>",

  "search_blob": "<concatenated lowercase string for search indexing>"
}
```

## Transformation Rules

### Traits
- `system.traits.rarity` → `rarity`
- `system.traits.size.value` → `size`
- `system.traits.value[]` → `traits[]`

### Attributes / Defenses
- `system.attributes.ac.value` → `defenses.ac`
- `system.attributes.hp.max` → `defenses.hp.max`
- `system.attributes.hp.details` → `defenses.hp.details`
- `system.attributes.allSaves.value` → `defenses.notes`
- `system.attributes.resistances[]` → `defenses.resistances[]`
- `system.attributes.weaknesses[]` → `defenses.weaknesses[]`
- `system.attributes.immunities[]` → `defenses.immunities[]`

### Details
- `system.details.level.value` → `level`
- `system.details.languages.value[]` → `languages.list[]`
- `system.details.languages.details` → `languages.details`
- `system.details.publicNotes` → `publicNotes_text`
  - HTML stripped, entities unescaped
  - whitespace normalized
  - maximum 1200 characters

### Saves
- `system.saves.fortitude.value` → `defenses.saves.fort`
- `system.saves.reflex.value` → `defenses.saves.save_reflex` (renamed)
- `system.saves.will.value` → `defenses.saves.will`

### Perception
- `system.perception.mod` → `perception.mod`
- `system.perception.senses[]` → `perception.senses[]`

### Speed
- `system.attributes.speed.value` → `speed.land`
- `system.attributes.speed.otherSpeeds[]` → `speed.other[]`

### Attacks
- Inspect `items` array:
  - If any `item.type == "melee"`, select the **first melee item**. Output under `attacks.melee`.
  - Otherwise, if no melee exists, use the **first item in the array**. Output under `attacks.range`.
- Fields copied:
  - `name` → `attacks.melee.name` or `attacks.range.name`
  - `system.bonus.value` → `bonus`
  - `system.damageRolls[0].damage` → `damage`
  - `system.damageRolls[0].damageType` → `damageType`
  - `system.traits.value[]` → `traits[]`
- If no items exist at all → omit `attacks`.

### Search Blob
A concatenated lowercase string built from:
- `name`, `traits[]`, `rarity`, `size`
- `languages.list`, `languages.details`
- `perception.senses[]`
- `defenses.immunities`, `defenses.resistances`, `defenses.weaknesses`
- `attacks.melee` or `attacks.range` info (name, bonus, damage, damageType, traits)
- `level`, `defenses.ac`, `defenses.hp.max`
- first 200 characters of `publicNotes_text`
- All punctuation replaced by spaces, multiple spaces collapsed.

---

## Example (Barghest, melee exists)

```json
{
  "id": "00uNOPsU5VognIcB",
  "name": "Barghest",
  "level": 4,
  "rarity": "common",
  "size": "med",
  "traits": ["fiend", "unholy"],

  "attacks": {
    "melee": {
      "name": "Jaws",
      "bonus": 13,
      "damage": "2d8+5",
      "damageType": "piercing",
      "traits": ["unarmed", "magical", "reach-5", "knockdown"]
    }
  },

  "search_blob": "barghest fiend unholy jaws +13 2d8+5 piercing ..."
}
```

## Example (if no melee exists, ranged only)

```json
"attacks": {
  "range": {
    "name": "Longbow",
    "bonus": 11,
    "damage": "1d8+3",
    "damageType": "piercing",
    "traits": ["range-100", "deadly-d10"]
  }
}
```
