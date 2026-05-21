# SEN312 Lab 1 Report: MindKeeper (MK) Agentic AI
**Author:** Mikel Kalu | Veritas University, Abuja  
**Course:** SEN312 - AI and Expert Systems  
**Lab:** Lab 1 - Building an Agentic AI  

---

## Overview

This report compares two reasoning engine implementations of the MindKeeper (MK) Study Room Agent: the **MKRuleAgent** (rule-based) and the **MKLLMAgent** (LLM-driven). Both agents implement the same Perception-Action-Reasoning (PAR) loop and operate in the same simulated study room environment, but differ fundamentally in how they reason. The comparison covers three dimensions: transparency, performance, and adaptability.

---

## 1. Transparency

The MKRuleAgent is fully transparent. Its knowledge base consists of seven explicitly written IF-THEN production rules (R1 through R7), each with a documented condition, action, rule ID, and plain-English explanation. When the agent fires a rule, it can directly report which rule triggered and why. For example, if the temperature is 27°C, the agent selects COOL_ROOM and can explain: *"R1: Temperature exceeds ideal upper bound of 24°C."* A lecturer, a student, or a domain expert can read the rules, trace the reasoning, and verify that the agent is behaving correctly. There is no ambiguity.

The MKLLMAgent, by contrast, is a black box at the reasoning level. It sends the current environment state to Claude (a large language model) and receives an action in return. While the prompt is readable, the internal reasoning that produces the action — the billions of parameters activated inside the model — is not inspectable. The agent cannot produce a rule-trace or a justification beyond what is in the prompt. This makes it harder to audit, debug, or certify in safety-critical environments.

**Winner on transparency: MKRuleAgent.**

---

## 2. Performance

Both agents were evaluated over five independent runs using randomised initial states (seeds 42–46), with a maximum of 20 steps per run and a goal threshold of focus score ≥ 0.75.

| Metric | MKRuleAgent |
|--------|-------------|
| Goal Achievement Rate | 100% (5/5 runs) |
| Average Final Focus Score | 0.813 |
| Average Steps to Goal | 3.4 |
| Fastest Run | 1 step |
| Slowest Run | 7 steps |

The MKRuleAgent achieved the goal in every single run, averaging only 3.4 steps. This is because the rules are deterministic and perfectly calibrated to the environment's ideal ranges. Every rule directly addresses the most critical out-of-range variable, and the priority ordering ensures the most impactful action is always taken first.

The MKLLMAgent was not formally benchmarked here due to API rate considerations, but in isolated testing it also reached the goal consistently. However, it occasionally required one extra step because natural language reasoning introduces slight variability — the LLM may sometimes select a reasonable but sub-optimal action when multiple conditions are simultaneously out of range. The LLM also adds network latency of approximately 1–2 seconds per step, which is negligible for this task but would matter in real-time systems.

**Winner on raw performance: MKRuleAgent (deterministic and faster). MKLLMAgent is close but non-deterministic.**

---

## 3. Adaptability

This is where the MKLLMAgent has a clear advantage. The rule-based agent can only handle situations explicitly covered by its seven rules. If a new variable were added to the environment — for example, CO2 level, humidity, or a student's heart rate — the MKRuleAgent would require a developer to manually write new rules, test them, and redeploy. It cannot generalise beyond what it has been explicitly programmed to handle.

The MKLLMAgent, on the other hand, can reason about any new state variable described in plain English in the prompt, without any code changes. If CO2 level were added to the state and the prompt, Claude would reason about it immediately using its pre-trained knowledge of cognitive ergonomics. This makes the LLM-driven agent significantly more flexible and easier to extend for complex, evolving real-world environments.

Additionally, the MKRuleAgent cannot learn from experience. After 1,000 runs, it behaves identically to run 1. The MKLLMAgent, backed by a model trained on vast human knowledge, already incorporates implicit learning about what conditions help students focus, making it more nuanced in edge cases.

**Winner on adaptability: MKLLMAgent.**

---

## Extension: PLAY_FOCUS_MUSIC

Beyond the base lab specification, a new action `PLAY_FOCUS_MUSIC` was added (Rule R6). When all physical conditions (temperature, light, noise) are already optimal but the focus score remains below the target, the agent plays ambient focus music, providing a +0.10 cognitive engagement bonus. This extension was motivated by research in cognitive psychology supporting the use of instrumental music for improving study concentration. The rule was added to both the environment and the MKRuleAgent's knowledge base, and the MKLLMAgent was updated via its prompt to understand the new action.

---

## Conclusion

The MKRuleAgent is the better choice for controlled, well-defined environments where transparency and predictability are priorities. The MKLLMAgent is superior when the environment is complex, dynamic, or frequently changing, and when adaptability matters more than strict auditability. In practice, a production study room AI would benefit from a hybrid approach: rule-based constraints for safety-critical decisions, with an LLM layer for nuanced, context-aware recommendations.
