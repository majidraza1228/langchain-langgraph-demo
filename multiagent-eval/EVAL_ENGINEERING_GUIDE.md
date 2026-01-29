# Eval Engineering: Why It Matters (With This Demo)

Eval engineering is the discipline of **measuring model/agent quality** in a way that’s repeatable, aligned with product goals, and resistant to regressions.

## The value of eval engineering
- **Protects you from silent regressions** when you tweak prompts, tools, or models.
- **Turns vague quality into concrete targets** ("must include risks", "must be valid JSON").
- **Lets you compare strategies** (single-agent vs multi-agent) with evidence.
- **Shows stability** across different random seeds or temperatures.

## What this demo evaluates
This repo contains a LangGraph multi-agent workflow + an evaluation harness:

- Multi-agent graph: Planner → Solver → Critic → Reviser
- Baseline: single-agent response
- Evaluation types:
  1) **Keyword coverage** (simple golden tests)
  2) **Schema validation** (structural correctness)
  3) **LLM rubric grading** (clarity/completeness/correctness)
  4) **Pairwise preference** (A/B evaluation against baseline)

Each eval type highlights a different failure mode:
- **Keyword** catches missing requirements.
- **Schema** catches structural invalidity.
- **Rubric** catches quality regressions that keywords miss.
- **Pairwise** shows whether multi-agent is *actually better*.

## How to run
```bash
# Run the multi-agent workflow
python3 multiagent_eval_langgraph.py

# Run evals without LLM judge (keyword + schema only)
python3 multiagent_eval_langgraph.py --run-eval

# Run full evals including LLM judge (rubric + pairwise)
python3 multiagent_eval_langgraph.py --run-eval --use-llm-judge
```

## Where to look in code
- Multi-agent graph: `multiagent_eval_langgraph.py`
- Eval harness: `Evaluator` class in the same file

## What to change if you want stronger evidence
- Add **more cases** from your real user prompts.
- Add **hard validators** (JSON schema, unit tests, SQL validation).
- Track results over time (store scores in a file or DB).
- Use **human review** for high-stakes quality decisions.
