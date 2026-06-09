import os
import yaml
import re
from datetime import datetime
import argparse

# Configuration based on RESEARCH-GUIDELINES.md
REQUIRED_FIELDS = ['title', 'date', 'status', 'source', 'categories', 'tags', 'summary']
ALLOWED_STATUSES = ['draft', 'review', 'published']
DEFAULT_DATE = datetime.now().strftime('%Y-%m-%d')

def get_default_frontmatter(file_path):
    """Generates a default frontmatter dictionary for a new file."""
    basename = os.path.basename(file_path).replace('_', '-').replace('.md', '')
    title = basename.strip('-').capitalize()
    return {
        'title': title,
        'date': DEFAULT_DATE,
        'status': 'draft',
        'source': None,
        'categories': [],
        'tags': [],
        'summary': 'Summary pending.'
    }

def standardize_file(file_path, mode='audit'):
    """
    Reads a file and checks its frontmatter.
    Returns (is_standardized, updated_content, issues).
    mode: 'audit' or 'externally_fixed' (we use 'fix' in main)
    """
    issues = []
    with open(file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()

    # Regex to find the frontmatter block
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.search(pattern, original_content, re.DOTALL)
    
    new_frontmatter = {}
    remaining_content = original_content

    if not match:
        issues.append("Missing frontmatter block")
        if mode == 'fix':
            new_frontmatter = get_default_frontmatter(file_path)
            # Content stays the same, but we'll prepend new FM in the fix step
            remaining_content = original_content
        else:
            return False, None, issues
    else:
        fm_text = match.group(1)
        remaining_content = original_content[match.end():].lstrip()
        try:
            new_frontmatter = yaml.safe_load(fm_text)
            if not isinstance(new_frontmatter, dict):
                raise ValueError("Frontmatter is not a dictionary")
        except Exception as e:
            issues.append(f"Invalid YAML error: {str(to_string(e))}")
            return False, None, issues

    # --- Validation and Standardization Logic ---
    needs_fix = False

    # 1. Check Required Fields
    for field in REQUIRED_FIELDS:
        if field not in new_frontmatter:
            issues.append(f"Missing required field: '{field}'")
            if mode == 'fix':
                needs_fix = True
                if field in ['categories', 'tags']:
                    new_frontmatter[field] = []
                elif field == 'source':
                    new_frontmatter[field] = None
                else:
                    # Default values for other fields
                    if field == 'title':
                        new_frontmatter[field] = os.path.basename(file_path).replace('_', '-').replace('.md', '').capitalize()
                    elif field == 'date':
                        new_frontmatter[field] = DEFAULT_DATE
                    else:
                        new_frontmatter[field] = None

    # 2. Validate/Fix Status
    current_status = new_frontmatter.get('status')
    if current_status is not None:
        normalized_status = str(current_status).lower().replace('ed', '').strip()
        if normalized_status in ALLOWED_STATUSES:
            if current_status != normalized_status:
                issues.append(f"Improper status formatting (normalized '{current_status}' -> '{normalized_status}')")
                new_frontmatter['status'] = normalized_status
                needs_fix = True
            else:
                # It is already correct and normalized
                pass
        else:
            issues.append(f"Invalid status value: '{current_status}'")
            if mode == 'fix':
                new_frontmatter['status'] = 'draft'
                needs_fix = True

    # 3. Validate/Fix Source
    source = new_frontmatter.get('source')
    source_str = str(source) if source is not None else ""
    if source in [None, '', 'Unknown', 'unknown']:
        if source is not None:
            issues.append(f"Non-standard source value: '{source}'")
        if mode == 'fix':
            new_frontmatter['source'] = None
            needs_fix = True

    # 4. Ensure Lists for Categories and Tags
    for list_field in ['categories', 'tags']:
        val = new_frontmatter.get(list_field)
        if not isinstance(val, list):
            issues.append(f"Field '{list_field}' must be a list (found {type(val).__name__})")
            if mode == 'fix':
                new_frontmatter[list_field] = [] if val is None else [str(val)]
                needs_fix = True

    is_standardized = len(issues) == 0
    
    # Construct updated content if fixing
    updated_content = None
    if mode == 'fix' and (needs_fix or not match):
        new_fm_yaml = yaml.dump(new_frontmatter, sort_keys=False, allow_unicode=True).strip()
        updated_content = f"---\n{new_fm_yaml}\n---\n\n{remaining_content}"

    return is_standardized, updated_content, issues

def to_string(e):
    return str(e)

def main():
    parser = argparse.ArgumentParser(description="Standardize Research Frontmatter")
    parser.add_argument('--audit', action='store_true', help='Audit files without changing them')
    parser.add_argument('--fix', action='store_true', help='Fix files that are non-standard')
    args = parser.parse_args()

    if not args.audit and not args.fix:
        parser.print_help()
        return

    mode = 'fix' if args.fix else 'audit'
    research_dir = "research"
    
    stats = {'audited': 0, 'standardized': 0, 'non_standard': 0, 'fixed': 0, 'errors': 0}
    
    print(f"{'MODE: ' + mode.upper():<10} | {'FILE':<50} | {'STATUS':<15} | {'ISSUES'}")
    print("-" * 110)

    for root, dirs, files in os.walk(research_dir):
        if '.git' in dirs:
            dirs.remove('.git')
            
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                stats['audited'] += 1
                
                try:
                    is_std, updated_content, issues = standardize_file(file_path, mode)
                    
                    status_str = "OK" if is_std else "NON-STANDARD"
                    if not is_std:
                        stats['non_standard'] += 1
                    else:
                        stats['standardized'] += 1

                    issue_str = "; ".join(issues) if issues else ""
                    print(f"{'':<10} | {file_path:<50} | {status_str:<15} | {issue_str}")

                    if args.fix and not is_std:
                        # If we have updated content to write back
                        if updated_content is not None:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(updated_content)
                            stats['fixed'] += 1
                        else:
                            # This shouldn't really happen with the logic above but for safety:
                            pass
                    elif args.fix and is_std and 'Improper status formatting' in issue_str:
                         # Handle cases where it was "standardized" but needed a small fix (like normalization)
                         # My standardize_file returns updated_content if needs_fix is True
                         pass

                except Exception as e:
                    print(f"{'':<10} | {file_path:<50} | {'ERROR':<15} | {str(e)}")
                    stats['errors'] += 1

    print("-" * 110)
    print(f"Summary: Audited: {stats['audited']}, Standardized: {stats['standardized']}, Non-Standard: {stats['non_standard']}, Fixed: {stats['fixed']}, Errors: {stats['errors']}")

if __name__ == "__main__":
    main()
