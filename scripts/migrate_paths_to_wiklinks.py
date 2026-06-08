import os
import re
import pathlib

# Regex to find markdown links: [text](path.md)
# This is a simplified regex.
LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+\.md)\)')

def migrate_links_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    def replacement(match):
        text = match.group(1)
        link_path = match.group(2)
        
        # Get the filename without extension
        path_obj = pathlib.Path(link_path)
        new_link = f"[[{path_obj.stem}]]"
        
        # For now, we'll just replace it with the wikilink.
        # In a real scenario, we might want to keep the text if we want [[text|link]] style
        # but the goal here is a migration to the new pattern.
        # Based on current files, it seems we use [[filename]]
        return new_link

    new_content = LINK_PATTERN.sub(replacement, content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Migrated: {file_path}")
        return True
    return False

def main():
    research_dir = 'research'
    if not os.path.exists(research_dir):
        print(f"Error: {research_dir} directory not found.")
        return

    count = 0
    for root, dirs, files in os.walk(research_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                if migrate_links_in_file(file_path):
                    count += 1
    
    print(f"Finished. Migrated {count} files.")

if __name__ == "__main__":
    main()
