---
name: synthesize
description: Analyzes all research documents in the repository to identify hidden connections, recurring themes, and cross-disciplinary links between disparate topics.
---

# Synthesize Skill

This skill performs a high-level cognitive analysis of the entire research repository to discover non-obvious relationships between established research files.

## Procedure

### 1. Repository Scan
- **File Discovery:** Recursively find all `.md` files within the `research/` directory.
- **Data Ingestion:** Read the full content of every discovered research file.

###   2. Connection Analysis (The "Synthesis" Phase)
Analyze the ingested data to identify the following types of connections:
- **Cross-Document Entities:** People, organizations, or places that appear in multiple unrelated research files (e.g., a person from `people/` mentioned in a `cases/` report).
- **Thematic Overlap:** Technical or scientific concepts (like "electrogravitics") that appear across different categories (e.g., in `technologies/` and `cases/`).
- **Causal/Logical Links:** Situations where an event in one file (e.s. a discovery) logically leads to or necessitates research into a topic in another file (e.g., a sighting leading to a need for studying a specific technology).
- **Patterned Terminology:** Recurring terminology or nomenclature that suggests a deeper, unmapped relationship between different research areas.

### 3. Presentation of Findings
Present each identified connection or new potential topic to the user clearly, using the following format:
**[Connection Name]**
- **Rationale:** [A brief explanation of why this is a connection/new area of interest, citing the related files/themes].
- **Proposed Entry:** `### [Suggested Topic Name] ([Category])`

### 4. User Decision & Action
For each finding presented, prompt the user for an action:
- **Input:** Prompt the user: "Add this to `research/pending-sresearch.md`? (y/n/skip)"
- **If 'y':** 
    - Append the findings to `research/pending-research.md` following the project's established format.
    - Ensure the entry includes the rationale/connection.
- **If 'n' or 'skip':** Move to the next finding without making any changes.

### 5. Finalization
- **Summary:** Once all findings have been processed, provide a final summary of how many new topics were successfully added to the pending research list.
- **Commit:** Commit all changes to `research/pending-research.md` and push to `origin main`.
