#!/usr/bin/env python3
"""LangGraph multi-agent demo with evaluation harness.

Requires:
  - langchain
  - langchain-openai
  - langgraph
  - pydantic

Set OPENAI_API_KEY in your environment.
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END


# -------------------------
# Models and config
# -------------------------

@dataclass
class AgentConfig:
    model: str
    temperature: float
    seed: Optional[int]


def build_llm(cfg: AgentConfig) -> ChatOpenAI:
    kwargs = {}
    if cfg.seed is not None:
        kwargs["seed"] = cfg.seed
    return ChatOpenAI(model=cfg.model, temperature=cfg.temperature, **kwargs)


# -------------------------
# Multi-agent graph
# -------------------------

class GraphState(BaseModel):
    task: str
    plan: Optional[str] = None
    draft: Optional[str] = None
    critique: Optional[str] = None
    final: Optional[str] = None


def planner_node(state: GraphState, cfg: AgentConfig) -> Dict[str, str]:
    llm = build_llm(cfg)
    msgs = [
        SystemMessage(content="You are the Planner. Output a short numbered plan."),
        HumanMessage(content=state.task),
    ]
    plan = llm.invoke(msgs).content
    return {"plan": plan}


def solver_node(state: GraphState, cfg: AgentConfig) -> Dict[str, str]:
    llm = build_llm(cfg)
    prompt = (
        f"Task: {state.task}\n\n"
        f"Plan:\n{state.plan}\n\n"
        "Write a concise answer."
    )
    msgs = [
        SystemMessage(content="You are the Solver. Produce the best final answer."),
        HumanMessage(content=prompt),
    ]
    draft = llm.invoke(msgs).content
    return {"draft": draft}


def critic_node(state: GraphState, cfg: AgentConfig) -> Dict[str, str]:
    llm = build_llm(cfg)
    prompt = (
        f"Task: {state.task}\n\n"
        f"Draft:\n{state.draft}\n\n"
        "Review the draft. Point out gaps and improvements."
    )
    msgs = [
        SystemMessage(content="You are the Critic. Be direct and specific."),
        HumanMessage(content=prompt),
    ]
    critique = llm.invoke(msgs).content
    return {"critique": critique}


def revise_node(state: GraphState, cfg: AgentConfig) -> Dict[str, str]:
    llm = build_llm(cfg)
    prompt = (
        f"Task: {state.task}\n\n"
        f"Draft:\n{state.draft}\n\n"
        f"Critique:\n{state.critique}\n\n"
        "Improve the draft to address the critique."
    )
    msgs = [
        SystemMessage(content="You are the Solver. Revise the answer."),
        HumanMessage(content=prompt),
    ]
    final = llm.invoke(msgs).content
    return {"final": final}


def build_graph(cfg: AgentConfig):
    graph = StateGraph(GraphState)
    graph.add_node("planner", lambda s: planner_node(s, cfg))
    graph.add_node("solver", lambda s: solver_node(s, cfg))
    graph.add_node("critic", lambda s: critic_node(s, cfg))
    graph.add_node("reviser", lambda s: revise_node(s, cfg))

    graph.set_entry_point("planner")
    graph.add_edge("planner", "solver")
    graph.add_edge("solver", "critic")
    graph.add_edge("critic", "reviser")
    graph.add_edge("reviser", END)

    return graph.compile()


def run_multi_agent(task: str, cfg: AgentConfig) -> GraphState:
    app = build_graph(cfg)
    result = app.invoke({"task": task})
    return GraphState(**result)


def run_single_agent(task: str, cfg: AgentConfig) -> str:
    llm = build_llm(cfg)
    msgs = [
        SystemMessage(content="You are the Solver. Provide the best possible answer."),
        HumanMessage(content=task),
    ]
    return llm.invoke(msgs).content


# -------------------------
# Eval engineering
# -------------------------

@dataclass
class EvalCase:
    name: str
    prompt: str
    must_have: Tuple[str, ...]
    expects_json: bool = False


class PlanJSON(BaseModel):
    title: str
    milestones: List[str]
    risks: List[str]


class RubricScore(BaseModel):
    clarity: int
    completeness: int
    correctness: int
    overall: int
    rationale: str


class Evaluator:
    def __init__(self, cases: Sequence[EvalCase]) -> None:
        self.cases = list(cases)

    @staticmethod
    def keyword_score(output: str, must_have: Sequence[str]) -> float:
        out = output.lower()
        hits = sum(1 for k in must_have if k.lower() in out)
        return hits / max(1, len(must_have))

    @staticmethod
    def json_schema_pass(output: str) -> bool:
        try:
            data = json.loads(output)
            PlanJSON(**data)
            return True
        except (json.JSONDecodeError, ValidationError):
            return False

    @staticmethod
    def rubric_score(llm: ChatOpenAI, task: str, output: str) -> RubricScore:
        prompt = (
            "Score the output on 1-5 for clarity, completeness, correctness, and overall. "
            "Return JSON matching the schema.\n\n"
            f"Task:\n{task}\n\n"
            f"Output:\n{output}"
        )
        structured = llm.with_structured_output(RubricScore)
        return structured.invoke(prompt)

    @staticmethod
    def pairwise_preference(llm: ChatOpenAI, task: str, a: str, b: str) -> str:
        prompt = (
            "Compare Output A and Output B for the task. "
            "Return only 'A', 'B', or 'TIE'.\n\n"
            f"Task:\n{task}\n\n"
            f"Output A:\n{a}\n\n"
            f"Output B:\n{b}"
        )
        msg = llm.invoke(prompt).content.strip().upper()
        return msg if msg in {"A", "B", "TIE"} else "TIE"

    def run(
        self,
        cfg: AgentConfig,
        use_llm_judge: bool,
        seeds: Sequence[int],
    ) -> Dict[str, Dict[str, float]]:
        llm = build_llm(cfg) if use_llm_judge else None
        results: Dict[str, Dict[str, float]] = {}

        for case in self.cases:
            keyword_scores: List[float] = []
            schema_passes: List[float] = []
            rubric_scores: List[float] = []
            pairwise_wins: List[float] = []

            for seed in seeds:
                cfg_seeded = AgentConfig(cfg.model, cfg.temperature, seed)
                multi = run_multi_agent(case.prompt, cfg_seeded).final or ""
                baseline = run_single_agent(case.prompt, cfg_seeded)

                keyword_scores.append(self.keyword_score(multi, case.must_have))
                if case.expects_json:
                    schema_passes.append(1.0 if self.json_schema_pass(multi) else 0.0)

                if use_llm_judge and llm is not None:
                    rubric = self.rubric_score(llm, case.prompt, multi)
                    rubric_scores.append(rubric.overall)
                    pref = self.pairwise_preference(llm, case.prompt, multi, baseline)
                    pairwise_wins.append(1.0 if pref == "A" else 0.5 if pref == "TIE" else 0.0)

            results[case.name] = {
                "keyword": statistics.mean(keyword_scores),
                "schema_pass": statistics.mean(schema_passes) if schema_passes else float("nan"),
                "rubric_overall": statistics.mean(rubric_scores) if rubric_scores else float("nan"),
                "pairwise_win": statistics.mean(pairwise_wins) if pairwise_wins else float("nan"),
            }

        return results


def default_cases() -> List[EvalCase]:
    return [
        EvalCase(
            name="launch_plan",
            prompt="Draft a concise launch plan for a weather app.",
            must_have=("plan", "launch", "risk", "metric"),
        ),
        EvalCase(
            name="meeting_summary",
            prompt="Summarize a meeting: include goals, blockers, and next steps.",
            must_have=("goals", "blockers", "next"),
        ),
        EvalCase(
            name="json_plan",
            prompt=(
                "Return ONLY JSON with fields: title (string), milestones (list of 3 strings), "
                "risks (list of strings)."
            ),
            must_have=("title", "milestones", "risks"),
            expects_json=True,
        ),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="LangGraph multi-agent + eval engineering demo")
    parser.add_argument("--task", default="Create a short launch plan for a weather app.")
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--run-eval", action="store_true")
    parser.add_argument("--use-llm-judge", action="store_true")
    args = parser.parse_args()

    # Load .env from the script folder, then fall back to repo root if present.
    script_dir = os.path.dirname(__file__)
    load_dotenv(os.path.join(script_dir, ".env"))
    load_dotenv(os.path.join(os.path.dirname(script_dir), ".env"))
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set.")

    cfg = AgentConfig(model=args.model, temperature=args.temperature, seed=args.seed)
    result = run_multi_agent(args.task, cfg)

    print("=== PLAN ===")
    print(result.plan)
    print("\n=== DRAFT ===")
    print(result.draft)
    print("\n=== CRITIQUE ===")
    print(result.critique)
    print("\n=== FINAL ===")
    print(result.final)

    if args.run_eval:
        evaluator = Evaluator(default_cases())
        scores = evaluator.run(cfg, use_llm_judge=args.use_llm_judge, seeds=[1, 2, 3])
        print("\n=== EVAL SCORES (avg over seeds) ===")
        for name, s in scores.items():
            print(
                f"{name}: keyword={s['keyword']:.2f} "
                f"schema_pass={s['schema_pass']:.2f} "
                f"rubric_overall={s['rubric_overall']:.2f} "
                f"pairwise_win={s['pairwise_win']:.2f}"
            )


if __name__ == "__main__":
    main()
