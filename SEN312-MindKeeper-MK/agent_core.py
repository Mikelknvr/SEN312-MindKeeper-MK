"""
SEN312 - Lab 1: Agentic AI
MindKeeper (MK) - Agent Core Base Class
Author: Mikel Kalu | Veritas University, Abuja
"""

from environment import StudyRoomEnvironment


class MKAgent:
    """
    Abstract base class for all MindKeeper (MK) Agent variants.
    Implements the Perception-Action-Reasoning (PAR) loop.
    """

    GOAL_THRESHOLD = 0.75

    def __init__(self, env: StudyRoomEnvironment):
        self.env = env
        self.history = []       # List of {step, action, focus} dicts
        self.step_count = 0

    # ------------------------------------------------------------------
    # PAR Loop Components
    # ------------------------------------------------------------------

    def perceive(self) -> dict:
        """Gather the current environment state (Perception)."""
        return self.env.get_state()

    def reason(self, state: dict) -> str:
        """
        Select an action based on the current state (Reasoning).
        Must be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement reason()")

    def act(self, action: str) -> str:
        """Execute the chosen action in the environment (Action)."""
        return self.env.apply_action(action)

    def evaluate(self, state: dict) -> float:
        """Return the current performance metric."""
        return state['student_focus_score']

    # ------------------------------------------------------------------
    # Main Control Loop
    # ------------------------------------------------------------------

    def run(self, steps: int = 15):
        """Run the full PAR loop for up to N steps."""
        print(f"\n{'='*60}")
        print(f"  Agent  : {self.__class__.__name__}")
        print(f"  Steps  : {steps}")
        print(f"  Goal   : focus_score >= {self.GOAL_THRESHOLD}")
        print(f"{'='*60}")

        for _ in range(steps):
            self.step_count += 1
            state   = self.perceive()
            action  = self.reason(state)
            feedback = self.act(action)
            new_state = self.perceive()
            score   = self.evaluate(new_state)

            self.history.append({
                'step':   self.step_count,
                'action': action,
                'focus':  score,
                'state':  new_state,
            })

            music_icon = " [MUSIC ON]" if new_state.get('focus_music_playing') else ""
            print(
                f"  Step {self.step_count:02d} | "
                f"Action: {action:<22s}| "
                f"Focus: {score:.3f}{music_icon}"
            )

            if score >= self.GOAL_THRESHOLD:
                print(f"\n  >>> GOAL ACHIEVED at step {self.step_count}! "
                      f"Focus = {score:.3f}")
                break

        self._print_summary()

    def _print_summary(self):
        if not self.history:
            print("  No steps taken.")
            return
        final = self.history[-1]['focus']
        goal_step = next(
            (h['step'] for h in self.history if h['focus'] >= self.GOAL_THRESHOLD),
            None
        )
        print(f"\n{'─'*60}")
        print(f"  Final focus score : {final:.3f}")
        print(f"  Goal reached      : {'Step ' + str(goal_step) if goal_step else 'Not reached'}")
        print(f"  Total steps run   : {self.step_count}")
        print(f"{'─'*60}\n")
