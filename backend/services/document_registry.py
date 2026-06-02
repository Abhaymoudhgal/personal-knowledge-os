import json
from pathlib import Path
from datetime import datetime

REGISTRY_FILE = Path(
    "backend/data/documents.json"
)


def load_registry():

    if not REGISTRY_FILE.exists():
        return []

    with open(
        REGISTRY_FILE,
        "r"
    ) as f:

        return json.load(f)


def save_registry(data):

    with open(
        REGISTRY_FILE,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )

def add_document(
    filename,
    chunk_count
):

    registry = load_registry()

    for doc in registry:

        if doc["filename"] == filename:
            return

    registry.append(
        {
            "filename": filename,
            "chunks": chunk_count,
            "indexed": True,
            "uploaded_at":
                datetime.now().isoformat()
        }
    )

    save_registry(registry)

def get_documents():

    return load_registry()