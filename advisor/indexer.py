import os
from pathlib import Path
from typing import List, Any, Optional
from langchain_community.vectorstores import FAISS
from advisor.parser import TemplateModel
from langchain_core.documents import Document

# Assuming the project root is one level up from the advisor directory
PROJECT_ROOT = Path(__file__).parent.parent
CACHE_DIR = PROJECT_ROOT / ".advisor_cache" / "faiss_index"

def load_faiss_index(embeddings_model: Any) -> Optional[FAISS]:
    """Load FAISS index from local cache if it exists."""
    if CACHE_DIR.exists():
        try:
            return FAISS.load_local(
                str(CACHE_DIR), 
                embeddings_model,
                allow_dangerous_deserialization=True
            )
        except Exception:
            return None
    return None

def save_faiss_index(vectorstore: FAISS) -> None:
    """Save FAISS index to local cache."""
    if vectorstore:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        vectorstore.save_local(str(CACHE_DIR))

def create_faiss_index(templates: List[TemplateModel], embeddings_model: Any) -> Optional[FAISS]:
    """
    Creates a FAISS vector store from a list of TemplateModel objects.
    Embeds the description and retains name and structure in metadata.
    """
    if not templates:
        return None
        
    documents = []
    for template in templates:
        doc = Document(
            page_content=template.description,
            metadata={
                "name": template.name,
                "structure": template.structure
            }
        )
        documents.append(doc)
    
    vectorstore = FAISS.from_documents(documents, embeddings_model)
    return vectorstore
