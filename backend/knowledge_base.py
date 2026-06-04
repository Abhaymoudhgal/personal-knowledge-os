from pathlib import Path

VECTOR_DIR = Path("backend/vector_store")

def get_all_documents():
    documents = []
    
    for file in VECTOR_DIR.glob("*.json"):
        # Safely extract the exact document name by removing the exact ".json" extension
        if file.name.endswith(".json"):
            doc_name = file.name[:-5]
            documents.append(doc_name)
            
    return documents