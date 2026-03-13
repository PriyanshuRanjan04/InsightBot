import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_huggingface import HuggingFaceEmbeddings
from config.config import EMBEDDING_MODEL

def get_embedding_model():
    """Initialize and return the HuggingFace embedding model"""
    try:
        embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )
        return embedding_model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize embedding model: {str(e)}")