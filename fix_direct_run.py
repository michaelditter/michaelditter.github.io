#!/usr/bin/env python3
"""
Fix for 'ImageDraw' object has no attribute 'textsize' error

This script can be used as a wrapper to run another Python script,
monkey-patching PIL.ImageDraw to handle the deprecated textsize method.

Usage:
  python fix_direct_run.py your_script.py [args...]
"""

import sys
import importlib.util
from PIL import ImageDraw, Image

# Add a backward-compatible textsize method to ImageDraw
def textsize_polyfill(self, text, font=None, spacing=4, direction=None, features=None, language=None, stroke_width=0):
    """
    Polyfill for the deprecated textsize method.
    Returns the size of a given string, in pixels.
    """
    if hasattr(self, 'textbbox'):
        left, top, right, bottom = self.textbbox((0, 0), text, font, spacing, direction, features, language, stroke_width)
        return right - left, bottom - top
    
    # If textbbox doesn't exist either, try other methods or use a fallback
    if font is None:
        font = self.getfont()
    if hasattr(font, 'getsize'):
        return font.getsize(text)
    elif hasattr(font, 'getbbox'):
        bbox = font.getbbox(text)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    else:
        # Very basic fallback - not accurate
        return len(text) * 10, 20

# Monkey patch the ImageDraw class
if not hasattr(ImageDraw.ImageDraw, 'textsize'):
    ImageDraw.ImageDraw.textsize = textsize_polyfill
    print("Added backward compatibility for 'textsize' method")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} your_script.py [args...]")
        sys.exit(1)
    
    script_path = sys.argv[1]
    sys.argv = sys.argv[1:]  # Remove this script's name from argv
    
    # Load and run the script
    try:
        spec = importlib.util.spec_from_file_location("module.name", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f"Executed {script_path} with ImageDraw.textsize patch")
    except Exception as e:
        print(f"Error executing {script_path}: {e}")
        sys.exit(1) 