from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
from backend.pdf_reader import extract_text
from backend.chunker import chunk_text
from backend.embedder import create_embeddings
from backend.search import search_chunks

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

@app.get("/documents")
def list_documents():
    return {
        "documents": [
            file.name
            for file in UPLOAD_DIR.iterdir()
            if file.is_file() and file.suffix == ".pdf"
        ]
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
        "chunks": chunks[:5]
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