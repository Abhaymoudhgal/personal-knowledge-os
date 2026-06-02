from backend.services.document_registry import (
    get_documents
)

from backend.services.memory import (
    get_history
)


def get_dashboard_stats():

    documents = get_documents()

    history = get_history()

    total_chunks = sum(
        doc["chunks"]
        for doc in documents
    )

    return {
        "documents": len(documents),
        "total_chunks": total_chunks,
        "messages": len(history)
    }