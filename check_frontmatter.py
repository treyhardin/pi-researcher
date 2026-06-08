import os

directory = 'research/people/'
files = [f for f in os.listdir(directory) if f.endswith('.md')]
missing_frontmatter = []

for filename in files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        if first_line != '---\n' and first_line != '---\r\n':
            missing_frontmatter.append(filename)

if missing_frontmatter:
    print("Files missing frontmatter:")
    for f in missing_frontmatter:
        print(f)
else:
    print("All files have frontmatter.")
