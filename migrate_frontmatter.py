import os
import yaml
import re
import shutil
from datetime import datetime

def migrate_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find the frontmatter block
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.search(pattern, content, re.DOTALL)

    new_frontmatter = {}
    remaining_content = content

    if match:
        # Existing frontmatter found
        fm_text = match.group(1)
        try:
            new_frontmatter = yaml.safe_load(fm_text)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML in {file_path}: {e}")
            return False
        remaining_content = content[match.end():]
    else:
        # No frontmatter found - initialize with defaults
        new_frontmatter = {
            'title': os.path.basename(file_path).replace('_', '-').replace('.md', ''),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'draft',
            'source': None,
            'categories': [],
            'tags': [],
            'summary': 'Summary pending.'
        }

    # --- Apply Transformations ---

    # 1. Fix source: "Unknown" or "" -> None (null)
    if new_frontmatter.get('source') == 'Unknown' or new_frontmatter.get('source') == '':
        new_frontmatter['source'] = None

    # 2. Fix status: any variation of "reviewed" -> "review"
    current_status = new_frontmatter.get('status')
    if isinstance(current_status, str) and 'reviewed' in current_status.lower():
        new_frontmatter['status'] = 'review'


    # 3. Ensure all required fields from RESEARCH-GUIDELINES.md exist
    required_fields = ['title', 'date', 'status', 'source', 'categories', 'tags', 'summary']
    for field in required_fields:
        if field not in new_frontmatter:
            new_frontmatter[field] = [] if field in ['categories', 'tags'] else None

    # 4. Ensure components are the correct type
    if not isinstance(new_frontmatter.get('categories'), list):
        new_frontmatter['categories'] = []
    if not isinstance(new_frontmatter.get('tags'), list):
        new_frontmatter['tags'] = []

    # Construct new content
    new_fm_yaml = yaml.dump(new_frontmatter, sort_keys=False, allow_unicode=True).strip()
    new_content = f"---\n{new_fm_yaml}\n---\n\n{remaining_content}".lstrip()

    # --- Atomic Write (Temp-and-Replace) ---
    temp_file = file_path + ".tmp"
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        os.replace(temp_file, file_path)
        return True
    except Exception as e:
        print(f"Failed to write {file_path}: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return False

def main():
    research_dir = "research"
    success_count = 0
    error_count = 0
    
    # Walk through the research directory
    for root, dirs, files in os.walk(research_dir):
        # Skip directories that shouldn't be migrated if any (e.g., .git)
        if '.git' in dirs:
            dirs.remove('.git')

        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                # Avoid migrating the migration script itself or other non-research docs if they were in research/
                if "migrate" in file:
                    continue
                    
                print(f"Migrating: {file_path}", end=' ')
                if migrate_file(file_path):
                    print("[OK]")
                    success_count += 1
                else:
                    print("[FAILED]")
                    error_count += 1

    print(f"\nMigration Complete!")
    print(f"Successfully migrated/updated: {success_count} files")
    print(f"Failed migrations: {error_count} files")

if __name__ == "__main__":
    main()
