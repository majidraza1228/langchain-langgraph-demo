# LangChain & LangGraph Demo Project

## Overview

This repository contains a comprehensive demonstration of building intelligent AI-powered applications using **LangChain** and **LangGraph**. The project showcases practical implementations of core concepts including prompt engineering, tool calling, retrieval-augmented generation (RAG), and stateful agent workflows with human-in-the-loop capabilities.

This demo is designed to help developers understand and implement production-ready LLM applications by providing clear, well-documented examples with detailed explanations of each concept.

## What You'll Learn

This demonstration covers the complete journey from basic LLM interactions to complex agentic systems:

### 🔹 LangChain Fundamentals
- **Prompt Templates**: Create reusable, structured prompts for consistent AI interactions
- **Chat Models**: Work with various LLM providers using a unified interface
- **LCEL (LangChain Expression Language)**: Build powerful chains by composing multiple components
- **Structured Output**: Extract typed, validated data from LLM responses
- **Tool Calling**: Enable LLMs to use external tools and APIs intelligently
- **RAG (Retrieval Augmented Generation)**: Augment LLMs with external knowledge sources

### 🔹 LangGraph Advanced Patterns
- **Stateful Workflows**: Build agents that maintain conversation context and state
- **Cyclical Graphs**: Implement reasoning loops where agents can plan, act, and iterate
- **Human-in-the-Loop**: Design systems that pause for human approval or clarification
- **Persistence & Memory**: Save and resume agent sessions for long-running workflows
- **Conditional Routing**: Create dynamic workflows that adapt based on agent decisions

### 🔹 Production-Ready Agent Development
- **Pre-built Agents**: Use high-level abstractions like `create_agent` for rapid development
- **Middleware Integration**: Add cross-cutting concerns like approval workflows
- **MCP (Model Context Protocol)**: Connect to external tool servers and services
- **Error Handling**: Implement robust error handling and recovery strategies

## Project Structure

```
├── 1_Langchain_Fundamentals.ipynb    # Introduction to core LangChain concepts
├── 2_Langgraph_Fundamentals.ipynb    # Building stateful agents with graphs
├── 3_Langchain_CreateAgent.ipynb     # High-level agent creation and middleware
├── langchain_prompts.py               # Reusable prompt templates for examples
├── langraph_prompts.py                # Agent-specific system prompts
├── mcp_server.py                      # Model Context Protocol server example
├── requirements.txt                   # Python dependencies
└── images/                            # Diagrams and visual aids
```

## Prerequisites

Before running this demo, ensure you have:

- **Python 3.8 or higher** installed on your system
- **OpenAI API Key** - [Get one here](https://platform.openai.com/api-keys)
- Basic understanding of Python programming
- Familiarity with Jupyter notebooks (recommended but not required)

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/majidraza1228/langchain-langgraph-demo.git
cd langchain-langgraph-demo
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Your API Keys

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
LANGSMITH_API_KEY=your_langsmith_key_here  # Optional, for tracing
```

Or export them in your shell:

```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

## Running the Demo

### Option 1: Jupyter Notebooks (Recommended)

```bash
jupyter notebook
```

Then open the notebooks in order:
1. `1_Langchain_Fundamentals.ipynb` - Start here to understand the basics
2. `2_Langgraph_Fundamentals.ipynb` - Learn about stateful agents
3. `3_Langchain_CreateAgent.ipynb` - Explore high-level agent creation

### Option 2: Python Scripts

You can also run individual Python files to test specific components:

```bash
python langchain_prompts.py
python mcp_server.py
```

## Demo Walkthrough

### Notebook 1: LangChain Fundamentals

**What it demonstrates:**
- How to structure prompts for consistent AI behavior
- Working with different LLM providers through a unified interface
- Building chains that connect prompts, models, and output parsers
- Extracting structured data using Pydantic models
- Implementing tool calling for mathematical operations
- Building a RAG system that answers questions from Wikipedia

**Use case example:** A date assistant that can parse natural language date requests and return structured date ranges.

**Key takeaways:**
- LangChain provides abstractions that work across multiple LLM providers
- Streaming provides better user experience for real-time applications
- Tools extend LLM capabilities beyond text generation
- RAG enables LLMs to answer questions using external knowledge

---

### Notebook 2: LangGraph Fundamentals

**What it demonstrates:**
- Creating tools that agents can use (checking balances, processing requests)
- Defining graph state to maintain conversation context
- Building nodes for reasoning (LLM) and action (tool execution)
- Implementing conditional edges for dynamic workflow routing
- Adding human-in-the-loop interrupts for missing information
- Using checkpointers for persistence and resumability

**Use case example:** A time-off request agent that checks balances, processes leave requests, and asks users for missing information.

**Key takeaways:**
- Graphs enable complex, non-linear agent workflows
- State management is crucial for multi-turn interactions
- Interrupts allow agents to pause and request human input
- Persistence enables resuming conversations from any point

---

### Notebook 3: LangChain Create Agent

**What it demonstrates:**
- Using high-level `create_agent` function for rapid development
- Implementing the same functionality with less boilerplate code
- Adding middleware for approval workflows
- Understanding the abstraction layers in LangChain

**Use case example:** The same time-off agent, but built with pre-configured components and enhanced with approval middleware.

**Key takeaways:**
- `create_agent` provides a production-ready agent template
- Middleware adds cross-cutting concerns without modifying core logic
- High-level abstractions speed up development while maintaining flexibility

## Common Use Cases

This demo can be adapted for various real-world applications:

### 🎯 Customer Support Automation
- Handle customer inquiries with context-aware responses
- Escalate to humans when needed
- Maintain conversation history across sessions

### 🎯 Internal Workflow Automation
- Automate approval processes (as demonstrated)
- Process structured requests (time-off, expense reports, etc.)
- Integrate with existing business systems via tools

### 🎯 Knowledge Base Q&A
- Answer questions from company documentation
- Cite sources for transparency
- Handle follow-up questions with context

### 🎯 Data Analysis Assistants
- Query databases using natural language
- Generate reports and visualizations
- Provide explanations of insights

## Understanding the Code

### Key Components Explained

#### Prompt Templates
```python
ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant..."),
    ("human", "{user_query}")
])
```
Templates separate the structure from the content, making prompts reusable and maintainable.

#### LCEL Chains
```python
chain = prompt | llm | StrOutputParser()
result = chain.invoke({"user_query": "..."})
```
The pipe operator (`|`) composes components into workflows where each output feeds the next input.

#### Tool Definitions
```python
@tool
def my_tool(arg: str) -> str:
    """Tool description that the LLM reads."""
    return "result"
```
Tools extend LLM capabilities by providing access to external functions, APIs, and data sources.

#### Graph State
```python
class GraphState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
```
State maintains conversation context and is updated as the graph executes.

## Debugging & Observability

### LangSmith Tracing

This demo includes LangSmith integration for debugging:

1. Sign up at [smith.langchain.com](https://smith.langchain.com)
2. Get your API key
3. Add to `.env`:
   ```
   LANGSMITH_API_KEY=your_key
   LANGSMITH_TRACING=true
   LANGSMITH_PROJECT=your-project-name
   ```

LangSmith provides:
- Complete execution traces
- Token usage tracking
- Latency analysis
- Error debugging

## Extending the Demo

### Adding New Tools

1. Define your tool with the `@tool` decorator
2. Add clear docstrings (LLMs read these!)
3. Include the tool in the tools list
4. The agent automatically learns when to use it

### Connecting to External APIs

```python
@tool
def fetch_weather(city: str) -> dict:
    """Get current weather for a city."""
    response = requests.get(f"https://api.weather.com/{city}")
    return response.json()
```

### Adding Database Integration

```python
@tool
def query_database(sql: str) -> list:
    """Execute SQL query safely."""
    # Implement with parameterized queries for security
    return db.execute(sql)
```

## Best Practices Demonstrated

✅ **Clear Documentation**: Every concept includes detailed explanations
✅ **Progressive Complexity**: Start simple, build to advanced patterns
✅ **Production Patterns**: Error handling, validation, security considerations
✅ **Code Reusability**: Modular prompts and tools
✅ **Observability**: Integrated tracing and debugging
✅ **Type Safety**: Pydantic models for structured outputs

## Troubleshooting

### Common Issues

**Issue: OpenAI API errors**
- Verify your API key is set correctly
- Check you have sufficient credits
- Ensure you're not rate-limited

**Issue: Import errors**
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
- Check Python version: `python --version` (should be 3.8+)

**Issue: Notebook kernel crashes**
- Restart the kernel: Kernel → Restart
- Clear outputs: Cell → All Output → Clear

**Issue: Tools not being called**
- Check tool docstrings are clear and descriptive
- Verify tool is included in the tools list
- Review LangSmith traces to see model reasoning

## Additional Resources

### Official Documentation
- [LangChain Python Docs](https://python.langchain.com/) - Complete API reference
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) - Graph-based agent patterns
- [LangSmith](https://smith.langchain.com/) - Observability and debugging platform

### Learning Materials
- [LangChain YouTube Channel](https://www.youtube.com/@LangChain) - Video tutorials
- [LangChain Use Cases](https://docs.langchain.com/oss/python/learn) - Real-world examples
- [LangChain Integrations](https://docs.langchain.com/oss/python/integrations/chat) - 100+ model providers

### Community
- [LangChain Discord](https://discord.gg/langchain) - Get help from the community
- [GitHub Discussions](https://github.com/langchain-ai/langchain/discussions) - Q&A and feature requests
- [Twitter/X](https://twitter.com/LangChainAI) - Latest updates and announcements

## Contributing

Found an issue or want to improve the demo? Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request with a clear description

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you have questions or need help:
- Open an issue on GitHub
- Check existing issues for similar problems
- Review the notebooks' detailed explanations

## Acknowledgments

This demo is built using:
- [LangChain](https://github.com/langchain-ai/langchain) - Framework for LLM applications
- [LangGraph](https://github.com/langchain-ai/langgraph) - Framework for stateful agents
- [OpenAI](https://openai.com/) - LLM provider

---

**Happy Building!** 🚀

For questions or feedback, please open an issue on GitHub.
