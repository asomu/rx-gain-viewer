"""
Test high quality PDF export
Compare low quality vs high quality
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from prototype.parsers.csv_parser import CsvParser
from prototype.utils.chart_generator import ChartGenerator
from prototype.utils.pdf_exporter import PDFExporter


def test_high_quality():
    """Generate high quality PNG and PDF"""

    print("="*70)
    print("High Quality PDF Test")
    print("="*70)

    csv_path = Path(__file__).parent.parent / "data" / "Bellagio_POC_Rx.csv"
    parser = CsvParser(str(csv_path))
    parser.load_consolidated()

    output_dir = Path(__file__).parent / "high_quality_test"
    output_dir.mkdir(exist_ok=True)

    # Generate high resolution PNG
    print("\n[1/3] Generating HIGH RESOLUTION PNG (1920x1200)...")

    grid_data = parser.get_grid_data('B41', 'G0_H', 'ANT1')
    fig = ChartGenerator.create_compact_grid(
        grid_data=grid_data,
        band='B41',
        lna_gain_state='G0_H',
        input_port='ANT1',
        compact_size=(300, 180)  # Larger chart size
    )

    png_high = output_dir / "B41_G0_H_ANT1_HIGH_RES.png"

    ChartGenerator.export_to_image(
        fig,
        str(png_high),
        width=1920,  # Full HD width
        height=1200  # Tall for 4 rows
    )

    print(f"[OK] High res PNG created: {png_high.name}")
    print(f"  Size: {png_high.stat().st_size / 1024:.1f} KB")

    # Generate 3 high res PNGs
    print("\n[2/3] Generating 3 high resolution PNGs...")

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
            compact_size=(300, 180)
        )

        filename = f"{band}_{lna}_{port}_HIGH.png"
        filepath = output_dir / filename

        ChartGenerator.export_to_image(
            fig,
            str(filepath),
            width=1920,
            height=1200
        )

        image_paths.append(filepath)
        print(f"  {filename}: {filepath.stat().st_size / 1024:.1f} KB")

    # Create HIGH QUALITY PDF (300 DPI, no resize)
    print("\n[3/3] Creating HIGH QUALITY PDF (300 DPI, original size)...")

    pdf_high = output_dir / "B41_HIGH_QUALITY.pdf"

    PDFExporter.images_to_pdf(
        image_paths=image_paths,
        output_pdf=pdf_high,
        title="B41 Analysis - High Quality",
        page_size=None,  # Keep original size!
        high_quality=True  # 300 DPI
    )

    print(f"\n[OK] High quality PDF created!")
    print(f"  File: {pdf_high}")
    print(f"  Size: {pdf_high.stat().st_size / (1024*1024):.2f} MB")

    print("\n" + "="*70)
    print("High Quality Test Complete!")
    print("="*70)
    print(f"\nCompare these files:")
    print(f"  High Res PNG: {png_high}")
    print(f"  High Quality PDF: {pdf_high}")
    print(f"\n  Open them and check the quality!")

    return True


if __name__ == "__main__":
    test_high_quality()
