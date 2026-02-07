# Document Chat Bot

A Streamlit chatbot that lets you upload documents (PDF, TXT, DOCX) and ask questions about their content. Powered by CrewAI multi-agent framework and GPT-4o.

Supports two Q&A modes:
- **RAG** -- chunks the document, embeds in ChromaDB, retrieves relevant passages per question
- **Context Stuffing** -- sends the full document text in the prompt

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed diagrams and component descriptions.

**RAG mode (recommended):**
```
Upload:   Document -> extract text -> chunk -> embed -> ChromaDB
Question: Agent searches ChromaDB for relevant chunks -> Q&A Specialist answers
```

**Context Stuffing mode:**
```
Upload:   Document -> extract full text
Question: Full text + question passed to Agent -> Q&A Specialist answers
```

Both modes use two CrewAI agents in a sequential pipeline:
1. **Document Analyst** -- finds relevant information (via search tool in RAG, or from full text in stuffing)
2. **Q&A Specialist** -- formulates a clear, grounded answer

## Setup

```bash
# Navigate to the crewai-demo directory
cd crewai-demo

# Activate the existing virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r document-chat/requirements.txt

# Make sure your OPENAI_API_KEY is set in one of these .env files:
#   - crewai-demo/.env
#   - langchain-langgraph-demo/.env

# Run the app
streamlit run document-chat/app.py
```

## Usage

1. Open the app in your browser (default: http://localhost:8501)
2. **Choose a mode** in the sidebar (RAG or Context Stuffing)
3. Upload a document (PDF, TXT, or DOCX) using the sidebar
4. Ask questions in the chat input at the bottom
5. View AI-generated answers based on your document content
6. Switch modes or upload a different document at any time

## File Structure

```
document-chat/
  app.py               # Streamlit UI (file upload, mode toggle, chat)
  agents.py            # CrewAI agents/tasks for both modes
  document_parser.py   # Text extraction for PDF, DOCX, TXT
  vector_store.py      # RAG: ChromaDB indexing via CrewAI RagTool
  ARCHITECTURE.md      # Detailed architecture diagrams
  requirements.txt     # Python dependencies
  README.md            # This file
```

## Limitations

- **PDF images/scanned text**: Only embedded text is extracted (no OCR)
- **Response time**: Each question requires two sequential GPT-4o API calls (~10-30 seconds)
- **Session-only**: Chat history is stored in memory and lost on app restart
- **Context Stuffing mode**: Limited to ~100K characters; larger documents are truncated
- **RAG mode**: Initial upload takes longer (chunking + embedding), but questions are faster and cheaper
