"""Document Chat Bot -- Streamlit application powered by CrewAI agents.

Supports two modes:
  - Context Stuffing: sends the full document text in the prompt
  - RAG: chunks, embeds, and searches document via vector store
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load API key from the shared .env location
for env_path in [
    os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
    os.path.join(os.path.dirname(__file__), "..", ".env"),
    os.path.join(os.path.dirname(__file__), ".env"),
]:
    if os.path.exists(env_path):
        load_dotenv(env_path, override=True)
        if "OPENAI_API_KEY" in os.environ:
            break

from document_parser import extract_text
from vector_store import create_rag_tool
from agents import ask_question_stuffing, ask_question_rag

# --- Page Configuration ---
st.set_page_config(
    page_title="Document Chat Bot",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Document Chat Bot")
st.caption("Upload a document and ask questions about its content. Powered by CrewAI + GPT-4o.")

# --- Check for API Key ---
if "OPENAI_API_KEY" not in os.environ:
    st.error(
        "OPENAI_API_KEY not found! Please add it to your .env file.\n\n"
        "Expected locations:\n"
        "- `crewai-demo/document-chat/.env`\n"
        "- `crewai-demo/.env`\n"
        "- `langchain-langgraph-demo/.env`"
    )
    st.stop()

# --- Initialize Session State ---
if "document_text" not in st.session_state:
    st.session_state.document_text = None
if "document_name" not in st.session_state:
    st.session_state.document_name = None
if "rag_tool" not in st.session_state:
    st.session_state.rag_tool = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Sidebar ---
with st.sidebar:
    st.header("📁 Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "txt", "docx"],
        help="Supported formats: PDF, TXT, DOCX",
    )

    st.divider()

    # Mode toggle
    st.header("⚙️ Mode")
    mode = st.radio(
        "Choose Q&A approach:",
        options=["RAG (Recommended)", "Context Stuffing"],
        help=(
            "**RAG**: Chunks the document, embeds it in a vector database, "
            "and retrieves only relevant passages per question. "
            "Better for large documents, lower cost per question.\n\n"
            "**Context Stuffing**: Sends the full document text in the prompt. "
            "Simpler but limited to ~100K characters and higher cost."
        ),
    )
    use_rag = mode == "RAG (Recommended)"

    # Process uploaded file
    if uploaded_file is not None:
        if st.session_state.document_name != uploaded_file.name:
            spinner_msg = (
                "Processing document and building search index..."
                if use_rag
                else "Extracting text from document..."
            )
            with st.spinner(spinner_msg):
                try:
                    file_bytes = uploaded_file.read()
                    text = extract_text(uploaded_file.name, file_bytes)

                    st.session_state.document_text = text
                    st.session_state.document_name = uploaded_file.name
                    st.session_state.chat_history = []
                    st.session_state.rag_tool = None

                    # Build RAG index if in RAG mode
                    if use_rag:
                        rag_tool = create_rag_tool(
                            document_text=text,
                            document_name=uploaded_file.name,
                        )
                        st.session_state.rag_tool = rag_tool

                    st.success(f"Loaded: {uploaded_file.name}")
                except Exception as e:
                    st.error(f"Error processing file: {e}")
                    st.session_state.document_text = None
                    st.session_state.document_name = None
                    st.session_state.rag_tool = None

        # Build RAG index if switching to RAG mode with existing document
        if (
            use_rag
            and st.session_state.document_text
            and st.session_state.rag_tool is None
        ):
            with st.spinner("Building search index for RAG mode..."):
                try:
                    rag_tool = create_rag_tool(
                        document_text=st.session_state.document_text,
                        document_name=st.session_state.document_name,
                    )
                    st.session_state.rag_tool = rag_tool
                except Exception as e:
                    st.error(f"Error building index: {e}")

        # Show document info
        if st.session_state.document_text:
            badge = "RAG" if use_rag and st.session_state.rag_tool else "Stuffing"
            st.info(
                f"**{st.session_state.document_name}** ({badge} mode)\n\n"
                f"{len(st.session_state.document_text):,} characters extracted"
            )
            with st.expander("Preview document text"):
                preview = st.session_state.document_text[:2000]
                if len(st.session_state.document_text) > 2000:
                    preview += "\n\n..."
                st.text(preview)

    st.divider()

    # Clear chat button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

    # How it works
    with st.expander("How it works"):
        if use_rag:
            st.markdown(
                "**RAG Mode (Active)**\n\n"
                "1. **Upload** a PDF, TXT, or DOCX file\n"
                "2. Document is **chunked and indexed** in a vector database (ChromaDB)\n"
                "3. **Ask** any question about the document\n"
                "4. Two CrewAI agents collaborate:\n"
                "   - **Document Analyst** searches for relevant passages using RAG\n"
                "   - **Q&A Specialist** formulates the answer\n"
                "5. Answers are based **only** on retrieved document chunks"
            )
        else:
            st.markdown(
                "**Context Stuffing Mode (Active)**\n\n"
                "1. **Upload** a PDF, TXT, or DOCX file\n"
                "2. Full document text is extracted\n"
                "3. **Ask** any question about the document\n"
                "4. Two CrewAI agents collaborate:\n"
                "   - **Document Analyst** reads the full document and extracts relevant info\n"
                "   - **Q&A Specialist** formulates the answer\n"
                "5. Answers are based **only** on document content"
            )

# --- Main Area: Chat Interface ---
if st.session_state.document_text is None:
    st.info(
        "👈 Upload a document using the sidebar to get started. "
        "You can upload PDF, TXT, or DOCX files."
    )
else:
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if question := st.chat_input("Ask a question about your document..."):
        # Add user message to history and display it
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        # Generate answer
        with st.chat_message("assistant"):
            spinner_msg = (
                "Searching document and generating answer..."
                if use_rag
                else "Analyzing document and generating answer..."
            )
            with st.spinner(spinner_msg):
                try:
                    if use_rag and st.session_state.rag_tool:
                        answer = ask_question_rag(
                            rag_tool=st.session_state.rag_tool,
                            question=question,
                        )
                    else:
                        answer = ask_question_stuffing(
                            document_text=st.session_state.document_text,
                            question=question,
                        )
                    st.markdown(answer)
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": answer}
                    )
                except Exception as e:
                    error_msg = f"An error occurred: {e}"
                    st.error(error_msg)
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": error_msg}
                    )
