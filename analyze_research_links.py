import os
import re
from collections import defaultdict

def find_all_md_files(directory):
    md_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files

def analyze_links(research_dir):
    md_files = find_all_md_files(research_dir)
    # Normalize paths to absolute for easier comparison
    abs_md_files = {os.path.abspath(f) for f in md_files}
    
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    orphans = []
    
    # Create a map of relative paths to absolute paths for quick lookup
    # We'll need to handle the context of the file being read.
    
    link_pattern = re.compile(r'\[.*?\]\((.*?)\)')

    for file_path in md_files:
        abs_file_path = os.path.abspath(file_path)
        has_out_links = False
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            links = link_pattern.findall(content)
            
            for link in links:
                # Clean link (remove anchors or queries)
                link_target = link.split('#')[0].split('?')[0]
                if not link_target: continue
 # Should not happen with regex
                
                # Resolve link relative to the current file's directory
                file_dir = os.path.dirname(file_path)
                target_abs_path = os.path.abspath(os.path.join(file_dir, link_target))
                
                if target_abs_path in abs_md_files:
                    in_degree[target_abs_path] += 1
                    out_degree[abs_file_path] += 1
                    has_out_links = True
            
            if not has_out_links:
                out_degree[abs_file_path] = 0

    # Find orphans: files that are never linked to
    for abs_f in abs_md_files:
        if in_degree[abs_f] == 0:
            orphans.append(abs_f)
            
    return in_degree, out_degree, orphans, abs_md_files

if __name__ == "__main__":
    research_dir = 'research'
    in_degree, out_degree, orphans, all_files = analyze_links(research_dir)
    
    print(f"Total MD files: {len(all_files)}")
    print(f"Files with in-links: {len(in_degree)}")
    print(f"Files with out-links: {len(out_degree)}")
    print(f"Orphan files: {len(orphans)}")
    
    if orphans:
        print("\nOrphan Files:")
        for orphan in sorted(orphans):
            print(f"  - {os.path.relpath(orphan, '.')}")

    print("\nTop Linked Files (In-degree):")
    sorted_in = sorted(in_degree.items(), key=lambda item: item[1], reverse=True)
    for path, count in sorted_in[:10]:
        print(f"  - {os.path.relpath(path, '.')}: {count}")

    print("\nTop Out-linking Files (Out-degree):")
    sorted_out = sorted(out_degree.items(), key=lambda item: item[1], reverse=True)
    for path, count in sorted_out[:10]:
        print(f"  - {os.path.relpath(path, '.')}: {count}")
