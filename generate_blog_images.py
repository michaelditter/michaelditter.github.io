#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
from pathlib import Path

def create_blog_image(title, filename, bg_color=(34, 66, 110), size=(1200, 630)):
    """
    Create a blog post image with title overlay
    
    Args:
        title: Title text to display on the image
        filename: Output filename (will be saved in img/blog/)
        bg_color: Background color as RGB tuple
        size: Image size as (width, height) tuple
    """
    width, height = size
    
    # Create a new image
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Load a font - try system fonts
    try:
        try:
            # macOS default
            font_path = "/System/Library/Fonts/Helvetica.ttc"
            title_font = ImageFont.truetype(font_path, 60)
        except:
            # Ubuntu default
            font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            title_font = ImageFont.truetype(font_path, 60)
    except:
        # Fallback to default
        title_font = ImageFont.load_default()
    
    # Add pattern
    for i in range(20):
        x1, y1 = i * 100, i * 40
        x2, y2 = width - (i * 100), height - (i * 40)
        color = (max(bg_color[0] - 20, 0), max(bg_color[1] - 20, 0), max(bg_color[2] - 20, 0))
        draw.line((x1, y1, x2, y2), fill=color, width=5)
    
    # Add a semi-transparent overlay for better text visibility
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 150))
    image.paste(Image.alpha_composite(Image.new('RGBA', image.size, (0, 0, 0, 0)), overlay).convert('RGB'), (0, 0))
    
    # Add text
    draw = ImageDraw.Draw(image)
    
    # Wrap text
    wrapped_text = textwrap.wrap(title, width=30)
    y_position = (height - len(wrapped_text) * 70) // 2
    
    for line in wrapped_text:
        # The new way: using textbbox (Pillow 9.2.0+)
        left, top, right, bottom = draw.textbbox((0, 0), line, font=title_font)
        text_width = right - left
        text_height = bottom - top
        
        # Center the text
        position = ((width - text_width) // 2, y_position)
        
        # Draw a shadow
        draw.text((position[0] + 2, position[1] + 2), line, font=title_font, fill=(0, 0, 0))
        # Draw the text
        draw.text(position, line, font=title_font, fill=(255, 255, 255))
        y_position += text_height + 10
    
    # Create output directory if it doesn't exist
    img_dir = Path("img/blog")
    img_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the image
    image_path = img_dir / filename
    image.save(image_path)
    print(f"Created image: {image_path}")

# Create missing images
if __name__ == "__main__":
    # Healthcare case study image
    create_blog_image(
        "AI in Healthcare: Case Study of a Successful Digital Transformation", 
        "ai-healthcare.jpg", 
        bg_color=(52, 152, 219)  # Medical blue
    )
    
    # Ethical AI frameworks image
    create_blog_image(
        "Building Ethical AI Frameworks", 
        "ethical-ai.jpg", 
        bg_color=(142, 68, 173)  # Purple for ethics
    )
    
    # Transfer learning image
    create_blog_image(
        "Transfer Learning Techniques", 
        "transfer-learning.jpg", 
        bg_color=(39, 174, 96)  # Green
    )
    
    # AI bias image
    create_blog_image(
        "AI Bias Mitigation Strategies", 
        "ai-bias.jpg", 
        bg_color=(231, 76, 60)  # Red for warning/caution
    ) 