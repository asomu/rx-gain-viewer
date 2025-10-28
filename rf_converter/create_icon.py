"""
Create a simple RF Converter icon
Uses PIL to generate a 256x256 icon with RF wave symbol
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_rf_icon():
    """Create RF Converter icon"""

    # Create 256x256 image with gradient background
    size = 256
    img = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(img)

    # Gradient background (blue to light blue)
    for y in range(size):
        color_value = int(220 - (y / size) * 100)  # 220 to 120
        draw.rectangle([(0, y), (size, y+1)], fill=(30, 120, color_value))

    # Draw RF wave symbol (sine wave)
    wave_points = []
    amplitude = 40
    frequency = 3
    y_offset = size // 2

    for x in range(0, size):
        import math
        y = y_offset + amplitude * math.sin(2 * math.pi * frequency * x / size)
        wave_points.append((x, int(y)))

    # Draw the wave (thicker line)
    for i in range(len(wave_points) - 1):
        draw.line([wave_points[i], wave_points[i+1]], fill=(255, 255, 255), width=8)

    # Draw border circle
    draw.ellipse([20, 20, size-20, size-20], outline=(255, 255, 255), width=6)

    # Add "RF" text
    try:
        # Try to use a bold font
        font_size = 80
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()

    # Draw "RF" text in center
    text = "RF"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2 - 10

    # Draw text shadow
    draw.text((text_x+3, text_y+3), text, fill=(0, 0, 0, 128), font=font)
    # Draw main text
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)

    # Save as PNG and ICO
    output_dir = os.path.dirname(os.path.abspath(__file__))

    # Save PNG (for PyQt6)
    png_path = os.path.join(output_dir, 'icon.png')
    img.save(png_path, 'PNG')
    print(f"✅ Created PNG icon: {png_path}")

    # Save ICO (for Windows)
    ico_path = os.path.join(output_dir, 'icon.ico')
    img.save(ico_path, 'ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print(f"✅ Created ICO icon: {ico_path}")

    # Create smaller version for taskbar
    img_small = img.resize((64, 64), Image.Resampling.LANCZOS)
    small_path = os.path.join(output_dir, 'icon_small.png')
    img_small.save(small_path, 'PNG')
    print(f"✅ Created small icon: {small_path}")

    return png_path, ico_path

if __name__ == '__main__':
    try:
        png, ico = create_rf_icon()
        print("\n🎉 Icon creation successful!")
        print(f"   PNG: {png}")
        print(f"   ICO: {ico}")
    except ImportError:
        print("❌ PIL (Pillow) not installed.")
        print("   Install with: pip install Pillow")
    except Exception as e:
        print(f"❌ Error: {e}")
