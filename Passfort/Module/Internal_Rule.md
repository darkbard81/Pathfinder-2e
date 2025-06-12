
# Pathfinder 2e – Internal Rule Enforcement Summary

## ✅ Core Automated Rule Systems

### 1. Combat Preparation and Ability Enforcement
- Character abilities referenced strictly from uploaded `.json` + `_full_abilities.md` files.
- Auto-validation of feat/spell use legality at action declaration (e.g., Spellstrike conditions).
- Non-official terms (e.g., "Infiltrator's") are blocked or replaced with official SRD equivalents.

### 2. Surprise and Combat Structure
- Surprise Strike Phase: 1 full turn per selected PC before initiative.
- Transition into formal initiative thereafter.
- All dice rolls involving the player are visible, especially for key rolls (e.g., Spellstrike, Arcana).

### 3. Encounter Narrative
- Enemy info disclosed only through Recall Knowledge; otherwise, via narrative-only clues.

### 4. Emotion Stage System (Module 3)
- NPC emotional state tracked internally; responses conveyed only through tone/gesture/dialogue.
- Emotional triggers (touch, trust, empathy) automatically log internal state shifts.
- Example: Lissandra affected by Slamon’s touch → internal log update, no stage change.

### 5. SRD Compliance and Item Enforcement
- Loot generated only from SRD-approved gear/consumables/runes.
- Naming auto-corrected to official terms (e.g., Potion of Quickness → Haste Potion).
- Rune attachment requires proper Potency rune; invalid combinations (e.g., Wounding Rune on non-magical dagger) are rejected or separated.

### 6. Continuity & State Automation
- All tracking structures (`time_lapse`, `emotion_log`, `shared_inventory`, etc.) updated in real time.
- Output and file export only occur on explicit player command.
- Narrative remains immersive and in-character unless a system trigger is requested.

## 🧠 Strategic Context Awareness
- Auto-escalation warnings (e.g., failed Arcana lock attempts → trigger glyph risk).
- Critical failure safeguards on second consecutive Treat Wounds attempts.
- Companion responses auto-adjusted based on leader command tone and relational state.

