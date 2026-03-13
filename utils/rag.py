import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from models.embeddings import get_embedding_model
from config.config import CHUNK_SIZE, CHUNK_OVERLAP, MAX_RETRIEVAL_DOCS

def load_and_split_document(file_path):
    """Load a PDF document and split into chunks"""
    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        chunks = text_splitter.split_documents(pages)
        return chunks
    except Exception as e:
        raise RuntimeError(f"Failed to load document: {str(e)}")

def create_vectorstore(chunks):
    """Create FAISS vectorstore from document chunks"""
    try:
        embedding_model = get_embedding_model()
        vectorstore = FAISS.from_documents(chunks, embedding_model)
        return vectorstore
    except Exception as e:
        raise RuntimeError(f"Failed to create vectorstore: {str(e)}")

def retrieve_relevant_chunks(vectorstore, query):
    """Retrieve relevant chunks from vectorstore based on query"""
    try:
        retriever = vectorstore.as_retriever(
            search_kwargs={"k": MAX_RETRIEVAL_DOCS}
        )
        docs = retriever.invoke(query)
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve chunks: {str(e)}")