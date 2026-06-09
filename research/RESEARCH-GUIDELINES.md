---
categories: []
date: '2026-06-08'
source: null
status: draft
summary: Summary pending.
tags: []
title: RESEARCH GUIDELINES
---

# Research Operations Guidelines

These guidelines are designed to ensure the integrity, accessibility, and reliability of all research findings and documentation within the Phenomenon Project.

## Objective
To maintain a high standard of evidence-backed research where all cited sources are verifiable and all internal documentation links are functional.

## Research Workflow

### 1. Information Gathering
- Use `web_search` and `librarian` to gather diverse perspectives and primary sources.
- For every critical claim or piece of data, identify at least one verifiable source.

### 2. Source Verification (Link Integrity)
- **URL Validation**: Before finalizing any research report (e.Markdown files), perform a "pre-flight" check on all URLs.
- **Handling Inaccessible Links**: If a source returns an error (e.g., HTTP 403, 404, or timeout):
    - **Attempt Recovery**: Use `web_search` to find an alternative URL or a cached version of the content.
    - **Search for Mirrors**: Check for academic repositories (like DTIC, arXiv, or ResearchGate) that might host the same paper.
    - **Document Failure**: If no alternative is found, do **not** leave a broken link. Instead, update the link text to include a note, e.g., `[Source Title (Link Inaccessible/403)](URL)`.
- **Path Integrity**: When creating links between files within the `/research` directory:
    - Always use relative paths that are correct from the perspective of the current file.
    - Avoid "path doubling" (e.g., `research/people/person.md` inside `research/people/summary.md`). Use `./person.md` or just `person.md`.

### 3. Documentation Standards
- All new research files must follow the established structure: `Summary`, `Detailed Findings`, `Key Entities/Facts`, and `Sources`.
- The `Sources` section must be clearly demarcated and use standard Markdown link syntax.

#### Frontmatter Schema
All research files MUST follow a standardized YAML frontmatter structure to ensure consistency and compatibility with automated parsing/indexing tools.

```yaml
---
title: <string>               # Descriptive title of the document (kebab-case or clean text)
date: <YYYY-MM-DD>           # Date of research completion or last major update
status: <draft|review|published> # Current stage of the research piece
source: <string|null>        # Primary source URL or name, use null if unknown/not applicable
categories: [<list>]         # High-level taxonomical categories (e.g., 'people', 'technology')
tags: [<list>]               # Granular, kebab-case tags for fine-grained search
summary: <string>            # A brief one or two sentence overview of the document's 
---
```

**Schema Implementation Notes:**
- **Atomicity**: Every file must have exactly ONE YAML frontmatter block at the very top of the file.
- **No Duplication**: Do not append new blocks; update existing ones.
- **Null values**: Use `null` for empty string/unknown fields where appropriate (especially `source`).

### 4. Continuous Audit
- Periodically run the `validate_links.py` script to identify and remediate any newly introduced broken links.
- Update these guidelines if new patterns of broken links or researcher-specific complexities emerge.

### 5. Cross-Referencing and Entity Linking
- **Identify Related Topics**: When conducting research, actively look for connections between different categories (people, places, technologies, organizations, etc.).
- **Categorical Linking**: If a subject (e.g., a location) is related to an entity in another directory (e.g., a person in `/research/people/`), add a clear reference to that entity in the `Key Entities/Facts` or a dedicated `Related Entities` section.
- **Maintain Directory Integrity**: Ensure all cross-references use the established relative pathing standards.
