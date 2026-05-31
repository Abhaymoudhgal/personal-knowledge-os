from fastapi import FastAPI

app = FastAPI(
    title="Personal Knowledge Operating System",
    version="0.0.1"
)

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