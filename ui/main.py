import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.loader import load_and_split
from app.vector_store import clear_and_add_documents
from app.rag_pipeline import rag_pipeline

st.set_page_config(page_title="RAG App")
st.title("📄RAG Document QA System")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "docs_loaded" not in st.session_state:
    st.session_state.docs_loaded = False
if "loaded_file_names" not in st.session_state:
    st.session_state.loaded_file_names = []

uploaded_files = st.file_uploader(
    "Upload one or more PDFs",
    type="pdf",
    accept_multiple_files=True
)

# Check if uploaded files changed
current_names = sorted([f.name for f in uploaded_files]) if uploaded_files else []
already_loaded = current_names == st.session_state.loaded_file_names

if uploaded_files and not already_loaded:
    all_chunks = []

    with st.spinner("Processing documents..."):
        for uploaded_file in uploaded_files:
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.read())

            chunks = load_and_split(temp_path, source_name=uploaded_file.name)
            all_chunks.extend(chunks)  # collect ALL chunks first
            os.remove(temp_path)

    # Store ALL chunks together in one single call
    total = clear_and_add_documents(all_chunks)
    st.session_state.docs_loaded = True
    st.session_state.loaded_file_names = current_names
    st.session_state.messages = []
    st.success(f"✅ {len(uploaded_files)} doc(s) processed — {total} chunks indexed!")

if not uploaded_files:
    st.session_state.docs_loaded = False
    st.session_state.loaded_file_names = []
    st.session_state.messages = []

# Display chat history
for role, msg in st.session_state.messages:
    if role == "user":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)

user_input = st.chat_input("Ask something about your documents...")

if user_input and st.session_state.docs_loaded:
    with st.spinner("Thinking..."):
        answer, docs = rag_pipeline(user_input)

    st.session_state.messages.append(("user", user_input))
    st.session_state.messages.append(("bot", answer))

    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(answer)

    with st.expander("📚 View Sources & Citations"):
        seen = set()
        for i, d in enumerate(docs):
            source = d['source']
            page = d['page']
            content = d['content']
            key = f"{source}_p{page}"
            if key not in seen:
                seen.add(key)
                st.markdown(f"**Citation {i+1}:** 📄 `{source}` — Page {page}")
                st.caption(content[:300] + "...")
                st.divider()

elif user_input and not st.session_state.docs_loaded:
    st.warning("⚠️ Please upload at least one PDF first.")