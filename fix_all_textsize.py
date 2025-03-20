#!/usr/bin/env python3
"""
This script finds and fixes all occurrences of draw.textsize in Python code embedded in YML files.
It replaces them with the modern textbbox equivalent.
"""

import os
import re
import glob

def replace_textsize_in_file(file_path):
    """
    Replace draw.textsize with textbbox in the given file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file contains the problematic method
    if 'textsize' not in content:
        return False, 0
    
    # Count occurrences before making changes (for reporting)
    original_count = content.count('textsize')
    
    # Find Python code blocks in YAML files (typically in GitHub Actions)
    if file_path.endswith(('.yml', '.yaml')):
        # Pattern for Python code blocks in GitHub Actions (using heredoc)
        python_blocks = re.findall(r'python.*<<\s*EOF\s*(.*?)\s*EOF', content, re.DOTALL)
        
        for i, block in enumerate(python_blocks):
            if 'textsize' in block:
                # Replace textsize with textbbox in the Python block
                modified_block = block.replace('draw.textsize', 'draw.textbbox((0, 0),')
                
                # Replace any direct assignments from textsize
                pattern = r'(\w+)\s*,\s*(\w+)\s*=\s*draw\.textbbox\(\(0,\s*0\),\s*([^)]+)\)'
                replacement = r'left, top, right, bottom = draw.textbbox((0, 0), \3)\n\1 = right - left\n\2 = bottom - top'
                modified_block = re.sub(pattern, replacement, modified_block)
                
                # Update the content with the modified block
                content = content.replace(block, modified_block)
    else:
        # Direct replacement for .py files
        pattern = r'(\w+)\s*,\s*(\w+)\s*=\s*draw\.textsize\(([^)]+)\)'
        replacement = r'left, top, right, bottom = draw.textbbox((0, 0), \3)\n\1 = right - left\n\2 = bottom - top'
        content = re.sub(pattern, replacement, content)
    
    # Count how many occurrences of textsize remain
    remaining = content.count('textsize')
    fixed_count = original_count - remaining
    
    if fixed_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {fixed_count} occurrences in {file_path}")
        return True, fixed_count
    
    return False, 0

def find_and_fix_textsize():
    """
    Find all YML files and fix any occurrences of draw.textsize.
    """
    yml_files = glob.glob('./**/*.yml', recursive=True)
    py_files = glob.glob('./**/*.py', recursive=True) 
    
    total_files_fixed = 0
    total_occurrences = 0
    
    for file_path in yml_files + py_files:
        # Skip virtual environment files
        if '/venv/' in file_path:
            continue
        
        fixed, count = replace_textsize_in_file(file_path)
        if fixed:
            total_files_fixed += 1
            total_occurrences += count
    
    print(f"\nSummary:")
    print(f"- Files fixed: {total_files_fixed}")
    print(f"- Total occurrences fixed: {total_occurrences}")
    
    if total_occurrences == 0:
        print("No occurrences of draw.textsize found.")
        print("The issue might be in a script being run directly or in a different format.")
        print("\nManual fix guidance:")
        print("1. Replace: left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
width = right - left
height = bottom - top")
        print("2. With: left, top, right, bottom = draw.textbbox((0, 0), text, font=font)")
        print("          width, height = right - left, bottom - top")

if __name__ == "__main__":
    find_and_fix_textsize() 