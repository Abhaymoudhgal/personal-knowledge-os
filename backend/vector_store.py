from pathlib import Path
import json

VECTOR_DIR = Path("backend/vector_store")

VECTOR_DIR.mkdir(exist_ok=True)


def save_embeddings(filename, chunks, embeddings):

    data = {
        "chunks": chunks,
        "embeddings": embeddings
    }

    path = VECTOR_DIR / f"{filename}.json"

    with open(path, "w") as f:
        json.dump(data, f)


def load_embeddings(filename):

    path = VECTOR_DIR / f"{filename}.json"

    if not path.exists():
        return None

    with open(path, "r") as f:
        return json.load(f)