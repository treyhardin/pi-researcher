# Decisions Log

## [2026-06-08] Standardized Frontmatter Schema

To enable better indexing, querying, and MOC (Map of Content) generation, all files within the `research/` directory must follow a standardized YAML frontmatter schema.

### Schema Definition

```yaml
---
title: "Title of the document"
date: YYYY-MM-DD # Date of creation or last significant update
source: "URL or Reference to original source"
status: "draft | review | complete" # Current state of the research
categories: [] # Array of categories/tags (e.g., ["propulsion", "uap", "case-study"])
tags: [] # Supplementary tags for fine-grained searching
summary: "A brief one or two sentence summary of the document's content"
---
```

### Implementation Requirements
- All new files must include this block.
- Existing files in `research/` will be updated during the "Audit current frontmatter" task.
- The `status` field must reflect the progress of the specific research item.
- `categories` should align with the primary MOC structure.
