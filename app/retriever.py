from app.vector_store import get_retriever

# Keywords that suggest the user wants comprehensive info
SUMMARY_KEYWORDS = [
    "list", "all", "summarise", "summarize", "summary", 
    "everything", "tell me about", "what are", "projects",
    "skills", "experience", "education"
]

def retrieve(query):
   
    query_lower = query.lower()
    is_summary = any(word in query_lower for word in SUMMARY_KEYWORDS)
    k = 10 if is_summary else 5

    retriever = get_retriever(k=k)
    docs = retriever.get_relevant_documents(query)

    return [
        {
            "content": doc.page_content,
            "source": doc.metadata.get("source", "Unknown"),
            "page": doc.metadata.get("page", "?")
        }
        for doc in docs
    ]