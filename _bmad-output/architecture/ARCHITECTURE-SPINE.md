# Architecture Spine: Project Structure Advisor

*This document contains the structural invariants for the Project Structure Advisor. These rules bind how independently-built modules must interact and prevent architectural drift.*

---

## Architecture Decisions (AD)

### AD-1: Pipeline Orchestration Pattern
- **Rule:** The core generation logic MUST be composed as a single, linear LangChain Expression Language (LCEL) chain. The flow is: `User Input -> FAISS Retriever -> Context Merge -> Prompt -> LLM -> PydanticOutputParser (wrapped in OutputFixingParser)`. 
- **Prevents:** Custom while-loops, AgentExecutor loops, or legacy `LLMChain` classes.

### AD-2: State & Data Passing
- **Rule:** The LCEL pipeline is stateless. Data is passed strictly as dictionaries into the `.invoke()` method. 
- **Prevents:** The use of mutable state objects, global variables, or class-level state to share context between the retriever and the refiner.

### AD-3: Strict Output Separation
- **Rule:** The LCEL pipeline's ONLY responsibility is returning a validated `ProjectStructure` Pydantic object. A separate, isolated `Renderer` class is responsible for taking that object and converting it to terminal output, markdown, or physical disk files.
- **Prevents:** The parser or the LLM chains from attempting to write directly to disk or the console, preserving testability of the LLM logic.

### AD-4: Index Caching Strategy
- **Rule:** [ASSUMPTION] The FAISS index generated from the YAML templates must be saved to a local `.advisor_cache/faiss_index` directory at the project root. On execution, the CLI checks for this directory. It uses `vectorstore.load_local()` if present, and only embeds/saves if missing.
- **Prevents:** Costly and slow embedding API calls on every single CLI invocation.

### AD-5: Dependency Injection at the Boundary
- **Rule:** [ASSUMPTION] The Typer CLI entrypoint (`main.py`) is solely responsible for loading environment variables (via `python-dotenv`) and instantiating the API keys and FAISS paths. These are passed down into the core logic.
- **Prevents:** Hidden environment dependencies (like `os.environ.get`) buried deep within the LangChain domain logic, which makes unit testing difficult.

---

## Deferred Decisions
- **Packaging & Distribution:** How the CLI will be packaged (e.g., PyPI, Docker, PyInstaller) is deferred until the core tool is functional.
- **Template Schema Validation:** Whether to strictly validate the user-provided YAML templates on startup is deferred; we assume well-formed YAML for now.
