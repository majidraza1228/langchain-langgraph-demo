# Multi-Agent Systems with CrewAI

A hands-on demo of **CrewAI** -- an open-source framework for orchestrating role-playing, autonomous AI agents. Instead of defining graphs and state machines (like LangGraph), you define agents with **roles, goals, and backstories** and let them collaborate as a crew.

## What This Demo Covers

| Section | Description |
|---------|-------------|
| **CrewAI vs LangChain/LangGraph** | Philosophy, pros, cons, and side-by-side comparison |
| **Core Concepts** | Agents, Tasks, Tools, Crews, and Processes |
| **Example 1: Sequential Process** | Research & Writing pipeline (Researcher --> Writer --> Editor) |
| **Example 2: Hierarchical Process** | Manager agent auto-delegates to specialists |
| **Example 3: Agent Delegation** | Agents hand off work to each other autonomously |

## How CrewAI Works

| Concept | Real-World Analogy |
|---------|-------------------|
| **Agent** | A team member with a job title, expertise, and personality |
| **Task** | A work item assigned to a team member |
| **Tool** | Software or resources the team member can use |
| **Crew** | The team itself |
| **Process** | How the team organizes work (sequential vs. hierarchical) |

## CrewAI vs LangGraph

| | CrewAI | LangGraph |
|---|---|---|
| **Core idea** | Role-playing agents with goals & backstories | Stateful graphs with explicit control flow |
| **Multi-agent** | First-class primitives (agents, tasks, crews) | Built manually via graph nodes and edges |
| **Control flow** | Implicit (process type + delegation) | Explicit (you wire every edge and condition) |
| **Setup effort** | ~30 lines for 3-agent pipeline | ~60-80 lines for equivalent pipeline |
| **Best for** | Quick prototypes, role-based teams | Complex branching, production systems |

### When to Use Which

| Scenario | Recommendation |
|----------|---------------|
| Quick multi-agent prototype | **CrewAI** |
| Complex branching/looping workflows | **LangGraph** |
| Role-based teams (researcher, writer, editor) | **CrewAI** |
| Production system with deep observability | **LangGraph + LangSmith** |
| Human-in-the-loop approvals | **LangGraph** |
| Simple delegation between agents | **CrewAI** |

## Examples

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

The crew performs a business analysis of the AI SaaS market, producing an executive report with market analysis and strategic recommendations.

### Example 3: Agent Delegation

When `allow_delegation=True`, agents autonomously decide to hand off work:

```
Lead Developer (allow_delegation=True)
    +-- "I need code review" --> Code Reviewer
    +-- "I need tests" -------> QA Engineer
```

A lead developer builds an email validation function and delegates review and testing to specialists -- no extra wiring needed.

## Setup

### Prerequisites

- Python >= 3.10
- OpenAI API key

### Installation

```bash
cd crewai-demo

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
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

Open the notebook in Jupyter or VS Code:

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
