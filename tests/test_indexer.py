from unittest.mock import MagicMock
from advisor.indexer import create_faiss_index
from advisor.parser import TemplateModel
from langchain_core.documents import Document

from langchain_core.embeddings import Embeddings

class FakeEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [[0.1] * 1536 for _ in texts]
    def embed_query(self, text):
        return [0.1] * 1536

def test_create_faiss_index_success():
    # Setup mock templates
    templates = [
        TemplateModel(name="test_1", description="A FastAPI project", structure={"folder": "file"}),
        TemplateModel(name="test_2", description="A React frontend", structure={"src": "index.js"})
    ]

    # Use FakeEmbeddings
    mock_embeddings = FakeEmbeddings()
    
    # Run the indexer
    vectorstore = create_faiss_index(templates, embeddings_model=mock_embeddings)
    
    # Validate the results
    assert vectorstore is not None
    
    results = vectorstore.similarity_search("fastapi", k=1)
    
    # We just want to make sure it returns a Document that retains metadata
    assert len(results) == 1
    assert isinstance(results[0], Document)
    assert results[0].metadata["name"] == "test_1"
    assert "structure" in results[0].metadata
