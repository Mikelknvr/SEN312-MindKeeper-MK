"""
SEN312 - Lab 1: Agentic AI
MindKeeper (MK) - LLM-Driven Agent (uses Groq API - free)
Author: Mikel Kalu | Veritas University, Abuja


Get a free key at: console.groq.com
"""

import os
from groq import Groq

from agent_core import MKAgent
from environment import StudyRoomEnvironment


GROQ_API_KEY = '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'   


class MKLLMAgent(MKAgent):
    """
    Agent that uses Groq (free LLM API) as its reasoning engine.
    The LLM receives the current state and returns the best action.
    """

    VALID_ACTIONS = [
        'COOL_ROOM',
        'HEAT_ROOM',
        'INCREASE_LIGHT',
        'REDUCE_LIGHT',
        'MUTE_NOISE',
        'PLAY_FOCUS_MUSIC',
        'STOP_MUSIC',
        'NO_OP',
    ]

    def __init__(self, env: StudyRoomEnvironment, model: str = 'llama-3.3-70b-versatile'):
        super().__init__(env)
        api_key = GROQ_API_KEY or os.environ.get('GROQ_API_KEY')
        self.client = Groq(api_key=api_key)
        self.model = model

    def reason(self, state: dict) -> str:
        """Ask the LLM to select the best action given the current state."""
        prompt = f"""You are controlling a smart university study room.
Current sensor readings:
- Temperature      : {state['temperature']:.1f}C  (ideal: 20-24C)
- Light Level      : {state['light_level']} lux   (ideal: 400-600 lux)
- Noise Level      : {state['noise_level']} dB    (ideal: below 45 dB)
- Focus Music      : {'ON' if state.get('focus_music_playing') else 'OFF'}
- Student Focus    : {state['student_focus_score']:.3f}  (goal: above 0.75)

Available actions: {self.VALID_ACTIONS}

Rules:
- Address the most critical environmental problem first.
- If all physical conditions are already ideal, play focus music if not already playing.
- If music is playing and everything is ideal, choose NO_OP.
- Only output EXACTLY ONE action name from the list above. Nothing else."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=20,
                messages=[{'role': 'user', 'content': prompt}]
            )
            action = response.choices[0].message.content.strip().upper()
            return action if action in self.VALID_ACTIONS else 'NO_OP'
        except Exception as e:
            print(f"  [MKLLMAgent] API error: {e}. Defaulting to NO_OP.")
            return 'NO_OP'


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    env   = StudyRoomEnvironment()
    agent = MKLLMAgent(env)
    agent.run(steps=10)
