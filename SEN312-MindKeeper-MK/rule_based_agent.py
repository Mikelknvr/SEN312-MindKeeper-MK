"""
SEN312 - Lab 1: Agentic AI
MindKeeper (MK) - Rule-Based Expert Agent
Author: Mikel Kalu | Veritas University, Abuja

Extension: Added PLAY_FOCUS_MUSIC action and corresponding rule.
Rule R6: If all primary conditions (temperature, noise, light) are within
         their ideal ranges but the focus score is still below target,
         playing focus music provides a productivity boost.
"""

from agent_core import MKAgent
from environment import StudyRoomEnvironment


class MKRuleAgent(MKAgent):
    """
    MindKeeper Rule Agent: expert-system style agent using a priority-ordered knowledge base of
    hand-crafted IF-THEN production rules.

    Knowledge Base (Priority Order):
    ---------------------------------
    R1: IF temperature > 24        THEN COOL_ROOM
    R2: IF temperature < 20        THEN HEAT_ROOM
    R3: IF noise_level > 45        THEN MUTE_NOISE
    R4: IF light_level < 400       THEN INCREASE_LIGHT
    R5: IF light_level > 600       THEN REDUCE_LIGHT
    R6: IF all primary OK AND      THEN PLAY_FOCUS_MUSIC   [EXTENSION]
        focus_music NOT playing
    R7: DEFAULT                    THEN NO_OP
    """

    RULES = [
        # (condition_lambda, action_string, rule_id, explanation)
        (
            lambda s: s['temperature'] > 24,
            'COOL_ROOM',
            'R1',
            'Temperature exceeds ideal upper bound of 24C.'
        ),
        (
            lambda s: s['temperature'] < 20,
            'HEAT_ROOM',
            'R2',
            'Temperature is below ideal lower bound of 20C.'
        ),
        (
            lambda s: s['noise_level'] > 45,
            'MUTE_NOISE',
            'R3',
            'Noise level exceeds 45dB threshold, reducing focus.'
        ),
        (
            lambda s: s['light_level'] < 400,
            'INCREASE_LIGHT',
            'R4',
            'Light level is below 400 lux; insufficient for study.'
        ),
        (
            lambda s: s['light_level'] > 600,
            'REDUCE_LIGHT',
            'R5',
            'Light level exceeds 600 lux; may cause glare and eye strain.'
        ),
        # EXTENSION RULE R6: Play focus music when physical environment is
        # already optimal but the student still needs a focus boost.
        (
            lambda s: (
                20 <= s['temperature'] <= 24
                and 400 <= s['light_level'] <= 600
                and s['noise_level'] <= 45
                and not s.get('focus_music_playing', False)
            ),
            'PLAY_FOCUS_MUSIC',
            'R6',
            'Physical environment is optimal. Playing focus music to '
            'boost cognitive engagement. (Extension rule)'
        ),
        (
            lambda s: True,
            'NO_OP',
            'R7',
            'All conditions are already at their optimal values.'
        ),
    ]

    def reason(self, state: dict) -> str:
        """
        Forward chain through the ordered rule set and return the action
        of the first rule whose condition evaluates to True.
        """
        for condition, action, rule_id, explanation in self.RULES:
            if condition(state):
                return action
        return 'NO_OP'

    def explain(self, state: dict) -> str:
        """Explanation facility: report which rule fired and why."""
        for condition, action, rule_id, explanation in self.RULES:
            if condition(state):
                return f"[{rule_id}] Action '{action}' selected because: {explanation}"
        return "[R7] No applicable rule found. Defaulting to NO_OP."


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    env   = StudyRoomEnvironment()
    agent = MKRuleAgent(env)
    agent.run(steps=15)
