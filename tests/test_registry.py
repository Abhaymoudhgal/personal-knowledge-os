from backend.services.document_registry import (
    add_document,
    get_documents
)

add_document(
    "test.pdf",
    25
)

print(
    get_documents()
)