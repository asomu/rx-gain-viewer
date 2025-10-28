"""
Test script for updated CSV parser with consolidated format support
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from prototype.parsers.csv_parser import CsvParser


def test_consolidated_csv():
    """Test consolidated CSV format parsing"""

    print("=" * 70)
    print("Testing Consolidated CSV Parser")
    print("=" * 70)

    csv_path = Path(__file__).parent.parent / "data" / "Bellagio_POC_Rx.csv"

    if not csv_path.exists():
        print(f"[ERROR] CSV file not found: {csv_path}")
        return False

    # Initialize parser
    parser = CsvParser(str(csv_path))
    print(f"\n[1/6] Parser initialized: {parser}")

    # Load consolidated format
    print("\n[2/6] Loading consolidated format...")
    try:
        parser.load_consolidated()
        print(f"[OK] Loaded successfully: {parser}")
    except Exception as e:
        print(f"[ERROR] Failed to load: {e}")
        return False

    # Get available bands
    print("\n[3/6] Getting available bands...")
    try:
        bands = parser.get_available_bands()
        print(f"[OK] Found {len(bands)} bands:")
        print(f"     {', '.join(bands[:10])}...")
    except Exception as e:
        print(f"[ERROR] Failed to get bands: {e}")
        return False

    # Get available paths for B1 band
    print("\n[4/6] Getting Active RF Paths for B1 band...")
    try:
        paths = parser.get_available_paths(band='B1')
        print(f"[OK] Found {len(paths)} Active RF Paths for B1:")
        for path_info in paths:
            print(f"     {path_info['active_rf_path']}: {path_info['port_label']}")
    except Exception as e:
        print(f"[ERROR] Failed to get paths: {e}")
        return False

    # Get data for B1, ANT1→RXOUT1 (S0706)
    print("\n[5/6] Extracting B1 band, S0706 (ANT1→RXOUT1) data...")
    try:
        data = parser.get_data_by_filter(band='B1', active_rf_path='S0706')
        print(f"[OK] Extracted {data['count']} data points")
        print(f"     Band: {data['band']}")
        print(f"     Active RF Path: {data['active_rf_path']}")
        print(f"     Ports: {data['input_port']} → {data['output_port']}")
        print(f"     Frequency range: {data['frequency'].min():.0f} - {data['frequency'].max():.0f} MHz")
        print(f"     Gain range: {data['gain_db'].min():.3f} - {data['gain_db'].max():.3f} dB")
    except Exception as e:
        print(f"[ERROR] Failed to extract data: {e}")
        return False

    # Get frequency range for B1
    print("\n[6/6] Getting frequency range for B1 band...")
    try:
        freq_min, freq_max = parser.get_band_frequency_range('B1')
        print(f"[OK] B1 frequency range: {freq_min:.0f} - {freq_max:.0f} MHz")
    except Exception as e:
        print(f"[ERROR] Failed to get frequency range: {e}")
        return False

    print("\n" + "=" * 70)
    print("[SUCCESS] All tests passed!")
    print("=" * 70)
    return True


def test_auto_detect():
    """Test auto-detection of CSV format"""

    print("\n" + "=" * 70)
    print("Testing Auto-Detection")
    print("=" * 70)

    csv_path = Path(__file__).parent.parent / "data" / "Bellagio_POC_Rx.csv"

    parser = CsvParser(str(csv_path))
    print(f"\nParser initialized: {parser}")

    print("\nAuto-detecting format...")
    try:
        parser.auto_detect_and_load()
        print(f"[OK] Auto-detected format: {parser.format_type}")
        print(f"     {parser}")
    except Exception as e:
        print(f"[ERROR] Auto-detection failed: {e}")
        return False

    print("\n" + "=" * 70)
    print("[SUCCESS] Auto-detection test passed!")
    print("=" * 70)
    return True


def test_multiple_bands():
    """Test data extraction for multiple bands"""

    print("\n" + "=" * 70)
    print("Testing Multiple Bands Extraction")
    print("=" * 70)

    csv_path = Path(__file__).parent.parent / "data" / "Bellagio_POC_Rx.csv"
    parser = CsvParser(str(csv_path))
    parser.load_consolidated()

    test_bands = ['B1', 'B3', 'B7', 'B41']
    print(f"\nTesting bands: {', '.join(test_bands)}")

    for band in test_bands:
        print(f"\n--- {band} ---")
        try:
            # Get frequency range
            freq_min, freq_max = parser.get_band_frequency_range(band)
            print(f"  Frequency: {freq_min:.0f} - {freq_max:.0f} MHz")

            # Get available paths
            paths = parser.get_available_paths(band=band)
            print(f"  Available paths: {len(paths)}")

            # Get data for first path
            if paths:
                first_path = paths[0]
                data = parser.get_data_by_filter(
                    band=band,
                    active_rf_path=first_path['active_rf_path']
                )
                print(f"  Sample data ({first_path['port_label']}): {data['count']} points, "
                      f"Gain {data['gain_db'].min():.2f} - {data['gain_db'].max():.2f} dB")
        except Exception as e:
            print(f"  [ERROR] {e}")

    print("\n" + "=" * 70)
    print("[SUCCESS] Multiple bands test completed!")
    print("=" * 70)
    return True


if __name__ == "__main__":
    print("\n" + "="*70)
    print("CSV Parser Test Suite")
    print("="*70)

    # Run all tests
    all_passed = True

    all_passed &= test_consolidated_csv()
    all_passed &= test_auto_detect()
    all_passed &= test_multiple_bands()

    print("\n" + "="*70)
    if all_passed:
        print("[FINAL RESULT] All tests PASSED ✓")
    else:
        print("[FINAL RESULT] Some tests FAILED ✗")
    print("="*70)
