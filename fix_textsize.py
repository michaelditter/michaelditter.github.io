#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_text_image(text, output_file="test_image.jpg"):
    # Create a new image
    width, height = 800, 400
    image = Image.new('RGB', (width, height), (34, 66, 110))
    draw = ImageDraw.Draw(image)
    
    # Load a font
    try:
        # Try to load a system font
        font_path = "/System/Library/Fonts/Helvetica.ttc"  # macOS default
        font = ImageFont.truetype(font_path, 32)
    except:
        # Fallback to default
        font = ImageFont.load_default()
    
    # Wrap text
    wrapped_text = textwrap.wrap(text, width=30)
    y_position = 50
    
    for line in wrapped_text:
        # The old way (deprecated)
        # width, height = draw.textsize(line, font=font)
        
        # The new way: using textbbox (Pillow 9.2.0+)
        left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
        text_width = right - left
        text_height = bottom - top
        
        # Or using alternative method
        # text_width = draw.textlength(line, font=font)
        # text_height = 32  # estimate based on font size
        
        # Center the text
        position = ((width - text_width) // 2, y_position)
        
        # Draw the text
        draw.text(position, line, font=font, fill=(255, 255, 255))
        y_position += text_height + 10
    
    # Save the image
    image.save(output_file)
    print(f"Created image: {output_file}")

if __name__ == "__main__":
    create_text_image("This is a test image with proper text size calculation") 