from services.chunking import chunk_text
from services.vector_store import build_index
from services.retrieval import retrive_chunks

def answer_question(resume_text: str , question:str):
    chunks = chunk_text(resume_text)

    index,_ = build_index(chunks)

    relevant_chunks = retrive_chunks(question,chunks,index)

    # ----LLM STUB (replace later) ----

    answer = "Based on the resume: \n\n"
    for c in relevant_chunks:
        answer += f"- {c[:200]}...\n"
    return answer