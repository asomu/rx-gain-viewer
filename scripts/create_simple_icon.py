"""
Simple icon generator for RF Converter
Creates a grid/table style icon matching the PyQt6 SP_FileDialogDetailedView theme
"""

from PIL import Image, ImageDraw

def create_grid_icon(size=256):
    """Create a simple grid/table icon"""
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors - using Windows system blue theme
    bg_color = (0, 120, 212, 255)  # Windows blue
    grid_color = (255, 255, 255, 255)  # White

    # Draw background rounded rectangle
    margin = size // 8
    draw.rounded_rectangle(
        [(margin, margin), (size - margin, size - margin)],
        radius=size // 16,
        fill=bg_color
    )

    # Draw grid lines (3x3 grid for simplicity)
    line_width = max(2, size // 64)
    inner_margin = margin + size // 16
    grid_size = size - 2 * inner_margin

    # Horizontal lines
    for i in range(1, 3):
        y = inner_margin + (grid_size // 3) * i
        draw.line(
            [(inner_margin, y), (size - inner_margin, y)],
            fill=grid_color,
            width=line_width
        )

    # Vertical lines
    for i in range(1, 3):
        x = inner_margin + (grid_size // 3) * i
        draw.line(
            [(x, inner_margin), (x, size - inner_margin)],
            fill=grid_color,
            width=line_width
        )

    # Draw border
    border_width = max(3, size // 48)
    draw.rounded_rectangle(
        [(inner_margin, inner_margin), (size - inner_margin, size - inner_margin)],
        radius=size // 32,
        outline=grid_color,
        width=border_width
    )

    return img

def main():
    """Generate icon in multiple sizes and save as .ico"""
    print("Generating RF Converter icon...")

    # ICO format supports multiple sizes
    sizes = [256, 128, 64, 48, 32, 16]
    images = []

    for size in sizes:
        img = create_grid_icon(size)
        images.append(img)
        print(f"  ✓ Created {size}x{size} icon")

    # Save as ICO file (multi-size)
    output_path = 'rf_converter/icon.ico'
    images[0].save(
        output_path,
        format='ICO',
        sizes=[(s, s) for s in sizes],
        append_images=images[1:]
    )

    print(f"\n✓ Icon saved to: {output_path}")
    print(f"  Contains {len(sizes)} sizes: {', '.join(f'{s}x{s}' for s in sizes)}")

if __name__ == '__main__':
    main()
