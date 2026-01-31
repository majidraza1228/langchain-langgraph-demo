"""CrewAI agents, tasks, and crew configuration for document Q&A."""

from crewai import Agent, Task, Crew, Process


def create_document_analyst() -> Agent:
    """Create the Document Analyst agent."""
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
    """Create the Q&A Specialist agent."""
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


def create_analysis_task(analyst: Agent) -> Task:
    """Create the document analysis task with interpolation placeholders."""
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


def create_answer_task(qa_specialist: Agent, analysis_task: Task) -> Task:
    """Create the Q&A task that uses the analysis as context."""
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


def ask_question(document_text: str, question: str) -> str:
    """
    Create a CrewAI crew and run it to answer a question about a document.

    Args:
        document_text: The extracted text content of the uploaded document.
        question: The user's question about the document.

    Returns:
        The answer as a string.
    """
    # Create agents
    analyst = create_document_analyst()
    qa_specialist = create_qa_specialist()

    # Create tasks
    analysis_task = create_analysis_task(analyst)
    answer_task = create_answer_task(qa_specialist, analysis_task)

    # Assemble crew
    crew = Crew(
        agents=[analyst, qa_specialist],
        tasks=[analysis_task, answer_task],
        process=Process.sequential,
        verbose=False,
    )

    # Escape curly braces in document text and question to avoid
    # interpolation errors (e.g., if the document contains JSON or code)
    safe_document_text = document_text.replace("{", "{{").replace("}", "}}")
    safe_question = question.replace("{", "{{").replace("}", "}}")

    # Run the crew
    result = crew.kickoff(
        inputs={
            "document_text": safe_document_text,
            "question": safe_question,
        }
    )

    return result.raw
