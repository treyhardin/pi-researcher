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
    - Repository Synchronization.

### 4. Confirmation
- **Finalize:** Upon completion of the `research` skill, confirm to the user that the research for "[Topic Name]" has been successfully documented and the repository is updated.
