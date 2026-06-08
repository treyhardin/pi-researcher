existing_files = ["research/programs/project-blue-book"]
link_part = "project-blue-book"
match_found = False
for ef in existing_files:
    if ef == "research/" + link_part or ef == link_part or ef.endswith("/" + link_part):
        match_found = True
        break
print(f"Match found: {match_found}")
