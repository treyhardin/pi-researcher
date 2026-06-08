import os
import re
import glob

def find_broken_links(base_dir):
    # Pattern for [[link]] and [[link|text]]
    pattern = re.compile(r'\[\[([^|\]]+)(?:\|[^\]]*)?\]\]')
    
    broken_links = []
    
    # Get all markdown files in research/
    md_files = glob.glob(os.path.join(base_dir, '**', '*.md'), recursive=True)
    
    # Get a set of all existing files (relative to base_dir, without .md)
    # We want to check if research/path/to/file.md exists when we see [[path/to/file]]
    # Actually, the links in the files might be relative to research/ or they might be absolute from research/
    # Looking at the grep output:
    # research/people/marco-rubio.md:related_entities: [[aaro], [mike-rounds]]
    # "aaro" likely refers to research/organizations/aaro.md or something similar. 
    # Wait, let me see where aaro is.
    # research/organizations/aaro.md exists.
    # So the link [[aaro]] doesn't specify the path. 
    # This means I need to check if ANY file in research/ matches the link name.
    
    existing_files_map = {} # name -> full_path
    for f in md_files:
        rel_path = os.path.relpath(f, base_dir)
        name = os.path.splitext(rel_path)[0]
        # Also map the basename
        basename = os.path.basename(f)
        basename_no_ext = os.path.splitext(basename)[0]
        
        existing_files_map[name] = f
        existing_files_map[basename_no_ext] = f

    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = pattern.finditer(content)
            for match in matches:
                link_target = match.group(1)
                
                # Check if link_target is an absolute path within research/ or a relative one
                # If it's just 'aaro', we check 'aaro' and 'organizations/aaro' etc.
                
                found = False
                # Try direct match
                if link_target in existing_files_map:
                    found = True
                else:
                    # Try checking if it's a path-like link, e.g., 'cases/summary'
                    # See if 'research/cases/summary.md' exists
                    test_path = os.path.join(base_dir, link_target + '.md')
                    if os.path.exists(test_path):
                        found = True
                    else:
                        # Try looking for it in the map by checking if it's a subpath
                        # This is getting complex. Let's see what the grep showed.
                        # 'research/people/summary.md:- [[christopher-mellon]]'
                        # 'christopher-mellun' is 'research/people/christopher-mellon.md'
                        # So it's looking for the basename.
                        
                        # Let's check if any existing file name contains the link_target as a basename
                        for name, path in existing_files_map.items():
                            if name == link_target:
                                found = True
                                break
                
                if not found:
                    broken_links.append((md_file, link_target))

    return broken_links

if __name__ == "__main__":
    base = 'research'
    broken = find_broken_links(base)
    if not broken:
        print("No broken links found.")
    for file, link in broken:
        print(f"{file}: [[{link}]] is broken")
