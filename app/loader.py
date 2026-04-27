from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_split(file_path, source_name=None):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    for doc in docs:
        doc.metadata["source"] = source_name or file_path
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_documents(docs)