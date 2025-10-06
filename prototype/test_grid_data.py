"""
Test script for CSV grid data extraction
Tests CA combinations, LNA gain states, and grid data structure
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from prototype.parsers.csv_parser import CsvParser


def test_ca_combinations():
    """Test CA combination extraction"""

    print("="*70)
    print("Test: CA Combinations Extraction")
    print("="*70)

    csv_path = Path(__file__).parent.parent / "data" / "Bellagio_POC_Rx.csv"
    parser = CsvParser(str(csv_path))
    parser.load_consolidated()

    # Test B1 band
    print("\n[1] B1 Band CA Combinations:")
    b1_ca = parser.get_ca_combinations('B1')
    for i, ca in enumerate(b1_ca, 1):
        print(f"  {i}. {ca}")

    # Test B41 band
    print("\n[2] B41 Band CA Combinations:")
    b41_ca = parser.get_ca_combinations('B41')
    for i, ca in enumerate(b41_ca, 1):
        print(f"  {i}. {ca}")

    # Test all bands
    print("\n[3] All CA Combinations (across all bands):")
    all_ca = parser.get_ca_combinations()
    print(f"  Total: {len(all_ca)} unique CA combinations")
    print(f"  Sample: {', '.join(all_ca[:10])}")

    return True


def test_lna_gain_states():
    """Test LNA gain state extraction"""

    print("\n" + "="*70)
    print("Test: LNA Gain States Extraction")
    print("="*70)

    csv_path = Path(__file__).parent.parent / "data" / "Bellagio_POC_Rx.csv"
    parser = CsvParser(str(csv_path))
    parser.load_consolidated()

    # Test B1 band
    print("\n[1] B1 Band LNA Gain States:")
    b1_lna = parser.get_lna_gain_states('B1')
    for i, lna in enumerate(b1_lna, 1):
        print(f"  {i}. {lna}")

    # Test all bands
    print("\n[2] All LNA Gain States:")
    all_lna = parser.get_lna_gain_states()
    for i, lna in enumerate(all_lna, 1):
        print(f"  {i}. {lna}")

    return True


def test_input_ports():
    """Test input port extraction"""

    print("\n" + "="*70)
    print("Test: Input Ports Extraction")
    print("="*70)

    csv_path = Path(__file__).parent.parent / "data" / "Bellagio_POC_Rx.csv"
    parser = CsvParser(str(csv_path))
    parser.load_consolidated()

    # Test all input ports
    print("\n[1] All Input Ports:")
    ports = parser.get_input_ports()
    for i, port in enumerate(ports, 1):
        print(f"  {i}. {port}")

    return True


def test_grid_data():
    """Test complete grid data extraction"""

    print("\n" + "="*70)
    print("Test: Grid Data Extraction")
    print("="*70)

    csv_path = Path(__file__).parent.parent / "data" / "Bellagio_POC_Rx.csv"
    parser = CsvParser(str(csv_path))
    parser.load_consolidated()

    # Test B41, G0_H, ANT1 (like the sample image)
    print("\n[1] Extracting Grid Data: B41, G0_H, ANT1")
    grid_data = parser.get_grid_data(
        band='B41',
        lna_gain_state='G0_H',
        input_port='ANT1'
    )

    print(f"\n  CA Combinations found: {len(grid_data)}")
    for ca_combo in grid_data.keys():
        print(f"    - {ca_combo}")

    print("\n  Grid Structure (4 rows x N columns):")
    print(f"  {'':12} ", end='')
    for ca_combo in grid_data.keys():
        print(f"{ca_combo:20} ", end='')
    print()
    print("  " + "-"*70)

    for rxout in ['RXOUT1', 'RXOUT2', 'RXOUT3', 'RXOUT4']:
        print(f"  {rxout:12} ", end='')
        for ca_combo in grid_data.keys():
            count = grid_data[ca_combo][rxout]['count']
            print(f"{count:4} points         ", end='')
        print()

    # Show sample data for first cell
    print("\n[2] Sample Data (B41, 1_3_40_32+41, RXOUT1):")
    first_ca = list(grid_data.keys())[0]
    sample_data = grid_data[first_ca]['RXOUT1']

    if sample_data['count'] > 0:
        freq = sample_data['frequency']
        gain = sample_data['gain_db']
        print(f"  Data points: {sample_data['count']}")
        print(f"  Frequency range: {freq.min():.1f} - {freq.max():.1f} MHz")
        print(f"  Gain range: {gain.min():.2f} - {gain.max():.2f} dB")
        print(f"  First 5 points:")
        for i in range(min(5, len(freq))):
            print(f"    {freq[i]:.1f} MHz -> {gain[i]:.2f} dB")
    else:
        print("  No data found")

    return True


def test_all_combinations_count():
    """Calculate total number of possible grid combinations"""

    print("\n" + "="*70)
    print("Test: Total Grid Combinations Count")
    print("="*70)

    csv_path = Path(__file__).parent.parent / "data" / "Bellagio_POC_Rx.csv"
    parser = CsvParser(str(csv_path))
    parser.load_consolidated()

    bands = parser.get_available_bands()
    lna_states = parser.get_lna_gain_states()
    input_ports = parser.get_input_ports()

    print(f"\n  Total Bands: {len(bands)}")
    print(f"  Total LNA Gain States: {len(lna_states)}")
    print(f"  Total Input Ports: {len(input_ports)}")

    total_grids = len(bands) * len(lna_states) * len(input_ports)

    print(f"\n  Total Possible Grid Pages: {total_grids}")
    print(f"  (Band x LNA x Port = {len(bands)} x {len(lna_states)} x {len(input_ports)})")

    print(f"\n  If exported as PDF:")
    print(f"    - {total_grids} pages")
    print(f"    - {total_grids} PNG/JPG images")
    print(f"    - Estimated file size: ~{total_grids * 0.2:.1f} MB (200KB per image)")

    return True


if __name__ == "__main__":
    print("\n" + "="*70)
    print("CSV Grid Data Test Suite")
    print("="*70)

    all_passed = True

    all_passed &= test_ca_combinations()
    all_passed &= test_lna_gain_states()
    all_passed &= test_input_ports()
    all_passed &= test_grid_data()
    all_passed &= test_all_combinations_count()

    print("\n" + "="*70)
    if all_passed:
        print("[SUCCESS] All tests passed!")
    else:
        print("[FAILED] Some tests failed")
    print("="*70)
