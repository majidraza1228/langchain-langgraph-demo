# 📘 Demo 1: LangChain Fundamentals

## Overview

This notebook introduces the core building blocks of LangChain - the foundational library for building LLM-powered applications. You'll learn how to interact with language models, structure prompts, chain operations together, and implement powerful patterns like tool calling and RAG (Retrieval Augmented Generation).

**Duration:** 45-60 minutes  
**Level:** Beginner  
**Prerequisites:** Basic Python knowledge, OpenAI API key

## What You'll Learn

### 1. 🔗 Prompt Templates
Learn to create reusable, structured prompts that ensure consistent AI behavior.

**Key Concepts:**
- System vs Human messages
- Variable placeholders
- Message formatting
- Prompt reusability

**Real-world Application:**  
Instead of writing the same instructions over and over, create templates once and reuse them thousands of times.

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant..."),
    ("human", "{user_query}")
])
```

---

### 2. 🤖 Chat Models
Work with different LLM providers through a unified interface.

**Key Concepts:**
- Model initialization
- The Runnable Interface
- Temperature settings
- Model selection

**Supported Providers:** OpenAI, Anthropic, Google, Cohere, and 100+ others

**Why This Matters:**  
Switch between different AI models (GPT-4, Claude, Gemini) without rewriting your code!

---

### 3. ⛓️ LCEL (LangChain Expression Language)
Build powerful chains by connecting components together.

**Key Concepts:**
- The pipe (`|`) operator
- Sequential processing
- Chain composition
- Reusable workflows

**Example:**
```python
chain = prompt | llm | StrOutputParser()
result = chain.invoke({"user_query": "..."})
```

**Think of it as:**  
An assembly line where output from one step becomes input for the next.

---

### 4. 📊 Structured Output
Get typed, validated responses instead of raw text.

**Key Concepts:**
- Pydantic models
- Type safety
- Data validation
- JSON schemas

**Before:**
```
"The start date is 2024-01-05 and end date is 2024-01-10"
```

**After:**
```python
DateRange(start_date='2024-01-05', end_date='2024-01-10')
```

**Why This Matters:**  
Integrate AI responses directly into your application logic without parsing messy text.

---

### 5. 🛠️ Tool Calling
Enable AI models to use external functions and APIs.

**Key Concepts:**
- Tool definitions
- Function calling
- Tool descriptions
- Automatic invocation

**Example Use Cases:**
- Calculator for math problems
- Weather API for current conditions
- Database queries for real-time data
- Web scraping for fresh information

**How It Works:**
1. Define a tool with `@tool` decorator
2. Bind tools to your model
3. AI automatically decides when to use them
4. You execute the tool and return results

---

### 6. 📚 RAG (Retrieval Augmented Generation)
Connect AI to your own data and documents.

**Key Concepts:**
- Document loaders
- Text splitters
- Vector stores
- Retrievers
- Embeddings

**The RAG Pipeline:**
```
1. Load documents (PDFs, web pages, databases)
2. Split into chunks
3. Create embeddings (numerical representations)
4. Store in vector database
5. Retrieve relevant chunks for queries
6. Generate answers using retrieved context
```

**Real-world Application:**  
Build a chatbot that answers questions about your company's documentation, policies, or knowledge base.

---

## What You'll Build

### Project 1: Date Assistant
An AI that understands natural language dates and converts them to structured format.

**Input:** "I need time off for the next 4 days"  
**Output:** `DateRange(start_date='2026-01-07', end_date='2026-01-10')`

---

### Project 2: Tool-Enabled Calculator
An AI that recognizes when it needs to do math and automatically uses a calculator tool.

**Input:** "I have a circular garden of radius 3. What's the area?"  
**Output:** AI calls `circle_area` tool → Returns "The area is approximately 28.27 square units."

---

### Project 3: Wikipedia Q&A System
A RAG system that answers questions using Wikipedia articles.

**Input:** "When was SpaceX founded?"  
**Output:** "SpaceX was founded on March 14, 2002, in El Segundo, California, U.S. The company was established by Elon Musk."

---

## Code Structure

### Key Files
- `Demo_1_Langchain_Fundamentals.ipynb` - Main notebook
- `langchain_prompts.py` - Shared prompt templates
- `mcp_server.py` - Model Context Protocol example (Python 3.10+)

### Important Imports
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
```

---

## Step-by-Step Guide

### 1. Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key
export OPENAI_API_KEY="your-key-here"

# Or create .env file
echo "OPENAI_API_KEY=your-key-here" > .env
```

### 2. Run the Notebook
```bash
jupyter notebook Demo_1_Langchain_Fundamentals.ipynb
```

### 3. Execute Cells Sequentially
Run each cell from top to bottom to see concepts build upon each other.

---

## Key Takeaways

✅ **Prompt Templates** make AI instructions reusable and consistent  
✅ **LCEL** lets you chain operations together elegantly  
✅ **Structured Output** gives you type-safe, validated responses  
✅ **Tool Calling** extends AI capabilities with custom functions  
✅ **RAG** connects AI to your own knowledge sources  
✅ **The Runnable Interface** works consistently across all components  

---

## Common Pitfalls & Solutions

### Problem: Import Errors
**Solution:** Make sure you're using the correct imports:
```python
from langchain_core.prompts import ChatPromptTemplate  # Correct
from langchain.prompts import ChatPromptTemplate      # Incorrect
```

### Problem: API Rate Limits
**Solution:** Add error handling and retry logic, or use a slower model.

### Problem: Tools Not Being Called
**Solution:** Make your tool descriptions crystal clear - the AI reads them!

---

## Next Steps

After completing this demo:

1. ✅ Move to [Demo 2: LangGraph Fundamentals](./Demo_2_README.md)
2. Try modifying the examples with your own use cases
3. Experiment with different models and temperatures
4. Build a simple RAG system with your own documents

---

## Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LCEL Guide](https://python.langchain.com/docs/expression_language/)
- [Tool Calling Guide](https://python.langchain.com/docs/modules/agents/tools/)
- [RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)

---

**[← Back to Main README](../README.md)** | **[Next: Demo 2 →](./Demo_2_README.md)**
