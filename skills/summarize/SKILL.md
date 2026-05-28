---
name: summarize
description: Generates a high-level, thematic, and integrated overview of all existing research in the `research/` directory, producing a `research/summary.md` file that connects people, organizations, technologies, and cases through shared themes.
---

# Summarize Skill

This skill performs a structural and thematic analysis of the entire research repository to create a unified, integrated narrative of the current state of research.

## Procedure

### 1. Repository Scan
- **File Discovery:** Recursively find all `.md` research files within the `research/` directory.
- **Data Ingestion:** Read the full content of every discovered research file.

### 2. Thematic Extraction & Synthesis
Analyze the ingested data to identify and group information into the following major thematic pillars:
- **Thematic Pillar 1: Physical Phenomena & Advanced Propulsion:** Identify links between scientific concepts, historical discoveries, and modern technologies (e.g., Biefeld-Brown effect $\rightarrow$ Electrogravitics $\rightarrow$ Ion Propulsion).
- **Thematic Pillar 2: Aerospace, Defense, & Intelligence:** Identify links between aerospace organizations, advanced aircraft/technologies, and government oversight/investigation bodies (e.g., Skunk Works $\rightarrow$ Stealth Technology $\rightarrow$ AARO).
- **Thematic Pillarary 3: Human Element, Disclosure, & Intelligence:** Identify links between individuals (whistleblowers, experts), intelligence agencies, and the broader movement of public disclosure.
- **Thematic Pillar 4: Documented Anomalous Events:** Identify specific case studies and sightings that serve as evidence or catalysts for the themes mentioned above.

### 3. Structural Generation
Compose the `research/summary.md` file using a structured, multi-layered approach:
- **High-Level Intro:** Briefly state the purpose of the summary.
- **Thematic Sections:** For each pillar identified in step 2, write a detailed section that synthesizes the findings, explicitly pointing out the connections between the different entities, technologies, and people.
- **Integration:** Ensure the narrative flows from one theme to the next, illustrating how technology drives interest, how sightings drive investigation, and how individuals drive disclosure.

### 4. Documentation Integrity
- **Verification:** Ensure all mentioned entities (People, Organizations, Technologies) are correctly referenced and their relationships are accurately described based on the source files.
- **Link Integrity:** Ensure all internal links within the summary (if any) use correct relative paths.

### 5. Finalization
- **Writing:** Overwrite or create `research/summary.md` with the new synthesized content.
- **Confirmation:** Confirm to the user that the `research/summary.md` has been updated with the new thematic overview.
