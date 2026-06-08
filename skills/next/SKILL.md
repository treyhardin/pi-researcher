---
name: next
description: Automatically processes the first task in `TODO.md`. Upon successful completion, the task is removed from `TODO.md`. If new tasks or follow-up research items are discovered during execution, they are appended to `TODO.md`.
---

# Next Skill

This skill is designed to drive continuous progress by automating the execution of the most immediate priority.

## Procedure

1.  **Read Priority Task:** Read the contents of `TODO.md`.
2.  **Check for Tasks:**
    - If `TODO.md` is empty or contains no actionable tasks, inform the user and terminate.
3.  **Execute Task:**
    - Identify the first entry in `TODO.md`.
    - Determine the necessary tools or skills (e.g., `research`, `summarize`, `audit`, etc.) required to fulfill this task.
    - Execute the task.
4.  **Handle Completion & Success:**
    - If the task is completed successfully:
        - Remove the first entry (the completed task) from `TODO.md`.
        - Use the `write` tool to overwrite `TODO.md` with the updated list.
        - **CRITICAL:** If during the execution of the task, you identified any new related research topics, follow-up actions, or necessary deeper dives, add these as new entries to the end of `TODO.md` immediately.
5.  **Handle Failure:**
    - If the task cannot be completed or encounters an error:
        - Do **not** remove the task from `TODO.md`.
        - Document the reason for failure (if possible) or simply stop and notify the user.
6.  **Post-Execution:**
    - If any changes were made to the repository (e.g., new research files, updated summaries), ensure they are committed and, if necessary, pushed to the remote repository as per `AGENTS.md` instructions.
