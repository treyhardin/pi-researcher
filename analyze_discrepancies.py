import json

def analyze_audit(audit_file):
    with open(audit_file, 'r') as f:
        data = json.load(f)
    
    required_fields = ['title', 'date', 'status', 'source', 'categories', 'tags', 'summary']
    allowed_statuses = ['draft', 'review', 'published']
    
    discrepancies = []
    
    for entry in data:
        file_path = entry['file']
        if entry['status'] != 'exists':
            discrepancies.append({'file': file_path, 'issue': entry['status']})
            continue
        
        fm = entry['data']
        issues = []
        
        # Check for missing fields
        for field in required_fields:
            if field not in fm:
                issues.append(f'missing_{field}')
            else:
                # Check value types/formats if possible
                val = fm[field]
                if field == 'source' and val == "Unknown":
                    issues.append('source_is_string_instead_of_null')
                if field == 'status' and val not in allowed_statuses:
                    issues.append(f'invalid_status_{val}')
                if field == 'categories' and not isinstance(val, list):
                    issues.append('categories_not_a_list')
                if field == 'tags' and not isinstance(val, list):
                    issues.append('tags_not_a_list')

        if issues:
            discrepancies.append({'file': file_path, 'issues': issues})
            
    return discrepancies

if __name__ == "__main__":
    results = analyze_audit('audit_results.json')
    print(json.dumps(results, indent=2))
