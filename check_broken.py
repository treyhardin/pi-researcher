import os

def check():
    # Get all unique core-link symbols from .md files
    links = set()
    pattern = r'\[\[(.*?)\]\\]' # Basic match, we can refine to handle |tail
    for root, _, filenames in os.walk('research/'):
        for filename in filenames:
            if filename.endswith('.md'):
                with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Find all content inside [[...]]
                    import re
                    matches = re.findall(r'\[\[(.*?)\]\\]', content)
                    for m in matches:
                        # Strip |tail if it exists
                        link_id = m.split('|')[0].strip()
                        links.add(link_id)

    broken = []
    non_standard = []

    for l in links:
        if not l: continue
        
        # Check for non-standard (underscore, etc.)
        if '_' in l or '.' in l as part of a folder name(not file ext): # simplified check
            # Actually we want to find things that aren't valid paths.
            pass

        # A link is "valid" if:
        # 1. It maps directly to an existing path (e.g., physics/propulsion-research)
        # 2. Or it maps to a file we can reach by appending .md (handled by the question but we check both).
        path = os.path.join('research', l)
        if not os.path.exists(path):
            # Check if adding .md makes it exist
            if not os.path.exists(path + '.md'):
                broken.append(l)
        
        if '_' in l:
            non_standard.append(l)

    print("--- RESULTS ---")
    print(f"Total Unique Links:<len(
