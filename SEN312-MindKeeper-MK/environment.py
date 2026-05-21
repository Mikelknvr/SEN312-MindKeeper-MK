"""
SEN312 - Lab 1: Agentic AI
MindKeeper (MK) - Study Room Environment Module
Author: Mikel Kalu | Veritas University, Abuja
"""

import random


class StudyRoomEnvironment:
    """Simulated smart study room environment for the autonomous agent."""

    IDEAL = {
        'temp': (20, 24),
        'light': (400, 600),
        'noise': (30, 45),
        'music': True,   # music helps focus when on
    }

    VALID_ACTIONS = [
        'COOL_ROOM',
        'HEAT_ROOM',
        'INCREASE_LIGHT',
        'REDUCE_LIGHT',
        'MUTE_NOISE',
        'PLAY_FOCUS_MUSIC',   # Extension: new action
        'STOP_MUSIC',          # Extension: complementary action
        'NO_OP',
    ]

    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)
        self.state = {
            'temperature':          random.uniform(15, 35),
            'light_level':          random.randint(100, 900),
            'noise_level':          random.randint(35, 85),
            'focus_music_playing':  False,   # Extension field
            'student_focus_score':  0.5,
        }
        self._update_focus_score()

    def get_state(self) -> dict:
        """Return a snapshot of the current environment state."""
        return self.state.copy()

    def apply_action(self, action: str) -> str:
        """Apply an agent action and return a feedback string."""
        if action not in self.VALID_ACTIONS:
            return f"Unknown action '{action}' ignored."

        if action == 'COOL_ROOM':
            self.state['temperature'] = max(15, self.state['temperature'] - 2)
        elif action == 'HEAT_ROOM':
            self.state['temperature'] = min(35, self.state['temperature'] + 2)
        elif action == 'INCREASE_LIGHT':
            self.state['light_level'] = min(1000, self.state['light_level'] + 100)
        elif action == 'REDUCE_LIGHT':
            self.state['light_level'] = max(0, self.state['light_level'] - 100)
        elif action == 'MUTE_NOISE':
            self.state['noise_level'] = max(30, self.state['noise_level'] - 10)
        elif action == 'PLAY_FOCUS_MUSIC':     # Extension
            self.state['focus_music_playing'] = True
        elif action == 'STOP_MUSIC':           # Extension
            self.state['focus_music_playing'] = False
        elif action == 'NO_OP':
            pass

        self._update_focus_score()
        return f"Action '{action}' applied. New state: {self.state}"

    def _update_focus_score(self):
        """
        Compute a simulated student focus score (0.0 to 1.0) based on
        environmental conditions.  Extension: focus_music_playing adds a bonus.
        """
        t = self.state['temperature']
        l = self.state['light_level']
        n = self.state['noise_level']

        temp_ok  = 1.0 if 20 <= t <= 24 else max(0.0, 1 - abs(t - 22) * 0.08)
        light_ok = 1.0 if 400 <= l <= 600 else max(0.0, 1 - abs(l - 500) * 0.002)
        noise_ok = 1.0 if n <= 45 else max(0.0, 1 - (n - 45) * 0.03)

        base_score = (temp_ok + light_ok + noise_ok) / 3

        # Extension: focus music gives a small but meaningful bonus (up to +0.10)
        music_bonus = 0.10 if self.state.get('focus_music_playing', False) else 0.0

        self.state['student_focus_score'] = round(min(1.0, base_score + music_bonus), 3)
