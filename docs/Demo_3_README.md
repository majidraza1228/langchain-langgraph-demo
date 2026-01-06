# 📙 Demo 3: High-Level Agent Development with `create_react_agent`

## Overview

This notebook shows you the "easy way" to build agents using `create_react_agent` - a high-level function that handles all the boilerplate of creating graphs, nodes, and edges automatically. You get the same powerful capabilities as manual graphs with ~80% less code!

**Duration:** 30-45 minutes  
**Level:** Intermediate  
**Prerequisites:** Complete Demo 1 & 2, understand graph concepts

## What You'll Learn

### 1. ⚡ `create_react_agent` Function
Build production-ready agents in minutes, not hours.

**What It Does Automatically:**
- Creates a `StateGraph` with proper state management
- Adds a model node for reasoning (LLM calls)
- Adds a tool node for executing actions
- Connects them with correct edges and loops
- Compiles into a ready-to-use agent

**Manual Graph (Demo 2):**
```python
# ~50 lines of code
graph = StateGraph(GraphState)
graph.add_node('reason_node', reason_node)
graph.add_node('action_node', action_node)
graph.add_conditional_edges(...)
# ... more setup
agent = graph.compile(checkpointer=checkpointer)
```

**With `create_react_agent` (Demo 3):**
```python
# ~5 lines of code
agent = create_react_agent(
    llm,
    tools=tools,
    prompt=system_prompt.text,
    checkpointer=InMemorySaver()
)
```

---

### 2. 🔄 Standard Interrupts
Handle missing information seamlessly with built-in interrupt support.

**Key Concepts:**
- Interrupts work automatically with `create_react_agent`
- Use the same `interrupt()` function from tools
- Resume with `Command(resume=...)`
- No additional graph configuration needed

---

### 3. 🎯 When to Use What

**Use `create_react_agent` when:**
- ✅ You need a standard ReAct agent (reason → act loop)
- ✅ You want rapid prototyping and development
- ✅ Your use case fits the common agent pattern
- ✅ You prefer less boilerplate code

**Build manual graphs when:**
- ✅ You need custom workflow logic beyond ReAct
- ✅ You require specialized routing or conditional logic
- ✅ You're implementing novel agent architectures
- ✅ You need fine-grained control over every step

---

## What You'll Build

### Same Time-Off Assistant, Less Code
The exact same time-off request assistant from Demo 2, but:
- 80% less code to write and maintain
- Same powerful capabilities
- Easier to read and understand
- Production-ready patterns built-in

**Example:**
```python
# Create agent in one call
agent = create_react_agent(
    llm,
    tools=[get_time_off_balance, process_time_off, get_additional_info_from_human],
    prompt=system_prompt.text,
    checkpointer=InMemorySaver()
)

# Use it exactly like before
result = agent.invoke(
    {"messages": [{"role": "user", "content": "I want to take leave"}]},
    config={'configurable': {'thread_id': user_id}}
)
```

---

## Key Differences from Demo 2

| Aspect | Demo 2 (Manual) | Demo 3 (create_react_agent) |
|--------|-----------------|----------------------------|
| **Lines of code** | ~100 lines | ~20 lines |
| **State definition** | You define it | Auto-created |
| **Nodes** | You write them | Auto-generated |
| **Edges** | You connect them | Auto-connected |
| **Conditional logic** | You implement it | Built-in |
| **Flexibility** | Full control | Standard patterns |
| **Learning curve** | Steeper | Gentler |

---

## Code Structure

### Complete Agent Creation
```python
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command, interrupt

# Define tools (same as Demo 2)
@tool
def get_time_off_balance(user_id: str) -> int:
    """Get the time off balance for a user."""
    return 10

@tool
def process_time_off(user_id: str, start_date: str, end_date: str) -> dict:
    """Process time-off request for a user."""
    # ... implementation
    return {"status": "success", "message": "..."}

@tool
def get_additional_info_from_human(message: str) -> str:
    """Ask user for additional information."""
    interrupt_result = interrupt(message)
    return interrupt_result['user_message']

# Create agent (this is it!)
agent = create_react_agent(
    llm=init_chat_model(model="gpt-4o", temperature=0),
    tools=[get_time_off_balance, process_time_off, get_additional_info_from_human],
    prompt=system_prompt.text,
    checkpointer=InMemorySaver()
)

# Use the agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "I want to take leave tomorrow"}]},
    config={'configurable': {'thread_id': 'user-1'}}
)
```

---

## Important Parameters

### `prompt` (not `system_prompt` or `state_modifier`)
The system message that defines agent behavior.

```python
agent = create_react_agent(
    llm,
    tools=tools,
    prompt=system_prompt.text,  # ← Correct parameter name
    checkpointer=InMemorySaver()
)
```

### `checkpointer`
Required for interrupts and state persistence.

**Options:**
- `InMemorySaver()` - For development/testing
- `PostgresSaver()` - For production
- `SQLiteSaver()` - For local persistence

---

## Step-by-Step Guide

### 1. Import Required Components
```python
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
```

### 2. Define Your Tools
```python
@tool
def my_tool(param: str) -> str:
    """Clear description of what the tool does."""
    return "result"
```

### 3. Create the Agent
```python
agent = create_react_agent(
    llm=init_chat_model(model="gpt-4o"),
    tools=[my_tool],
    prompt="You are a helpful assistant...",
    checkpointer=InMemorySaver()
)
```

### 4. Invoke the Agent
```python
result = agent.invoke(
    {"messages": [{"role": "user", "content": "user question"}]},
    config={'configurable': {'thread_id': 'session-123'}}
)
```

### 5. Handle Interrupts
```python
# If interrupted
agent.invoke(
    Command(resume={'user_message': "user's answer"}),
    config=config
)
```

---

## Key Takeaways

✅ **`create_react_agent`** dramatically simplifies agent creation  
✅ **Same capabilities** as manual graphs, less code  
✅ **Production-ready** patterns built-in  
✅ **Interrupts work** automatically with proper checkpointer  
✅ **Perfect for** standard ReAct workflows  
✅ **Know when** to use high-level vs low-level approaches  

---

## Middleware (Note)

The notebook originally referenced `HumanInTheLoopMiddleware`, which is not currently available in the stable LangChain release. For human-in-the-loop functionality:

**Current Approach:**
- Use the `interrupt()` function within tools (as demonstrated)
- Create custom approval tools
- Or build manual graphs with approval nodes (Demo 2)

**Future:**
- Middleware patterns may be added in future releases
- Check [LangChain documentation](https://docs.langchain.com/) for updates

---

## Common Issues & Solutions

### Problem: `TypeError: unexpected keyword arguments`
**Cause:** Using wrong parameter names  
**Solution:** Use `prompt` not `system_prompt` or `state_modifier`

```python
# ❌ Wrong
agent = create_react_agent(llm, tools, system_prompt=prompt)

# ✅ Correct
agent = create_react_agent(llm, tools, prompt=prompt)
```

### Problem: Import Error for `create_react_agent`
**Cause:** Importing from wrong module  
**Solution:** Import from `langgraph.prebuilt`

```python
# ❌ Wrong
from langchain.agents import create_agent

# ✅ Correct
from langgraph.prebuilt import create_react_agent
```

### Problem: Interrupts Not Working
**Cause:** No checkpointer provided  
**Solution:** Always include a checkpointer

```python
agent = create_react_agent(
    llm, tools, prompt,
    checkpointer=InMemorySaver()  # ← Required for interrupts!
)
```

---

## Next Steps

After completing this demo:

1. ✅ Move to [Demo 4: Advanced RAG Patterns](./Demo_4_README.md)
2. Compare Demo 2 & 3 side-by-side to understand the tradeoffs
3. Build a new agent for a different use case
4. Explore when you need manual graphs vs `create_react_agent`

---

## Additional Resources

- [LangGraph Prebuilt Agents](https://langchain-ai.github.io/langgraph/how-tos/create-react-agent/)
- [create_react_agent API](https://langchain-ai.github.io/langgraph/reference/prebuilt/#create_react_agent)
- [When to Use Prebuilt](https://langchain-ai.github.io/langgraph/concepts/high_level/)

---

**[← Back to Demo 2](./Demo_2_README.md)** | **[Back to Main](../README.md)** | **[Next: Demo 4 →](./Demo_4_README.md)**
