import os
import re

def update_links(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Replacement rules (Old string -> New string)
                replacements = {
                    'research/propulsion_and_advanced_pshyics_research': 'technologies/propulsion-systems-overview', # typo check in my thought? no, let me check actual
                    'propulsion_and_advanced_physics_research': 'technologies/propulsion-systems-overview',
                    'technologies/ion-propulsion': 'technologies/propulsion-systems-overview',
                    'research/ion-propulsion': 'technologies/propulsion-systems-overview',
                }

                new_content = content
                for old, new in replacements.items():
                    # Using regex to handle potential variations or partial matches safely
                    pattern = re.compile(re.escape(old))
                    if pattern.search(new_content):
                        print(f"Updating {filepath}: {old} -> {new}")
                        new_content = pattern.sub(new, new_content)

                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)

if __name__ == "__main__":
    update_links('/home/trumancreative/projects/phenomenon/research/')
