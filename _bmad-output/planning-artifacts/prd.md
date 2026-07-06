---
title: "Project Structure Advisor"
status: "final"
created: "2026-07-06"
updated: "2026-07-06"
---

# PRD: Project Structure Advisor

## 1. Product Vision & Scope
An AI-assisted CLI tool that takes a user's plain-text project description and generates an industry-standard folder structure. It leverages FAISS for semantic template retrieval and LangChain (LCEL) for structured LLM-based refinement.

**Target Audience:** Developers (Solo or Internal teams) scaffolding new projects.

## 2. Functional Requirements (FRs)

### FR-1: Template Library & Ingestion
- **FR-1.1:** The system must read YAML files from a `templates/` directory containing `name`, `description`, and `structure` (the folder tree).
- **FR-1.2:** The system must embed the `description` of each template and index them using FAISS.

### FR-2: Semantic Retrieval
- **FR-2.1:** The CLI must accept a natural language description of a project stack (e.g., "Go backend, Postgres").
- **FR-2.2:** The system must use FAISS to retrieve the top-K semantically closest templates based on the user's description.

### FR-3: LLM Refiner Pipeline (LCEL)
- **FR-3.1:** The system must compose an LCEL chain (`prompt | llm | parser`) to merge the retrieved templates with the user's specific details.
- **FR-3.2:** The pipeline must use a `PydanticOutputParser` bound to a `ProjectStructure` schema to ensure valid structured output.
- **FR-3.3:** The parser MUST be wrapped in an `OutputFixingParser` to automatically retry malformed JSON responses.

### FR-4: Output Generation
- **FR-4.1:** The system must support rendering the generated `ProjectStructure` as an indented text tree in the terminal.
- **FR-4.2:** The system must support rendering the structure as markdown.
- **FR-4.3:** The system should optionally support physically creating the folders and files on disk.

## 3. Non-Functional Requirements (NFRs)
- **NFR-1 (Performance):** FAISS indexes must be saved locally (`vectorstore.save_local()`) to prevent re-embedding static templates on every execution.
- **NFR-2 (Reliability):** LLM generation must use `temperature=0` for strict determinism.
- **NFR-3 (Efficiency):** The default refiner LLM will be a small, fast model (e.g., `gpt-4o-mini` or `claude-haiku-4-5`) to optimize for speed and cost.


