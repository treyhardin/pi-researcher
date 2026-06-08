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

## Coding Standards & Practices
- [e.g., Use TypeScript for all new files.]
- [e.g., Follow the project's existing linting rules.]

## Project Context
- This directory is a research tool for topics related to the matter of UAPs, UFOs, and non-human intelligence (NHI).

## Available Skills
Detailed skill implementations can be found in the `skills/` directory. The following skills are available for specialized tasks. When creating new skills, ensure they are added to this list.
- `lint`: For auditing the `research/` directory for organization and completeness.
- `research`: For conducting broad web-based research.
- `research-executor`: For executing structured research tasks.
- `summarize`: For condensing information into concise summaries.
- `synthesize`: For combining information from multiple sources into a cohesive whole.
- `librarian`: Research open-source libraries with evidence-backed answers and GitHub permalinks.
- `audit`: Review research documents to identify opportunities for improvement and populate `TODO.md`.
- `searxng_research`: Conducts deep web research using a local SearXNG instance and organizes findings.
- `next`: Automatically processes the first task in `TODO.md`.

## Autonomous Updates & Continuous Improvement
- Relevant project information, including discovered research findings, established workflows, and updated coding standards, should be documented in `AGENTS.md` or new context files (e.g., `RESEARCH_LOG.md`, `DECISIONS.md`) as they emerge, without explicit instruction.
- Analyze all interactions to identify recurring or evolving user preferences, project-specific constraints, and technical patterns.
- When new skills are discovered, they should be added to the list of available skills.
- **Continuous Context Optimization:** Upon completion of any significant task or interaction, review the session context and interaction history to identify patterns, errors, or friction points. Use these insights to proactively update `AGENTS.md` or other relevant documentation to ensure more successful and streamlined future sessions.

## Operational Lessons Learned
- **Web Search Strategy:** For research-related tasks, always use the `queries` parameter (array of 2-4 varied angles) in `web_search` rather than a single `query` string to ensure broad and comprehensive coverage. **Always prioritize searching via the local SearXNG instance (http://100.98.175.34:8089/) if available.** **To prevent "search curation cancelled (stale)" errors, always set `workflow: "none"` in the initial `web_search` call.**
- **Robust File Editing:** If an `edit` call fails due to an `oldText` mismatch (often caused by invisible whitespace or newlines), immediately pivot to using the `write` tool to overwrite the entire file with the correct content rather than attempting repeated, localized `edit` fixes.
- **Data Integrity:** After performing a `write` operation, especially when replacing large blocks of text, always verify the integrity of the file (e.g., using `read`) to ensure no truncation or accidental corruption occurred.
- **Immediate Synchronization:** Strictly adhere to the `CRITICAL` instruction to execute `git push origin main` immediately after committing research findings. Never assume the user will prompt for the push.
- **Discrepancy Analysis:** In cases involving multiple witness accounts or historical reports, actively search for and document discrepancies in timeline, physical dimensions, and descriptions to provide a comprehensive view of the phenomenon.
- **Bulk Deletions/Cleanups:** For tasks involving removing multiple items or restructuring a file (e.g., clearing completed TODOs), prefer using `write` to overwrite the file with its desired final state rather than multiple `edit` calls. This reduces the risk of partial updates and `oldText` mismatches.
- **Post-Deletion Verification:** After bulk deletion or cleanup tasks, always perform a `read` of the modified file to verify that the deletions were successful and the file's structure remains intact.
- **Git Status Awareness:** Before performing large-scale file restructuring or deletions, use `git status` to ensure there are no uncommitted changes in the target files that could lead to complex merge conflicts or loss of work.
- **Atomic Edit Strategy:** For multi-line edits, if the `oldText` is large, prefer `write` to ensure atomicity, preventing the creation of a "partially updated" file if an error occurs mid-edit.

## Decision Protocol
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
