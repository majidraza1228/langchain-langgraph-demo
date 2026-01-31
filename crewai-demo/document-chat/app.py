"""Document Chat Bot -- Streamlit application powered by CrewAI agents."""

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
from agents import ask_question

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
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Sidebar: Document Upload ---
with st.sidebar:
    st.header("📁 Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "txt", "docx"],
        help="Supported formats: PDF, TXT, DOCX",
    )

    if uploaded_file is not None:
        # Only re-parse if the file changed
        if st.session_state.document_name != uploaded_file.name:
            with st.spinner("Extracting text from document..."):
                try:
                    file_bytes = uploaded_file.read()
                    text = extract_text(uploaded_file.name, file_bytes)
                    st.session_state.document_text = text
                    st.session_state.document_name = uploaded_file.name
                    st.session_state.chat_history = []
                    st.success(f"Loaded: {uploaded_file.name}")
                except Exception as e:
                    st.error(f"Error reading file: {e}")
                    st.session_state.document_text = None
                    st.session_state.document_name = None

        # Show document info
        if st.session_state.document_text:
            st.info(
                f"**{st.session_state.document_name}**\n\n"
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
        st.markdown(
            "1. **Upload** a PDF, TXT, or DOCX file\n"
            "2. **Ask** any question about the document\n"
            "3. Two CrewAI agents collaborate to answer:\n"
            "   - **Document Analyst** extracts relevant info\n"
            "   - **Q&A Specialist** formulates the answer\n"
            "4. Answers are based **only** on document content"
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
            with st.spinner("Analyzing document and generating answer..."):
                try:
                    answer = ask_question(
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
