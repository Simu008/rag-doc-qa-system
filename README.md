# RAG DOCUMENT QA SYSTEM

## Live Demo
- https://rag-doc-app-system-cu5ndappdvv4zrtdkuqquyf.streamlit.app/

## Demo
![App Screenshot](./Assets/Demo1.png)
![App Screenshot](./Assets/Demo2.png)

## Overview
A RAG-based QA system where users upload PDF documents and ask questions in natural language. Answers are generated with source citations showing which document and page the answer came from.

## Features
- Upload and query multiple PDFs simultaneously
- Source citations: filename + page number for every answer
- Dynamic retrieval: k=10 for broad questions, k=5 for specific ones

## Tech Stack
- LLM: Groq (llama-3.3-70b-versatile)
- Embeddings: HuggingFace all-MiniLM-L6-v2
- Vector DB: ChromaDB
- Frontend: Streamlit
- Framework: LangChain

## Setup
- git clone https://github.com/Simu008/rag-doc-qa-system.git
- cd rag_system
- pip install -r requirements.txt

## Add your API key to .env
GROQ_API_KEY=your_key_here

## Run
streamlit run ui/main.py

## Project Structure
- loader.py: document processing
- vector_store.py: embeddings & storage
- retriever.py: search
- generator.py: LLM response
- rag_pipeline.py: pipeline
 
