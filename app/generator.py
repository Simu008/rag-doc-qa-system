from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

def generate_answer(query, context):
    if not context.strip():
        return "I could not find relevant information in the uploaded documents."

    prompt = f"""You are a strict document assistant. Follow these rules:
1. Answer ONLY using the context provided below.
2. If the answer is not in the context, say "I don't have enough information in the documents to answer this."
3. Do NOT use your own knowledge or assumptions.
4. Be concise and accurate.
5. If information comes from multiple documents, mention which document.

---
CONTEXT:
{context}

---
QUESTION:
{query}

---
ANSWER:"""

    response = llm.invoke(prompt)
    return response.content