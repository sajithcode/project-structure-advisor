---
stepsCompleted:
  - "step-01-validate-prerequisites"
  - "step-02-design-epics"
  - "step-03-create-stories"
inputDocuments:
  - "e:\\leo-d\\ai\\project-structure-advisor\\_bmad-output\\planning-artifacts\\prd.md"
  - "e:\\leo-d\\ai\\project-structure-advisor\\_bmad-output\\architecture\\ARCHITECTURE-SPINE.md"
---

# Project Structure Advisor - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Project Structure Advisor, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR-1.1: Read YAML files from a `templates/` directory containing name, description, and structure.
FR-1.2: Embed the `description` of each template and index them using FAISS.
FR-2.1: Accept natural language description of a project stack via CLI.
FR-2.2: Retrieve top-K semantically closest templates using FAISS based on description.
FR-3.1: Compose an LCEL chain to merge retrieved templates with user's details.
FR-3.2: Use `PydanticOutputParser` bound to `ProjectStructure` schema.
FR-3.3: Wrap parser in `OutputFixingParser`.
FR-4.1: Render generated `ProjectStructure` as an indented text tree in the terminal.
FR-4.2: Render the structure as markdown.
FR-4.3: Support optionally physically creating the folders and files on disk.

### NonFunctional Requirements

NFR-1 (Performance): Save FAISS indexes locally (`vectorstore.save_local()`)
NFR-2 (Reliability): Use `temperature=0` for strict determinism in LLM generation.
NFR-3 (Efficiency): Default refiner LLM will be a small, fast model (e.g., `gpt-4o-mini`).

### Additional Requirements

- [Architecture AD-1] The core generation logic MUST be composed as a single, linear LCEL chain.
- [Architecture AD-2] The LCEL pipeline is stateless. Data is passed strictly as dictionaries into `.invoke()`.
- [Architecture AD-3] The LCEL pipeline's ONLY responsibility is returning a validated `ProjectStructure`. A separate `Renderer` class handles terminal output/disk writes.
- [Architecture AD-4] FAISS index must be saved to a local `.advisor_cache/faiss_index` directory at the project root.
- [Architecture AD-5] The Typer CLI entrypoint (`main.py`) is solely responsible for loading environment variables and injecting paths.

### UX Design Requirements

N/A

### FR Coverage Map

FR-1.1: Epic 1 - Template reading
FR-1.2: Epic 1 - FAISS embedding & indexing
FR-2.1: Epic 2 - CLI natural language input
FR-2.2: Epic 2 - FAISS template retrieval
FR-3.1: Epic 2 - LCEL chain pipeline
FR-3.2: Epic 2 - Pydantic parsing
FR-3.3: Epic 2 - OutputFixingParser resilience
FR-4.1: Epic 2 - Terminal tree rendering
FR-4.2: Epic 2 - Markdown rendering
FR-4.3: Epic 3 - Physical file/folder creation

## Epic List

### Epic 1: Advisor Knowledge Base
Users can point the tool at their `templates/` folder, and the system automatically reads and indexes them into a fast, local semantic cache.
**FRs covered:** FR-1.1, FR-1.2

### Epic 2: Intelligent Project Generation
Users can describe their desired project stack via the CLI, and the tool semantically retrieves the right template, refines it with the LLM, and outputs a validated text tree or markdown to the terminal.
**FRs covered:** FR-2.1, FR-2.2, FR-3.1, FR-3.2, FR-3.3, FR-4.1, FR-4.2

### Epic 3: Physical Project Bootstrapping
Users can optionally instruct the tool to physically create the scaffolded folders and files on their local disk so they can start coding immediately.
**FRs covered:** FR-4.3

---

## Epic 1: Advisor Knowledge Base

Users can point the tool at their `templates/` folder, and the system automatically reads and indexes them into a fast, local semantic cache.

### Story 1.1: Template Ingestion System

As a CLI User,
I want the system to parse YAML files from a `templates/` directory,
So that their name, description, and structure are available in memory for indexing.

**Acceptance Criteria:**

**Given** a directory containing valid YAML template files
**When** the CLI initialization sequence runs
**Then** the system successfully parses the `name`, `description`, and `structure` from each file
**And** ignores any non-YAML files or malformed YAML without crashing the app

### Story 1.2: Semantic FAISS Indexing

As a CLI User,
I want the parsed templates to be embedded and indexed via FAISS,
So that I can perform semantic searches against their descriptions.

**Acceptance Criteria:**

**Given** parsed template objects in memory
**When** the indexing process is triggered
**Then** the system creates a FAISS vector store using the templates' descriptions
**And** the vector store can accurately return the top-K closest matches for a semantic test query

### Story 1.3: FAISS Local Caching

As a CLI User,
I want the FAISS index to be saved locally to `.advisor_cache/faiss_index` and loaded on subsequent runs,
So that the system doesn't waste time and API costs re-embedding static templates.

**Acceptance Criteria:**

**Given** an existing FAISS index on disk at `.advisor_cache/faiss_index`
**When** the CLI application starts
**Then** the system loads the local index instead of re-parsing the `templates/` directory
**And** if the directory does not exist, it builds the index from scratch and saves it there

---

## Epic 2: Intelligent Project Generation

Users can describe their desired project stack via the CLI, and the tool semantically retrieves the right template, refines it with the LLM, and outputs a validated text tree or markdown to the terminal.

### Story 2.1: CLI Interface & Stack Parsing

As a Developer,
I want to invoke the tool via a CLI command and pass a natural language description of my stack,
So that the tool knows what kind of project to generate.

**Acceptance Criteria:**
**Given** the Typer CLI is configured
**When** the user runs the `generate` command with a description (e.g., "fastapi with postgres")
**Then** the Typer app captures the string and passes it down into the core logic pipeline
**And** environment variables (like API keys) are loaded at this Typer boundary

### Story 2.2: FAISS Semantic Retrieval

As a Developer,
I want the tool to use my natural language description to fetch the most relevant template from the FAISS index,
So that the LLM has the correct baseline structure to work from.

**Acceptance Criteria:**
**Given** a user input string and a loaded FAISS index
**When** the retrieval step runs
**Then** it queries FAISS and returns the stringified content of the closest template(s)
**And** merges this template string with the user's original request into a single prompt dictionary

### Story 2.3: LCEL Pipeline Composition & Execution

As a Developer,
I want the tool to pass the retrieved template and my description through an LCEL pipeline,
So that a small LLM (like gpt-4o-mini) refines the template and outputs a rigid JSON structure.

**Acceptance Criteria:**
**Given** the merged prompt dictionary
**When** the LCEL chain (`Prompt -> LLM (temp=0) -> PydanticOutputParser -> OutputFixingParser`) runs
**Then** it returns a validated `ProjectStructure` python object
**And** it relies entirely on the `.invoke()` dictionary for state (no global mutation)

### Story 2.4: Structure Rendering

As a Developer,
I want the validated `ProjectStructure` object to be rendered as an indented text tree or markdown in my terminal,
So that I can visually review the generated structure.

**Acceptance Criteria:**
**Given** a valid `ProjectStructure` object
**When** the `Renderer` class processes it
**Then** it prints a formatted ASCII tree or markdown block to the terminal console
**And** the LLM parsing chain is completely isolated from this console output

---

## Epic 3: Physical Project Bootstrapping

Users can optionally instruct the tool to physically create the scaffolded folders and files on their local disk so they can start coding immediately.

### Story 3.1: Physical Disk Bootstrapping

As a Developer,
I want an optional flag (e.g., `--write-to-disk`) to physically create the files and folders,
So that I don't have to manually create the structure myself after generating it.

**Acceptance Criteria:**
**Given** a generated `ProjectStructure` and the `--write-to-disk` flag enabled
**When** the `Renderer` class executes
**Then** it creates the exact folder hierarchy and empty files on the local filesystem
**And** it safely handles cases where folders might already exist
