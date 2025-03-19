#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def create_ethics_flow_diagram(output_filename="ai-ethics-flow.png", size=(800, 400)):
    """
    Creates a simple AI ethics flow diagram showing the decision process
    """
    width, height = size
    
    # Create a new image with white background
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # Try to load a system font
    try:
        try:
            # macOS default
            font_path = "/System/Library/Fonts/Helvetica.ttc"
            title_font = ImageFont.truetype(font_path, 20)
            box_font = ImageFont.truetype(font_path, 14)
        except:
            # Ubuntu default
            font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            title_font = ImageFont.truetype(font_path, 20)
            box_font = ImageFont.truetype(font_path, 14)
    except:
        # Fallback to default
        title_font = ImageFont.load_default()
        box_font = ImageFont.load_default()
    
    # Draw title
    title = "AI Ethical Decision Flow"
    left, top, right, bottom = draw.textbbox((0, 0), title, font=title_font)
    text_width = right - left
    draw.text(((width - text_width) // 2, 20), title, font=title_font, fill=(0, 0, 0))
    
    # Define process stages
    stages = [
        {"name": "Project Conception", "color": (230, 126, 34), "x": 100, "y": 100, "w": 140, "h": 60},
        {"name": "Ethics Impact\nAssessment", "color": (155, 89, 182), "x": 300, "y": 100, "w": 140, "h": 60},
        {"name": "Data Collection\n& Processing", "color": (52, 152, 219), "x": 500, "y": 100, "w": 140, "h": 60},
        {"name": "Model Development", "color": (46, 204, 113), "x": 500, "y": 200, "w": 140, "h": 60},
        {"name": "Testing & Validation", "color": (41, 128, 185), "x": 300, "y": 200, "w": 140, "h": 60},
        {"name": "Deployment\nDecision", "color": (155, 89, 182), "x": 100, "y": 200, "w": 140, "h": 60},
        {"name": "Monitoring &\nReevaluation", "color": (230, 126, 34), "x": 100, "y": 300, "w": 140, "h": 60},
    ]
    
    # Draw arrows connecting stages
    arrows = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0)
    ]
    
    # Function to draw an arrow between two boxes
    def draw_arrow(start_box, end_box, color=(80, 80, 80), width=2):
        # Get centers of boxes
        start_x = start_box["x"] + start_box["w"] // 2
        start_y = start_box["y"] + start_box["h"] // 2
        end_x = end_box["x"] + end_box["w"] // 2
        end_y = end_box["y"] + end_box["h"] // 2
        
        # Adjust starting and ending points to be at the edge of boxes
        if abs(start_x - end_x) > abs(start_y - end_y):
            # Horizontal dominant
            if start_x < end_x:
                start_x = start_box["x"] + start_box["w"]
                end_x = end_box["x"]
            else:
                start_x = start_box["x"]
                end_x = end_box["x"] + end_box["w"]
        else:
            # Vertical dominant
            if start_y < end_y:
                start_y = start_box["y"] + start_box["h"]
                end_y = end_box["y"]
            else:
                start_y = start_box["y"]
                end_y = end_box["y"] + end_box["h"]
        
        # Draw line
        draw.line((start_x, start_y, end_x, end_y), fill=color, width=width)
        
        # Draw arrowhead
        arrow_size = 8
        angle = 0
        
        # Calculate angle
        if end_x - start_x != 0:  # Avoid division by zero
            angle = math.atan2(end_y - start_y, end_x - start_x)
        else:
            angle = math.pi/2 if end_y > start_y else -math.pi/2
            
        # Draw arrowhead
        x1 = end_x - arrow_size * math.cos(angle - math.pi/6)
        y1 = end_y - arrow_size * math.sin(angle - math.pi/6)
        x2 = end_x - arrow_size * math.cos(angle + math.pi/6)
        y2 = end_y - arrow_size * math.sin(angle + math.pi/6)
        
        draw.polygon([(end_x, end_y), (x1, y1), (x2, y2)], fill=color)
    
    # Draw boxes for each stage
    for stage in stages:
        # Draw rounded rectangle
        x, y, w, h = stage["x"], stage["y"], stage["w"], stage["h"]
        draw.rectangle([x, y, x + w, y + h], fill=stage["color"], outline=(50, 50, 50), width=2)
        
        # Add text
        lines = stage["name"].split('\n')
        line_height = 16
        total_height = len(lines) * line_height
        
        for i, line in enumerate(lines):
            left, top, right, bottom = draw.textbbox((0, 0), line, font=box_font)
            text_width = right - left
            text_y = y + (h - total_height) // 2 + i * line_height
            draw.text((x + (w - text_width) // 2, text_y), line, font=box_font, fill=(255, 255, 255))
    
    # Draw arrows between stages
    import math
    for start_idx, end_idx in arrows:
        draw_arrow(stages[start_idx], stages[end_idx])
    
    # Draw ethics checkpoints
    checkpoints = [
        {"text": "Ethics Review", "x": 220, "y": 80},
        {"text": "Data Ethics Check", "x": 420, "y": 80},
        {"text": "Fairness Testing", "x": 420, "y": 220},
        {"text": "Impact Assessment", "x": 220, "y": 220},
        {"text": "Ongoing Monitoring", "x": 220, "y": 280},
    ]
    
    for checkpoint in checkpoints:
        x, y = checkpoint["x"], checkpoint["y"]
        
        # Draw checkpoint marker
        marker_size = 15
        draw.ellipse([x-marker_size, y-marker_size, x+marker_size, y+marker_size], 
                    fill=(255, 255, 255), outline=(231, 76, 60), width=2)
        draw.line([x-8, y-8, x+8, y+8], fill=(231, 76, 60), width=2)
        draw.line([x-8, y+8, x+8, y-8], fill=(231, 76, 60), width=2)
        
        # Add text label
        left, top, right, bottom = draw.textbbox((0, 0), checkpoint["text"], font=box_font)
        text_width = right - left
        draw.text((x - text_width // 2, y + marker_size + 5), 
                checkpoint["text"], font=box_font, fill=(0, 0, 0))
    
    # Create directories if needed
    img_dir = Path("img/blog")
    img_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the image
    output_path = img_dir / output_filename
    image.save(output_path)
    print(f"Created ethics flow diagram: {output_path}")

if __name__ == "__main__":
    create_ethics_flow_diagram() 