import os
import glob
import re

base_dir = '/home/tushardevx01/Documents/Full-stack'
files = glob.glob(f'{base_dir}/*/notes.md')

def process_file(filepath):
    if '08-databases' in filepath:
        return # Skip the template itself
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 1. Strip frontmatter ---
    if content.startswith('---'):
        content = content[3:].lstrip()
        # Find the next ---
        next_dashes = content.find('---')
        if next_dashes != -1:
            # Remove the second --- as well
            content = content[:next_dashes] + content[next_dashes+3:]
            content = content.lstrip()

    lines = content.split('\n')
    new_lines = []
    
    in_nav = False
    
    for line in lines:
        # 2. Remove Module Navigation block
        if re.match(r'^(#|##|###)?\s*Module Navigation', line, re.IGNORECASE) or '> **Navigation:**' in line:
            in_nav = True
            continue
        
        if in_nav:
            # End of nav block usually denoted by --- or a new heading # Table of Contents
            if line.startswith('---') or 'Table of Contents' in line:
                in_nav = False
                if line.startswith('---'):
                    continue # Skip the separator
            else:
                continue # Skip nav content
                
        # 3. Standardize Chapter Headers
        # Change `## Chapter X: Title` or `# Chapter X: Title` to `# CHAPTER X: Title`
        m = re.match(r'^(#|##)\s*Chapter\s+(\d+):\s*(.*)', line, re.IGNORECASE)
        if m:
            new_lines.append(f"# CHAPTER {m.group(2)}: {m.group(3)}")
            continue
            
        new_lines.append(line)
        
    # Write back
    with open(filepath, 'w') as f:
        f.write('\n'.join(new_lines))

for f in files:
    print(f"Processing {f}...")
    process_file(f)

print("Done.")
