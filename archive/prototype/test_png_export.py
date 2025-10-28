"""
Test PNG export functionality with kaleido
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from prototype.parsers.csv_parser import CsvParser
from prototype.utils.chart_generator import ChartGenerator


def test_png_export():
    """Test PNG image export"""

    print("="*70)
    print("PNG Export Test")
    print("="*70)

    # Load CSV and generate chart
    csv_path = Path(__file__).parent.parent / "data" / "Bellagio_POC_Rx.csv"
    parser = CsvParser(str(csv_path))
    parser.load_consolidated()

    print("\n[1/3] Generating B41 grid chart...")
    grid_data = parser.get_grid_data('B41', 'G0_H', 'ANT1')

    fig = ChartGenerator.create_compact_grid(
        grid_data=grid_data,
        band='B41',
        lna_gain_state='G0_H',
        input_port='ANT1',
        compact_size=(250, 150)
    )

    # Export to PNG
    output_png = Path(__file__).parent / "test_export_B41_G0_H_ANT1.png"

    print(f"\n[2/3] Exporting to PNG: {output_png.name}...")

    try:
        ChartGenerator.export_to_image(
            fig,
            str(output_png),
            width=1200,
            height=800
        )
        print(f"[OK] PNG exported successfully!")
        print(f"  File: {output_png}")
        print(f"  Size: {output_png.stat().st_size / 1024:.1f} KB")

    except Exception as e:
        print(f"[ERROR] PNG export failed: {e}")
        return False

    # Test with different size
    output_large = Path(__file__).parent / "test_export_B41_G0_H_ANT1_large.png"

    print(f"\n[3/3] Exporting large version: {output_large.name}...")

    try:
        ChartGenerator.export_to_image(
            fig,
            str(output_large),
            width=1600,
            height=1000
        )
        print(f"[OK] Large PNG exported!")
        print(f"  File: {output_large}")
        print(f"  Size: {output_large.stat().st_size / 1024:.1f} KB")

    except Exception as e:
        print(f"[ERROR] Large PNG export failed: {e}")
        return False

    print("\n" + "="*70)
    print("[SUCCESS] PNG export working correctly!")
    print("="*70)

    return True


if __name__ == "__main__":
    test_png_export()
