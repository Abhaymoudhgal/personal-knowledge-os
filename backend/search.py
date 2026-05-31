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

from pathlib import Path

from backend.pdf_reader import extract_text
from backend.chunker import chunk_text


UPLOAD_DIR = Path("backend/uploads")


def search_document(filename, query):

    file_path = UPLOAD_DIR / filename

    text = extract_text(file_path)

    chunks = chunk_text(text)

    return search_chunks(
        query,
        chunks
    )