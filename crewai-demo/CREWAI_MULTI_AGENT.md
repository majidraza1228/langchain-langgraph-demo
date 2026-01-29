# Multi-Agent Systems with CrewAI

A hands-on demo of **CrewAI** -- an open-source, standalone framework for orchestrating role-playing, autonomous AI agents. Instead of defining graphs and state machines, you define agents with **roles, goals, and backstories** and let them collaborate as a crew.

> **Jump to:** [Why CrewAI?](#why-crewai) | [CrewAI vs LangChain/LangGraph](#crewai-vs-langchainlanggraph) | [CrewAI vs Other Frameworks](#crewai-vs-other-multi-agent-frameworks) | [Architecture](#architecture-deep-dive) | [Demo Examples](#demo-examples) | [Setup](#setup)

---

## Why CrewAI?

Building a multi-agent system in LangGraph requires defining state schemas (`TypedDict`), writing node functions, wiring graph edges, and building router logic. CrewAI replaces all of that with three concepts: **Agents** (who), **Tasks** (what), and **Crews** (how).

```python
# CrewAI: 3-agent pipeline in ~30 lines
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential
)
result = crew.kickoff()
```

The equivalent in LangGraph takes ~60-80 lines: a `TypedDict` state schema, 3 node functions, a `StateGraph` with `add_node`/`add_edge` calls, compilation, and invocation.

**CrewAI is the right choice when:**
- Your agents have clear, distinct roles (researcher, analyst, writer, reviewer)
- You want a working multi-agent prototype with minimal code
- Sequential or manager-delegates-to-specialists patterns fit your workflow
- You don't need complex branching, loops, or human-in-the-loop approvals

**Stick with LangGraph when:**
- You need fine-grained control over data flow (conditional edges, cycles, fan-out/fan-in)
- Production observability is critical (LangSmith integration)
- Human-in-the-loop approvals are required (first-class `interrupt_before`/`interrupt_after`)
- You need built-in state persistence and checkpointing

---

## CrewAI vs LangChain/LangGraph

### Philosophy

| | CrewAI | LangChain | LangGraph |
|---|---|---|---|
| **Core idea** | Role-playing agents with goals & backstories | Composable chains and integrations | Stateful graph workflows |
| **Abstraction level** | High -- describe *what* each agent does | Medium -- compose prompt/model/parser | Low-to-medium -- define *how* data flows |
| **Multi-agent** | First-class (Agent, Task, Crew) | Not built-in (single-agent focus) | Manual (graph nodes + conditional edges) |
| **Control flow** | Implicit (process type + delegation) | Linear (chain pipes) | Explicit (you wire every edge) |

### Head-to-Head: CrewAI vs LangGraph for Multi-Agent

| | CrewAI | LangGraph |
|---|---|---|
| **Setup for 3-agent pipeline** | ~30 lines | ~60-80 lines |
| **Define an agent** | `Agent(role=..., goal=..., backstory=...)` | Write a node function + craft system prompt |
| **Define a task** | `Task(description=..., expected_output=...)` | Encode in state + node logic |
| **Wire the flow** | `Crew(process=Process.sequential)` | `add_edge(START, "node1")`, `add_edge(...)` |
| **Manager/Supervisor** | `Process.hierarchical` (one line) | Custom supervisor node + Pydantic routing + conditional edges |
| **Agent delegation** | `allow_delegation=True` (agent decides) | Manual conditional edges + router functions |
| **Pass data between agents** | `context=[previous_task]` | Explicit `TypedDict` state schema, you manage every field |
| **State persistence** | Limited | Built-in checkpointing |
| **Human-in-the-loop** | `human_input=True` on tasks (basic) | First-class interrupt/approval with checkpointing |
| **Observability** | AMP Suite (emerging) | LangSmith (production-grade) |
| **Ecosystem** | Standalone, growing | 100+ integrations |
| **Loops / cycles** | Not directly supported | First-class |
| **Branching** | Only via hierarchical process | Arbitrary conditional edges |

### Code Comparison: Building a Research + Writing Pipeline

**CrewAI:**
```python
from crewai import Agent, Task, Crew, Process

researcher = Agent(
    role="Research Analyst",
    goal="Find comprehensive information on the topic",
    backstory="Experienced researcher with attention to detail",
    llm="gpt-4o"
)
writer = Agent(
    role="Content Writer",
    goal="Create engaging content from research",
    backstory="Professional writer who makes complex topics accessible",
    llm="gpt-4o"
)

research_task = Task(
    description="Research the current state of AI agents",
    expected_output="Structured summary with key findings",
    agent=researcher
)
writing_task = Task(
    description="Write a concise article from the research",
    expected_output="300-500 word article",
    agent=writer,
    context=[research_task]  # Automatically receives researcher's output
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential
)
result = crew.kickoff()
```

**LangGraph equivalent:**
```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

class State(TypedDict):
    topic: str
    research: str
    article: str

llm = ChatOpenAI(model="gpt-4o")

def research_node(state: State) -> dict:
    result = llm.invoke(f"Research: {state['topic']}")
    return {"research": result.content}

def writing_node(state: State) -> dict:
    result = llm.invoke(f"Write article based on: {state['research']}")
    return {"article": result.content}

graph = StateGraph(State)
graph.add_node("researcher", research_node)
graph.add_node("writer", writing_node)
graph.add_edge(START, "researcher")
graph.add_edge("researcher", "writer")
graph.add_edge("writer", END)
app = graph.compile()

result = app.invoke({"topic": "AI agents"})
```

The CrewAI version is shorter, but the LangGraph version gives you full control over state, edges, and can be extended with loops, branches, and human-in-the-loop without refactoring.

---

## CrewAI vs Other Multi-Agent Frameworks

| | CrewAI | AutoGen (Microsoft) | LangGraph | Swarm (OpenAI) |
|---|---|---|---|---|
| **Approach** | Role-based agents in crews | Conversational agents | Graph-based workflows | Lightweight agent handoffs |
| **Multi-agent** | First-class | First-class | Manual | First-class |
| **Delegation** | Built-in (`allow_delegation`) | Agent-to-agent chat | Manual routing | Handoff functions |
| **Process types** | Sequential, Hierarchical | Conversational | Any graph topology | Sequential handoffs |
| **Learning curve** | Low | High | High | Low |
| **Production ready** | Yes | Research-stage | Yes | Experimental |
| **Observability** | AMP Suite | Limited | LangSmith | None |
| **State management** | Task context chaining | Conversation history | Full checkpointing | Minimal |
| **Boilerplate** | ~30 lines (3 agents) | ~40 lines (2 agents) | ~60-80 lines (3 agents) | ~20 lines (2 agents) |
| **Standalone** | Yes | Yes | Needs LangChain | Needs OpenAI SDK |

### When to Use Each

```
Need multi-agent collaboration?
|
+-- No --> LangChain (single agent/chain is enough)
|
+-- Yes --> Do you need fine-grained workflow control?
              |
              +-- Yes --> Need loops, branching, fan-out/fan-in?
              |            |
              |            +-- Yes --> LangGraph
              |            |
              |            +-- No --> Need human-in-the-loop approvals?
              |                        |
              |                        +-- Yes --> LangGraph
              |                        +-- No --> CrewAI
              |
              +-- No --> Are your agents role-based specialists?
                          |
                          +-- Yes --> CrewAI
                          |
                          +-- No --> Want autonomous agent-to-agent chat?
                                      |
                                      +-- Yes --> AutoGen
                                      +-- No --> LangGraph
```

---

## Architecture Deep Dive

CrewAI is built around **5 core primitives** that map directly to how a real-world team operates:

```
+-----------------------------------------------------+
|                      CREW                            |
|  (The team -- bundles agents + tasks + process)      |
|                                                      |
|   Process: Sequential | Hierarchical                 |
|                                                      |
|   +----------+  +----------+  +----------+           |
|   |  AGENT   |  |  AGENT   |  |  AGENT   |           |
|   | -------- |  | -------- |  | -------- |           |
|   | role     |  | role     |  | role     |           |
|   | goal     |  | goal     |  | goal     |           |
|   | backstory|  | backstory|  | backstory|           |
|   | tools[ ] |  | tools[ ] |  | tools[ ] |           |
|   +----+-----+  +----+-----+  +----+-----+           |
|        |              |              |                |
|   +----v-----+  +----v-----+  +----v-----+           |
|   |   TASK   |  |   TASK   |  |   TASK   |           |
|   | -------- |  | -------- |  | -------- |           |
|   | desc     |  | desc     |-->| desc     |           |
|   | expected |  | expected |  | expected |           |
|   | context[]|  | context[]|  | context[]|           |
|   +----------+  +----------+  +----------+           |
+-----------------------------------------------------+
```

### 1. Agents -- The Team Members

Each agent is an LLM wrapped with a persona. The `role`, `goal`, and `backstory` are injected into the system prompt to shape behavior.

| Parameter | Purpose |
|-----------|---------|
| `role` | Job title -- defines specialization |
| `goal` | What the agent is trying to achieve |
| `backstory` | Context and personality -- guides behavior |
| `llm` | Which model to use (default: gpt-4) |
| `tools` | List of tools the agent can call |
| `allow_delegation` | Let the agent hand off work to others |
| `verbose` | Print detailed execution logs |

Under the hood, CrewAI builds a structured system prompt from `role` + `goal` + `backstory`, then uses ReAct-style reasoning (Thought -> Action -> Observation) when the agent has tools.

### 2. Tasks -- The Work Items

| Parameter | Required | Purpose |
|-----------|----------|---------|
| `description` | Yes | What needs to be done |
| `expected_output` | Yes | Definition of done |
| `agent` | No | Which agent handles this |
| `context` | No | List of tasks whose outputs feed into this one |
| `output_file` | No | Save result to a file |
| `output_pydantic` | No | Enforce structured output via Pydantic model |
| `human_input` | No | Ask for human review before finalizing |

**Key feature -- context chaining:** When Task B has `context=[task_a]`, it automatically receives Task A's output. No state schemas or graph edges needed.

### 3. Tools -- The Capabilities

Custom tools use the `@tool` decorator. CrewAI also ships built-in tools via `crewai-tools` (web scraping, file reading, PDF parsing) and supports LangChain-compatible tools.

```python
from crewai.tools import tool

@tool("Word Counter")
def word_counter(text: str) -> str:
    """Count the number of words in the given text."""
    return f"The text contains {len(text.split())} words."
```

### 4. Crews -- The Team

Brings agents and tasks together under a process type.

### 5. Processes -- How Work Gets Organized

| Process | How It Works | Analogy |
|---------|-------------|---------|
| `Process.sequential` | Tasks run in order: Task 1 -> 2 -> 3 | Assembly line |
| `Process.hierarchical` | Manager agent auto-created, delegates to specialists, validates results | Manager + team |

### Execution Flow

```
crew.kickoff()
       |
       +-- Sequential Process
       |     |
       |     +-- Task 1: Agent A executes
       |     |     +-- Receives: task description
       |     |     +-- Reasons: using role/goal/backstory
       |     |     +-- Acts: calls tools if needed
       |     |     +-- Delegates: to another agent (if allow_delegation=True)
       |     |     +-- Returns: output matching expected_output
       |     |
       |     +-- Task 2: Agent B executes
       |     |     +-- Receives: task description + Task 1 output (via context)
       |     |
       |     +-- Task 3: Agent C executes
       |           +-- Receives: task description + prior outputs (via context)
       |           +-- Returns: final result
       |
       +-- Hierarchical Process
             |
             +-- Manager agent (auto-created) reads all tasks
             +-- Manager: "Task 1 goes to Agent A"
             +-- Agent A executes, returns result to manager
             +-- Manager validates, assigns Task 2 to Agent B
             +-- Agent B executes with context
             +-- Manager validates, assigns Task 3
             +-- Returns: final validated result
```

---

## Demo Examples

This notebook (`Demo_CrewAI_Multi_Agent.ipynb`) includes three complete examples:

### Example 1: Sequential Process

Tasks run one after another, each building on the previous output:

```
Researcher --> Writer --> Editor --> Final Article
```

Three agents collaborate on writing an article about AI agents in 2025. The researcher gathers facts, the writer creates the article, and the editor polishes it.

### Example 2: Hierarchical Process

A manager agent automatically delegates work to specialists:

```
                        +--> Data Analyst
Manager (auto-created) -+--> Business Strategist
                        +--> Report Writer
```

The crew performs a business analysis of the AI SaaS market, producing an executive report with market analysis and strategic recommendations. Compare this with Demo 5's supervisor pattern in LangGraph -- same concept, but CrewAI needs just `process=Process.hierarchical` vs building a custom supervisor node with Pydantic routing.

### Example 3: Agent Delegation

When `allow_delegation=True`, agents autonomously decide to hand off work:

```
Lead Developer (allow_delegation=True)
    +-- "I need code review" --> Code Reviewer
    +-- "I need tests" -------> QA Engineer
```

A lead developer builds an email validation function and delegates review and testing to specialists -- no extra wiring needed. In LangGraph, this would require explicit conditional edges and a router function.

---

## Best Practices

1. **Start with sequential** -- add hierarchy only when you need dynamic delegation
2. **Keep agents focused** -- one role per agent, clear goals
3. **Use context chaining** -- `context=[previous_task]` to pass outputs forward
4. **Be specific in descriptions** -- vague tasks produce vague results
5. **Monitor token usage** -- each agent makes LLM calls; more agents = more tokens
6. **Set `verbose=True` during development** -- turn it off in production

---

## Setup

### Prerequisites

- Python >= 3.10
- OpenAI API key

### Installation

```bash
cd crewai-demo

python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

### API Key

The notebook looks for `OPENAI_API_KEY` in these locations (in order):

1. `../langchain-langgraph-demo/.env` (shared with the main demo)
2. `../.env`
3. `.env` (local to this folder)

Create a `.env` file with:

```
OPENAI_API_KEY=your_key_here
```

### Run

```bash
jupyter notebook Demo_CrewAI_Multi_Agent.ipynb
```

## Key Dependencies

| Package | Purpose |
|---------|---------|
| `crewai` | Core framework for agents, tasks, and crews |
| `crewai-tools` | Built-in tools (web search, file read, scraping) |
| `python-dotenv` | Load API keys from `.env` files |
| `langchain-openai` | OpenAI model integration |

## Resources

- [CrewAI Documentation](https://docs.crewai.com)
- [CrewAI GitHub](https://github.com/crewAIInc/crewAI)
- [Demo 5: Multi-Agent Systems with LangGraph](../Demo_5_Multi_Agent_Systems.ipynb) -- LangGraph comparison
- [FRAMEWORKS_COMPARISON.md](../FRAMEWORKS_COMPARISON.md) -- Full framework comparison (LangChain, LlamaIndex, AutoGen, Haystack, and more)
