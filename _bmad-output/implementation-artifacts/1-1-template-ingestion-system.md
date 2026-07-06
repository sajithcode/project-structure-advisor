---
baseline_commit: fcc8be3fb7cd9eebeefb10ce4120dd7a08bbcb5e
---

# Story 1.1: Template Ingestion System

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a CLI User,
I want the system to parse YAML files from a `templates/` directory,
so that their name, description, and structure are available in memory for indexing.

## Acceptance Criteria

1. **Given** a directory containing valid YAML template files
2. **When** the CLI initialization sequence runs
3. **Then** the system successfully parses the `name`, `description`, and `structure` from each file
4. **And** ignores any non-YAML files or malformed YAML without crashing the app

## Tasks / Subtasks

- [x] Task 1: Define the Template Schema (AC: 1, 3)
  - [x] Use Pydantic to create a `TemplateModel` capturing `name` (str), `description` (str), and `structure` (dict/Any).
- [x] Task 2: Implement the Directory Scanner (AC: 1, 2)
  - [x] Write a utility to list all `.yaml` and `.yml` files in a given `templates/` path.
- [x] Task 3: Implement Resilient YAML Parsing (AC: 3, 4)
  - [x] Safely parse each file using `yaml.safe_load`.
  - [x] Validate parsed content against `TemplateModel`.
  - [x] Catch parser errors and validation errors, logging warnings instead of crashing.
- [x] Task 4: Unit Testing
  - [x] Test with a mix of valid templates, invalid YAML, and non-YAML files to ensure stability.

## Dev Notes

- **Architecture AD-2 Constraint:** Keep the pipeline completely stateless. The parser utility should just take a `directory_path` string and return a `List[TemplateModel]`. Do not use global state to store templates.
- **Resilience:** Use `logging` or a simple print warning for skipped templates. A single bad template must not block the entire application start.

### Project Structure Notes

- Alignment with unified project structure: Place logic in a core/domain module (e.g., `advisor/parser.py` or similar).

### References

- [Source: epics.md#Epic-1]
- [Source: ARCHITECTURE-SPINE.md#AD-2]

## Dev Agent Record

### Agent Model Used

Antigravity

### Debug Log References

N/A

### Completion Notes List

- Implemented `TemplateModel` using Pydantic.
- Created `parse_template_directory` in `advisor/parser.py` to scan and safely parse YAML files.
- Added comprehensive unit tests in `tests/test_parser.py` covering valid, invalid, and non-YAML scenarios. Tests pass.

### File List

- `advisor/__init__.py` [NEW]
- `advisor/parser.py` [NEW]
- `tests/test_parser.py` [NEW]
