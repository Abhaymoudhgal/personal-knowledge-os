from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
from backend.services.pdf_reader import extract_text
from backend.services.chunker import chunk_text
from backend.services.embedder import create_embeddings
from backend.services.search import search_chunks
from backend.services.llm import ask_llm
from backend.vector_store import (
    save_embeddings,
    load_embeddings
)
from backend.services.retriever import (
    search_all_documents
)
from backend.knowledge_base import get_all_documents
from backend.services.knowledge_qa import (
    ask_knowledge_base
)
from backend.services.memory import (
    get_history,
    clear_history
)
from backend.services.document_registry import (
    add_document
)



app = FastAPI(
    title="Personal Knowledge Operating System",
    version="0.0.1"
)

UPLOAD_DIR = Path("backend/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
def root():
    return {
        "message": "Welcome to PKOS"
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "filename": file.filename,
        "status": "uploaded"
    }


@app.get("/documents/{filename}")
def read_document(filename: str):

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    text = extract_text(file_path)

    return {
        "filename": filename,
        "characters": len(text),
        "preview": text[:1000]
    }

@app.get("/documents/{filename}/chunks")
def get_chunks(filename: str):

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    text = extract_text(file_path)

    chunks = chunk_text(text)

    return {
        "filename": filename,
        "total_chunks": len(chunks),
        "chunks": chunks
    }

@app.get("/documents/{filename}/embeddings")
def get_embeddings(filename: str):

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    text = extract_text(file_path)

    chunks = chunk_text(text)

    embeddings = create_embeddings(chunks)

    return {
        "filename": filename,
        "total_chunks": len(chunks),
        "embedding_dimension": len(embeddings[0]),
        "sample_embedding": embeddings[0][:10]
    }

@app.get("/documents/{filename}/search")
def search_document(
    filename: str,
    query: str
):

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    text = extract_text(file_path)

    chunks = chunk_text(text)

    results = search_chunks(
        query,
        chunks
    )

    return {
        "query": query,
        "results": results
    }

@app.get("/ask/{filename}")
def ask_document(filename: str, question: str):

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    text = extract_text(file_path)

    chunks = chunk_text(text)

    results = search_chunks(
        question,
        chunks
    )

    context = "\n\n".join(
        [chunk for chunk, score in results]
    )

    print("========== CONTEXT ==========")
    print(context)
    print("=============================")

    result = ask_llm(
        context,
        question
    )

    return {
    "question": question,
    "answer": result["answer"],
    "sources": result["sources"]
}

@app.post("/documents/{filename}/index")
def index_document(filename: str):

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    text = extract_text(file_path)

    chunks = chunk_text(text)

    embeddings = create_embeddings(chunks)

    save_embeddings(
        filename,
        chunks,
        embeddings
    )

    add_document(
        filename,
        len(chunks)
    )

    return {
        "message": "Document indexed"
    }


@app.get("/search")
def search_knowledge_base(query: str):

    results = search_all_documents(query)

    return {
        "query": query,
        "results": results
    }

@app.get("/ask-kb")
def ask_kb(question: str):

    result = ask_knowledge_base(question)

    return {
        "question": question,
        "answer": result["answer"],
        "sources": result["sources"]
    }

@app.get("/history")
def chat_history():

    return {
        "history": get_history()
    }

@app.delete("/history")
def delete_history():

    clear_history()

    return {
        "message": "History cleared"
    }

@app.get("/documents")
def list_documents():

    from backend.services.document_registry import (
        get_documents
    )

    return {
        "documents":
            get_documents()
    }

@app.delete("/documents/{filename}")
def delete_document_api(filename: str):

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    file_path.unlink()

    from backend.services.document_registry import (
        delete_document
    )

    delete_document(filename)

    return {
        "message": f"{filename} deleted"
    }   