import os
import re

def get_all_links():
    # matches [[some|title]] or [[some]]
    pattern = re.compile(r'\[\[(.*?)\]\\]')
    results = []
    for root, _, files in os.walk('research/'):
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                matches = pattern.findall(content)
                for m in matches:
                    link_id = m.split('|')[0].strip()
                    results.append({'file': full_path, 'link': link_id})
    return results

def check():
    all_links = get_all_links()
    issues = [] # (file_path, raw_link)
    
    for item in all_links:
        l = item['link']
        f = item['file']
        if not l: continue
        
        is_bad = False
        reasons = []
        
        # 1. Check for underscores (non-standard)
        if '_' in l:
            is_bad = True
            reasons.append(f"Non-standard character (_)")

        # 2. Check if it exists on disk
        path = os.path.join('research', l)
        if not os.path.exists(path):
            # Try appending .md
            if not os.path.exists(path + '.md'):
                is_bad = True
                reasons.append("Broken (not found on disk)")

        if is_bad:
            issues.append((f, l, reasons))
    
    print(f"Total links processed: {len(
