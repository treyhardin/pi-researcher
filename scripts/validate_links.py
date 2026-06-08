import os
import re
import pathlib

# Regex to find wikilinks: [[link]] or [[link|alias]]
WIKILINK_PATTERN = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')

def get_all_md_targets(research_dir):
    """Returns a set of all .md targets (stems and relative paths) in the research directory."""
    targets = set()
    research_path = pathlib.Path(research_dir).resolve()
    
    for root, dirs, files in os.walk(research_dir):
        for file in files:
            if file.endswith('.md'):
                full_path = (pathlib.Path(root) / file).resolve()
                # Add the stem (for [[summary]])
                targets.add(full_path.stem)
                # Add the relative path without extension (for [[cases/summary]])
                try:
                    rel_path = full_path.relative_to(research_path).with_suffix('')
                    targets.add(str(rel_path))
                except ValueError:
                    pass
                
    return targets

def validate_links(research_dir):
    """Scans all .md files in research_dir for broken [[links]]."""
    targets = get_all_md_targets(research_dir)
    broken_links = []

    for root, dirs, files in os.walk(research_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    links = WIKILINK_PATTERN.findall(content)
                    for link in links:
                        # link is the part before the |
                        if link not in targets:
                            broken_links.append((file_path, link))
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return broken_links

def main():
    research_dir = 'research'
    if not os.path.exists(research_dir):
        print(f"Error: {research_dir} directory not found.")
        return

    print(f"Validating links in {research_dir}...")
    broken_links = validate_links(research_dir)
    
    if not broken_links:
        print("No broken links found!")
        return 0
    else:
        print(f"Found {len(broken_links)} broken links:")
        for file_path, link in broken_links:
            print(f"  {file_path} -> [[{link}]]")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
