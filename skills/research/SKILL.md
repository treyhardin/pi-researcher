---
name: research
description: Conducts deep web research on a provided topic and organizes the findings into a structured repository within the `research/` directory, while also identifying and tracking potential new research topics.
---

# Research Skill

Conducts deep web research on a provided topic and organizes the findings into a structured repository within the `research/` directory, while also identifying and tracking potential new research topics.

## Procedure

### 1. Topic Analysis & Categorization
- **Identify Topic:** Receive the research topic from the user.
- **Determine Category:** Analyze the topic to determine an appropriate category (e.g., `people`, `organizations`, `places`, `cases`, `technologies`, `events`, etc.).
- **Directory Check:**
    - Check if `research/{category}/` exists.
    - **If it exists:** Proceed to step 2.
    - **If it does NOT exist:**
        - Stop the process.
        - Prompt the `user`: "I've identified a new category: '{category}'. Should I create a new subdirectory for it, or would you prefer to categorize this under an existing directory?"
        - Wait for user input.
        - If the user provides a new name, create the directory.
        - If the user provides an existing name, use that.

### 2. Deep Web Research
- **Search Execution:** Use `web_search` with 3-4 varied and comprehensive queries to cover different angles of the topic.
- **Detailed Extraction:** For the most promising results, use `intends_use_fetch_content` to extract the full text/content.
- **Information Synthesis:** Synthesize the gathered information to ensure accuracy and depth.

### 3. Discovery & Pending Research Identification
- **Identify Sub-topics:** During research, scan the gathered information for significant, recurring entities or topics (e.g., names, places, technologies, events) that are not the primary subject of the current research.
- **For each candidate topic:**
    - **Check Existence:** Verify if the topic already has a dedicated research file in its appropriate directory (e.g., `research/people/john-doe.md`).
    - **Determine Category:** Assign the candidate to a category (e.g., `people`, `places`, `technologies`).
    - **Handle New Category for Sub-topic:** 
        - If the directory `research/{category}/` does not exist:
            - Stop and prompt the user: "I've discovered a potential new topic: '{topic-name}'. It seems to belong to a new category: '{category}'. Should I create this subdirectory, or would you prefer a different category name?"
            - Wait for user input.
            - Once a category name is confirmed, create the directory.
    - **Update Pending Research (MANDATORY):** If the topic does not yet have a research file, you MUST add an entry to `research/pending-research.md`.
        - Ensure `research/pending-research.md` exists (create with header if not).
        - **Append using the Anchor Method:** To avoid overwriting, do NOT overwrite the whole file. Instead, find the last line of the file (the "anchor") and use the `edit` tool to replace that line with itself plus the new entry.
        - Add an entry with:
            - `### [Topic Name] ([Category])`
            - A brief summary of why it's worth further research (e.g., "Appears frequently in research regarding [Primary Topic]").
        - Ensure the new entry is on a new line.

### 4. Report Generation
- **File Naming:** Generate a slugified version of the topic name (e.g., "John Doe" -> `john-doe.md`).
- **Storage:** Save the report to `research/{category}/{topic-slug}.md`.
- **Report Content Structure:**
    - `# [Topic Name]`
    - `## Summary`
    - `## Detailed Findings`
    - `## Key Entities/Facts`
    - `## Sources`

### 5. Summary Update
- **Locate Summary File:** Check for `research/{category}/summary.md`.
- **Create if Missing:** If it doesn't exist, create it with an introductory header.
- **Update Content:**
    - Add a new entry for the research just completed.
    - The update should include a concise summary of the new report.
    - Ensure `summary.md` maintains a clear, navigable structure.
    - Reorganize the `summary.md` structure if necessary for clarity.
