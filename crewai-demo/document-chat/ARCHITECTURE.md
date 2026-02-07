# Document Chat Bot -- Architecture

This document describes the architecture of the Document Chat Bot, which supports
two Q&A modes: **Context Stuffing** and **RAG (Retrieval-Augmented Generation)**.

---

## High-Level Overview

```
                    ┌─────────────────────────────────────┐
                    │         Streamlit UI (app.py)        │
                    │   File Upload  |  Mode Toggle  |Chat │
                    └──────┬──────────────┬───────────┬────┘
                           │              │           │
                    ┌──────▼──────┐  ┌────▼────┐  ┌──▼──────────┐
                    │  document   │  │ vector  │  │   agents.py  │
                    │ _parser.py  │  │_store.py│  │  (CrewAI)    │
                    │             │  │         │  │              │
                    │ PDF/DOCX/TXT│  │ RagTool │  │ 2 Agents     │
                    │ extraction  │  │ ChromaDB│  │ 2 Tasks      │
                    └─────────────┘  └─────────┘  └──────────────┘
```

---

## Mode 1: Context Stuffing

The full document text is injected directly into the agent's prompt.

```
    ┌──────────┐     ┌──────────────┐     ┌──────────────────────────────┐
    │ User     │     │ document     │     │ CrewAI Sequential Pipeline   │
    │ uploads  │────>│ _parser.py   │     │                              │
    │ document │     │ extract_text │     │  ┌────────────────────────┐  │
    └──────────┘     └──────┬───────┘     │  │ Document Analyst      │  │
                            │             │  │                        │  │
                       Full text          │  │ Receives FULL document │  │
                       (up to 100K)       │  │ + question in prompt   │  │
                            │             │  └───────────┬────────────┘  │
    ┌──────────┐            │             │              │               │
    │ User     │            │             │         analysis             │
    │ asks     │────────────┼────────────>│              │               │
    │ question │            │             │  ┌───────────▼────────────┐  │
    └──────────┘            │             │  │ Q&A Specialist         │  │
                            │             │  │                        │  │
                            │             │  │ Formulates answer from │  │
                            │             │  │ analyst's output       │  │
                            │             │  └───────────┬────────────┘  │
                            │             └──────────────┼───────────────┘
                            │                            │
                            │                       ┌────▼─────┐
                            │                       │  Answer   │
                            │                       └──────────┘
```

**Characteristics:**
- Simple, no vector store needed
- Full document sent on every question
- Limited to ~100K characters
- Higher token cost per question

---

## Mode 2: RAG (Retrieval-Augmented Generation)

Document is chunked, embedded, and stored in a vector database.
The agent searches for relevant chunks per question.

```
    DOCUMENT UPLOAD (one-time)
    ══════════════════════════

    ┌──────────┐     ┌──────────────┐     ┌──────────────────────────┐
    │ User     │     │ document     │     │ vector_store.py          │
    │ uploads  │────>│ _parser.py   │────>│ create_rag_tool()        │
    │ document │     │ extract_text │     │                          │
    └──────────┘     └──────────────┘     │  1. Chunk text           │
                                          │     (1500 chars/150 ovlp)│
                                          │  2. Embed chunks         │
                                          │     (text-embedding-     │
                                          │      3-small)            │
                                          │  3. Store in ChromaDB    │
                                          └──────────┬───────────────┘
                                                     │
                                               ┌─────▼──────┐
                                               │  ChromaDB   │
                                               │  Collection │
                                               └─────────────┘


    QUESTION ANSWERING (per question)
    ═════════════════════════════════

    ┌──────────┐     ┌──────────────────────────────────────────┐
    │ User     │     │ CrewAI Sequential Pipeline               │
    │ asks     │────>│                                          │
    │ question │     │  ┌────────────────────────────────────┐  │
    └──────────┘     │  │ Document Analyst (has RagTool)     │  │
                     │  │                                    │  │
                     │  │  "revenue figures" ──> ChromaDB    │  │
                     │  │  "Q3 results"     ──> ChromaDB    │  │
                     │  │                                    │  │
                     │  │  Receives top-8 relevant chunks    │  │
                     │  │  Compiles structured analysis      │  │
                     │  └──────────────┬─────────────────────┘  │
                     │                 │                         │
                     │            analysis                      │
                     │                 │                         │
                     │  ┌──────────────▼─────────────────────┐  │
                     │  │ Q&A Specialist                     │  │
                     │  │                                    │  │
                     │  │ Formulates clear answer from       │  │
                     │  │ the analyst's retrieved passages   │  │
                     │  └──────────────┬─────────────────────┘  │
                     └─────────────────┼─────────────────────────┘
                                       │
                                  ┌────▼─────┐
                                  │  Answer   │
                                  └──────────┘
```

**Characteristics:**
- Handles large documents (500K+ characters)
- Only relevant chunks sent to LLM per question
- Lower token cost per question
- Agent can issue multiple search queries for complex questions

---

## Component Details

| File | Responsibility |
|------|---------------|
| `app.py` | Streamlit UI: file upload, mode toggle, chat interface, session state |
| `agents.py` | CrewAI agent/task definitions for both modes, crew execution |
| `document_parser.py` | Text extraction from PDF (PyPDF2), DOCX (python-docx), TXT |
| `vector_store.py` | Thin wrapper around CrewAI's `RagTool` for ChromaDB management |

---

## RAG Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Embedding Model | `text-embedding-3-small` | Fast, cheap, 1536 dimensions |
| Vector DB | ChromaDB (persistent) | Already bundled with CrewAI, no server needed |
| Chunk Size | 1500 chars | CrewAI TextChunker default, good for paragraphs |
| Chunk Overlap | 150 chars | Preserves context across chunk boundaries |
| Top-K Results | 8 | Enough context for complex questions |
| Similarity Threshold | 0.3 | Low threshold favors recall; agent handles relevance |

---

## Comparison: Stuffing vs RAG

| Aspect | Context Stuffing | RAG |
|--------|-----------------|-----|
| Document size limit | ~100K chars | 500K+ chars |
| Cost per question | High (full doc every time) | Low (only relevant chunks) |
| Setup complexity | None | Chunking + embedding on upload |
| Answer accuracy | Good for small docs | Better for large docs (focused) |
| Upload speed | Fast (text only) | Slower (embed + index) |
| Multi-query search | No | Yes (agent can search multiple times) |
| Dependencies | CrewAI only | CrewAI + ChromaDB |

---

## Technology Stack

- **Framework**: CrewAI 1.9.2 (multi-agent orchestration)
- **LLM**: GPT-4o via OpenAI API
- **Embeddings**: OpenAI text-embedding-3-small
- **Vector Store**: ChromaDB 1.1.1 (persistent, in-process)
- **UI**: Streamlit 1.53.1
- **Document Parsing**: PyPDF2, python-docx
