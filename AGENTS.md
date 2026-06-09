# Agent Instructions for Phenomenon Project

This file contains instructions on how the AI agent should behave, communicate, and operate within this specific project directory.

## Persona & Communication Style
- Be concise and direct.
- Always explain the reasoning behind complex bash commands.
- If a user's instruction is highly ambiguous or unclear, ask clarifying follow-up questions instead of making a best-guess interpretation.

## Workflow & Task Execution
- Always run tests before committing changes.
- Prefer using `npm test` for verification.
- **TODO Management:** Once a task in `TODO.md` is completed, it must be entirely removed from the document, leaving only pending `[ ]` tasks.
- **Large-Scale Structural Refactoring:** 
  - **Avoid "Edit Exhaustion":** When a task requires modifying more than 5-10 files (e.g., renaming, mass-updating metadata, or restructuring directories), **do not** use individual `edit` calls for each file. This is inefficient and risks hitting tool call limits.
  - **The Scripted Transformation Pattern:** Instead, use a **Two-Pass Scripting Strategy**:
    1. **Pass 1 (Baseline):** Use a `bash` one-liner to identify files lacking a baseline structure and use `print` or `sed` to prepend/initialize them with a minimal standard (e.g., a basic YAML header).
    2. **Pass 2 (Migration):** Write and execute a temporary Python script (using `PyYAML`) to parse the existing, complex metadata and migrate it into the new, standardized schema.
  - **Robustness & Error Handling:** When writing transformation scripts:
    - Always use `try...except` blocks in Python to identify "malformed source" files that fail parsing (as encountered with `electrogravitics.md`).
    - Use a temporary file approach (`file.tmp` $\rightarrow$ `mv`) to ensure atomicity and prevent data loss if the script is interrupted.

## Coding Standards & Practices
- [e.g., Use TypeScript for all new files.]
- [e.g., Follow the project's existing linting rules.]

## Project Context
- This directory is a research tool for topics related to the matter of UAPs, UFOs, and non-human intelligence (NHI).

## Available Skills
Detailed skill implementations can be found in the `skills/` directory. The following skills are available for specialized tasks. When creating new skills, ensure they are added to this list.
- `lint`: For auditing the `research/` directory for organization and completeness.
- `research`: For conducting broad web-based research.
- `research_executor`: For executing structured research tasks.
- `summarize`: For condensing information into concise summaries.
- `synthesize`: For combining information from multiple sources into a cohesive whole.
- `librarian`: Research open-source libraries with evidence-backed answers and GitHub permalinks.
- `audit`: Review research documents to identify opportunities for improvement and populate `TODO.md`.
- `searxng_research`: Conducts deep web research using a local SearXNG instance and organizes findings.
- `next`: Automatically processes the first task in `TODO.md`.
- **Validation Scripts:** Use `validate_links.py` (root) to verify standard Markdown links (`[text](link)`) and `scripts/validate_links.py` to verify internal wikilinks (`[[link]]`).

## Autonomous Updates & Continuous Improvement
- Relevant project information, including discovered research findings, established workflows, and updated coding standards, should be documented in `AGENTS.md` or new context files (e.g., `RESEARCH_LOG.md`, `DECISIONS.md`) as they emerge, without explicit instruction.
- Analyze all interactions to identify recurring or evolving user preferences, project-specific constraints, and technical patterns.
- When new skills are discovered, they should be added to the list of available skills.
- **Continuous Context Optimization:** Upon completion of any significant task or interaction, review the session context and interaction history to identify patterns, errors, or friction points. Use these insights to proactively update `AGENTS.md` or other relevant documentation to ensure more successful and streamlined future sessions.

## Operational Lessons Learned
- **Web Search Strategy:** For research-related tasks, always use the `queries` parameter (array of 2-4 varied angles) in `web_search` rather than a single `query` string to ensure broad and comprehensive coverage. **Always prioritize searching via the local SearXNG instance (http://100.98.175.34:8089/) if available.** **To prevent "search curation cancelled (stale)" errors, always set `workflow: "none"` in the initial `web_search` call.**
- **Ambiguous Filename Handling:** When search results or list commands return files that differ only by minor punctuation (e.g., `non_leaf_...` vs `non-leaf_...`), do not assume they are duplicates or choose one at random. Verify the result with `ls -l`, confirm the specific file's contents, and use explicit paths to avoid ambiguity during edit operations.
- **Multi-Point Link Validation:** For broad terms (e.g., \"tgd\"), verify all occurrences in the project before editing. Ensure that intended wiki-link replacements are applied across all instances while avoiding unrelated strings or segments of URLs that may contain the same term.
- **Immediate Synchronization:** Strictly adhere to the `CRITICAL` instruction to execute `git push origin main` immediately after committing research findings. Never assume the user will prompt for the push.
- **Discrepancy Analysis:** In cases involving multiple witness accounts or historical reports, actively search for and document discrepancies in timeline, physical dimensions, and descriptions to provide a comprehensive view of the phenomenon.
- **Bulk Deletions/Cleanups:** For tasks involving removing multiple items or restructuring a file (e.g., clearing completed TODOs), prefer using `write` to overwrite the file with its desired final state rather than multiple `edit` calls. This reduces the risk of partial updates and `oldText` mismatches.
- **Post-Deletion Verification:** After bulk deletion or cleanup tasks, always perform a `read` of the modified file to verify that the deletions were successful and the file's structure remains intact.
- **Git Status Awareness:** Before performing large-scale file restructuring or deletions, use `git status` to ensure there are no uncommitted changes in the target files that could lead to complex merge conflicts or loss of work.
- **Atomic Edit Strategy:** For multi-line edits, if the `oldText` is large, prefer `write` to ensure atomicity, preventing the creation of a "partially updated" file if an error occurs mid-edit.\n\n## Data Migration Optimizations\n\n### Pattern: The Validation-Driven Loop\nTo avoid \"error chasing\" during structural refactoring, follow this sequence:\n1. **Define Schema:** Identify required/new fields for the documentation.\n2. **Update Validator:** Modify the `audit_*.py` scripts to recognize the new schema (preventing false positives).\n3. **Develop Migrator:** Create the `migrate_*.py` script.\n4. **Verify:** Run migration $\\rightarrow$ Run Audit. If the audit fails, identify the edge case and repeat from Step 3.\n\n### Pattern: Atomic Migration Unit\nWhen performing structural migrations (e.g., adding a `source` field), treat the **Schema Definition**, **Migration Logic**, and **Audit Logic** as a single atomic unit of work. Never finalize or commit a migration script until its corresponding Audit script has been an updated to accommodate the new structure.\n\n### Pattern: Defensive Migration Execution\nWhen writing Python scripts that bulk-edit files:\n*   **Regex Robustness:** Always use `re.DOTALL` when parsing YAML frontmatter blocks to ensure multi-line delimiters are captured correctly.\n*   **Atomic Writes (Python):** Implement the **Temp-and-Replace** pattern using a temporary file and `os.replace()` (e.g., `file.tmp` $\\rightarrow$ `file`) to prevent data loss or corrupted files in case of an interrupted execution or crash.\n\n## Decision Protocol
- Reason about a task ONCE before acting. Do not re-evaluate the same decision.
- If you find yourself reconsidering a choice you already made, STOP and execute instead.
- "I will check X" means you check X immediately in the next tool call — not plan to check it.

## Prohibited Patterns
- Do not output phrases like "wait", "actually", "let me reconsider", or "on second thought"
- Do not explain what you're about to do — just do it
- Do not restate the task before acting on it

## Reasoning Budget
Limit internal deliberation to identifying: (1) what file/tool to touch, (2) what change to make.
Do not reason about whether your previous reasoning was correct.

## Before Any File Operation
State only:
- TARGET: <file path>
- ACTION: <create | edit | delete>
- REASON: <one sentence>
Then execute immediately.
