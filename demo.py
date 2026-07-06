import os
import shutil
from pathlib import Path
from advisor.parser import parse_template_directory
from advisor.indexer import create_faiss_index, load_faiss_index, save_faiss_index
from tests.test_indexer import FakeEmbeddings

def setup_dummy_templates():
    """Create a temporary templates directory with some sample files."""
    templates_dir = Path("templates")
    if templates_dir.exists():
        shutil.rmtree(templates_dir)
    templates_dir.mkdir()

    # Create a valid template
    valid_file = templates_dir / "react_app.yaml"
    valid_file.write_text("""
name: React + Vite App
description: A modern React application using Vite for fast builds.
structure:
  src/:
    components/: {}
    App.tsx: ""
  package.json: ""
""")

    # Create another valid template
    valid_file_2 = templates_dir / "fastapi_app.yaml"
    valid_file_2.write_text("""
name: FastAPI App
description: A fast python API using FastAPI.
structure:
  main.py: ""
  requirements.txt: ""
""")

    # Create a malformed template (missing 'description')
    invalid_file = templates_dir / "bad_template.yaml"
    invalid_file.write_text("""
name: Bad Template
structure:
  foo/: {}
""")

    return templates_dir

if __name__ == "__main__":
    print("--- 1. Setting up dummy 'templates/' directory ---")
    templates_dir = setup_dummy_templates()
    print("Files created: react_app.yaml (valid), fastapi_app.yaml (valid), bad_template.yaml (invalid)\n")
    
    print("--- 2. Running parse_template_directory() ---")
    parsed_templates = parse_template_directory(templates_dir)
    
    print("\n--- 3. Results ---")
    print(f"Successfully parsed {len(parsed_templates)} template(s):")
    for t in parsed_templates:
        print(f"- {t.name}: {t.description}")

    print("\n--- 4. Indexing templates with FAISS ---")
    # Using FakeEmbeddings for demo purposes without needing OpenAI keys
    embeddings = FakeEmbeddings()
    
    # Try to load from cache first
    vectorstore = load_faiss_index(embeddings)
    
    if vectorstore:
        print("Loaded FAISS vector store from local cache!")
    else:
        print("Local cache not found. Creating new FAISS vector store...")
        vectorstore = create_faiss_index(parsed_templates, embeddings)
        if vectorstore:
            save_faiss_index(vectorstore)
            print("Successfully created and saved FAISS vector store to cache!")
    
    if vectorstore:
        print("\n--- 5. Semantic Search ---")
        query = "A frontend framework"
        print(f"Searching for: '{query}'")
        # In a real scenario, this would use semantic similarity.
        # With FakeEmbeddings, it will just return the closest mock vectors.
        results = vectorstore.similarity_search(query, k=1)
        for r in results:
            print(f"Found match: {r.metadata['name']}")
            print(f"Structure: {r.metadata['structure']}")
    else:
        print("Failed to create FAISS vector store.")

    # Clean up (but don't delete cache so user can see it works next time)
    shutil.rmtree(templates_dir)
