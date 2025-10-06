"""
Generate sample grids for testing
Only generates B1 and B41 bands (42 grids total)
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

from prototype.parsers.csv_parser import CsvParser
from prototype.utils.chart_generator import ChartGenerator


def generate_sample_grids():
    """Generate sample grids for B1 and B41 bands"""

    output_dir = Path(__file__).parent / "sample_grids"
    output_dir.mkdir(exist_ok=True)

    print("="*70)
    print("Sample Grid Generation (B1 and B41 only)")
    print("="*70)

    # Load CSV
    csv_path = Path(__file__).parent.parent / "data" / "Bellagio_POC_Rx.csv"
    parser = CsvParser(str(csv_path))
    parser.load_consolidated()

    print(f"\n[OK] CSV loaded")

    # Sample bands
    sample_bands = ['B1', 'B41']
    lna_states = parser.get_lna_gain_states()
    input_ports = parser.get_input_ports()

    total = len(sample_bands) * len(lna_states) * len(input_ports)

    print(f"\nGenerating {total} grids:")
    print(f"  Bands: {', '.join(sample_bands)}")
    print(f"  LNA States: {', '.join(lna_states)}")
    print(f"  Input Ports: {', '.join(input_ports)}")

    start_time = time.time()
    generated = 0

    for band in sample_bands:
        print(f"\n[{band}]")
        for lna in lna_states:
            for port in input_ports:
                filename = f"{band}_{lna}_{port}.html"
                filepath = output_dir / filename

                try:
                    grid_data = parser.get_grid_data(band, lna, port)

                    fig = ChartGenerator.create_compact_grid(
                        grid_data=grid_data,
                        band=band,
                        lna_gain_state=lna,
                        input_port=port,
                        compact_size=(250, 150)
                    )

                    ChartGenerator.export_to_html(fig, str(filepath), auto_open=False)

                    generated += 1
                    print(f"  [{generated:2}/{total}] {filename}")

                except Exception as e:
                    print(f"  [ERROR] {filename}: {e}")

    elapsed = time.time() - start_time

    print(f"\n{'='*70}")
    print(f"[OK] Generated {generated} grids in {elapsed:.1f} seconds")
    print(f"  Output: {output_dir.absolute()}")
    print(f"  Average: {elapsed/generated:.2f} sec/file")
    print(f"{'='*70}")


if __name__ == "__main__":
    generate_sample_grids()
