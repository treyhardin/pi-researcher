# Agent Instructions for Phenomenon Project

This file contains instructions on how the AI agent should behave, communicate, and operate within this specific project directory.

## Persona & Communication Style
- Be concise and direct.
- Always explain the reasoning behind complex bash commands.
- If a user's instruction is highly ambiguous or unclear, ask clarifying follow-up questions instead of making a best-guess interpretation.

## Workflow & Task Execution
- Always run tests before committing changes.
- Prefer using `npm test` for verification.
- **CRITICAL:** After performing any research-related task and committing changes (including updates to `pending-research.md` and `summary.md`), you **MUST** execute `git push origin main` to ensure the remote repository is synchronized with the local changes.

## Coding Standards & Practices
- [e.g., Use TypeScript for all new files.]
- [e.g., Follow the project's existing linting rules.]

## Project Context
- This directory is a research tool for topics related to the matter of UAPs, UFOs, and non-human intelligence (NHI).

## Autonomous Updates & Continuous Improvement
- Relevant project information, including discovered research findings, established workflows, and updated coding standards, should be documented in `AGENTS.md` or new context files (e.g., `RESEARCH_LOG.md`, `DECISIONS.md`) as they emerge, without explicit instruction.
- Analyze all interactions to identify recurring or evolving user preferences, project-specific constraints, and technical patterns.
- Proactively suggest updates to `AGENTS.md` or the creation of additional context files when you identify opportunities to better persist memory, capture learned behaviors, or improve the quality and relevance of future outputs.
- Treat every interaction as an opportunity to refine your persona, workflow, and the overall project context to ensure long-term continuity and improved performance.
- Adhere to the protocols defined in `research/RESEARCH_GUIDELINES.md` during all research-related tasks.

## Operational Lessons Learned
- **Web Search Strategy:** For research-related tasks, always use the `queries` parameter (array of 2-4 varied angles) in `web_search` rather than a single `query` string to ensure broad and comprehensive coverage.
- **Robust File Editing:** If an `edit` call fails due to an `oldText` mismatch (often caused by invisible whitespace or newlines), immediately pivot to using the `write` tool to overwrite the entire file with the correct content rather than attempting repeated, localized `edit` fixes.
- **Data Integrity:** After performing a `write` operation, especially when replacing large blocks of text, always verify the integrity of the file (e._g., using `read`) to ensure no truncation or accidental corruption occurred.
- **Immediate Synchronization:** Strictly adhere to the `CRITICAL` instruction to execute `git push origin main` immediately after committing research findings. Never assume the user will prompt for the push.
