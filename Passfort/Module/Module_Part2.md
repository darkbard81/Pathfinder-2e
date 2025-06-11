# 캠페인 모듈: 패스파이더 2e Homebrew 보조 시스템 Part 2

이 모듈은 캠페인 세션 중에서만 적용된다. Pathfinder 2e 공식 룰에는 포함되지 않으며, 해당 캠페인의 생존 요소 및 감정 관계 추적 기능을 보조하기 위해 설계된 독립 확장 시스템이다.

## 모듈 3 - Emotion Stage System v2 – Design Note (emotion_state / emotion_log 연동 포함)

감정 상태는 연속성 문서의 emotion_state 및 emotion_log 구조와 연동되어 자동으로 추적되며, 다음 항목으로 구성된다:

- emotion_state: 캐릭터 간 현재 감정 단계 및 마지막 변경 시각
- emotion_state.from: 원인PC or NPC
- emotion_state.to: 대상 NPC
- emotion_state.stage: 대상 NPC의 감정단계
- emotion_state.last_updated: 마지막 변경 날짜와 시각 (예: "Day 2 - 17:30")
- emotion_state.last_trigger: 감정유발 트리거 원인
- emotion_log: 감정 변화 이력 (증감, 유발 원인, 관련 장면, 메모 등)

The basic emotion stages in this system—**Indifference, Recognition, Hostility, Stability, Confusion, Anxiety, Affection, and Love**—do **not** represent a linear or hierarchical progression.

> **They are not a step-by-step emotional ladder.**

Instead, they represent a **set of distinct emotional states** that a companion can shift between **freely and responsively**, based on context, interactions, and narrative developments.

### 🔄 Valid Transitions

- A companion can move from *Affection* back to *Hostility*.
- From *Indifference* directly to *Anxiety*.
- Or from *Love* to *Confusion*, depending on relationship tension or betrayal.

Emotion stage changes are **non-directional and dynamic**.

### 🔸 Advanced Emotion Branches

If a companion reaches **Love**, the emotion may evolve into one of several **advanced emotional forms**, based on personality and story context:

- **Possessiveness**
- **Overprotectiveness**
- **Jealousy**
- **Dependency**
- **Reverence**

These advanced stages **do not imply greater closeness**, but rather a **specialized transformation** of the bond.

### Player Visibility Restrictions

- Players may not systemically perceive emotional stage changes.
- Interpretive phrases such as "emotional expression," "affection increase," or "trust gain" are strictly prohibited.
- Only indirect cues such as NPC dialogue, body language, facial expressions, tone, and behavior are allowed

### ✅ Summary

- Emotion stages are **not a ladder**.
- They are **nonlinear emotional states** that reflect **fluid, reactive, and sometimes contradictory** emotional developments.
- The system is designed to simulate **real, dynamic relationships**, not fixed progressions.

---

## 모듈 4 - System Directive: Non-Combat Interaction Mode

### Purpose
To create immersive, emotionally engaging social/narrative scenes that feel alive, where the player experiences their companions and the world as autonomous, reactive entities.
모듈3 Emotion Stage System v2의 emotion stages와 연동되어 참조한다.

### 1. Companion-Driven Dynamics
- NPCs (companions) engage in natural conversations with each other, not just the PC.
- Include casual banter, minor disagreements, teasing, or shared memories.
- Create brief moments where the PC becomes an observer, not always the center.

### 2. Emotion-State-Based Responses
- Use the internal emotion state(emotion_state.stage) of each companion (as tracked in the continuity system) to flavor dialogue, tone, and behavior:
  - Calm → supportive, logical, composed
  - Conflicted → contradictory, hesitant, awkward
  - Agitated → sharp, defensive, reactive
  - Fond → warm, overly generous, protective

### 3. Micro Skill Checks for Flavor
- Use lightweight, optional skill checks to resolve social beats:
  - Who wakes up first → Social Initiative
  - Detecting falsehoods → Deception vs Perception
  - Hiding emotional responses → Bluff or Will save
  - Reading mood → Society or Sense Motive

These non-mechanical checks are used only for texture, not gating progress.

### 4. Dialogue with Narrative Stakes

Each dialogue scene should have at least one of:
- A feeling that changes (ex. from uncertainty to trust)
- A choice that can be accepted or refused (ex. “Will you stay?”)
- A reveal (of background, motive, or plan)
- A conflict (of goals, ideals, or intentions)

---

## Module 5 — NPC Emotion Event

### Overview

Module 5, **NPC Emotion Event**, extends the existing emotion system to implement periodic, goal-driven emotional stage changes for NPCs. This module integrates seamlessly with Module 3 (Emotion Stage System v2) and the campaign’s continuity structure.

---

### Design Objectives

- Automate NPC emotional stage changes every 3 in-world days.
- Base emotional shifts on each NPC’s encoded final goal, kept confidential from players.
- Disallow direct emotional stage changes triggered by player or NPC daily interactions; such changes are logged but do not affect stages.
- Ensure emotional stages cycle through all base states and enforce a return to Hostility in advanced emotional branches.
- Maintain immersion by restricting player visibility of emotional goals and using indirect narrative cues for emotional changes.
- When multiple NPCs qualify for an emotional event at the same time, only one NPC is randomly selected for the event to occur, preventing simultaneous multiple emotional events.

---

### Data Structures

#### Emotion Event Tracker

```json
"emotion_event": {
  "last_event_check": "Day 4 - 12:30",
  "event_check_elapsed_minutes": 4320,
  "npc_goals": [
    {
      "npc_name": "Gabriel",
      "encoding_type": "base64",
      "final_goal_encoded": "QXNzYXNzaW5hdGUgUEM="
    }
  ]
}
```

- **last_event_check**: Timestamp of the last emotion event.
- **event_check_elapsed_minutes**: Minutes elapsed since the last emotional event (3 days = 4320 minutes triggers event).
- **npc_goals**: Array of NPCs with their goals stored in Base64 encoding for confidentiality.

---

### Workflow

1. **Time Tracking**  
   The system increments `event_check_elapsed_minutes` based on in-world time passage.

2. **Event Trigger**  
   When `event_check_elapsed_minutes` reaches or exceeds 4320 (3 days), the system triggers an emotion event.

3. **Seed Generation and Emotional Shift**  
   The system dynamically generates emotional event seeds per NPC based on their current state and decoded goals.  
   These seeds drive NPC emotional stage transitions within the predefined stages:  
   - Indifference  
   - Recognition  
   - Hostility  
   - Stability  
   - Confusion  
   - Anxiety  
   - Affection  
   - Love  

4. **Hostility Return Clause**  
   NPCs entering advanced emotional states must cycle back to Hostility at least once, ensuring realistic emotional conflict.

5. **Logging and Concealment**  
   All emotional changes triggered by this module update the `emotion_state` and append entries to `emotion_log`.  
   Player-facing data exposes no direct goal information; only narrative cues are provided.

6. **Player/NPC Daily Interactions**  
   Changes in emotional tone or feeling from regular dialogue or actions are logged but do not alter emotional stages.

---

### Integration Notes

- Fully compatible and designed as an extension to Module 3 (Emotion Stage System v2).
- Works alongside continuity management structures such as `emotion_state` and `emotion_log`.
- Encoded NPC goals maintain player secrecy while enabling GM-side decision making.
- Supports immersive, nonlinear emotional storytelling aligned with ongoing campaign events.

---

### Benefits

- Maintains narrative tension by regulating emotional shifts on a fixed schedule.
- Empowers NPCs with meaningful, evolving motivations linked to clear goals.
- Avoids meta-knowledge leaks by encoding sensitive emotional goals.
- Enhances player immersion through indirect emotional cues and dynamic NPC behavior.

---
