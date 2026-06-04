from backend.vector_store import load_embeddings
from backend.knowledge_base import get_all_documents
from backend.services.search import cosine_similarity
from backend.services.embedder import create_embeddings

def search_all_documents(query):
    documents = get_all_documents()
    query_embedding = create_embeddings([query])[0]
    results = []

    for document in documents:
        data = load_embeddings(document)
        
        # Safety check: skip if the file is empty or missing expected keys
        if not data or "chunks" not in data or "embeddings" not in data:
            continue

        chunks = data["chunks"]
        embeddings = data["embeddings"]

        for chunk, embedding in zip(chunks, embeddings):
            score = cosine_similarity(query_embedding, embedding)
            results.append({
                "document": document,
                "chunk": chunk,
                "score": float(score)
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:10]