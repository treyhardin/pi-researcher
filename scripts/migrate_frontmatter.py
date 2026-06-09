import os
import glob
import yaml
import re
import sys

def migrate_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    # Regex to find frontmatter block
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    
    data = {}
    remaining_content = content
    
    if match:
        yaml_block = match.group(1)
        remaining_content = content[match.end():]
        try:
            data = yaml.safe_load(yaml_block)
            if data is None:
                data = {}
        except Exception as e:
            print(f"Error parsing YAML in {filepath}: {e}")
            data = {}
    else:
        # Treat as no frontmatter (Pass 1 scenario)
        pass

    # Prepare defaults
    base_title = os.path.basename(filepath).replace('_', ' ').replace('-', ' ').split('.')[0]
    defaults = {
        'title': base_title,
        'date': '2026-06-08',
        'status': 'draft',
        'source': 'Unknown',
        'categories': [],
        'tags': [],
        'summary': 'Summary pending.'
    }

    # Apply defaults for missing or empty keys
    for key, default_val in defaults.items():
        if key not in data or data[key] == '' or data[key] is None:
            data[key] = default_val

    # Reconstruct the content
    new_yaml_block = yaml.dump(data, sort_keys=False).strip()
    new_frontmatter = f"---\n{new_yaml_block}\n---\n\n"
    new_content = new_trans_content = new_frontmatter + remaining_content

    # Atomic Write (Temp-and-Replace)
    temp_path = filepath + ".tmp"
    try:
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        os.replace(temp_path, filepath)
        print(f"Successfully migrated {filepath}")
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        print(f"Error writing {filepath}: {e}")

def main(directory):
    md_files = glob.glob(os.path.join(directory, '**/*.md'), recursive=True)
    # Focus on research files
    md_files = [f for f in md_files if 'research/' in f]
    
    if not md_files:
        print(f"No markdown files found in {directory}")
        return

    print(f"Starting migration of {len(md_files)} files...")
    for filepath in md_files:
        migrate_file(filepath)
    print("Migration complete.")

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    main(target_dir)
