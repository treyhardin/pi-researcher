import os
import glob
import yaml
import re
import sys

def audit_file(filepath):
    errors = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [f"Could not read file: {str(e)}"]

    # Check for frontmatter block at the beginning of the file
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return ["Missing Frontmatter"]

    yaml_block = match.group(1)
    try:
        data = yaml.safe_load(yaml_block)
        if data is None:
            return ["Empty Frontmatter"]
    except Exception as e:
        return [f"Malformed YAML: {str(e)}"]

    # Define schema requirements
    required_keys = {
        'title': str,
        'date': lambda x: isinstance(x, str) and re.match(r'^\d{4}-\d{2}-\d{2}$', x),
        'status': lambda x: x in ['draft', 'reviewed', 'verified'],
        'source': str,
        'categories': list,
        'tags': list,
        'summary': str
    }

    # Validate keys and types
    for key, validator in required_keys.items():
        if key not in data:
            errors.append(f"Missing Key: '{key}'")
            continue
        
        val = data[key]
        try:
            if callable(validator) and not validator(val):
                if key == 'date':
                    errors.append("Invalid Date Format: expected YYYQ-MM-DD")
                elif key == 'status':
                    errors.append("Invalid Status: must be [draft, reviewed, verified]")
                else:
                    errors.append(f"Invalid Value for '{key}': {val}")
            elif isinstance(validator, type) and not isinstance(val, validator):
                errors.append(f"Invalid Type for '{key}': expected {validator.__name__}")
        except Exception as e:
            errors.append(f"Error validating '{key}': {str(e)}")

    return errors

def main(directory):
    md_files = glob.glob(os.path.join(directory, '**/*.md'), recursive=True)
    # Exclude non-research files if any are in the path (though we target research/)
    md_files = [f for f in md_files if 'research/' in f]
    
    if not md_files:
        print(f"No markdown files found in {directory}")
        return

    all_errors = {}
    for filepath in md_files:
        file_errors = audit_file(filepath)
        if file_errors:
            all_errors[filepath] = file_errors

    if not all_errors:
        print("PASS: All research files follow the standard schema.")
    else:
        for filepath, errors in all_errors.items():
            print(f"{filepath}: {', '.join(errors)}")

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    main(target_dir)
