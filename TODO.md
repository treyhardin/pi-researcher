# TODO: Structural Reorganization of Research Syllabus

This document tracks the transformation of the research folder from a hierarchical siloed structure into a networked knowledge graph (MOC/Wikilink pattern).

## ✅ Completed Tasks
- [x] Standardize frontmatter across all research files
  - [x] Define a standard schema (e.g., date, source, status, categories)
  - [x] Audit current frontmatter in the `research/` directory
  - [x] Apply bulk updates to align existing documents with new schema
- [x] Create or update MOCs (Maps of Content) for major research categories
  - [x] Identify and define primary knowledge hubs
  - [x] Develop draft content for each MOC
  - [x] Map inter-linkages between related MOCs
- [x] Consolidate redundant technology and propulsion documents
  - [x] Audit `technology/` and `propulsion/` to identify overlapping files
  - [x] Extract unique data from duplicates into consolidated "hub" docs
  - [x] Update all incoming references to point to the new primary sources

## ⚪ Pending Tasks
- [x] Ensure all research sub-directories have an entry point (index.md or MOC.md)
  - [x] Map out current directory tree in `research/`
  - [x] Create missing index pages for each leaf-node subdirectory
- [ ] Fix specific link in Theory MOC ([theory-of-psychic_quanta] in theories/summary.md)
  - [ ] Verify the correct path for "theory-of_psychic_quanta"
  - [ ] Update the reference in `theories/summary.md`
- [ ] Expand Case Study MOC to include missing items (kumburgaz, ww2-foo_fighters, the-orange-orb)
  - [ ] Locate source material for: kumburgaz, ww2-foo_fighters, and the-orange-orb
  - [ ] Link these entries into the `case_studies` MOC
- [ ] Standardize internal link formatting across research docs (remove underscores)
  - [ ] Identify all occurrences of underscores in wiki-links
  - [ ] Batch replace underscored links with standard kebab-case or clean format
  - [ ] Verify referential integrity across full directory post-update
