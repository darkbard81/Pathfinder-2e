
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

### Attacks (Unified: melee, weapon, actions, spellcastingEntry, spell)
Output container:
- Create an `attacks` object.
- Inside `attacks`, include ONLY the following keys that actually have qualifying data:
  - "melee"                // object, at most 1
  - "weapon"               // object, at most 1  (NOTE: singular)
  - "actions"              // array, at most 3 entries
  - "spell"                // object, at most 1
  - "spellcastingEntry"    // object, at most 1
- If a section has no qualifying item(s), OMIT that section (do not include empty objects/arrays).

--------------------------------------------------------------------
GENERAL SELECTION & FIELD MAPPING
--------------------------------------------------------------------
1) “First” = the first element by the original order in the creature’s `items` array (lowest index).

2) Accessing the first damage roll when keys are unknown:
   - Let R = item.system.damageRolls (an object keyed by arbitrary IDs).
   - Sort R’s keys as strings ascending and take the first key.
   - Use that entry for `damage` and `damageType`.

3) Field mappings (omit a field if missing on the source item):
   - name        := item.name
   - bonus       := item.system.bonus.value
   - damage      := firstKey(item.system.damageRolls).damage
   - damageType  := firstKey(item.system.damageRolls).damageType
   - traits[]    := item.system.traits.value (array; default to [])

--------------------------------------------------------------------
MELEE  (0–1 entry)
--------------------------------------------------------------------
Select:
- If there exists any item with item.type == "melee", take the FIRST such item.
- Otherwise, do not define `attacks.melee`.

Output (when selected):
attacks.melee = {
  "name": <name>,
  "bonus": <bonus>,
  "damage": <damage>,
  "damageType": <damageType>,
  "traits": <traits[]>
}

--------------------------------------------------------------------
WEAPON  (0–1 entry)   // singular
--------------------------------------------------------------------
Select:
- If there exists any item with item.type == "weapon", take the FIRST such item.
- Otherwise, do not define `attacks.weapon`.

Output (when selected):
attacks.weapon = {
  "name": <name>,
  "bonus": <bonus>,
  "damage": <damage>,
  "damageType": <damageType>,
  "traits": <traits[]>
}

--------------------------------------------------------------------
ACTIONS (0–3 entries)  // offensive + action-type only
--------------------------------------------------------------------
Filter:
- Include ONLY items with ALL of the following:
  - item.type == "action"
  - item.system.category == "offensive"
  - item.system.actionType.value == "action"

Order & limit:
- Preserve original `items` order.
- Take up to the FIRST THREE qualifying actions.

For each included action, build:
base = {
  "name": item.name,
  "actionType": item.system.actionType.value,   // will be "action"
  "traits": item.system.traits.value || []
}

Then parse item.system.description.value (HTML/markup) and EXTRACT ONLY these tokens:
- All @Template[...]
- All @Damage[...]
- All @Check[...]
For each token type, append the raw bracket contents (inside [...]) to arrays:
- base.template = [ "<contents1>", ... ]     // from @Template[...]
- base.damage   = [ "<contents1>", ... ]     // from @Damage[...]
- base.check    = [ "<contents1>", ... ]     // from @Check[...]
Omit any of these keys that would be empty.
DO NOT include the original description string.

attacks.actions = [ base, ... ]   // up to 3 entries

--------------------------------------------------------------------
SPELL  (0–1 entry)
--------------------------------------------------------------------
Select:
- Take the FIRST item with item.type == "spell".
- Otherwise, omit `attacks.spell`.

Output (when selected):
attacks.spell = {
  "name": item.name,
  "level": item.system.level.value,
  "traits": item.system.traits.value || []
}

--------------------------------------------------------------------
SPELLCASTING ENTRY  (0–1 entry)
--------------------------------------------------------------------
Select:
- Take the FIRST item with item.type == "spellcastingEntry".
- Otherwise, omit `attacks.spellcastingEntry`.

Output (when selected):
attacks.spellcastingEntry = {
  "name": item.name,
  "tradition": item.system.tradition.value,
  "dc": item.system.spelldc.value
}


### Search Blob
A concatenated lowercase string built from:
- `name`, `traits[]`, `rarity`, `size`
- `languages.list`, `languages.details`
- `perception.senses[]`
- `defenses.immunities`, `defenses.resistances`, `defenses.weaknesses`
- `attacks.melee` or `attacks.weapon` info (name, bonus, damage, damageType, traits)
- `level`, `defenses.ac`, `defenses.hp.max`
- `attacks.spellcastingEntry`
- All punctuation replaced by spaces, multiple spaces collapsed.

---
