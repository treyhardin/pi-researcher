import os
import yaml
import re

def audit_frontmatter(directory):
    audit_results = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract frontmatter using regex
                match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                if match:
                    frontmatter_str = match.group(1)
                    try:
                        frontmatter = yaml.safe_load(frontmatter_str)
                        audit_results.append({
                            'file': file_path,
                            'status': 'exists',
                            'data': frontmatter
                        })
                    except Exception as e:
                        audit_results.append({
                            'file': file_path,
                            'status': f'error: {str(e)}',
                            'data': None
                        })
                else:
                    audit_results.append({
                        'file': file_path,
                        'status': 'missing',
                        'data': None
                    })
    return audit_results

if __name__ == "__main__":
    research_dir = "research"
    results = audit_frontmatter(research_dir)
    import json
    print(json.dumps(results, indent=2))
