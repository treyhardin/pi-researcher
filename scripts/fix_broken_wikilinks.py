import os
import re
import pathlib

# Regex to find wikilinks that might have the wrong format:
# 1. [[research/path/to/file.md]] -> [[path/to/file]]
# 2. [[path/to/file.md]] -> [[path/to/file]]
# 3. [[research/file.md|alias]] -> [[file|alias]]
# 4. [[research/file|alias]] -> [[file|alias]]
# 5. [[research/some/path]] -> [[some/path]]
# 6. [[some/path]] -> [[some/path]]
# We target both the .md extension and the 'research/' prefix.
BROKEN_FORMAT_PATTERN = re.compile(r'\[\[(?:research/)?([^|\]]+?)(?:\.md)?(?:\|([^\]]+))?\]\]')

def fix_links_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    def replacement(match):
        path = match.group(1)
        alias = match.group(2)
        if alias:
            return f"[[{path}|{alias}]]"
        else:
            return f"[[{path}]]"

    new_content = BROKEN_FORMAT_PATTERN.sub(replacement, content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed: {file_path}")
        return True
    return False

def main():
    research_dir = 'research'
    if not os.path.exists(research_dir):
        print(f"Error: {format_research_dir_error(research_dir)}")
        return

    count = 0
    for root, dirs, files in os.walk(research_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                if fix_links_in_file(file_path):
                    count += 1
    
    print(f"Finished. Fixed {count} files.")

def format_research_dir_error(research_dir):
    return f"{research_dir} directory not found."

if __name__ == "__main__":
    main()
