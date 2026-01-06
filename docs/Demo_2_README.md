# 📗 Demo 2: LangGraph Fundamentals

## Overview

This notebook introduces LangGraph - a powerful library for building stateful, multi-actor AI agents with complex workflows. Unlike simple chains, LangGraph lets you create agents that can loop, make decisions, pause for human input, and maintain conversation state.

**Duration:** 60-75 minutes  
**Level:** Intermediate  
**Prerequisites:** Complete Demo 1, understand LangChain basics

## What You'll Learn

### 1. 🛠️ Tools (Agent Capabilities)
Define the "skills" your agent can use to accomplish tasks.

**Key Concepts:**
- Tool definitions with `@tool` decorator
- Clear tool descriptions
- Type hints for parameters
- Return value documentation

**Example Tools:**
- `get_time_off_balance` - Query vacation days
- `process_time_off` - Book time off requests
- `get_additional_info_from_human` - Ask clarifying questions

---

### 2. 💾 State Management
The "shared memory" that tracks conversation context and data.

**Key Concepts:**
- `TypedDict` for state schema
- `Annotated` types with reducers
- `operator.add` for message accumulation
- Immutable state updates

**Why This Matters:**  
Without state, your agent would forget every previous message - making real conversations impossible!

```python
class GraphState(TypedDict):
    chat_history: Annotated[list[AnyMessage], operator.add]
    user_id: Optional[str]
```

---

### 3. 🔄 Nodes & Edges
The building blocks of your agent's workflow.

**Nodes** = Processing steps (functions that do work)  
**Edges** = Connections between nodes (workflow logic)

**Two Types of Edges:**
1. **Normal Edges** - Always go to the same next node
2. **Conditional Edges** - Route based on logic/conditions

**Example Workflow:**
```
START → reason_node → [conditional] → action_node → reason_node → END
                              ↓
                             END
```

---

### 4. 👤 Human-in-the-Loop
Pause agent execution to request clarification or approval.

**Key Concepts:**
- `interrupt()` function
- Checkpointer for state persistence
- `Command(resume=...)` to continue
- Thread management

**Real-world Use Cases:**
- "What dates do you need off?"
- "Should I approve this $10,000 expense?"
- "I'm not sure - can you provide more details?"

---

### 5. 💿 Persistence (State Management)
Save and resume agent sessions across restarts.

**Key Concepts:**
- Checkpointers (InMemorySaver, PostgresSaver)
- Thread IDs for session tracking
- State snapshots
- Resume from interrupts

**Why This Matters:**  
Users can close their browser and resume exactly where they left off!

---

## What You'll Build

### Time-Off Request Assistant
A complete AI agent that:
1. Takes vacation requests from employees
2. Checks their available vacation balance
3. Asks for missing information (dates, etc.)
4. Validates requests against balance
5. Approves or denies based on rules
6. Remembers conversation history

**Example Interaction:**
```
User: "I want to take leave"
Agent: [calls get_additional_info_from_human]
Agent: "Please provide the start and end dates for your leave request."

[Agent pauses - waiting for user input]

User: "tomorrow"
Agent: [calls get_time_off_balance] → 10 days available
Agent: [calls process_time_off] → Books 1 day
Agent: "Your time off request for January 7, 2026 has been processed. 
       You have 9 days remaining."
```

---

## Architecture

### The ReAct Pattern
**ReAct = Reasoning + Acting**

1. **Reason** - LLM analyzes the situation and decides what to do
2. **Act** - Execute tools based on that decision
3. **Observe** - See the results
4. **Repeat** - Loop until task is complete

```
┌─────────────┐
│ User Input  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Reason Node │ ◄──┐
│  (LLM call) │    │
└──────┬──────┘    │
       │           │
       ▼           │
  [Need tool?]     │
       ├─No────────┤
       │           │
       Yes         │
       │           │
       ▼           │
┌─────────────┐    │
│ Action Node │    │
│ (Run tools) │────┘
└─────────────┘
```

---

## Code Structure

### Key Components

**1. State Definition**
```python
class GraphState(TypedDict):
    chat_history: Annotated[list[AnyMessage], operator.add]
    user_id: Optional[str]
```

**2. Tool Definitions**
```python
@tool
def get_time_off_balance(user_id: str) -> int:
    """Get the time off balance for a user."""
    return 10
```

**3. Nodes**
```python
def reason_node(state: GraphState) -> GraphState:
    # LLM decides what to do next
    llm_response = llm_with_tools.invoke(state['chat_history'])
    return {'chat_history': [llm_response]}

def action_node(state: GraphState):
    # Execute the tools LLM requested
    results = []
    for tool_call in state['chat_history'][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        results.append(ToolMessage(...))
    return {'chat_history': results}
```

**4. Graph Construction**
```python
graph = StateGraph(GraphState)
graph.add_node('reason_node', reason_node)
graph.add_node('action_node', action_node)
graph.add_edge(START, 'reason_node')
graph.add_conditional_edges('reason_node', conditional_router)
graph.add_edge('action_node', 'reason_node')
agent = graph.compile(checkpointer=InMemorySaver())
```

---

## Step-by-Step Guide

### 1. Define Your Tools
```python
@tool
def get_additional_info_from_human(message: str) -> str:
    """Raises an interrupt to fetch additional information."""
    interrupt_result = interrupt(message)
    return interrupt_result['user_message']
```

### 2. Create State Schema
```python
class GraphState(TypedDict):
    chat_history: Annotated[list[AnyMessage], operator.add]
    user_id: Optional[str]
```

### 3. Build Nodes
- `reason_node` - LLM reasoning
- `action_node` - Tool execution

### 4. Add Edges
- Normal edges for fixed flows
- Conditional edges for routing logic

### 5. Compile & Run
```python
agent = graph.compile(checkpointer=InMemorySaver())
result = agent.invoke(input_data, config={'configurable': {'thread_id': 'user-123'}})
```

---

## Key Concepts Explained

### Conditional Routing
```python
def conditional_router(state: GraphState):
    if state['chat_history'][-1].tool_calls:
        return 'action_node'  # Need to run tools
    else:
        return 'end'  # Done!
```

### Human-in-the-Loop
```python
# In your tool
interrupt_result = interrupt("What dates do you need?")

# Resume later
agent.invoke(Command(resume={'user_message': "March 15-20"}), config=config)
```

### Persistence
```python
# Save state with checkpointer
checkpointer = InMemorySaver()
agent = graph.compile(checkpointer=checkpointer)

# Resume later with same thread_id
config = {'configurable': {'thread_id': 'user-123'}}
```

---

## Key Takeaways

✅ **LangGraph** enables complex, stateful agent workflows  
✅ **Nodes** are processing steps, **Edges** define flow  
✅ **State** tracks conversation history and context  
✅ **Interrupts** enable human-in-the-loop patterns  
✅ **Checkpointers** allow pause/resume functionality  
✅ **ReAct pattern** combines reasoning and action effectively  

---

## Common Pitfalls & Solutions

### Problem: State Not Updating
**Solution:** Make sure you're using `Annotated` with `operator.add` for lists.

### Problem: Agent Loops Forever
**Solution:** Add proper termination conditions in your conditional router.

### Problem: Interrupts Not Working
**Solution:** Ensure you compiled the graph with a checkpointer.

---

## Next Steps

After completing this demo:

1. ✅ Move to [Demo 3: Create Agent](./Demo_3_README.md)
2. Build your own custom graph for a different use case
3. Add more tools to expand agent capabilities
4. Experiment with different state structures

---

## Additional Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [StateGraph Guide](https://langchain-ai.github.io/langgraph/concepts/low_level/)
- [Human-in-the-Loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/)
- [Persistence Guide](https://langchain-ai.github.io/langgraph/concepts/persistence/)

---

**[← Back to Demo 1](./Demo_1_README.md)** | **[Back to Main](../README.md)** | **[Next: Demo 3 →](./Demo_3_README.md)**
