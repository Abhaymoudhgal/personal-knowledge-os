import numpy as np

from backend.services.embedder import create_embeddings
from backend.vector_store import load_embeddings
from pathlib import Path


def cosine_similarity(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def search_chunks(query, chunks):

    embeddings = create_embeddings(
        chunks + [query]
    )

    query_embedding = embeddings[-1]

    chunk_embeddings = embeddings[:-1]

    scores = []

    for chunk, embedding in zip(
        chunks,
        chunk_embeddings
    ):

        similarity = cosine_similarity(
        query_embedding,
        embedding
        )

        if query.lower() in chunk.lower():
            similarity += 0.5

        scores.append(
            (chunk, float(similarity))
        )

    scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    for chunk, score in scores:
        print("\nSCORE:", score)
        print(chunk[:200])
        print("=" * 50)

    return scores[:10]

def search_document(filename, query):

    data = load_embeddings(filename)

    if data is None:
        return []

    chunks = data["chunks"]

    chunk_embeddings = data["embeddings"]

    query_embedding = create_embeddings(
        [query]
    )[0]

    scores = []

    for chunk, embedding in zip(
        chunks,
        chunk_embeddings
    ):

        similarity = cosine_similarity(
            query_embedding,
            embedding
        )

        if query.lower() in chunk.lower():
            similarity += 0.5

        scores.append(
            (chunk, float(similarity))
        )

    scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return scores[:10]