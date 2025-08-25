
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

### Attacks (Unified: melee, ranged, action, spellcastingEntry, spell)

This section defines **selection caps** and **mechanical inclusion rules** for what counts as an attack and how many of each type may be emitted per creature.

#### A. Inclusion Types
- **melee** â weapon Strikes (PF2e `type:"melee"`)
- **ranged** â weapon Strikes (PF2e `type:"ranged"`)
- **action** â *only* active actions with an action cost (PF2e `type:"action"` **and** `system.actions.value â {1,2,3}`); **exclude** `passive`, `free`, `reaction`
- **spellcastingEntry** â the creatureâs spellcasting profile (tradition, DC, attack bonus, prepared mode)
- **spell** â individual offensive spells (see filters below)

> Notes:
> - `aura` items stay in abilities, not attacks.
> - Reactions such as *Freezing Blood* are not attacks under this cap (they go to abilities).

#### B. Selection Caps
- **melee**: at most **1** entry
- **ranged**: at most **1** entry
- **spell**: at most **1** offensive spell entry
- **action**: up to **3** entries meeting the action filter (see Â§C).  
- **spellcastingEntry**: **always include** exactly **1** per tradition present (if multiple traditions exist, include each one as a separate spellcastingEntry line).

#### C. Filters and Rankers

##### C1. melee (pick 1)
**Filter:** all `type:"melee"` retained for scoring.  
**Score:** pick the single best by this deterministic order:
1) highest average damage per Strike (sum all damageRolls, average per die)  
2) if tie, prefer trait set containing any of: `reach-*`, `agile`, `deadly*`, `fatal*`, `grab`, `trip`, `disarm`, `forceful`, `sweep` (presence count, higher wins)  
3) if tie, higher attack bonus  
4) if tie, alphabetical by name

##### C2. ranged (pick 1)
**Filter:** all `type:"ranged"`.  
**Score:** 
1) highest average damage per Strike  
2) if tie, prefer longer effective range (parse `range` or `thrown X/volley X`)  
3) if tie, presence of impactful traits: `deadly*`, `fatal*`, `reload-0/1`, `capacity-*`  
4) if tie, higher attack bonus â then name

##### C3. action (pick up to 3)
**Filter:** only if `type:"action"` **and** `system.actionType.value == "action"` **and** `system.actions.value â {1,2,3}`.  
**Exclude:** `system.actionType.value â {"passive","free","reaction"}` or missing action count.  
**Score (threat-based):**
- Primary score = max of:
  - parsed damage DPR surrogate (sum of all `@Damage[...]` dice averages)  
  - presence of incapacitating effects (`petrify, paralyze, stun, swallow, engulf, devour, banish, dominate`) adds +X = 10
- Add +2 if an on-use **save DC** is present (`@Check[...|dc:N]`), +1 if **area** (cone/line/burst/emanation) present.
- Break ties by higher DC, then larger area, then lower action cost (1 < 2 < 3), then name.

##### C4. spellcastingEntry (always include)
Keep one entry **per tradition** with: `tradition`, `spelldc.value`, `attack bonus`, `prepared.value` and any `autoHeighten`. No cap beyond per-tradition.

##### C5. spell (pick 1)
**Filter:** offensive-only. Include if any of:
- `level.value â¥ 3`, **and** (has damage, or causes a save, or has incapacitation/debilitating keywords), **or**
- name/traits contain any of: `disintegrate, cone, line, burst, ray, bolt, wall, summon, dominate, banish, petrify, chain lightning, spirit blast, wails of the damned`.
**Score:**  
1) highest spell **level**; then  
2) larger **area** (size, then AoE type priority: line > cone > burst > emanation > single), then  
3) greater average **damage** (if any), then  
4) presence of **incapacitation**/**save or suck** effects, then  
5) shorter **action cost** (2 < 3), then name.

#### D. Output Shape (per selected entry)

```json
// melee / ranged
{
  "name": "string",
  "type": "melee|ranged",
  "traits": ["..."],
  "numbers": { "attackBonus": +?, "damage": "XdY+Z type", "range": "ft(optional)" },
  "tags": ["reach-10","agile","deadly d10", "..."]
}

// action
{
  "name": "string",
  "type": "action",
  "actionCost": "1|2|3",
  "traits": ["..."],
  "numbers": { "dc": ?, "damage": "XdY type", "area": "cone 30 ft (optional)" },
  "note": "1-line summary parsed from description"
}

// spellcastingEntry
{
  "name": "Arcane Innate Spells",
  "type": "spellcastingEntry",
  "tradition": "arcane",
  "dc": 28,
  "attackBonus": 20,
  "prepared": "innate",
  "autoHeighten": 5
}

// spell
{
  "name": "Cone of Cold",
  "type": "spell",
  "level": 5,
  "traits": ["cold","attack"],
  "numbers": { "dc": 28, "damage": "12d6 cold", "area": "cone 60 ft", "range": "" },
  "tags": ["innate","at-will"]
}
```

#### E. Post-Cap Tie-Down
After picking winners per C1âC5, enforce the caps from Â§B. If any bucket still exceeds its cap, drop lowest-scoring entries by the bucketâs score rule, then by name.

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
