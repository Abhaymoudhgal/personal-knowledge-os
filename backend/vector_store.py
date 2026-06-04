from pathlib import Path
import json

VECTOR_DIR = Path("backend/vector_store")
VECTOR_DIR.mkdir(parents=True, exist_ok=True)

def save_embeddings(filename, chunks, embeddings):
    data = {
        "chunks": chunks,
        "embeddings": embeddings
    }
    path = VECTOR_DIR / f"{filename}.json"
    
    # Explicitly use utf-8 to prevent crashes on complex PDF characters
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_embeddings(filename):
    path = VECTOR_DIR / f"{filename}.json"
    
    if not path.exists():
        return None
        
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)