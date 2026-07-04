# Project Structure Advisor (LangChain Edition)

An AI-assisted tool that takes a user's project description (stack, type, deployment target) and returns an **industry-standard folder structure** — using LangChain for semantic template retrieval and structured LLM-based refinement.

## What it does

1. User describes their project in plain text (e.g. "Go backend, Postgres, deployed on AWS")
2. The description is embedded and matched against a curated library of templates using FAISS
3. The matched template(s) + user's specific details are sent through an LCEL chain that produces a merged, validated folder structure
4. The result is rendered as a text tree, markdown, or actual folders/files on disk

## Folder structure

```
project-structure-advisor/
│
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── main.py                         # CLI entry point
│
├── templates/                      # curated folder-structure templates
│   ├── backend_fastapi.yaml
│   ├── backend_go.yaml
│   ├── frontend_react.yaml
│   ├── frontend_nextjs.yaml
│   ├── mobile_flutter.yaml
│   ├── fullstack_react_go.yaml
│   └── multi_agent_llm.yaml
│
├── core/
│   ├── __init__.py
│   ├── template_loader.py          # loads YAML templates + builds description strings
│   ├── vector_store.py             # builds/loads FAISS index over template descriptions
│   ├── retriever_chain.py          # embeds user input, retrieves top-k templates
│   ├── schemas.py                  # Pydantic models: FolderNode, ProjectStructure
│   ├── refiner_chain.py            # ChatPromptTemplate + LLM + PydanticOutputParser (LCEL)
│   ├── pipeline.py                 # composes retriever + refiner into one runnable
│   └── generator.py                # renders ProjectStructure as text tree / real files
│
├── cli/
│   ├── __init__.py
│   └── interactive.py              # asks user questions, prints resulting tree
│
├── api/                             # optional: expose as a web service
│   ├── __init__.py
│   ├── routes.py
│   └── request_schemas.py
│
├── examples/
│   └── sample_outputs.md           # example inputs and generated structures
│
└── tests/
    ├── __init__.py
    ├── test_vector_store.py
    ├── test_retriever_chain.py
    ├── test_refiner_chain.py
    └── test_generator.py
```

## Requirements

```
langchain
langchain-openai          # or langchain-anthropic
langchain-community        # for FAISS integration
faiss-cpu
pydantic
python-dotenv
typer                      # CLI framework
pyyaml
pytest
```

## Setup

```bash
git clone <your-repo-url>
cd project-structure-advisor

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env and add your API key:
# OPENAI_API_KEY=sk-...
# or ANTHROPIC_API_KEY=sk-ant-...
```

## Implementation steps

### Phase 1 — Template library
- [ ] Write a YAML file per template under `templates/`, each containing:
  - `name`: short id (e.g. `backend_go`)
  - `description`: a rich, keyword-natural sentence used for embedding (this is what retrieval quality depends on)
  - `structure`: the actual folder tree for that stack
- [ ] Write `template_loader.py` to parse all YAML files into Python objects and extract `(name, description)` pairs for embedding

### Phase 2 — Vector store
- [ ] In `vector_store.py`, embed all template descriptions with `OpenAIEmbeddings` (or `HuggingFaceEmbeddings` if you want a free/local option)
- [ ] Build a FAISS index with `FAISS.from_texts(descriptions, embeddings, metadatas=[...])`
- [ ] Persist the index locally (`vectorstore.save_local("template_index")`) so you don't re-embed on every run

### Phase 3 — Retriever chain
- [ ] In `retriever_chain.py`, load the saved FAISS index and wrap it: `vectorstore.as_retriever(search_kwargs={"k": 2})`
- [ ] Given raw user input, retrieve the top-k closest templates with their metadata

### Phase 4 — Schemas
- [ ] In `schemas.py`, define `FolderNode` (recursive: name, children, description) and `ProjectStructure` (wraps a root `FolderNode`)

### Phase 5 — Refiner chain (LCEL)
- [ ] In `refiner_chain.py`, build:
  - A `ChatPromptTemplate` with a system message (architect persona + constraints) and a human message (matched templates + user input + format instructions)
  - A `PydanticOutputParser` bound to `ProjectStructure`
  - The chain: `prompt | llm | parser`
- [ ] Wrap with `OutputFixingParser` so malformed output gets one automatic retry instead of crashing

### Phase 6 — Pipeline composition
- [ ] In `pipeline.py`, compose retriever + refiner into a single callable: raw user text in, validated `ProjectStructure` out
- [ ] This is the one function the CLI/API actually calls

### Phase 7 — Generator
- [ ] In `generator.py`, write a function that walks `ProjectStructure.root` recursively and:
  - Renders it as an indented text tree (for terminal output)
  - Renders it as markdown (for docs)
  - Optionally creates real folders/files on disk with `os.makedirs` / `open(..., "w")`

### Phase 8 — CLI
- [ ] In `cli/interactive.py`, use `typer` to prompt the user for a description (or accept it as an argument), call the pipeline, print the tree

### Phase 9 — Tests
- [ ] Mock the LLM in chain tests (LangChain supports `FakeListLLM` for deterministic testing)
- [ ] Test the retriever against known stack descriptions to confirm it returns the expected template
- [ ] Test the generator's tree-rendering logic independent of the LLM

### Phase 10 — Examples & polish
- [ ] Run 3–5 real examples, save input/output pairs to `examples/sample_outputs.md`
- [ ] Add a short architecture diagram to this README or a `docs/` folder

## Running it

```bash
python main.py
# Describe your project: Go backend, Postgres, deployed on AWS

# Or non-interactively:
python main.py --input "React frontend, Go backend, PostgreSQL, AWS deployment"
```

Example output:

```
Matched templates: fullstack_react_go (92% match)

project-name/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── services/
│   └── package.json
├── backend/
│   ├── cmd/
│   ├── internal/
│   │   ├── handlers/
│   │   ├── services/
│   │   └── repository/
│   ├── migrations/
│   └── go.mod
├── docker-compose.yml
└── .github/workflows/
```

## Design notes worth knowing before you build

- **Why FAISS over keyword matching**: embeddings capture meaning, not exact words, so a query like "typed server-side routes" can still match a FastAPI template without using that name explicitly.
- **Why `temperature=0` on the refiner LLM**: you want consistent, deterministic structure output, not creative variation between runs.
- **Why start with a smaller model** (`gpt-4o-mini` or `claude-haiku-4-5`): this task is bounded structured transformation, not open-ended reasoning — a small model is usually enough, and keeps iteration cheap. Only escalate to a larger model if you observe real quality problems on your test set.
- **Why `OutputFixingParser` matters**: without it, a single malformed JSON response crashes the pipeline. With it, a failed parse gets sent back to the LLM once with the validation error, which is usually enough to self-correct.

## Future improvements

- Expand the template library based on real usage (microservices, data pipelines, mobile-only)
- Swap keyword-based template descriptions for richer embeddings that also encode folder purpose, not just stack name
- Add an option to scaffold the generated structure directly into a new git repository
- Add a small eval script comparing output quality across 2–3 candidate LLMs on your example set

## License

MIT
