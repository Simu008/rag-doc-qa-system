from app.retriever import retrieve
from app.generator import generate_answer

def rag_pipeline(query):
    # Step 1: Retrieve relevant chunks
    docs = retrieve(query)
    
    if not docs:
        return "No relevant content found in the documents.", []
    
    # Step 2: Build context with source labels for the LLM
    context = "\n\n---\n\n".join(
        [f"[Source: {d['source']} | Page: {d['page']}]\n{d['content']}" 
         for d in docs]
    )
    
    # Step 3: Generate answer
    answer = generate_answer(query, context)
    return answer, docs