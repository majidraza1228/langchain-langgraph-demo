#!/usr/bin/env python3
"""Multi-agent demo with a lightweight evaluation harness.

This runs without external dependencies. If you want to plug in a real LLM,
implement the LLMClient.generate method and set USE_REAL_LLM=true.
"""
from __future__ import annotations

import argparse
import random
import textwrap
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple


@dataclass
class Message:
    role: str
    content: str


class LLMClient:
    """Minimal interface for text generation."""

    def generate(self, messages: Sequence[Message], seed: int | None = None) -> str:
        raise NotImplementedError


class ToyLLM(LLMClient):
    """Deterministic placeholder model for offline demo purposes."""

    def generate(self, messages: Sequence[Message], seed: int | None = None) -> str:
        rng = random.Random(seed)
        joined = "\n".join(f"{m.role}: {m.content}" for m in messages)
        # Very simple patterning to simulate different agent styles.
        if "You are the Planner" in joined:
            bullets = [
                "Clarify requirements and success criteria",
                "Design architecture and data sources",
                "Build MVP and iterate on UX",
                "Add monitoring, analytics, and launch checklist",
            ]
            rng.shuffle(bullets)
            return "Plan:\n" + "\n".join(f"- {b}" for b in bullets[:3])
        if "You are the Critic" in joined:
            critiques = [
                "Check for missing risks or constraints",
                "Ensure outputs are measurable and testable",
                "Add a fallback or validation step",
            ]
            return "Review:\n" + "\n".join(f"- {c}" for c in critiques)
        # Solver/default
        options = [
            "Here is a concise response with clear steps and risks.",
            "Answer includes scope, milestones, and validation points.",
            "Provides a structured plan and brief rationale.",
        ]
        return options[rng.randint(0, len(options) - 1)]


@dataclass
class Agent:
    name: str
    system_prompt: str
    llm: LLMClient

    def respond(self, user_prompt: str, seed: int | None = None) -> str:
        messages = [
            Message(role="system", content=self.system_prompt),
            Message(role="user", content=user_prompt),
        ]
        return self.llm.generate(messages, seed=seed)


class MultiAgentOrchestrator:
    def __init__(self, llm: LLMClient) -> None:
        self.planner = Agent(
            name="Planner",
            system_prompt="You are the Planner. Output a short numbered plan.",
            llm=llm,
        )
        self.solver = Agent(
            name="Solver",
            system_prompt="You are the Solver. Produce the final answer.",
            llm=llm,
        )
        self.critic = Agent(
            name="Critic",
            system_prompt="You are the Critic. Point out gaps and improvements.",
            llm=llm,
        )

    def run(self, task: str, seed: int | None = None) -> Dict[str, str]:
        plan = self.planner.respond(task, seed=seed)
        draft = self.solver.respond(
            f"Task: {task}\n\nPlan:\n{plan}\n\nWrite the answer.",
            seed=seed,
        )
        critique = self.critic.respond(
            f"Task: {task}\n\nDraft:\n{draft}\n\nReview the draft.",
            seed=seed,
        )
        revised = self.solver.respond(
            f"Task: {task}\n\nDraft:\n{draft}\n\nCritique:\n{critique}\n\nImprove the draft.",
            seed=seed,
        )
        return {
            "plan": plan,
            "draft": draft,
            "critique": critique,
            "final": revised,
        }


@dataclass
class EvalCase:
    name: str
    prompt: str
    must_have: Tuple[str, ...]


class Evaluator:
    """Simple keyword-based evaluator for demo purposes."""

    def __init__(self, cases: Sequence[EvalCase]) -> None:
        self.cases = list(cases)

    def score(self, output: str, case: EvalCase) -> float:
        output_lower = output.lower()
        hits = sum(1 for k in case.must_have if k.lower() in output_lower)
        return hits / max(1, len(case.must_have))

    def run(self, orchestrator: MultiAgentOrchestrator, seeds: Sequence[int]) -> Dict[str, float]:
        results: Dict[str, float] = {}
        for case in self.cases:
            scores: List[float] = []
            for seed in seeds:
                final = orchestrator.run(case.prompt, seed=seed)["final"]
                scores.append(self.score(final, case))
            results[case.name] = sum(scores) / len(scores)
        return results


def build_default_eval_cases() -> List[EvalCase]:
    return [
        EvalCase(
            name="weather_app_plan",
            prompt="Create a concise launch plan for a weather app.",
            must_have=("plan", "launch", "risk"),
        ),
        EvalCase(
            name="meeting_summary",
            prompt="Summarize a meeting: discuss goals, blockers, next steps.",
            must_have=("goals", "blockers", "next"),
        ),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-agent demo with eval harness")
    parser.add_argument("--task", default="Draft a short launch plan for a weather app.")
    parser.add_argument("--run-eval", action="store_true")
    args = parser.parse_args()

    llm = ToyLLM()
    orchestrator = MultiAgentOrchestrator(llm)

    result = orchestrator.run(args.task, seed=7)
    print("=== PLAN ===")
    print(result["plan"])
    print("\n=== DRAFT ===")
    print(result["draft"])
    print("\n=== CRITIQUE ===")
    print(result["critique"])
    print("\n=== FINAL ===")
    print(result["final"])

    if args.run_eval:
        evaluator = Evaluator(build_default_eval_cases())
        scores = evaluator.run(orchestrator, seeds=[1, 2, 3])
        print("\n=== EVAL SCORES (avg over seeds) ===")
        for name, score in scores.items():
            print(f"{name}: {score:.2f}")


if __name__ == "__main__":
    main()
