---
project_name: 'project-structure-advisor'
user_name: 'Sajith'
date: '2026-07-06'
sections_completed:
  ['technology_stack', 'language_rules', 'framework_rules', 'testing_rules', 'quality_rules', 'workflow_rules', 'anti_patterns']
status: 'complete'
rule_count: 17
optimized_for_llm: true
existing_patterns_found: 0
---

# Project Context for AI Agents

_This file contains critical rules and patterns that AI agents must follow when implementing code in this project. Focus on unobvious details that agents might otherwise miss._

---

## Technology Stack & Versions

- **Language:** Python
- **LLM Orchestration:** `langchain`, `langchain-openai`, `langchain-anthropic`, `langchain-community`
- **Vector Store:** `faiss-cpu`
- **Data Validation & Parsing:** `pydantic`
- **CLI Framework:** `typer`
- **Configuration & Env:** `pyyaml`, `python-dotenv`
- **Testing:** `pytest`

*(Note: Exact versions have not been strictly bound yet; agents should default to the latest stable versions unless otherwise specified.)*

## Critical Implementation Rules

### Language-Specific Rules

- **Strict Type Hinting:** Use standard Python type hints everywhere. This is especially critical for `pydantic` schemas (`schemas.py`) which rely on them for validation.
- **Environment Management:** Always load configuration via `python-dotenv`. Never hardcode API keys or environments (expect `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`).
- **Imports:** Group standard library imports, third-party imports (like `langchain` and `typer`), and local module imports separately.

### Framework-Specific Rules

- **LangChain Expression Language (LCEL):** Build the refiner pipeline using the modern LCEL syntax (`prompt | llm | parser`) rather than legacy LangChain constructs.
- **LLM Determinism:** Always instantiate your refiner LLM with `temperature=0`. The goal is rigid structural transformation, not creative variation.
- **Parser Resilience:** The base `PydanticOutputParser` MUST be wrapped inside an `OutputFixingParser`. This ensures that a single malformed JSON response is passed back to the LLM for self-correction rather than crashing the pipeline.
- **Vector Search (FAISS):** The template embedding index must be persisted and loaded locally (`vectorstore.save_local()`) to avoid re-embedding static templates on every CLI run.

### Testing Rules

- **Mock LLMs:** Always use LangChain's `FakeListLLM` (or equivalent mocks) in chain tests to ensure deterministic results without hitting live OpenAI/Anthropic APIs.
- **Generator Isolation:** Test the `generator.py` tree-rendering logic entirely independent of the LLM refiner step.
- **Retriever Validation:** Tests for the retriever must validate it against known stack descriptions to confirm it reliably returns the expected YAML template.
- **Test Framework:** Use `pytest` for all unit and integration tests.

### Code Quality & Style Rules

- **Code Formatting:** Adhere to PEP 8 standards. Use `snake_case` for variables/functions and `PascalCase` for Pydantic models (e.g., `FolderNode`, `ProjectStructure`).
- **Separation of Concerns:** Keep the retrieval logic (`retriever_chain.py`) completely isolated from the generation logic (`refiner_chain.py`). Only compose them together inside `pipeline.py`.
- **Docstrings:** All public functions, especially those exposed in the API or CLI, must have concise docstrings explaining their inputs and outputs.

### Development Workflow Rules

- **Dependency Management:** Whenever a new pip package is added to the virtual environment, agents must ensure `requirements.txt` is updated accordingly.
- **Commit Messages:** Use conventional commit formatting (e.g., `feat:`, `fix:`, `chore:`) to maintain a clean Git history.
- **Phased Implementation:** When developing, strictly follow the 10 implementation phases outlined in the README. Do not skip ahead or mix logic from multiple phases into a single commit.

### Critical Don't-Miss Rules

- **Avoid Keyword Matching:** Do not attempt to use regex or string-matching for template retrieval. You MUST rely on FAISS semantic embeddings, as user queries often won't perfectly match the template name (e.g., "typed server-side routes" matching a FastAPI template).
- **Enforce OutputFixingParser:** Never instantiate a raw `PydanticOutputParser` inside the LCEL chain without wrapping it in an `OutputFixingParser`. A single JSON syntax error from the LLM will crash the app without it.
- **Default to Small Models:** Always default to smaller, faster LLMs (like `gpt-4o-mini` or `claude-haiku-4-5`) for the generation task. Do not jump to massive reasoning models, as this task is a bounded structural transformation, not open-ended reasoning.

---

## Usage Guidelines

**For AI Agents:**

- Read this file before implementing any code
- Follow ALL rules exactly as documented
- When in doubt, prefer the more restrictive option
- Update this file if new patterns emerge

**For Humans:**

- Keep this file lean and focused on agent needs
- Update when technology stack changes
- Review quarterly for outdated rules
- Remove rules that become obvious over time

Last Updated: 2026-07-06
