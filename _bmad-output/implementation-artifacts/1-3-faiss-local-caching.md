---
baseline_commit: 826b8839f9e124e579ee7901de815f352a5ccfe4
---
# Story 1.3: FAISS Local Caching

## Story Foundation

**User Story Statement:**
As a CLI User,
I want the FAISS index to be saved locally to `.advisor_cache/faiss_index` and loaded on subsequent runs,
So that the system doesn't waste time and API costs re-embedding static templates.

**Business Context & Value:**
Re-embedding static templates on every CLI run wastes time and money (API costs). By saving the FAISS index locally, subsequent runs will be significantly faster, providing a snappy CLI experience.

**Acceptance Criteria:**
- [x] **Given** an existing FAISS index on disk at `.advisor_cache/faiss_index`
- [x] **When** the CLI application starts
- [x] **Then** the system loads the local index instead of re-parsing the `templates/` directory
- [x] **And** if the directory does not exist, it builds the index from scratch and saves it there

---

## Developer Context

### Technical Requirements
- Extend `advisor.indexer` with logic to save and load the FAISS index from disk.
- You can use Langchain FAISS's `save_local()` and `load_local()` methods.
- **CRITICAL:** In recent Langchain versions, `FAISS.load_local()` uses Python's `pickle` under the hood. You must pass `allow_dangerous_deserialization=True` explicitly when loading a local index to avoid exceptions.
- Ensure the cache folder `.advisor_cache/faiss_index` is created relative to the project root.

### Architecture Compliance
- **Caching Awareness (AD-4):** FAISS index must be saved to a local `.advisor_cache/faiss_index` directory at the project root.
- Continue to decouple concerns: `indexer.py` should provide the caching methods (e.g. `get_or_create_faiss_index` or extending the existing indexer to cache), and clients (`demo.py` or `main.py`) should call it.

### Library/Framework Requirements
- `langchain_community.vectorstores.FAISS`
- `os` and `pathlib` for checking if the cache directory exists.

### File Structure Requirements
- Update `advisor/indexer.py` to add load/save functionality.
- Update `tests/test_indexer.py` to cover saving/loading indices.

### Previous Story Intelligence
- In Story 1.2, we found that `FAISS.from_documents` crashes on an empty document list. We added a check to return `None`. Be sure that the caching logic handles this gracefully (e.g., don't save a `None` index to disk, or handle cases where index loading fails).
- Mocking: Use `FakeEmbeddings` for any new unit tests as done previously.

## Project Context Reference
- Epic 1: Advisor Knowledge Base
- Related Architecture Rules: AD-4

## File List
- `advisor/indexer.py` (Modified: Added `load_faiss_index` and `save_faiss_index`)
- `tests/test_indexer.py` (Modified: Added `test_load_and_save_faiss_index`)
- `demo.py` (Modified: Updated logic to try to load from cache before parsing and indexing)

## Dev Agent Record
**Completion Notes:**
- Created `CACHE_DIR` constant configured for `.advisor_cache/faiss_index`.
- Created `load_faiss_index` to fetch FAISS cache safely passing `allow_dangerous_deserialization=True`.
- Created `save_faiss_index` to safely create folders and cache.
- Updated `tests/test_indexer.py` passing unit tests for load/save logic using patched paths and fake embeddings.
- Verified test suite passes without regressions.

## Completion Status
- **Status:** `done`
- **Note:** Implementation is complete and ready for review.

### Review Findings
- [x] [Review][Patch] `CACHE_DIR` uses relative path [advisor/indexer.py:8]
- [x] [Review][Patch] Missing exception handling for `load_local` [advisor/indexer.py:10]
