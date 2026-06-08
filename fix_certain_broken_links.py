import os
import re

def fix_certain_broken_links(research_dir):
    # Mapping of certain broken links to their correct paths
    mapping = {
        'intelligence/summary': 'government-and-policy/summary',
        'ticonderoga': 'technologies/ticonderoga-class-cruiser',
        'spay-1': 'technologies/an-spy-1-radar',
        'hynek_j_allen': 'people/j-allen-hynek',
        'j-allen-hynek': 'people/j-allen-hynek',
    }

    changes_made = 0

    for root, dirs, files in os.walk(research_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                for broken, fixed in mapping.items():
                    # We need to handle both [[broken]] and [[broken|display]]
                    # But wait, it's safer to just replace the content inside [[ ]] if it matches
                    # Let's use regex to find [[broken]] or [[broken|...]]
                    pattern = re.compile(rf'\[\[{re.escape(broken)}(?:\|[^\]]+)?\]\]')
                    
                    # We want to find the display text if it exists
                    matches = re.findall(rf'\[\[{re.escape(broken)}(\|[^\]]+)?\]\]', content)
                    # Actually, it's easier to just replace the target part.
                    # If it's [[broken|display]], we want [[fixed|display]]
                    
                    # Let's try a more surgical approach:
                    # Find all matches of [[...]] and if the target is in our mapping, replace it.
                    
                # New approach for this script:
                wiki_link_pattern = re.compile(r'\[\[([^|\]]+)(\|[^\]]+)?\]\]')
                
                def replace_func(match):
                    nonlocal changes_made
                    target = match.group(1)
                    suffix = match.group(2) if match.group(2) else ""
                    if target in mapping:
                        changes_made += 1
                        return f"[[{mapping[target]}{suffix}]]"
                    return match.group(0)

                new_content = wiki_link_pattern.sub(replace_func, new_content)

                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed certain broken link in: {file_path}")

    return changes_made

if __name__ == "__main__":
    research_dir = "research"
    count = fix_certain_broken_links(research_dir)
    print(f"\nTotal certain broken links fixed: {count}")
