# Multi-Agent + Eval Engineering (Concise Guide)

This guide explains **eval engineering** and how it’s applied in the demo program.

## What is eval engineering?
Eval engineering is the practice of **measuring model or agent performance** in a way that is repeatable, traceable, and aligned with real product goals. In practice, it means turning “good enough” into a **measurable target** and continuously checking that changes don’t regress performance.

## Why it matters for multi-agent systems
Multi-agent pipelines can fail in subtle ways (bad plans, weak critiques, shallow synthesis). Eval engineering helps you:
- Detect regressions when you change prompts/roles
- Compare agent strategies and prompts objectively
- Guardrail outputs with measurable requirements

## Common eval types
- **Golden tests:** fixed prompts with expected answers or keywords
- **Rubric grading:** score outputs on criteria (clarity, completeness, correctness)
- **Pairwise preference:** A/B comparisons between outputs
- **Task success checks:** objective validators (e.g., JSON schema, test suite)

## A minimal eval loop
1) **Define goals** (e.g., “plan must include risks and launch steps”).
2) **Collect or write test cases** that represent your real usage.
3) **Choose metrics** (keyword hits, rubric score, pass/fail).
4) **Run regularly** (CI or local) and **track drift**.
5) **Analyze failures** and refine prompts/agents.

## How the demo applies eval engineering
The demo includes a small evaluator that:
- Runs multiple **seeded** trials to check stability.
- Uses **keyword-based scoring** to mimic a basic rubric.
- Produces average scores per test case.

This is intentionally simple, but it shows the workflow you can scale up to
human grading, model-graded rubrics, or unit-test style validators.

## How to run
```bash
python3 multiagent_eval_demo.py
python3 multiagent_eval_demo.py --run-eval
```

## Next steps (if you want a production eval)
- Use a **real LLM** for the agent responses.
- Add **human-graded** rubrics for quality.
- Log results over time and track regressions.
- Expand the test suite to cover edge cases and failures.
