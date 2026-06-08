import os
import re

def find_broken_links(root_dir):
    broken_links = []
    # Regex to find [[link]] or [[link|text]]
    # Group 1: target, Group 2: text (optional)
    link_pattern = re.compile(r'\[\[([^|\]]+)(?:\|([^\]]+))?\]\]')

    # Pre-index all .md files in the research directory for quick lookup
    # We'll store the basename (without .md) mapping to the full path
    # To handle paths like [[cases/summary]], we'll store both the relative path and the basename.
    all_md_files = {}

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                full_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(full_path, root_dir)
                # Remove .md for the key
                key_rel = os.path.splitext(rel_path)[0]
                key_base = os.path.splitext(filename)[0]
                
                # Store both relative and basename for lookup
                all_md_files[key_rel] = full_path
                all_md_files[key_base] = full_path

    # Traverse and find links
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.
                        # Reading line by line or whole file? Whole file is easier for multiline links.
                        content = f.read()
                        for match in link_pattern.finditer(content):
                            target = match.group(1).strip()
                            text = match.group(2).strip() if match.group(2) else target
                            
                            # Check if the target exists as a relative path from root_dir
                            # e.g., targets='cases/summary' -> research/cases/summary.md
                            target_as_rel_path = target
                            target_as_full_path = os.path.join(root_dir, target + '.md')
                            
                            found = False
                            if os.path.exists(target_as_full_path):
                                found = True
                            elif target in all_md_files:
                                found = True
                            
                            if not found:
                                broken_links.append({
                                    'source': filepath,
                                    'target': target,
                                    'text': text,
                                    'type': 'not_found'
                                })
                            else:
                                # If found, check if the target name matches the text (as per TODO requirement)
                                # "where the target file name does not match the link text"
                                # This is a bit ambiguous, but let's assume it means the target name
                                # is significantly different from the text, or we want to standardize.
                                # Let's check the provided example: [[anunnaki]] vs [[anunnaki-igigi]]
                                # This means the target itself is 'anunnaki' but the file is 'anunnaki-igigi'.
                                # My 'found' logic above handles if 'anunnaki.md' doesn't exist.
                                # But what if 'anunnaki' is a partial match?
                                
                                # Let's check for partial/prefix matches to identify the "anunnaki" case.
                                actual_path = all_md_files.get(target)
                                if not actual_path:
                                    # Check if target is a prefix of any existing file
                                    for k, v in all_md_files.items():
                                        if k.startswith(target) and k != target:
                                            broken_links.append({
                                                'source': filepath,
                                                'target': target,
                                                'text': text,
                                                'type': 'prefix_mismatch',
                                                'actual_file': k
                                            })
                                            break
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

    return broken_links

if __name__ == "__main__":
    root = "research"
    if not os.path.exists(root):
        print(f"Error: {root} not found.")
    else:
        results = find_broken_links(root)
        if not results:
            print("No broken links found.")
        else:
            print(f"Found {len(results)} issues:")
            for issue in results:
                print(f"Source: {issue['source']}")
                print(f"Link: [[{issue['target']}{'|' + issue['text'] if issue['text'] != issue['target'] else ''}]]")
                if issue['type'] == 'prefix_mismatch':
                    print(f"  Issue: Target is a prefix of another file: {issue['actual_file']}")
                else:
                    print("  Issue: Target file not found.")
                print("-" * 20)

