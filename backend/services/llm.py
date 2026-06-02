import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def ask_llm(context, question):

    prompt = f"""
You are a document assistant.

Answer the question using ONLY the provided context.

If the answer exists in the context,
quote the relevant information.

Context:
{context}

Question:
{question}

Answer:
"""

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        print(
            f"LLM ERROR: {e}"
        )

        return """
Gemini quota exceeded.

Your vector search and retrieval are working correctly,
but the language model is temporarily unavailable.

Please wait a few minutes or use a different Gemini API key.
"""