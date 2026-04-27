from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

def clear_and_add_documents(chunks):
    vectordb = Chroma(
        collection_name="rag_collection",
        persist_directory="chroma_db",
        embedding_function=embedding
    )
    vectordb.delete_collection()

    vectordb = Chroma(
        collection_name="rag_collection",
        persist_directory="chroma_db",
        embedding_function=embedding
    )
    vectordb.add_documents(chunks)
    vectordb.persist()
    return len(chunks)

def get_retriever(k=5):
    vectordb = Chroma(
        collection_name="rag_collection",
        persist_directory="chroma_db",
        embedding_function=embedding
    )
    return vectordb.as_retriever(search_kwargs={"k": k})