from services.gemini_client import get_embedding
from services.vector_store import query_vectors
import google.generativeai as genai

def ask_question(question):
    q_embedding = get_embedding(question)
    results = query_vectors(q_embedding)

    context = " ".join(results["documents"][0])

    prompt = f"""
    Answer strictly from the context below:
    {context}

    Question: {question}
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    return response.text
