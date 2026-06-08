import os
import re

def audit_links(research_dir):
    available_files = set()
    # Map filename (without extension) to its relative path
    # e.g., 'igigi' -> 'mythology/igigi'
    name_to_path = {}

    for root, dirs, files in os.walk(research_dir):
        for file in files:
            if file.endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, file), research_dir)
                name_no_ext = os.path.splitext(rel_path)[0]
                full_rel_path = os.path.splitext(rel_path)[0]
                
                available_files.add(full_rel_path)
                
                # Also map the base name to the full relative path
                base_name = os.path.basename(rel_path).replace(".md", "")
                if base_name not in name_to_path:
                    name_to_path[base_name] = []
                name_to_path[base_name].append(full_rel_path)

    wiki_link_pattern = re.compile(r'\[\[([^|\]]+)(?:\|([^\]]+))?\]\]')

    ok_links = []
    missing_prefix_links = []
    broken_links = []

    for root, dirs, files in os.walk(research_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    matches = wiki_link_pattern.findall(content)
                    for target, display in matches:
                        display_text = display if display else target
                        
                        if target in available_files:
                            ok_links.append((file_path, target, display_text))
                        elif target in name_to_path:
                            # It's a missing prefix. We found the file(s) by just their name.
                            # If multiple files have this name, it's ambiguous, but we'll report it.
                            suggestions = name_to_path[target]
                            missing_prefix_links.append((file_path, target, display_text, suggestions))
                        else:
                            # Check if the target could be a partial path/prefix? 
                            # For now, let's just call it broken.
                            broken_links.append((file_path, target, display_text))

    return ok_links, missing_prefix_links, broken_links

if __name__ == "__main__":
    research_dir = "research"
    ok, missing, broken = audit_links(research_dir)
    
    print(f"--- OK Links: {len(ok)} ---")
    # print(f"--- Broken Links (No match found) ---") # Too many
    # for link in broken:
    #     print(f"File: {link[0]} | Link: [[{link[1]}]] (Display: {link[2]})")

    print(f"\n--- Missing Prefix Links (Needs path correction) ---")
    if not missing:
        print("None")
    for link in missing:
        print(f"File: {link[0]} | Link: [[{link[1]}]] (Display: {link[2]}) -> Suggestions: {link[3]}")

    print(f"\n--- Broken Links (Truly broken) ---")
    if not broken:
        print("None")
    for link in broken:
        print(f"File: {link[0]} | Link: [[{link[1]}]] (Display: {link[2]})")
