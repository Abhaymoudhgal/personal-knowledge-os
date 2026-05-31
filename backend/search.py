import numpy as np

from backend.embedder import create_embeddings


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

        scores.append(
            (chunk, float(similarity))
        )

    scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return scores[:3]