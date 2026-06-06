---
name: lint
description: Audits the existing research repository to identify miscategorized documents, proposes structural reorganizations, identifies topics for deeper investigation, and flags gaps in the research.
---

# Lint Skill

Audits the existing research repository to identify miscategorized documents, proposes structural reorganizations, identifies topics for deeper investigation, and flags gaps in the research.

## Procedure

The `lint` skill is a meta-analytical tool used to ensure the integrity, organization, and comprehensiveness of the research repository.

### 1. Repository Audit
- **Scan Documents:** Traverse the entire `research/` directory, reading all `.md` files.
- **Examine structure:** Analyze the current directory structure (`research/{category}/`) and the contents of `research/{category}/summary.md` files.
- **Verify `pending-research.md`:** Review `research/pending-research.md` to understand the current research queue.

### 2. Identification of Issues

#### A. Miscategorized Documents
- **Analyze Content vs. Directory:** For each research file, check if the content aligns with its current category directory.
    - *Example:* A file in `research/places/` that primarily discusses a person.
- **Check for Consistency:** Ensure the naming convention (`slugified-name.md`) and content structure are consistent with the category's purpose.

#### B. Deep Research Opportunities (Flags)
- **Identify Under-developed Topics:** Look for research reports that are thin, lack depth, or contain many unanswered questions.
- **Identify Emerging Trends:** Identify recurring names, places, or technologies mentioned across multiple different research files that haven't been given their own dedicated report yet.
- **Check for Missing Links:** Identify where connections between existing reports are mentioned but not explicitly linked via relative paths.

#### C. Automatic Link Enrichment (AUTOMATIC)
- **Cross-Reference Detection:** While scanning documents, identify instances where a research document's slug (the filename without extension) or a significant part of its title is mentioned in the text of another document.
- **Automated Linking:** For every match found, use the `edit` tool to transform the plain text mention into a proper relative markdown link (e.g., `[Slug](../path/to/slug.md)`).
- **Constraint:** Ensure links are only created if they point to valid files within the `research/` directory.

#### D. Gap Identification
- **Identify Information Voids:** Based on the project's core themes (UAP, NHI, etc.), identify areas where there is a noticeable lack of research (e.g., "We have much on 'people' but very little on 'technologies'").

### 3. Action & Implementation

#### A. Automated Updates (MANDATORY)
- **Update `pending-research.md`:** For any "Deep Research Opportunity" or "Gap Identification" item that represents a new or significant topic:
    - **Check for Duplicates:** Verify the topic isn't already in `pending-research.md`.
    - **Append via Disjoint Edit:** Use the `edit` tool to add the new entry to `research/pending-research.md` as described in the `research` skill documentation.
    - **Format:** 
        - `### [Topic Name] ([Category])`
        - A brief reason why it's being added (e.g., "Identified during linting: [Reason]").

#### C. Automated Linking (AUTOMATIC)
- **Implementation:** Automatically apply relative Markdown links to any text matches that refer to existing research files found during the scan. No user confirmation is required for this step.

### 4. Reporting
- After the audit is complete, provide a summary of the findings:
    - **`pending-research.md` updates:** List what was added.
    - **Issues found:** List miscategorizations and structural issues.
    - **Proposed actions:** Clearly state what requires user confirmation.
