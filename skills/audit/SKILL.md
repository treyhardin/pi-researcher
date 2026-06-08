---
name: audit
description: Review research documents to identify opportunities for improvement in structure, cross-linking, error-fixes, new topics, deeper-dives, or potential redundancies/consolidations. The primary purpose of an audit is to populate `TODO.md` with identified tasks. For each finding, prompt the user with a yes-or-no question on whether to add it to `TODO.md`. After an item is added, proceed immediately to the next finding.
---

# Audit

Review the current research documents to identify potential areas for improvement in:
- Structure and cross-linking (MOC/Wikilink patterns).
- Error-fixes (broken links, typos, etc.).
- New research topics and deeper-dives.
- Identification of duplicates or areas for potential consolidation or restructuring of existing documents or content.

**Findings from an audit should not be executed immediately; they are presented as candidates for the `TODO.md` list.** For each finding, prompt the user with a yes-or-no question on whether to add it to `TODO.md`. 
**CRITICAL:** After a user confirms an item and it is added to `TODO.md`, do not stop the session; proceed immediately to the next finding.

`TODO.md` should remain a simple list of action-items, with enough context for future sessions to be able to action on them. Action items that are complete should be removed from this list automatically as you go.
