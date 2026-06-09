import yaml
import sys
import os

def migrate_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.startswith('---'):
            return False

        # Split frontmatter and body
        parts = content.split('---', 2)
        if len(parts) < 3:
            return False
        
        frontmatter_raw = parts[1]
        body = parts[2].lstrip()

        try:
            data = yaml.safe_load(frontmatter_raw)
        except yaml.YAMLError:
            return False

        if not data:
            data = {}

        new_data = {}
        
        # 1. Title (Already added by my previous bash script, but let's ensure it's here)
        new_data['title'] = data.get('title', os.path.basename(filepath).replace('.md', '').replace('_', ' ').replace('-', ' '))
        
        # 2. Date (Use existing or default to current)
        new_data['date'] = data.get('date', '2026-06-08')
        
        # 3. Source
        new_data['source'] = data.get('source', None)
        
        # 4. Status
        new_data['status'] = data.get('status', 'draft')
        
        # 5. Categories (from domain or type)
        categories = []
        if 'domain' in data:
            val = data['domain']
            categories.append(val if isinstance(val, str) else str(val))
        if 'type' in data:
            val = data['type']
            if isinstance(val, list):
                categories.extend([str(v) for v in val])
            else:
                categories.append(str(val))
        
        # Dedup and clean categories
        new_data['categories'] = sorted(list(set(categories)))
        
        # 6. Tags (from related_people, related_platforms, or existing tags)
        tags = []
        if 'tags' in data:
            if isinstance(data['tags'], list):
                tags.extend([str(t) for t in data['tags']])
            else:
                tags.append(str(data['tags']))
        
        for key in ['related_people', 'related_platforms']:
            if key in data:
                val = data[key]
                if isinstance(val, list):
                    tags.extend([str(v) for v in val])
                else:
                    tags.append(str(val))
        
        new_data['tags'] = sorted(list(set(tags)))
        
        # 7. Summary
        new_data['summary'] = data.get('summary', '')

        # Reconstruct content
        new_frontmatter = yaml.dump(new_data, sort_keys=False)
        new_content = f"---{new_frontmatter}---{body}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

for line in sys.stdin:
    path = line.strip()
    if path and os.path.exists(path):
        if migrate_file(path):
            print(f"Successfully migrated: {path}")
        else:
            print(f"Failed to migrate: {path}")
