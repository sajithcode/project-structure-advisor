from unittest.mock import MagicMock, patch
from advisor.indexer import create_faiss_index, save_faiss_index, load_faiss_index, CACHE_DIR
from advisor.parser import TemplateModel
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
import shutil

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

def test_load_and_save_faiss_index(tmp_path):
    # Setup mock templates
    templates = [
        TemplateModel(name="test_cache", description="A test template", structure={})
    ]
    mock_embeddings = FakeEmbeddings()
    vectorstore = create_faiss_index(templates, mock_embeddings)
    
    with patch("advisor.indexer.CACHE_DIR", tmp_path / ".advisor_cache" / "faiss_index"):
        # Initially, cache does not exist
        assert load_faiss_index(mock_embeddings) is None
        
        # Save it
        save_faiss_index(vectorstore)
        
        # Now it should load
        loaded_vectorstore = load_faiss_index(mock_embeddings)
        assert loaded_vectorstore is not None
        assert isinstance(loaded_vectorstore, FAISS)
        
        # Test search on loaded index
        results = loaded_vectorstore.similarity_search("test", k=1)
        assert len(results) == 1
        assert results[0].metadata["name"] == "test_cache"
