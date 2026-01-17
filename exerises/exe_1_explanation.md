# Exercise 1: RAG Micro-App with Gradio UI

This exercise demonstrates how to build a simple **Retrieval-Augmented Generation (RAG)** application with a web interface using Gradio.

## Overview

The notebook creates a minimal RAG chatbot that:
1. Stores knowledge in a vector database (FAISS)
2. Retrieves relevant context based on user questions
3. Uses an LLM to generate answers with citations
4. Provides a web UI for interaction

## Architecture

```
User Question
      |
      v
+------------------+
|    Retriever     |  <-- FAISS Vector Store
|  (finds relevant |      (embedded text chunks)
|     context)     |
+------------------+
      |
      v
+------------------+
|   LLM (GPT-4o)   |  <-- Prompt with context + question
|  (generates      |
|    answer)       |
+------------------+
      |
      v
   Answer with Citations
```

## Code Breakdown

### 1. Setup & Dependencies

```python
!pip -q install langchain langchain-community langchain-openai faiss-cpu tiktoken gradio
```

Installs required packages:
- **langchain**: Core framework for LLM applications
- **langchain-community**: Community integrations (FAISS, etc.)
- **langchain-openai**: OpenAI model integration
- **faiss-cpu**: Facebook AI Similarity Search for vector storage
- **tiktoken**: Token counting for OpenAI models
- **gradio**: Web UI framework

### 2. Environment Setup

```python
from dotenv import load_dotenv
load_dotenv()
```

Loads the `OPENAI_API_KEY` from a `.env` file.

### 3. RAG Components

#### Vector Store Creation
```python
texts = ["RAG grounds answers", "Hybrid retrieval helps", "Citations improve trust"]
vs = FAISS.from_texts(texts, OpenAIEmbeddings())
retriever = vs.as_retriever(k=2)
```

- **texts**: Sample knowledge base (3 short statements about RAG)
- **FAISS.from_texts()**: Creates embeddings and stores them in FAISS
- **as_retriever(k=2)**: Returns top 2 most relevant documents

#### LLM & Prompt
```python
llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template(
    "Use context to answer and cite short quotes.\nContext: {context}\nQ: {q}"
)
```

- Uses GPT-4o-mini for fast, cost-effective responses
- Prompt instructs the model to use context and cite quotes

#### Answer Function
```python
def answer(q: str):
    docs = retriever.invoke(q)
    ctx = "\n".join(d.page_content for d in docs)
    return (prompt | llm).invoke({"context": ctx, "q": q}).content
```

**Flow:**
1. Retrieve relevant documents for the question
2. Concatenate document contents into context string
3. Use LCEL pipe (`|`) to chain prompt and LLM
4. Return the generated answer

### 4. Gradio UI

```python
ui = gr.Interface(fn=answer, inputs=gr.Textbox(label="Question"), outputs=gr.Markdown())
ui.launch()
```

Creates a simple web interface:
- **Input**: Text box for questions
- **Output**: Markdown-rendered answers
- **launch()**: Starts local web server (typically at `http://127.0.0.1:7860`)

## Key Concepts Demonstrated

| Concept | Implementation |
|---------|----------------|
| **Embeddings** | OpenAIEmbeddings converts text to vectors |
| **Vector Store** | FAISS stores and searches embeddings |
| **Retrieval** | `retriever.invoke(q)` finds relevant docs |
| **Prompt Template** | Structures the LLM input with context |
| **LCEL Chaining** | `prompt \| llm` pipes data through components |
| **Web UI** | Gradio provides instant web interface |

## Common Issues & Fixes

### Import Error: `HfFolder` not found

The `gradio` package has a dependency conflict with newer `huggingface_hub` versions.

**Fix:**
```python
import sys
!{sys.executable} -m pip install "huggingface_hub<0.25"
```

Then restart the kernel.

### Better pip install (ensures correct Python environment)

```python
import sys
!{sys.executable} -m pip -q install langchain langchain-community langchain-openai faiss-cpu tiktoken gradio "huggingface_hub<0.25"
```

## Try It Yourself

1. Run all cells in order
2. When Gradio launches, open the provided URL
3. Ask questions like:
   - "What helps with retrieval?"
   - "How can I improve trust in AI answers?"
   - "What does RAG do?"

## Extensions to Explore

- Add more documents to the knowledge base
- Use a PDF loader instead of hardcoded texts
- Add conversation memory for multi-turn chat
- Deploy to Hugging Face Spaces
