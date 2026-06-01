from backend.services.llm import ask_llm

response = ask_llm(
    "Abhay worked at DRDO.",
    "Where did Abhay work?"
)

print(response)