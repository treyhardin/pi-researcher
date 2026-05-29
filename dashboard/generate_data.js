const fs = require('fs');
const path = require('path');

const researchDir = '/home/trumancreative/projects/phenomenon/research';

function getFilesRecursively(dir) {
  let results = [];
  try {
    const list = fs.readdirSync(dir);
    list.forEach(file => {
      file = path.resolve(dir, file);
      const stat = fs.statSync(file); // Error here, should be fs.statSync
      if (stat && stat.isDirectory()) {
        results = results.concat(getFilesRecursively(file));
      } else if (file.endsWith('.md')) {
        results.push(file);
      }
    });
  } catch (e) {
    // skip errors
  }
  return results;
}

function parseMarkdown(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const relativePath = path.relative(researchDir, filePath);
  const title = path.basename(filePath, '.md').replace(/-/g, ' ').replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase());
  
  let body = content;
  const frontmatterMatch = content.match(/^---\s*([\s\S]*?)\s*---/);
  if (frontmatterMatch) {
    body = content.replace(frontmatterMatch[0], '');
  }

  return {
    title,
    content: body.trim(),
    path: relativePath
  };
}

function main() {
  const files = getFilesRecursively(researchDir);
  const data = {};

  files.forEach(file => {
    const relativePath = path.relative(researchDir, file);
    const parts = relativePath.split(path.sep);
    
    let currentLevel = data;
    for (let i = 0; i < parts.length - 1; i++) {
      const part = parts[i];
      if (!currentLevel[part]) {
        currentLevel[part] = {};
      }
      currentLevel = currentLevel[part];
    }

    const fileName = parts[parts.length - 1];
    if (fileName.endsWith('.md')) {
        const key = path.basename(fileName, '.md');
        currentLevel[key] = parseMarkdown(file);
    }
  });

  fs.writeFileSync('research_data.json', JSON.stringify(data, null, 2));
  console.log('Research data JSON generated successfully.');
}

main();
