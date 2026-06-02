from backend.services.document_registry import (
    get_documents
)

from backend.vector_store import (
    load_embeddings
)

from backend.services.search import (
    search_chunks
)


def find_relevant_documents(query):

    matches = []

    documents = get_documents()

    for doc in documents:

        data = load_embeddings(
            doc["filename"]
        )

        if not data:
            continue

        chunks = data["chunks"]

        results = search_chunks(
            query,
            chunks
        )

        best_score = results[0][1]

        matches.append(
            {
                "filename":
                    doc["filename"],
                "score":
                    round(best_score, 4)
            }
        )

    matches.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return matches[:5]