from typing import List, Any, Optional
from langchain_community.vectorstores import FAISS
from advisor.parser import TemplateModel
from langchain_core.documents import Document

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
