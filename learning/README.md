# LangChain & LangGraph Learning Path

A progressive 10-notebook course to master LangChain and LangGraph fundamentals.

---

## Course Overview

| # | Notebook | Topic | Key Concepts |
|---|----------|-------|--------------|
| 1 | `learning_1_hello_llm.ipynb` | Hello LLM | ChatOpenAI, invoke, stream, messages |
| 2 | `learning_2_prompt_templates.ipynb` | Prompt Templates | PromptTemplate, ChatPromptTemplate, variables |
| 3 | `learning_3_simple_chains.ipynb` | Simple Chains | LCEL, pipe operator, StrOutputParser |
| 4 | `learning_4_tools_basics.ipynb` | Tools Basics | @tool decorator, bind_tools, tool calls |
| 5 | `learning_5_first_graph.ipynb` | First Graph | StateGraph, nodes, edges, START/END |
| 6 | `learning_6_conditional_edges.ipynb` | Conditional Edges | Routing, branching workflows |
| 7 | `learning_7_loops.ipynb` | Loops in Graphs | Cycles, retry logic, iteration |
| 8 | `learning_8_agent_with_tools.ipynb` | Agent with Tools | ReAct pattern, ToolNode, agent loop |
| 9 | `learning_9_memory_and_state.ipynb` | Memory & State | Checkpointers, persistence, threads |
| 10 | `learning_10_human_in_the_loop.ipynb` | Human in the Loop | Interrupts, approvals, resume |

---

## Part 1: LangChain Basics (Notebooks 1-4)

### Learning 1: Hello LLM
Your first LLM call using LangChain.

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
response = llm.invoke("Hello, world!")
print(response.content)
```

**You'll learn:**
- Creating an LLM instance
- Sending messages with `.invoke()`
- Streaming responses with `.stream()`
- Using SystemMessage, HumanMessage, AIMessage

---

### Learning 2: Prompt Templates
Create reusable prompt structures.

```python
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_template("Explain {topic} simply")
messages = template.format_messages(topic="AI")
```

**You'll learn:**
- PromptTemplate for simple strings
- ChatPromptTemplate for chat models
- Variable placeholders with `{variable}`
- Few-shot prompting with examples

---

### Learning 3: Simple Chains
Connect components with the pipe operator.

```python
chain = prompt | llm | StrOutputParser()
result = chain.invoke({"topic": "Python"})
```

**You'll learn:**
- LCEL (LangChain Expression Language)
- The `|` pipe operator
- StrOutputParser for clean output
- RunnableParallel for concurrent chains

---

### Learning 4: Tools Basics
Give LLMs the ability to take actions.

```python
@tool
def calculate(expression: str) -> str:
    """Calculate a math expression."""
    return str(eval(expression))

llm_with_tools = llm.bind_tools([calculate])
```

**You'll learn:**
- Creating tools with `@tool`
- Binding tools to LLMs
- Understanding tool calls
- Executing tools and returning results

---

## Part 2: LangGraph Fundamentals (Notebooks 5-7)

### Learning 5: First Graph
Build your first LangGraph workflow.

```python
from langgraph.graph import StateGraph, START, END

class MyState(TypedDict):
    value: str

def my_node(state):
    return {"value": "processed"}

graph = StateGraph(MyState)
graph.add_node("process", my_node)
graph.add_edge(START, "process")
graph.add_edge("process", END)

app = graph.compile()
```

**You'll learn:**
- State definition with TypedDict
- Creating nodes as functions
- Connecting with edges
- Compiling and running graphs

---

### Learning 6: Conditional Edges
Create branching workflows.

```python
def router(state) -> str:
    if state["score"] > 50:
        return "pass"
    return "fail"

graph.add_conditional_edges("check", router)
```

**You'll learn:**
- Router functions
- `add_conditional_edges()`
- Multi-path workflows
- Routing to END

---

### Learning 7: Loops in Graphs
Create cycles for iterative processing.

```python
def should_continue(state) -> str:
    if state["count"] < state["target"]:
        return "loop"  # Go back
    return "done"      # Exit
```

**You'll learn:**
- Creating cycles (loops)
- Retry patterns
- Iteration control
- Preventing infinite loops

---

## Part 3: Advanced Patterns (Notebooks 8-10)

### Learning 8: Agent with Tools
Combine LLM + Tools in a graph.

```
              ┌──────────────┐
              ↓              │ (tool calls)
[START] → [Agent] ──────→ [Tools]
              │
              ↓ (done)
            [END]
```

**You'll learn:**
- The ReAct pattern (Reason → Act → Observe)
- Using prebuilt ToolNode
- Message accumulation with `Annotated[list, operator.add]`
- Streaming agent execution

---

### Learning 9: Memory & State
Persist state across conversations.

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
app = graph.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "user-123"}}
app.invoke({"messages": [...]}, config)
```

**You'll learn:**
- Checkpointers (MemorySaver, SqliteSaver)
- Thread IDs for separate conversations
- Getting state with `get_state()`
- Viewing history with `get_state_history()`

---

### Learning 10: Human in the Loop
Add human approval to workflows.

```python
app = graph.compile(
    checkpointer=memory,
    interrupt_before=["sensitive_action"]
)

# Workflow pauses...
# Human reviews...
app.update_state(config, {"approved": True})
app.invoke(None, config)  # Resume
```

**You'll learn:**
- `interrupt_before` / `interrupt_after`
- Updating state while paused
- Resuming execution
- Approval workflows

---

## Quick Reference

### LangChain Imports
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
```

### LangGraph Imports
```python
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated
import operator
```

### State Pattern
```python
class MyState(TypedDict):
    messages: Annotated[list, operator.add]  # Append
    value: str                                # Replace
```

### Graph Pattern
```python
builder = StateGraph(MyState)
builder.add_node("name", function)
builder.add_edge(START, "name")
builder.add_edge("name", END)
app = builder.compile()
result = app.invoke(initial_state)
```

---

## Prerequisites

1. Python 3.9+
2. OpenAI API key in `.env` file
3. Required packages:
```bash
pip install langchain langchain-openai langgraph python-dotenv
```

## How to Use

1. Start with `learning_1_hello_llm.ipynb`
2. Complete each notebook in order
3. Run all cells and do the exercises
4. Move to the next notebook

Each notebook builds on previous concepts. Don't skip ahead!

---

*Happy learning!*
