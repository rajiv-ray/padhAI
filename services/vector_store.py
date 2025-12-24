import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

import chromadb

client = chromadb.Client()
collection = client.create_collection("padhai_notes")

def store_chunks(chunks, embeddings):
    for i, emb in enumerate(embeddings):
        collection.add(
            documents=[chunks[i]],
            embeddings=[emb],
            ids=[str(i)]
        )

def query_vectors(query_embedding):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )
