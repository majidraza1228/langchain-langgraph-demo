# LangChain & LangGraph Learning Demo

A hands-on demo for building AI applications with **LangChain**, **LangGraph**, and **CrewAI**. Covers prompt templates, chains, tool calling, RAG, stateful agents, multi-agent systems, and observability.

## What You'll Learn

- **LangChain Basics** -- Prompt templates, chat models, chains, structured output, tool calling, RAG
- **LangGraph** -- Stateful graphs, memory, decision-making, human-in-the-loop, checkpointing
- **Multi-Agent Systems** -- Supervisor patterns, parallel agents, agent delegation (LangGraph + CrewAI)
- **Observability** -- Tracing, evaluation, and debugging with LangSmith

## Project Structure

```
langchain-langgraph-demo/
├── Demo_1_Langchain_Fundamentals.ipynb   # Prompt templates, chains, tools, RAG
├── Demo_2_Langgraph_Fundamentals.ipynb   # State graphs, memory, decision-making
├── Demo_3_Langchain_CreateAgent.ipynb    # Pre-built agent templates, approval systems
├── Demo_4_Advanced_RAG_Patterns.ipynb    # Query rewriting, hybrid search, evaluation
├── Demo_5_Multi_Agent_Systems.ipynb      # Supervisor, parallel, and swarm patterns
├── Demo_6_LangSmith_Observability.ipynb  # Tracing, cost tracking, evaluation
├── LangGraph_Diagrams.ipynb              # Visual architecture diagrams
├── FRAMEWORKS_COMPARISON.md              # LangChain vs LlamaIndex vs CrewAI vs others
├── crewai-demo/                          # CrewAI multi-agent demo (separate venv)
│   ├── Demo_CrewAI_Multi_Agent.ipynb     # Sequential, hierarchical, delegation patterns
│   ├── requirements.txt
│   └── CREWAI_MULTI_AGENT.md
├── multiagent-eval/                      # Multi-agent + eval engineering demo
├── learning/                             # Step-by-step learning notebooks (basics)
├── exerises/                             # Practice exercises
├── docs/                                 # Additional documentation
├── images/                               # Diagrams and visual aids
├── langchain_prompts.py                  # Prompt templates used across demos
├── langraph_prompts.py                   # Agent prompt templates
├── langgraph_diagram.py                  # Diagram generation script
├── mcp_server.py                         # MCP tool server example
├── test_imports.py                       # Import verification script
└── requirements.txt                      # Python dependencies
```

## Prerequisites

- Python 3.8+ (3.10+ for MCP and CrewAI features)
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))

## Setup

```bash
git clone https://github.com/majidraza1228/langchain-langgraph-demo.git
cd langchain-langgraph-demo

python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

### API Key Configuration

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_key_here
LANGSMITH_API_KEY=your_langsmith_key_here  # Optional
```

**Google Colab**: Add `OPENAI_API_KEY` to Colab secrets (key icon in sidebar). The notebooks auto-detect Colab and use secrets manager.

## Learning Path

### Core Lessons (follow in order)

| # | Notebook | Topics |
|---|----------|--------|
| 1 | [Demo_1_Langchain_Fundamentals](Demo_1_Langchain_Fundamentals.ipynb) | Prompt templates, chat models, chains, structured output, tool calling, RAG |
| 2 | [Demo_2_Langgraph_Fundamentals](Demo_2_Langgraph_Fundamentals.ipynb) | State graphs, tools, memory, conditional edges, human-in-the-loop |
| 3 | [Demo_3_Langchain_CreateAgent](Demo_3_Langchain_CreateAgent.ipynb) | Pre-built agent templates, approval middleware |

### Advanced Topics

| # | Notebook | Topics |
|---|----------|--------|
| 4 | [Demo_4_Advanced_RAG_Patterns](Demo_4_Advanced_RAG_Patterns.ipynb) | Query rewriting, hybrid search, relevance filtering, evaluation |
| 5 | [Demo_5_Multi_Agent_Systems](Demo_5_Multi_Agent_Systems.ipynb) | Supervisor, parallel, and swarm multi-agent patterns (LangGraph) |
| 6 | [Demo_6_LangSmith_Observability](Demo_6_LangSmith_Observability.ipynb) | Tracing, cost tracking, automated evaluation, feedback |

### CrewAI (Alternative Multi-Agent Framework)

| Notebook | Topics |
|----------|--------|
| [Demo_CrewAI_Multi_Agent](crewai-demo/Demo_CrewAI_Multi_Agent.ipynb) | Role-based agents, sequential/hierarchical processes, delegation |

CrewAI uses a role-playing paradigm (agents with roles, goals, backstories) instead of explicit graph wiring. See the [CrewAI guide](crewai-demo/CREWAI_MULTI_AGENT.md) for setup and details.

## Running the Demos

```bash
jupyter notebook
```

Then open the notebooks in order starting with `Demo_1_Langchain_Fundamentals.ipynb`.

## Troubleshooting

**Import errors / ModuleNotFoundError**: Verify your Jupyter kernel matches the Python environment where you installed dependencies. Run this in a notebook cell to check:

```python
import sys
print('sys.executable:', sys.executable)
```

Then install packages using that exact path: `/path/to/python -m pip install -r requirements.txt`

**API errors**: Check that `.env` has the correct key with no extra spaces, and that your OpenAI account has credits. Restart the Jupyter kernel after updating `.env`.

**MCP section skipped**: Requires Python 3.10+. This is expected on Python 3.9 and doesn't affect other lessons.

## Resources

- [LangChain Docs](https://python.langchain.com/) | [LangGraph Docs](https://langchain-ai.github.io/langgraph/) | [LangSmith](https://smith.langchain.com/)
- [CrewAI Docs](https://docs.crewai.com) | [CrewAI GitHub](https://github.com/crewAIInc/crewAI)
- [FRAMEWORKS_COMPARISON.md](FRAMEWORKS_COMPARISON.md) -- Detailed comparison of LangChain, LlamaIndex, CrewAI, AutoGen, and others

## License

MIT License -- free for learning, teaching, and building.
