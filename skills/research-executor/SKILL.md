---
name: research-executor
description: Identifies pending research topics from `research/pending-research.md`, presents them for selection, and initiates the `research` skill for the chosen topic.
---

# Research Executor Skill

This skill automates the transition from "pending research" to "active research" by facilitating selection and execution.

## Procedure

### 1. Parse Pending Topics
- **Read File:** Access `research/pending-progress.md` (or `research/pending-research.md` - check existence).
- **Extract Entries:** Parse the markdown file to find all entries following the pattern: `### [Topic Name] ([Category])`.
- **Format List:** Present a numbered list of these topics to the user, clearly showing both the **Topic Name** and its **Category**.

### 2. User Selection
- **Wait for Input:** Prompt the user to enter the number corresponding to their choice.
- **Handle Invalid Input:** If the user enters an invalid number or an unrecognized command, re-display the list and ask again.

### 3. Execute Research Workflow
- **Data Extraction:** Once a valid number is chosen, extract the specific **Topic Name** and **Category** associated with that entry.
- **Initiate Research Skill:** Perform all steps defined in the `research` skill (`skills/research/SKILL.md`) using the extracted topic and category. This includes:
    - Topic Analysis & Categorization.
    - Deep Web Research.
    - Discovery & Pending Research Identification.
    - Report Generation.
    - Summary Update.
    - Repository Synchronization (Commit only).
- **Cleanup Pending Research:** Once the research is complete, remove the entry for "[Topic Name]" from `research/pending-research.md`.
- **Push to GitHub:** Use `git push origin main` to push all changes (including the removal of the entry) to the remote repository.

### 4. Confirmation & Continuation
- **Finalize:** Upon completion of the research workflow, confirm to the user that the research for "[Topic Name]" has been successfully documented, the pending entry has been removed, and the repository has been updated.
- **Looping:** If there are still pending topics in `research/pending-research.md`, return to **Step 1** to allow the user to select another topic. If no topics remain, conclude the execution.
