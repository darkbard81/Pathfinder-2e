# NDJSON Conversion Specification for Pathfinder Monsters (Extended with Attacks)

This document defines the transformation rules for converting Pathfinder creature JSON data into a **flattened, search-friendly NDJSON format**.

---

## Input Scope
From the original JSON, only the following fields are used:

- `_id`
- `name`
- `system.traits`
- `system.attributes{ac, allSaves, hp, resistances, speed, weaknesses, immunities}`
- `system.details{level, publicNotes, languages}`
- `system.saves`
- `system.perception`
- `items` (for extracting attacks)

---

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
    "melee": { /* at most 1 */ },
    "weapon": { /* at most 1 */ },
    "actions": [ /* up to 3 */ ],
    "spell": { /* at most 1 */ },
    "spellcastingEntry": { /* at most 1 */ }
  },

  "search_blob": "<concatenated lowercase string for search indexing>",

  "publicNotes_text": "<system.details.publicNotes converted to plain text, max length 1200 characters>"
}
```

> Note: `publicNotes_text` must always be the **last key** in the object.

---

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
  - Strip HTML  
  - Unescape entities  
  - Normalize whitespace  
  - Truncate to **1200 characters**

### Saves
- `system.saves.fortitude.value` → `defenses.saves.fort`
- `system.saves.reflex.value` → `defenses.saves.save_reflex`
- `system.saves.will.value` → `defenses.saves.will`

### Perception
- `system.perception.mod` → `perception.mod`
- `system.perception.senses[]` → `perception.senses[]`

### Speed
- `system.attributes.speed.value` → `speed.land`
- `system.attributes.speed.otherSpeeds[]` → `speed.other[]`

---

## Attacks (Unified)

### General Rules
- Create `attacks` object with only present sections.  
- Include only the first qualifying item for **melee, weapon, spell, spellcastingEntry**.  
- Include up to three qualifying items for **actions**.  
- Extract damage rolls using the **first key in ascending order**.  
- If no qualifying item exists, omit that key.

---

### Melee (0–1)
Select the first item where `item.type == "melee"`.

```jsonc
"melee": {
  "name": <item.name>,
  "bonus": <item.system.bonus.value>,
  "damage": <first damageRoll.damage>,
  "damageType": <first damageRoll.damageType>,
  "traits": <item.system.traits.value[]>
}
```

---

### Weapon (0–1)
Select the first item where `item.type == "weapon"`.

```jsonc
"weapon": {
  "name": <item.name>,
  "bonus": <item.system.bonus.value>,
  "damage": <first damageRoll.damage>,
  "damageType": <first damageRoll.damageType>,
  "traits": <item.system.traits.value[]>
}
```

---

### Actions (0–3)
Include items where:
- `item.type == "action"`
- `item.system.category == "offensive"`
- `item.system.actionType.value == "action"`

Order preserved. Up to first 3.

```jsonc
"actions": [
  {
    "name": <item.name>,
    "actionType": <item.system.actionType.value>,
    "traits": <item.system.traits.value[]>,
    "cost": <item.system.actions.value>,    // action cost
    "template": [ "<...>" ],  // from @Template[...] in description
    "damage": [ "<...>" ],    // from @Damage[...] in description
    "check": [ "<...>" ]      // from @Check[...] in description
  }
]
```

Only include arrays if they contain values.

---

### Spell (0–1)
Select the first item where `item.type == "spell"`.

```jsonc
"spell": {
  "name": <item.name>,
  "level": <item.system.level.value>,
  "traits": <item.system.traits.value[]>
}
```

---

### Spellcasting Entry (0–1)
Select the first item where `item.type == "spellcastingEntry"`.

```jsonc
"spellcastingEntry": {
  "name": <item.name>,
  "tradition": <item.system.tradition.value>,
  "dc": <item.system.spelldc.value>
}
```

---

## Search Blob
- The `search_blob` is a single string created by concatenating specific fields, then **slugifying** all content.
- Fields included: `name`, `traits[]`, `level` (as `level-<number>`), `size`, `rarity`, `attacks.spellcastingEntry` fields (`name`, `tradition`, `dc`).
- Normalization: convert to lowercase, replace all punctuation and special characters with a single hyphen `-`, collapse multiple separators (spaces, hyphens, underscores, punctuation) into a single `-`, trim leading/trailing separators.


---

## Ordering and Omission Rules
- **Omit keys** when values are missing or arrays are empty.  
- **Always place** `publicNotes_text` as the **last key** in the object.

