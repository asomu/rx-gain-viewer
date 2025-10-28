"""
Test script for compact grid chart generation
Generates sample grid like the uploaded image
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from prototype.parsers.csv_parser import CsvParser
from prototype.utils.chart_generator import ChartGenerator


def test_b41_grid():
    """
    Generate B41 grid chart (like the sample image)
    Band: B41, LNA: G0_H, Input: ANT1
    """

    print("="*70)
    print("Test: Generate B41 Compact Grid Chart")
    print("="*70)

    # Load CSV
    csv_path = Path(__file__).parent.parent / "data" / "Bellagio_POC_Rx.csv"
    parser = CsvParser(str(csv_path))
    parser.load_consolidated()

    print("\n[1/4] CSV loaded successfully")
    print(f"  {parser}")

    # Get grid data
    print("\n[2/4] Extracting grid data for B41, G0_H, ANT1...")
    grid_data = parser.get_grid_data(
        band='B41',
        lna_gain_state='G0_H',
        input_port='ANT1'
    )

    print(f"  CA combinations: {len(grid_data)}")
    for ca in grid_data.keys():
        print(f"    - {ca}")

    # Generate chart
    print("\n[3/4] Generating compact grid chart...")
    fig = ChartGenerator.create_compact_grid(
        grid_data=grid_data,
        band='B41',
        lna_gain_state='G0_H',
        input_port='ANT1',
        compact_size=(250, 150)  # Slightly larger for better visibility
    )

    # Save to HTML
    output_path = Path(__file__).parent / "demo_compact_grid_B41.html"
    print(f"\n[4/4] Saving chart to {output_path.name}...")
    ChartGenerator.export_to_html(fig, str(output_path), auto_open=False)

    print(f"\n[OK] Chart saved successfully!")
    print(f"  File: {output_path}")
    print(f"  Grid size: 4 rows x {len(grid_data)} columns")

    return True


def test_b1_grid():
    """
    Generate B1 grid chart for comparison
    Band: B1, LNA: G0_H, Input: ANT1
    """

    print("\n" + "="*70)
    print("Test: Generate B1 Compact Grid Chart")
    print("="*70)

    # Load CSV
    csv_path = Path(__file__).parent.parent / "data" / "Bellagio_POC_Rx.csv"
    parser = CsvParser(str(csv_path))
    parser.load_consolidated()

    # Get grid data
    print("\n[1/3] Extracting grid data for B1, G0_H, ANT1...")
    grid_data = parser.get_grid_data(
        band='B1',
        lna_gain_state='G0_H',
        input_port='ANT1'
    )

    print(f"  CA combinations: {len(grid_data)}")
    for ca in grid_data.keys():
        print(f"    - {ca}")

    # Generate chart
    print("\n[2/3] Generating compact grid chart...")
    fig = ChartGenerator.create_compact_grid(
        grid_data=grid_data,
        band='B1',
        lna_gain_state='G0_H',
        input_port='ANT1',
        compact_size=(250, 150)
    )

    # Save to HTML
    output_path = Path(__file__).parent / "demo_compact_grid_B1.html"
    print(f"\n[3/3] Saving chart to {output_path.name}...")
    ChartGenerator.export_to_html(fig, str(output_path), auto_open=False)

    print(f"\n[OK] Chart saved successfully!")
    print(f"  File: {output_path}")

    return True


def test_multiple_lna_states():
    """
    Generate grids for different LNA gain states (B41, ANT1)
    """

    print("\n" + "="*70)
    print("Test: Generate Multiple LNA Gain State Grids")
    print("="*70)

    csv_path = Path(__file__).parent.parent / "data" / "Bellagio_POC_Rx.csv"
    parser = CsvParser(str(csv_path))
    parser.load_consolidated()

    # Get available LNA states for B41
    lna_states = parser.get_lna_gain_states('B41')
    print(f"\nLNA Gain States for B41: {', '.join(lna_states)}")

    # Generate first 3 LNA states
    print(f"\nGenerating grids for first 3 LNA states...")

    for lna_state in lna_states[:3]:
        print(f"\n  Processing {lna_state}...")

        grid_data = parser.get_grid_data(
            band='B41',
            lna_gain_state=lna_state,
            input_port='ANT1'
        )

        fig = ChartGenerator.create_compact_grid(
            grid_data=grid_data,
            band='B41',
            lna_gain_state=lna_state,
            input_port='ANT1',
            compact_size=(250, 150)
        )

        output_path = Path(__file__).parent / f"demo_compact_grid_B41_{lna_state}_ANT1.html"
        ChartGenerator.export_to_html(fig, str(output_path), auto_open=False)

        print(f"    Saved: {output_path.name}")

    print(f"\n[OK] Multiple LNA state grids generated!")

    return True


if __name__ == "__main__":
    print("\n" + "="*70)
    print("Compact Grid Chart Generation Test Suite")
    print("="*70)

    all_passed = True

    all_passed &= test_b41_grid()
    all_passed &= test_b1_grid()
    all_passed &= test_multiple_lna_states()

    print("\n" + "="*70)
    if all_passed:
        print("[SUCCESS] All charts generated successfully!")
        print("\nGenerated files:")
        print("  - demo_compact_grid_B41.html")
        print("  - demo_compact_grid_B1.html")
        print("  - demo_compact_grid_B41_G0_H_ANT1.html")
        print("  - demo_compact_grid_B41_G0_L_ANT1.html")
        print("  - demo_compact_grid_B41_G1_ANT1.html")
    else:
        print("[FAILED] Some tests failed")
    print("="*70)
