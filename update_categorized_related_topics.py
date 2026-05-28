import os
import re

def main():
    research_dir = os.path.abspath("research")
    if not os.path.exists(research_dir):
        print(f"Directory {research_dir} not found.")
        return

    # 1. Gather all relevant research files
    research_files = []
    for root, dirs, filenames in os.walk(research_dir):
        for filename in filenames:
            if filename.endswith(".md") and filename not in [
                "summary.md", "pending-research.md", "RESEARCH_GUIDELINES.md", "AGENTS.md"
            ]:
                research_files.append(os.path.abspath(os.path.join(root, filename)))

    # 2. Create a mapping of absolute path -> {title, category}
    mapping = {}
    for f_path in research_files:
        try:
            with open(f_path, "r", encoding="utf-8") as file:
                lines = file.splitlines() if hasattr(file, 'splitlines') else file.readlines()
                # Re-read properly
                file.seek(0)
                lines = file.readlines()
                if not lines:
                    continue
                
                # Extract Title (first line)
                title = re.sub(r"^#\s*", "", lines[0].strip())
                
                # Extract Category (from directory structure)
                rel_to_research = os.path.relpath(f_path, research_dir)
                parts = rel_to_research.split(os.sep)
                category = parts[0].capitalize() if len(parts) > 1 else "Other"

                mapping[f_path] = {
                    "title": title,
                    "category": category
                }
        except Exception as e:
            print(f"Error processing {f_path} for mapping: {so_string_placeholder}")
            # I'll fix this in the final version
            pass

    # Let's use a more robust approach for the mapping part
    mapping = {}
    for f_path in research_files:
        try:
            with open(f_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                if not lines:
                    continue
                title = re.sub(r"^#\s*", "", lines[0].strip())
                rel_to_research = os.path.relpath(f_path, research_dir)
                parts = rel_to_research.split(os.sep)
                category = parts[0].capitalize() if len(parts) > 1 else "Other"
                mapping[f_path] = {"title": title, "category": category}
        except Exception as e:
            print(f"Error mapping {f_path}: {e}")

    # 3. Process each file
    files_updated = 0
    for f_path in research_files:
        try:
            with open(f_path, "r", encoding="utf-8") as file:
                content = file.read()
            
            current_dir = os.path.dirname(f_path)
            found_related = []
            
            # Regex for markdown links: [text](path)
            link_pattern = re.compile(
                r'\[(?P<text>[^\]]+)\]\((?P<path>[^)]+)\)'
            )
            
            for match in link_pattern.finditer(content):
                link_text = match.group('text')
                link_path_raw = match.group('path')
                
                # Resolve the link path relative to the current file
                resolved_link_path = os.path.abspath(os.path.join(current_dir, link_path_raw))
                
                if resolved_link_path in mapping and resolved_link_path != f_path:
                    target_info = mapping[resolved_link_path]
                    rel_to_current = os.path.relpath(resolved_link_path, current_dir)
                    
                    found_related.append({
                        "title": target_info["title"],
                        "category": target_info["category"],
                        "rel_path": rel_to_current
                    })

            # Grouping
            categorized = {}
            for item in found_related:
                cat = item["category"]
                if cat not in categorized:
                    categorized[cat] = []
                
                if not any(existing["title"] == item["title"] for existing in categorized[cat]):
                    categorized[cat].append(item)

            # Remove existing Related Topics section (regex handles multi-line)
            # We look for "## Related Topics" up to the next "##" or end of string
            new_content = re.sub(r"## Related Topics.*?(?=\n##|$)", "", content, flags=re.DOTALL)

            # Build new section
            if categorized:
                new_section_lines = ["## Related Topics"]
                for cat in sorted(categorized.keys()):
                    new_section_lines.append(f"### {cat}")
                    sorted_topics = sorted(categorized[cat], key=lambda x: x["title"])
                    for topic in sorted_topics:
                        new_section_lines.append(f"- [{topic['title']}]({topic['rel_path']})")
                
                new_related_block = "\n" + "\n".join(new_section_lines) + "\n"

                # Insert block before "## Sources" if it exists
                if "## Sources" in new_content:
                    parts = re.split(r"(## Sources)", new_content)
                    if len(parts) >= 3:
                        updated_content = parts[0] + new_related_block + parts[1] + parts[2]
                    else:
                        updated_content = new_content + new_related_block
                else:
                    updated_content = new_content + new_related_block
                
                # Check if we actually changed anything
                if updated_content.strip() != content.strip():
                    with open(f_path, "w", encoding="utf-8") as file:
                        file.write(updated_content)
                    files_updated += 1
                    print(f"Updated: {os.path.relpath(f_path, os.path.dirname(f_path))}")
            else:
                # If no related topics, we just use the content without the section.
                # But if the content changed (because we removed the old section), we must write it.
                if new_content.strip() != content.strip():
                    with open(f_path, "w", encoding="utf-8") as file:
                        file.write(new_content)
                    files_updated += 1
                    print(f"Removed old section from: {os.path.relpath(f_path, os.path.dirname(f_path))}")

        except Exception as e:
            print(f"Error processing {f_path}: {e}")

    print(f"\nProcess complete. Total files updated: {files_updated}")

if __name__ == "__main__":
    main()
