"""Test filename parsing for special cases"""

import re
from core.parsers.base_parser import BaseMeasurementParser
from core.parsers.rx_parser import RxGainParser


def test_filename_parsing():
    """Test various filename formats"""

    parser = RxGainParser()

    test_cases = [
        "X_ANT1_B1@1_(G0H).s2p",
        "X_ANT1_B1[B7]@2_(G0H).s2p",
        "X_ANT1_B41[NA]@3_(G0).s2p",  # Problem case
        "X_ANT1_B3[B7]@1_(G0L).s2p",
        "X_ANT2_B41@2_(G0H).s2p",
    ]

    print("=" * 80)
    print("Filename Parsing Test")
    print("=" * 80)

    for filename in test_cases:
        print(f"\n📄 Filename: {filename}")
        metadata = parser.parse_filename(filename)

        print(f"  ✓ port_in:    {metadata.get('port_in', 'NOT FOUND')}")
        print(f"  ✓ band:       {metadata.get('band', 'NOT FOUND')}")
        print(f"  ✓ ca_config:  {metadata.get('ca_config', 'NOT FOUND')}")
        print(f"  ✓ port_out:   {metadata.get('port_out', 'NOT FOUND')}")
        print(f"  ✓ lna_state:  {metadata.get('lna_state', 'NOT FOUND')}")

        # Check if B41[NA] pattern works
        if "B41[NA]" in filename:
            print("\n  🔍 Special Case: B41[NA]")
            # Test regex pattern directly
            band_pattern = r'(B\d+(?:\[B\d+\])?)\@?(\d+)?'
            match = re.search(band_pattern, filename)
            if match:
                print(f"     Current regex matched: {match.group(1)}")
            else:
                print(f"     ❌ Current regex FAILED")

            # Test improved pattern
            improved_pattern = r'(B\d+(?:\[[^\]]+\])?)\@?(\d+)?'
            match2 = re.search(improved_pattern, filename)
            if match2:
                print(f"     ✅ Improved regex matched: {match2.group(1)}")


if __name__ == '__main__':
    test_filename_parsing()
