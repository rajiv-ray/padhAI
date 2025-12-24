import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text):
    result = genai.embed_content(
        model="models/embedding-001",
        content=text
    )
    return result["embedding"]
