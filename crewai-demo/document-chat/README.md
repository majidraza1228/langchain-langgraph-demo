# Document Chat Bot

A Streamlit chatbot that lets you upload documents (PDF, TXT, DOCX) and ask questions about their content. Powered by CrewAI multi-agent framework and GPT-4o.

## Architecture

Two CrewAI agents collaborate in a sequential pipeline for each question:

```
User Question + Document Text
        |
        v
[Document Analyst]    -- reads document, extracts relevant sections
        |
        v  (context chain)
[Q&A Specialist]      -- formulates a clear, grounded answer
        |
        v
Answer displayed in Streamlit chat
```

### Why Two Agents?

- **Document Analyst** focuses on comprehension and relevance extraction
- **Q&A Specialist** focuses on clear, user-friendly answer formulation
- The context-chain pattern means the Q&A Specialist receives a pre-digested, focused summary rather than the raw document, leading to more precise answers

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
2. Upload a document (PDF, TXT, or DOCX) using the sidebar
3. Ask questions in the chat input at the bottom
4. View AI-generated answers based on your document content
5. Upload a different document at any time -- chat history resets automatically

## File Structure

```
document-chat/
  app.py               # Streamlit UI (file upload + chat interface)
  agents.py            # CrewAI agent/task/crew configuration
  document_parser.py   # Text extraction for PDF, DOCX, TXT
  requirements.txt     # Python dependencies
  README.md            # This file
```

## Limitations

- **PDF images/scanned text**: Only embedded text is extracted (no OCR)
- **Large documents**: Text is truncated at ~100K characters to stay within the LLM context window
- **Response time**: Each question requires two sequential GPT-4o API calls (~10-30 seconds)
- **Session-only**: Chat history is stored in memory and lost on app restart

## CrewAI Configuration

| Component | Value |
|-----------|-------|
| Agents | 2 (Document Analyst + Q&A Specialist) |
| Process | Sequential |
| LLM | GPT-4o |
| Delegation | Disabled (deterministic pipeline) |
| Input method | Template interpolation (`{document_text}`, `{question}`) |
