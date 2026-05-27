import os
import re
import subprocess
import urllib.parse

def check_url(url):
    try:
        # Using curl to check the URL status code
        command = ['curl', '-I', '-s', '-L', '-o', '/dev/null', '-w', '%{http_code}', url]
        result = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8').strip()
        if result == '200':
            return True, "200 OK"
        else:
            return False, f"HTTP {result}"
    except Exception as e:
        return False, str(e)

def check_local_path(base_dir, link_path):
    # link_path is relative to the file containing the link
    full_path = os.path.abspath(os.path.join(base_dir, link_path))
    if os.path.exists(full_path):
        return True, f"Exists: {full_path}"
    else:
        return False, f"Not found: {full_path}"

def validate_markdown_links(root_dir):
    # Regex to find markdown links: [text](link)
    # This is a simplified regex; it might not catch all edge cases but should work for standard links
    link_regex = re.compile(r'\[.*?\]\((.*?)\)')
    
    results = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    links = link_regex.findall(content)
                    
                    for link in links:
                        # Skip anchors like #section
                        if link.startswith('#'):
                            continue
                        
                        if link.startswith(('http://', 'https://')):
                            is_valid, status = check_url(link)
                            if not is_valid:
                                results.append((file_path, link, f"Invalid URL: {status}"))
                        else:
                            # Check if it's a local path
                            # some links might be relative to root or current file
                            # If it starts with '/', we treat it as absolute from root (project root?)
                            # For this task, let's assume relative to the current file's directory
                            is_valid, status = check_local_path(dirpath, link)
                            if not is_valid:
                                results.append((file_path, link, f"Invalid Path: {status}"))
    
    return results

if __name__ == "__main__":
    research_dir = "/home/trumancreative/projects/phenomenon/research"
    invalid_links = validate_markdown_links(research_dir)
    
    if not invalid_links:
        print("All links are valid.")
    else:
        print(f"Found {len(invalid_links)} invalid links:")
        for file, link, error in invalid_links:
            print(f"- {file} -> {link} ({error})")
