from pathlib import Path
from backend.vector_store import load_embeddings

VECTOR_DIR = Path("backend/vector_store")


def get_all_documents():

    documents = []

    for file in VECTOR_DIR.glob("*.json"):

        documents.append(
            file.stem.replace(".pdf", ".pdf")
        )

    return documents