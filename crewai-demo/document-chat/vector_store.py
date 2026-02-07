"""Vector store management for document RAG pipeline using CrewAI's RagTool."""

import hashlib

from crewai_tools import RagTool


def _collection_name(doc_name: str, content_length: int) -> str:
    """Generate a stable, ChromaDB-safe collection name from document identity."""
    raw = f"{doc_name}_{content_length}"
    hash_hex = hashlib.md5(raw.encode()).hexdigest()[:12]
    return f"doc-{hash_hex}"


def create_rag_tool(document_text: str, document_name: str) -> RagTool:
    """
    Create a RagTool initialized with the given document content.

    Chunks the text, embeds it with OpenAI text-embedding-3-small,
    and stores in a ChromaDB collection for semantic search.

    Args:
        document_text: Full extracted text of the uploaded document.
        document_name: Filename (used for collection naming).

    Returns:
        A RagTool instance ready for agent use.
    """
    collection = _collection_name(document_name, len(document_text))

    rag_tool = RagTool(
        name="Document Search",
        description=(
            "Search the uploaded document for information relevant to a query. "
            "Pass a search query string and get back the most relevant passages "
            "from the document."
        ),
        collection_name=collection,
        similarity_threshold=0.3,
        limit=8,
        config={
            "vectordb": {
                "provider": "chromadb",
                "config": {},
            },
            "embedding_model": {
                "provider": "openai",
                "config": {
                    "model_name": "text-embedding-3-small",
                },
            },
        },
    )

    # Add document text -- RagTool internally uses TextChunker
    # (1500 chars, 150 overlap) and embeds into ChromaDB
    rag_tool.add(document_text, data_type="text")

    return rag_tool
