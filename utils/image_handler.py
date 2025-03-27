import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import base64
from io import BytesIO
import random

def generate_avatar_placeholder(size=(200, 200), bg_color=None, text="User", text_color="#FFFFFF"):
    """Generate a more appealing placeholder avatar image"""
    # Choose a color from our theme colors if none specified
    if bg_color is None:
        theme_colors = ["#3498db", "#2980b9", "#9b59b6", "#16a085", "#f39c12", "#e74c3c", "#2c3e50"]
        bg_color = random.choice(theme_colors)
    
    # Create a new image with a solid color
    avatar = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(avatar)
    
    # Try to use a font or default to a simple centered initial
    try:
        font_size = size[0] // 3
        try:
            # Try to use a common font
            common_fonts = ["Arial", "Helvetica", "Verdana", "Tahoma", "Trebuchet MS"]
            font = None
            for font_name in common_fonts:
                try:
                    font = ImageFont.truetype(font_name, font_size)
                    break
                except:
                    continue
            
            if font is None:
                font = ImageFont.load_default()
                font_size = 40  # Adjust size for default font
        except:
            font = ImageFont.load_default()
            font_size = 40  # Adjust size for default font
        
        # Get the first initial
        initial = text[0].upper()
        
        # Calculate text position for center alignment
        # For PIL versions that might not have textbbox
        try:
            left, top, right, bottom = draw.textbbox((0, 0), initial, font=font)
            text_width = right - left
            text_height = bottom - top
        except:
            text_width, text_height = draw.textsize(initial, font=font)
        
        position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2 - 10)
        
        # Draw a circle background for the initial
        circle_radius = min(size) // 2 - 20
        circle_center = (size[0] // 2, size[1] // 2)
        circle_color = "rgba(255, 255, 255, 0.3)"
        
        # Draw semi-transparent white circle
        for r in range(circle_radius, circle_radius - 5, -1):
            alpha = int(100 + (circle_radius - r) * 30)  # Increasing opacity for inner circles
            draw.ellipse((circle_center[0] - r, circle_center[1] - r, 
                         circle_center[0] + r, circle_center[1] + r), 
                         fill=(255, 255, 255, alpha))
        
        # Draw the initial
        draw.text(position, initial, fill=text_color, font=font)
        
        # Add a decorative element - small circle in corner
        small_circle_radius = min(size) // 10
        draw.ellipse((size[0] - small_circle_radius * 2, size[1] - small_circle_radius * 2,
                      size[0], size[1]), fill="#ffffff")
        
    except Exception as e:
        # Fallback to a simple circle if text drawing fails
        print(f"Error creating text avatar, using fallback: {str(e)}")
        circle_center = (size[0] // 2, size[1] // 2)
        circle_radius = min(size) // 2 - 20
        draw.ellipse((circle_center[0] - circle_radius, circle_center[1] - circle_radius,
                      circle_center[0] + circle_radius, circle_center[1] + circle_radius),
                     fill="#ffffff")
    
    # Save the image if assets directory exists
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    avatar_path = os.path.join(assets_dir, "avatar.png")
    avatar.save(avatar_path)
    
    return avatar_path

def generate_login_image_placeholder(size=(500, 400), bg_color="#f0f2f6"):
    """Generate a more appealing placeholder login image"""
    # Create a new image with a gradient background
    login_img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(login_img)
    
    # Create a business dashboard illustration
    
    # Draw main container / monitor
    monitor_width = size[0] * 0.7
    monitor_height = size[1] * 0.6
    monitor_left = (size[0] - monitor_width) / 2
    monitor_top = (size[1] - monitor_height) / 3
    
    # Draw monitor body (with gradient)
    for i in range(int(monitor_width)):
        # Create a blue gradient from left to right
        blue_val = 180 - int(120 * (i / monitor_width))
        draw.line(
            [(monitor_left + i, monitor_top), 
             (monitor_left + i, monitor_top + monitor_height)],
            fill=(52, blue_val, 219)
        )
    
    # Draw monitor frame
    draw.rectangle(
        [monitor_left, monitor_top, 
         monitor_left + monitor_width, monitor_top + monitor_height],
        outline="#2c3e50", width=3
    )
    
    # Draw monitor stand
    stand_width = monitor_width * 0.2
    stand_height = monitor_height * 0.15
    stand_left = monitor_left + (monitor_width - stand_width) / 2
    stand_top = monitor_top + monitor_height
    
    draw.rectangle(
        [stand_left, stand_top,
         stand_left + stand_width, stand_top + stand_height],
        fill="#2c3e50", outline="#2c3e50", width=2
    )
    
    # Draw stand base
    base_width = stand_width * 1.5
    base_height = stand_height * 0.3
    base_left = stand_left + (stand_width - base_width) / 2
    base_top = stand_top + stand_height
    
    draw.rectangle(
        [base_left, base_top,
         base_left + base_width, base_top + base_height],
        fill="#2c3e50", outline="#2c3e50", width=2
    )
    
    # Draw dashboard elements inside monitor
    padding = 15
    content_left = monitor_left + padding
    content_top = monitor_top + padding
    content_width = monitor_width - padding * 2
    content_height = monitor_height - padding * 2
    
    # Draw sidebar
    sidebar_width = content_width * 0.2
    draw.rectangle(
        [content_left, content_top,
         content_left + sidebar_width, content_top + content_height],
        fill="#ffffff"
    )
    
    # Draw main content area
    main_left = content_left + sidebar_width
    draw.rectangle(
        [main_left, content_top,
         content_left + content_width, content_top + content_height],
        fill="#f0f2f6"
    )
    
    # Draw sidebar menu items
    menu_items = 6
    menu_height = 20
    menu_padding = 10
    menu_start = content_top + 70
    
    # Draw sidebar avatar circle
    avatar_size = 50
    avatar_left = content_left + (sidebar_width - avatar_size) / 2
    avatar_top = content_top + 10
    
    draw.ellipse(
        [avatar_left, avatar_top,
         avatar_left + avatar_size, avatar_top + avatar_size],
        fill="#3498db"
    )
    
    # Draw menu items
    for i in range(menu_items):
        item_top = menu_start + i * (menu_height + menu_padding)
        
        # Menu item background
        item_color = "#3498db" if i == 0 else "#f5f5f5"
        draw.rectangle(
            [content_left + 10, item_top,
             content_left + sidebar_width - 10, item_top + menu_height],
            fill=item_color, radius=5
        )
    
    # Draw KPI cards in main area
    card_width = (content_width - sidebar_width - padding * 3) / 2
    card_height = (content_height - padding * 3) / 2
    
    # Top row cards
    for i in range(2):
        card_left = main_left + padding + i * (card_width + padding)
        draw.rectangle(
            [card_left, content_top + padding,
             card_left + card_width, content_top + padding + card_height],
            fill="#ffffff", radius=8
        )
        
        # Add a color bar to the card
        bar_colors = ["#3498db", "#e74c3c"]
        draw.rectangle(
            [card_left, content_top + padding,
             card_left + 5, content_top + padding + card_height],
            fill=bar_colors[i % len(bar_colors)]
        )
        
        # Add chart indicator
        if i == 0:
            # Bar chart
            bar_count = 5
            bar_width = card_width * 0.1
            bar_spacing = card_width * 0.05
            chart_top = content_top + padding + card_height * 0.5
            
            for j in range(bar_count):
                bar_height = random.randint(20, 50)
                bar_left = card_left + 20 + j * (bar_width + bar_spacing)
                
                draw.rectangle(
                    [bar_left, chart_top + 50 - bar_height,
                     bar_left + bar_width, chart_top + 50],
                    fill="#3498db"
                )
        else:
            # Line chart
            points = []
            point_count = 10
            chart_width = card_width - 40
            chart_height = 50
            chart_top = content_top + padding + card_height * 0.5
            
            for j in range(point_count):
                x = card_left + 20 + j * (chart_width / (point_count - 1))
                y = chart_top + 50 - random.randint(10, chart_height)
                points.append((x, y))
            
            for j in range(len(points) - 1):
                draw.line([points[j], points[j+1]], fill="#e74c3c", width=2)
    
    # Bottom row cards
    for i in range(2):
        card_left = main_left + padding + i * (card_width + padding)
        card_top = content_top + padding * 2 + card_height
        draw.rectangle(
            [card_left, card_top,
             card_left + card_width, card_top + card_height],
            fill="#ffffff", radius=8
        )
        
        # Add a color bar to the card
        bar_colors = ["#9b59b6", "#f39c12"]
        draw.rectangle(
            [card_left, card_top,
             card_left + 5, card_top + card_height],
            fill=bar_colors[i % len(bar_colors)]
        )
        
        # Add chart indicators
        if i == 0:
            # Pie chart
            center_x = card_left + card_width * 0.5
            center_y = card_top + card_height * 0.5
            radius = min(card_width, card_height) * 0.3
            
            # Draw pie segments
            segments = [(0, 90, "#9b59b6"), (90, 210, "#3498db"), (210, 360, "#e74c3c")]
            for start, end, color in segments:
                draw.pieslice(
                    [center_x - radius, center_y - radius,
                     center_x + radius, center_y + radius],
                    start, end, fill=color
                )
        else:
            # Table
            rows = 4
            cols = 2
            cell_width = card_width * 0.8 / cols
            cell_height = card_height * 0.6 / rows
            table_left = card_left + card_width * 0.1
            table_top = card_top + card_height * 0.2
            
            for r in range(rows):
                for c in range(cols):
                    cell_left = table_left + c * cell_width
                    cell_top = table_top + r * cell_height
                    
                    draw.rectangle(
                        [cell_left, cell_top,
                         cell_left + cell_width, cell_top + cell_height],
                        outline="#e0e0e0"
                    )
    
    # Save the image
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    login_path = os.path.join(assets_dir, "login_image.png")
    login_img.save(login_path)
    
    return login_path

def get_base64_encoded_image(image_path):
    """Convert an image to base64 encoding for embedding in HTML/CSS"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def ensure_images_exist():
    """Make sure all necessary images exist"""
    if not os.path.exists("assets/avatar.png"):
        generate_avatar_placeholder()
    
    if not os.path.exists("assets/login_image.png"):
        generate_login_image_placeholder() 