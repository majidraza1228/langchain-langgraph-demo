# LangChain & LangGraph: Basic Concepts Guide

A simple guide to understand LangChain and LangGraph for beginners.

---

## Part 1: LangChain Basics

### What is LangChain?

LangChain is a framework for building applications with Large Language Models (LLMs). Think of it as **building blocks** that help you connect LLMs to data, tools, and other services.

### Core Concepts

#### 1. LLM (Language Model)

The brain of your application - it's what generates text responses.

```python
from langchain_openai import ChatOpenAI

# Create an LLM instance
llm = ChatOpenAI(model="gpt-4o-mini")

# Ask a simple question
response = llm.invoke("What is Python?")
print(response.content)
```

#### 2. Prompts

Templates that structure what you ask the LLM.

```python
from langchain_core.prompts import ChatPromptTemplate

# Create a reusable prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful {role}."),
    ("user", "{question}")
])

# Fill in the blanks
formatted = prompt.invoke({
    "role": "cooking assistant",
    "question": "How do I boil an egg?"
})
```

#### 3. Chains

Connect multiple steps together (prompt → LLM → output).

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Define components
prompt = ChatPromptTemplate.from_template("Explain {topic} in simple terms")
llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# Chain them together using |
chain = prompt | llm | parser

# Run the chain
result = chain.invoke({"topic": "machine learning"})
print(result)
```

**Visual:**
```
[User Input] → [Prompt Template] → [LLM] → [Output Parser] → [Result]
```

#### 4. Tools

External functions the LLM can call to perform actions.

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    # In real app, this would call a weather API
    return f"The weather in {city} is sunny, 72°F"

@tool
def calculate(expression: str) -> str:
    """Calculate a math expression."""
    return str(eval(expression))

# Now LLM can use these tools!
tools = [get_weather, calculate]
```

---

## Part 2: LangGraph Basics

### What is LangGraph?

LangGraph builds on LangChain to create **stateful, multi-step workflows**. Think of it as a flowchart where:
- **Nodes** = Actions/Steps
- **Edges** = Connections between steps
- **State** = Data that travels through the workflow

### When to Use LangGraph vs LangChain?

| Scenario | Use LangChain | Use LangGraph |
|----------|---------------|---------------|
| Simple Q&A | ✅ | ❌ |
| One-shot tasks | ✅ | ❌ |
| Multi-step workflows | ❌ | ✅ |
| Need to remember context | ❌ | ✅ |
| Loops/cycles in logic | ❌ | ✅ |
| Human approval needed | ❌ | ✅ |

### Core Concepts

#### 1. State

A dictionary that holds all the data flowing through your graph.

```python
from typing import TypedDict, Annotated
import operator

class MyState(TypedDict):
    messages: Annotated[list, operator.add]  # Appends new messages
    user_name: str                            # Replaces value
    counter: int                              # Replaces value
```

#### 2. Nodes

Functions that process and update the state.

```python
def greet_user(state: MyState) -> dict:
    """Node that greets the user"""
    name = state["user_name"]
    return {
        "messages": [f"Hello, {name}!"]
    }

def count_up(state: MyState) -> dict:
    """Node that increments counter"""
    return {
        "counter": state["counter"] + 1
    }
```

#### 3. Edges

Connections that define the flow between nodes.

```python
# Simple edge: always go from A to B
graph.add_edge("node_a", "node_b")

# Conditional edge: decide based on state
def route_decision(state: MyState) -> str:
    if state["counter"] > 5:
        return "finish"
    else:
        return "continue"

graph.add_conditional_edges("decision_node", route_decision)
```

---

## Example 1: Simple Greeting Graph

A basic graph that greets a user.

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# 1. Define State
class GreetingState(TypedDict):
    name: str
    greeting: str

# 2. Define Nodes
def create_greeting(state: GreetingState) -> dict:
    return {"greeting": f"Hello, {state['name']}! Welcome!"}

# 3. Build Graph
graph = StateGraph(GreetingState)
graph.add_node("greeter", create_greeting)
graph.add_edge(START, "greeter")
graph.add_edge("greeter", END)

# 4. Compile and Run
app = graph.compile()
result = app.invoke({"name": "Alice", "greeting": ""})
print(result["greeting"])  # "Hello, Alice! Welcome!"
```

**Visual Flow:**
```
[START] → [greeter] → [END]
```

---

## Example 2: Conditional Routing

A graph that takes different paths based on conditions.

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# 1. Define State
class AgeState(TypedDict):
    age: int
    message: str

# 2. Define Nodes
def check_adult(state: AgeState) -> dict:
    return state  # Just pass through

def adult_message(state: AgeState) -> dict:
    return {"message": "You can vote!"}

def minor_message(state: AgeState) -> dict:
    return {"message": "You're too young to vote."}

# 3. Define Routing Function
def route_by_age(state: AgeState) -> str:
    if state["age"] >= 18:
        return "adult"
    return "minor"

# 4. Build Graph
graph = StateGraph(AgeState)
graph.add_node("check", check_adult)
graph.add_node("adult", adult_message)
graph.add_node("minor", minor_message)

graph.add_edge(START, "check")
graph.add_conditional_edges("check", route_by_age)
graph.add_edge("adult", END)
graph.add_edge("minor", END)

# 5. Compile and Run
app = graph.compile()

print(app.invoke({"age": 25, "message": ""}))  # "You can vote!"
print(app.invoke({"age": 15, "message": ""}))  # "You're too young to vote."
```

**Visual Flow:**
```
                    ┌─→ [adult] ─→ [END]
[START] → [check] ──┤
                    └─→ [minor] ─→ [END]
```

---

## Example 3: Loop Until Done

A graph that loops until a condition is met.

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# 1. Define State
class CounterState(TypedDict):
    count: int
    target: int

# 2. Define Nodes
def increment(state: CounterState) -> dict:
    print(f"Count: {state['count']}")
    return {"count": state["count"] + 1}

# 3. Define Routing
def should_continue(state: CounterState) -> str:
    if state["count"] >= state["target"]:
        return "done"
    return "continue"

# 4. Build Graph
graph = StateGraph(CounterState)
graph.add_node("counter", increment)

graph.add_edge(START, "counter")
graph.add_conditional_edges(
    "counter",
    should_continue,
    {"continue": "counter", "done": END}  # Loop back or finish
)

# 5. Compile and Run
app = graph.compile()
result = app.invoke({"count": 0, "target": 3})
# Output: Count: 0, Count: 1, Count: 2
# Final: {"count": 3, "target": 3}
```

**Visual Flow:**
```
              ┌──────────────┐
              ↓              │ (count < target)
[START] → [counter] ────────┘
              │
              ↓ (count >= target)
            [END]
```

---

## Example 4: Agent with Tools

A graph where an LLM decides which tools to use.

```python
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from typing import TypedDict, Annotated
import operator

# 1. Define Tools
@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

tools = [add, multiply]

# 2. Define State
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

# 3. Create LLM with Tools
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)

# 4. Define Nodes
def agent(state: AgentState) -> dict:
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

tool_node = ToolNode(tools)

# 5. Define Routing
def should_use_tools(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"

# 6. Build Graph
graph = StateGraph(AgentState)
graph.add_node("agent", agent)
graph.add_node("tools", tool_node)

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_use_tools, {"tools": "tools", "end": END})
graph.add_edge("tools", "agent")  # After tools, go back to agent

# 7. Compile and Run
app = graph.compile()
result = app.invoke({
    "messages": [HumanMessage(content="What is 5 + 3?")]
})
```

**Visual Flow:**
```
              ┌──────────────┐
              ↓              │ (has tool calls)
[START] → [agent] ──────→ [tools]
              │
              ↓ (no tool calls)
            [END]
```

---

## Quick Reference

### LangChain Components

| Component | Purpose | Example |
|-----------|---------|---------|
| LLM | Generate text | `ChatOpenAI()` |
| Prompt | Structure input | `ChatPromptTemplate` |
| Chain | Connect steps | `prompt \| llm \| parser` |
| Tool | External actions | `@tool` decorator |
| Retriever | Fetch documents | `vectorstore.as_retriever()` |

### LangGraph Components

| Component | Purpose | Example |
|-----------|---------|---------|
| State | Data container | `TypedDict` |
| Node | Process step | `def my_node(state):` |
| Edge | Connection | `add_edge("a", "b")` |
| Conditional Edge | Routing | `add_conditional_edges()` |
| START/END | Entry/exit | Built-in constants |

### State Annotation Patterns

```python
from typing import Annotated
import operator

class MyState(TypedDict):
    # Append new items to list
    messages: Annotated[list, operator.add]

    # Replace with new value (default behavior)
    current_user: str

    # Custom reducer function
    total: Annotated[int, lambda old, new: old + new]
```

---

## Next Steps

1. **Run the notebooks** in this repo to see working examples
2. **Start simple** - build a basic chain before trying graphs
3. **Add complexity gradually** - one feature at a time
4. **Check the docs**:
   - [LangChain Docs](https://python.langchain.com/docs/)
   - [LangGraph Docs](https://langchain-ai.github.io/langgraph/)

---

*Happy building!*
