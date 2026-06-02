from backend.services.retriever import (
    search_all_documents
)
from backend.services.llm import ask_llm
from backend.services.memory import (
    add_message,
    get_history
)

def ask_knowledge_base(question):

    add_message(
        "user",
        question
    )

    results = search_all_documents(question)

    if not results:
        return "No relevant information found in the knowledge base."

    # print("\nTOP RESULTS")
    # print("=" * 50)

    # for i, item in enumerate(results[:10], start=1):
    #     print(f"\nRESULT {i}")
    #     print(item["chunk"][:300])
    #     print("=" * 50)

    history = get_history()

    memory_context = "\n".join(
        [
            f"{msg['role']}: {msg['content']}"
            for msg in history[-10:]
        ]
    )

    context = "\n\n".join(
        [
            item["chunk"]
            for item in results[:10]
        ]
    )

    full_context = f"""
Conversation History:
{memory_context}

Knowledge Base Context:
{context}
"""

    answer = ask_llm(
        full_context,
        question
    )

    sources = []

    for item in results[:5]:

        sources.append(
            {
                "document":
                    item["document"],
                "score":
                    round(
                        item["score"],
                        4
                    )
            }
        )

    add_message(
        "assistant",
        answer
    )

    return {
        "answer": answer,
        "sources": sources
    }