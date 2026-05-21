"""
SEN312 - Lab 1: Agentic AI
MindKeeper (MK) - Agent Evaluation Script
Author: Mikel Kalu | Veritas University, Abuja

Runs the MKRuleAgent over multiple seeds and produces a performance report.
Uncomment the MKLLMAgent section if you have an Anthropic API key set.
"""

import random
from environment import StudyRoomEnvironment
from rule_based_agent import MKRuleAgent
# from llm_agent import MKLLMAgent   # Uncomment if API key is available


def run_experiment(n_runs: int = 5, base_seed: int = 42, steps: int = 20):
    """
    Run n_runs independent experiments with the MKRuleAgent and
    report summary statistics.
    """
    print("\n" + "=" * 60)
    print("  SEN312 Lab 1 - Agent Evaluation Report")
    print("  Agent: MKRuleAgent (MindKeeper)")
    print(f"  Runs : {n_runs}  |  Max Steps per Run: {steps}")
    print("=" * 60)

    results = []

    for i in range(n_runs):
        seed = base_seed + i
        env   = StudyRoomEnvironment(seed=seed)
        agent = MKRuleAgent(env)
        agent.run(steps=steps)

        final_score = agent.history[-1]['focus'] if agent.history else 0.0
        steps_to_goal = next(
            (h['step'] for h in agent.history if h['focus'] >= agent.GOAL_THRESHOLD),
            None
        )
        results.append({
            'run':           i + 1,
            'seed':          seed,
            'final_score':   final_score,
            'steps_to_goal': steps_to_goal,
        })

    # ── Summary ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  EVALUATION SUMMARY")
    print("=" * 60)
    print(f"  {'Run':<5} {'Seed':<8} {'Final Score':<15} {'Goal Reached'}")
    print(f"  {'─'*4} {'─'*7} {'─'*14} {'─'*15}")

    for r in results:
        goal_str = f"Step {r['steps_to_goal']}" if r['steps_to_goal'] else "Not reached"
        print(f"  {r['run']:<5} {r['seed']:<8} {r['final_score']:<15.3f} {goal_str}")

    avg_score   = sum(r['final_score'] for r in results) / n_runs
    goal_rate   = sum(1 for r in results if r['steps_to_goal']) / n_runs * 100
    avg_steps   = (
        sum(r['steps_to_goal'] for r in results if r['steps_to_goal'])
        / max(1, sum(1 for r in results if r['steps_to_goal']))
    )

    print(f"\n  Average Final Focus Score : {avg_score:.3f}")
    print(f"  Goal Achievement Rate     : {goal_rate:.0f}%")
    if goal_rate > 0:
        print(f"  Avg Steps to Goal         : {avg_steps:.1f}")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    run_experiment(n_runs=5, base_seed=42, steps=20)
