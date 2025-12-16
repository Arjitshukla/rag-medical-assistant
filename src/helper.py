from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# extract text from pdfs
def load_pdf_files(file_path):
    loader = DirectoryLoader(
        file_path,
        glob="*.pdf", 
        loader_cls=PyPDFLoader)

    documents = loader.load()
    return documents



# filter to minimal data from documents
def filter_to_minimal_documents(documents: List[Document]) -> List[Document]:
    """this is return a new list of documents objects that have 
       containing only 'Source' in metadata and the original page_content.
    """
    minimal_doc :List[Document] = []
    for doc in documents:
        src =doc.metadata.get("Source")
        minimal_doc.append(
            Document(
                page_content=doc.page_content,
                metadata={"Source": src}
            )
        )
    return minimal_doc



# split documents into chunks
def split_text(minimal_documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=40,
    )
    test_chunks = text_splitter.split_documents(minimal_documents)
    return test_chunks



# download embeddings model
def download_embeddings():
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name
    )
    return embeddings
