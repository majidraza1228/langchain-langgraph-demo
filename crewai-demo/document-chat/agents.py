"""CrewAI agents, tasks, and crew configuration for document Q&A.

Supports two modes:
  - Context Stuffing: full document text injected into the prompt
  - RAG: agent uses a search tool to retrieve relevant chunks from a vector store
"""

from crewai import Agent, Task, Crew, Process


# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------

def create_document_analyst(rag_tool=None) -> Agent:
    """Create the Document Analyst agent.

    Args:
        rag_tool: If provided, the agent uses this tool to search the document (RAG mode).
                  If None, the agent expects the full document in the task description (stuffing mode).
    """
    if rag_tool:
        # RAG mode -- agent searches via tool
        return Agent(
            role="Document Analyst",
            goal=(
                "Search the uploaded document to find and extract the most relevant "
                "sections and information that relate to the user's question. "
                "Use the Document Search tool to query for relevant passages."
            ),
            backstory=(
                "You are an expert document analyst with years of experience in "
                "reading, comprehending, and extracting key information from all "
                "types of documents. You have access to a search tool that lets you "
                "find relevant passages in the document. You should search with "
                "multiple queries if needed to find all relevant information. "
                "You always work strictly from the document and never fabricate information."
            ),
            verbose=False,
            allow_delegation=False,
            llm="gpt-4o",
            tools=[rag_tool],
        )
    else:
        # Stuffing mode -- agent reads the full document from the prompt
        return Agent(
            role="Document Analyst",
            goal=(
                "Thoroughly read and understand the provided document content. "
                "Extract the most relevant sections and information that relate "
                "to the user's question."
            ),
            backstory=(
                "You are an expert document analyst with years of experience in "
                "reading, comprehending, and extracting key information from all "
                "types of documents. You excel at identifying relevant passages, "
                "understanding context, and summarizing complex content. You always "
                "work strictly from the provided document and never fabricate information."
            ),
            verbose=False,
            allow_delegation=False,
            llm="gpt-4o",
        )


def create_qa_specialist() -> Agent:
    """Create the Q&A Specialist agent (same for both modes)."""
    return Agent(
        role="Q&A Specialist",
        goal=(
            "Provide clear, accurate, and well-structured answers to the "
            "user's question based strictly on the document analysis provided."
        ),
        backstory=(
            "You are a knowledgeable Q&A specialist who excels at formulating "
            "precise, helpful answers. You synthesize information from document "
            "analysis into clear, conversational responses. If the document does "
            "not contain enough information to answer the question, you honestly "
            "state that rather than guessing."
        ),
        verbose=False,
        allow_delegation=False,
        llm="gpt-4o",
    )


# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------

def create_analysis_task_stuffing(analyst: Agent) -> Task:
    """Create the analysis task for STUFFING mode (full document in prompt)."""
    return Task(
        description=(
            "Analyze the following document and extract all information "
            "relevant to the user's question.\n\n"
            "USER QUESTION: {question}\n\n"
            "DOCUMENT CONTENT:\n{document_text}\n\n"
            "Instructions:\n"
            "1. Read the entire document carefully.\n"
            "2. Identify all sections, passages, and facts relevant to the question.\n"
            "3. If the document does not contain relevant information, state that clearly.\n"
            "4. Do NOT make up information that is not in the document."
        ),
        expected_output=(
            "A structured analysis containing:\n"
            "- Relevant excerpts or key points from the document\n"
            "- Context around those points\n"
            "- An assessment of how well the document addresses the question"
        ),
        agent=analyst,
    )


def create_analysis_task_rag(analyst: Agent) -> Task:
    """Create the analysis task for RAG mode (agent uses search tool)."""
    return Task(
        description=(
            "Find all information in the uploaded document that is relevant "
            "to the user's question. Use the Document Search tool to search "
            "for relevant passages.\n\n"
            "USER QUESTION: {question}\n\n"
            "Instructions:\n"
            "1. Analyze the question and identify key concepts to search for.\n"
            "2. Use the Document Search tool with targeted queries to find relevant passages.\n"
            "3. If the first search doesn't find enough information, try rephrasing "
            "your query or searching for related terms.\n"
            "4. Compile all relevant excerpts and information found.\n"
            "5. If the document does not contain relevant information, state that clearly.\n"
            "6. Do NOT make up information that is not in the document."
        ),
        expected_output=(
            "A structured analysis containing:\n"
            "- Relevant excerpts or key points from the document\n"
            "- Context around those points\n"
            "- An assessment of how well the document addresses the question"
        ),
        agent=analyst,
    )


def create_answer_task(qa_specialist: Agent, analysis_task: Task) -> Task:
    """Create the Q&A task (same for both modes)."""
    return Task(
        description=(
            "Based on the document analysis provided, answer the following "
            "question clearly and accurately.\n\n"
            "USER QUESTION: {question}\n\n"
            "Instructions:\n"
            "1. Use ONLY the information from the document analysis to form your answer.\n"
            "2. Be direct and concise. Do not repeat the question.\n"
            "3. If the document does not contain enough information, say so honestly.\n"
            "4. Use a helpful, conversational tone."
        ),
        expected_output=(
            "A clear, well-structured answer to the user's question based "
            "on the document content. If the answer cannot be found in the "
            "document, state that explicitly."
        ),
        agent=qa_specialist,
        context=[analysis_task],
    )


# ---------------------------------------------------------------------------
# Crew execution
# ---------------------------------------------------------------------------

def ask_question_stuffing(document_text: str, question: str) -> str:
    """Answer a question using STUFFING mode (full document in prompt).

    Args:
        document_text: The extracted text content of the uploaded document.
        question: The user's question about the document.

    Returns:
        The answer as a string.
    """
    analyst = create_document_analyst(rag_tool=None)
    qa_specialist = create_qa_specialist()

    analysis_task = create_analysis_task_stuffing(analyst)
    answer_task = create_answer_task(qa_specialist, analysis_task)

    crew = Crew(
        agents=[analyst, qa_specialist],
        tasks=[analysis_task, answer_task],
        process=Process.sequential,
        verbose=False,
    )

    # Escape curly braces to avoid interpolation errors
    safe_document_text = document_text.replace("{", "{{").replace("}", "}}")
    safe_question = question.replace("{", "{{").replace("}", "}}")

    result = crew.kickoff(
        inputs={
            "document_text": safe_document_text,
            "question": safe_question,
        }
    )

    return result.raw


def ask_question_rag(rag_tool, question: str) -> str:
    """Answer a question using RAG mode (agent searches vector store).

    Args:
        rag_tool: A RagTool instance for document retrieval.
        question: The user's question about the document.

    Returns:
        The answer as a string.
    """
    analyst = create_document_analyst(rag_tool=rag_tool)
    qa_specialist = create_qa_specialist()

    analysis_task = create_analysis_task_rag(analyst)
    answer_task = create_answer_task(qa_specialist, analysis_task)

    crew = Crew(
        agents=[analyst, qa_specialist],
        tasks=[analysis_task, answer_task],
        process=Process.sequential,
        verbose=False,
    )

    safe_question = question.replace("{", "{{").replace("}", "}}")

    result = crew.kickoff(
        inputs={
            "question": safe_question,
        }
    )

    return result.raw
