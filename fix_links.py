import os
import re

def fix_links(research_dir):
    available_files = set()
    name_to_path = {}

    for root, dirs, files in os.walk(research_dir):
        for file in files:
            if file.endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, file), research_dir)
                full_rel_path = os.path.splitext(rel_path)[0]
                available_files.add(full_rel_path)
                
                base_name = os.path.basename(rel_path).replace(".md", "")
                if base_name not in name_to_path:
                    name_to_path[base_name] = []
                name_to_path[base_name].append(full_rel_path)

    wiki_link_pattern = re.compile(r'\[\[([^|\]]+)(?:\|([^\]]+))?\]\]')
    
    # We'll use a different pattern for replacement to be safe
    # This pattern matches the whole [[target|display]] or [[target]]
    replacement_pattern = re.compile(r'\[\[([^|\]]+)((?:\|[^\]]+)?)]\]')

    changes_made = 0

    for root, dirs, files in os.walk(research_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                matches = wiki_link_pattern.findall(content)
                
                # We want to iterate through matches that need fixing
                # To avoid issues with changing indices, we'll collect all replacements first
                replacements = []
                
                for target, display in matches:
                    if target not in available_files and target in name_to_path:
                        # It's a missing prefix
                        suggestion = name_to_path[target][0] # Take the first suggestion
                        # We need to replace the target part in the match
                        # The match is [[target]] or [[target|display]]
                        # Creating a regex for this specific match to avoid accidental replacements elsewhere
                        # We must escape target for regex
                        escaped_target = re.escape(target)
                        if display:
                            escaped_display = re.escape(display)
                            pattern = re.compile(f'\[\[{escaped_target}\|{escaped_display}\]\]')
                            replacement = f'[[{suggestion}|{display}]]'
                        else:
                            pattern = re.compile(f'\[\[{escaped_target}\]\]')
                            replacement = f'[[{suggestion}]]'
                        
                        replacements.append((pattern, replacement))

                if not replacements:
                    continue

                # Apply replacements
                for pattern, replacement in replacements:
                    new_content = pattern.sub(replacement, new_content)
                    changes_made += 1
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed links in: {file_path}")

    return changes_made

if __name__ == "__main__":
    research_dir = "research"
    count = fix_links(research_dir)
    print(f"\nTotal replacement operations performed: {count}")
