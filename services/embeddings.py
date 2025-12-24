from services.gemini_client import get_embedding

def generate_embeddings(chunks):
    return [get_embedding(chunk) for chunk in chunks]
