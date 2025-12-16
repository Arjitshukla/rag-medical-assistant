# store_index.py

from langchain_community.vectorstores import FAISS
from src.helper import (
    load_pdf_files,
    filter_to_minimal_documents,
    split_text,
    download_embeddings
)

def create_and_save_faiss_index():
    print("📄 Loading PDFs...")
    documents = load_pdf_files("data")

    print("🧹 Filtering documents...")
    documents = filter_to_minimal_documents(documents)

    print("✂️ Splitting text into chunks...")
    chunks = split_text(documents)

    print("🧠 Loading embeddings model...")
    embeddings = download_embeddings()

    print("📦 Creating FAISS index...")
    vector_store = FAISS.from_documents(chunks, embeddings)

    print("💾 Saving FAISS index to disk...")
    vector_store.save_local("faiss_index")

    print("✅ FAISS index created and saved successfully")

if __name__ == "__main__":
    create_and_save_faiss_index()
