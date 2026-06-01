from backend.services.retriever import (
    search_all_documents
)

from backend.services.llm import ask_llm


def ask_knowledge_base(question):

    results = search_all_documents(question)

    if not results:
        return "No relevant information found in the knowledge base."

    # print("\nTOP RESULTS")
    # print("=" * 50)

    # for i, item in enumerate(results[:10], start=1):
    #     print(f"\nRESULT {i}")
    #     print(item["chunk"][:300])
    #     print("=" * 50)

    context = "\n\n".join(
        [
            item["chunk"]
            for item in results[:10]
        ]
    )

    answer = ask_llm(
        context,
        question
    )

    return answer