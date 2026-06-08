import os
import re

def audit_links(research_dir):
    # 1. Get all available file names (without .md)
    available_files = set()
    for root, dirs, files in os.walk(research_dir):
        for file in files:
            if file.endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, file), research_dir)
                name = os.path.splitext(rel_path)[0]
                available_files.add(name)

    # 2. Regex for wikilinks: [[link]] or [[link|display]]
    # Group 1 is the link target, Group 2 is the display text (optional)
    wiki_link_pattern = re.compile(r'\[\[([^|\]]+)(?:\|([^\]]+))?\]\]')

    broken_links = []
    mismatched_links = [] # links that point to something that looks like it might be a partial match

    # 3. Iterate through all .md files
    for root, dirs, files in os.walk(research_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    matches = wiki_link_pattern.findall(content)
                    for target, display in matches:
                        # target is the part before the pipe
                        if target not in available_files:
                            # Check for partial matches (e.g., target is prefix of an available file)
                            potential_matches = [f for f in available_files if f.startswith(target) or target.startswith(f)]
                            
                            if potential_matches:
                                mismatched_links.append({
                                    'file': file_path,
                                    'target': target,
                                    'display': display if display else target,
                                    'suggestions': potential_matches
                                })
                            else:
                                broken_links.append({
                                    'file': file_path,
                                    'target': target,
                                    'display': display if display else target
                                })

    return broken_links, mismatched_links

if __name__ == "__main__":
    research_dir = "research"
    broken, mismatched = audit_links(research_dir)
    
    print(f"--- Broken Links (No match found) ---")
    if not broken:
        print("None")
    for link in broken:
        print(f"File: {link['file']} | Link: [[{link['target']}]] (Display: {link['display']})")

    print(f"\n--- Mismatched Links (Potential partial matches) ---")
    if not mismatched:
        print("None")
    for link in mismatched:
        print(f"File: {link['file']} | Link: [[{link['target']}]] (Display: {link['display']}) -> Suggestions: {link['suggestions']}")
