from services.local_embeddings import get_embedding
from services.vector_store import query_vectors
from services.gemini_client import generate_answer

def ask_question(question: str) -> str:
    # 1️⃣ Embed the question
    query_embedding = get_embedding(question)

    # 2️⃣ Retrieve relevant chunks
    docs = query_vectors(query_embedding, top_k=3)

    if not docs:
        return "Answer not found in the document."

    # 3️⃣ Build context
    context = "\n\n".join(docs)

    # 4️⃣ 🔥 QUESTION-AWARE PROMPT (THIS IS THE FIX)
    prompt = f"""
You are a study assistant.
Answer the question STRICTLY using the document context below.

Document context:
{context}

Question:
{question}

Rules:
- Answer only what is asked
- Be concise and clear
- If answer is not in context, say: "Answer not found in the document."
"""

    # 5️⃣ Let Gemini think
    return generate_answer(prompt)
