# SEN312 - Lab 1: MindKeeper (MK) — Agentic AI Study Room Agent
### MindKeeper Study Agent (MK)
**Author:** Mikel Kalu | Veritas University, Abuja 
**Matric:** VUG/SEN/22/8227   
**Course:** SEN312 - AI and Expert Systems

---

## Overview

This project implements an autonomous **MindKeeper Study Agent (MK)** that monitors and optimises environmental conditions (temperature, light, noise) to maximise a student's focus score. It demonstrates the full **Perception-Action-Reasoning (PAR)** loop at the heart of all agentic AI systems.

Two agent variants are implemented:
1. **MKRuleAgent** – Uses a hand-crafted expert system knowledge base (priority-ordered IF-THEN production rules).
2. **MKMKLLMAgent** – Uses Anthropic Claude as a natural language reasoning engine (requires API key).

---

## File Structure

```
lab1/
├── environment.py       # Simulated study room environment
├── agent_core.py        # Abstract base class with PAR loop
├── rule_based_agent.py  # Rule-based agent (no API key needed)
├── llm_agent.py         # LLM-driven agent (Anthropic Claude)
├── evaluate_agents.py   # Multi-run evaluation and reporting
└── README.md            # This file
```

---

## Setup

```bash
# Python 3.10+ required. No external dependencies for the rule-based agent.
# For the LLM agent, install the Anthropic SDK:
pip install anthropic

# Set your API key (for LLM agent only):
export ANTHROPIC_API_KEY='your-key-here'
```

---

## How to Run

**Run the Rule-Based Agent:**
```bash
python rule_based_agent.py
```

**Run the LLM Agent (requires API key):**
```bash
python llm_agent.py
```

**Run the Evaluation Suite:**
```bash
python evaluate_agents.py
```

---

## Extension: PLAY_FOCUS_MUSIC Action

A new action `PLAY_FOCUS_MUSIC` was added to the environment and agent beyond the base lab specification.

**What it does:**  
When the physical environment (temperature, light, noise) is already within its ideal range but the focus score is still below the 0.75 goal, the agent plays focus music. This provides a cognitive engagement bonus of +0.10 to the student's focus score.

**Rule added to the knowledge base (Rule R6):**

```
IF temperature is in [20, 24]
AND light_level is in [400, 600]
AND noise_level <= 45
AND focus_music_playing = FALSE
THEN PLAY_FOCUS_MUSIC
```

**Justification:**  
Research in cognitive psychology supports the use of ambient instrumental music (e.g., lo-fi, classical) for improving concentration in study environments. This extension makes the agent more realistic by addressing cognitive, not just physical, environmental factors.

---

## Knowledge Base Summary (MKRuleAgent)

| Rule | Condition | Action |
|------|-----------|--------|
| R1 | temperature > 24°C | COOL_ROOM |
| R2 | temperature < 20°C | HEAT_ROOM |
| R3 | noise_level > 45 dB | MUTE_NOISE |
| R4 | light_level < 400 lux | INCREASE_LIGHT |
| R5 | light_level > 600 lux | REDUCE_LIGHT |
| R6 | All physical OK AND music not playing | PLAY_FOCUS_MUSIC *(Extension)* |
| R7 | Default | NO_OP |

---

## Agent Comparison

| Feature | MKRuleAgent | MKMKLLMAgent |
|---------|---------------|----------|
| Transparency | High (rules are readable) | Moderate (reasoning in natural language) |
| Requires API Key | No | Yes |
| Adaptability | Low (fixed rules) | High (generalises to new scenarios) |
| Explainability | Built-in (rule ID + explanation) | Via prompt engineering |
| Speed | Very fast | Network-dependent |
