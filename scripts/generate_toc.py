#!/usr/bin/env python3
"""
Table of Contents Generator for README.md
This script generates an efficient table of contents with jump links for better navigation.
"""

import re
from pathlib import Path

def generate_toc(readme_path):
    """
    Generate a table of contents from markdown headers.
    
    Args:
        readme_path: Path to the README.md file
    
    Returns:
        String containing the table of contents
    """
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all headers (## level and below)
    headers = re.findall(r'^(#{2,})\s+(.+)$', content, re.MULTILINE)
    
    if not headers:
        return ""
    
    toc_lines = ["## 目录 (Table of Contents)\n"]
    
    for level_str, title in headers:
        level = len(level_str) - 1  # Adjust level (## = level 1)
        indent = "  " * (level - 1)
        
        # Create anchor link (GitHub style)
        anchor = title.lower()
        anchor = re.sub(r'[^\w\s-]', '', anchor)  # Remove special chars
        anchor = re.sub(r'[-\s]+', '-', anchor)   # Replace spaces with hyphens
        
        toc_lines.append(f"{indent}- [{title}](#{anchor})")
    
    return "\n".join(toc_lines) + "\n"

def add_toc_to_readme(readme_path):
    """
    Add or update table of contents in README.md
    
    Args:
        readme_path: Path to the README.md file
    """
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    toc = generate_toc(readme_path)
    
    # Check if TOC already exists
    toc_marker_start = "<!-- TOC START -->"
    toc_marker_end = "<!-- TOC END -->"
    
    if toc_marker_start in content and toc_marker_end in content:
        # Update existing TOC
        pattern = f"{re.escape(toc_marker_start)}.*?{re.escape(toc_marker_end)}"
        new_toc = f"{toc_marker_start}\n{toc}\n{toc_marker_end}"
        content = re.sub(pattern, new_toc, content, flags=re.DOTALL)
    else:
        # Add new TOC after the first image/title
        lines = content.split('\n')
        insert_pos = 2  # After the first line (image reference)
        
        toc_section = f"\n{toc_marker_start}\n{toc}\n{toc_marker_end}\n"
        lines.insert(insert_pos, toc_section)
        content = '\n'.join(lines)
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Table of contents {'updated' if toc_marker_start in content else 'added'} to README.md")

def main():
    """Main function to generate and insert TOC."""
    repo_root = Path(__file__).parent.parent
    readme_path = repo_root / 'README.md'
    
    if not readme_path.exists():
        print(f"Error: README.md not found at {readme_path}")
        return 1
    
    add_toc_to_readme(readme_path)
    return 0

if __name__ == '__main__':
    exit(main())
