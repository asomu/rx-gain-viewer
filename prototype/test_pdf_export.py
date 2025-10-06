"""
Test PDF export functionality
First generate a few PNG images, then combine into PDF
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from prototype.parsers.csv_parser import CsvParser
from prototype.utils.chart_generator import ChartGenerator
from prototype.utils.pdf_exporter import PDFExporter


def test_pdf_creation():
    """Test creating PDF from multiple PNG images"""

    print("="*70)
    print("PDF Export Test")
    print("="*70)

    # Step 1: Generate a few PNG images
    print("\n[Step 1/3] Generating sample PNG images...")

    csv_path = Path(__file__).parent.parent / "data" / "Bellagio_POC_Rx.csv"
    parser = CsvParser(str(csv_path))
    parser.load_consolidated()

    output_dir = Path(__file__).parent / "test_pdf_images"
    output_dir.mkdir(exist_ok=True)

    # Generate 3 PNG images: B41 with different LNA states
    test_configs = [
        ('B41', 'G0_H', 'ANT1'),
        ('B41', 'G0_L', 'ANT1'),
        ('B41', 'G1', 'ANT1'),
    ]

    image_paths = []

    for band, lna, port in test_configs:
        grid_data = parser.get_grid_data(band, lna, port)

        fig = ChartGenerator.create_compact_grid(
            grid_data=grid_data,
            band=band,
            lna_gain_state=lna,
            input_port=port,
            compact_size=(250, 150)
        )

        filename = f"{band}_{lna}_{port}.png"
        filepath = output_dir / filename

        ChartGenerator.export_to_image(fig, str(filepath), width=1200, height=800)

        image_paths.append(filepath)
        print(f"  Generated: {filename}")

    # Step 2: Create PDF from images
    print(f"\n[Step 2/3] Creating PDF from {len(image_paths)} images...")

    output_pdf = Path(__file__).parent / "test_report.pdf"

    try:
        PDFExporter.images_to_pdf(
            image_paths=image_paths,
            output_pdf=output_pdf,
            title="B41 Band Analysis Report - Sample"
        )

        print(f"\n[OK] PDF created successfully!")
        print(f"  File: {output_pdf}")
        print(f"  Size: {output_pdf.stat().st_size / (1024*1024):.2f} MB")

    except Exception as e:
        print(f"[ERROR] PDF creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Step 3: Test directory-based PDF creation
    print(f"\n[Step 3/3] Creating PDF from directory...")

    output_pdf2 = Path(__file__).parent / "test_report_from_dir.pdf"

    try:
        PDFExporter.create_report_from_directory(
            image_dir=output_dir,
            output_pdf=output_pdf2,
            pattern="*.png"
        )

        print(f"\n[OK] Directory-based PDF created!")

    except Exception as e:
        print(f"[ERROR] Directory PDF creation failed: {e}")
        return False

    print("\n" + "="*70)
    print("[SUCCESS] PDF export working correctly!")
    print("="*70)
    print(f"\nGenerated files:")
    print(f"  - {output_pdf}")
    print(f"  - {output_pdf2}")

    return True


if __name__ == "__main__":
    test_pdf_creation()
