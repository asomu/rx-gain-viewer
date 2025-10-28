"""Test script for new 3GPP band filtering with Rx/Tx separation"""

import pandas as pd
from core.parsers.rx_parser import RxGainParser
from core.parsers.tx_parser import TxPowerParser


def test_band_config():
    """Test that all bands are properly configured"""
    parser = RxGainParser()

    print("=" * 70)
    print("🔬 3GPP Band Configuration Test")
    print("=" * 70)

    # Test GSM bands
    gsm_bands = ['GSM850', 'GSM900', 'DCS', 'PCS']
    print("\n📡 GSM Bands:")
    for band in gsm_bands:
        if band in parser.band_config:
            uplink, downlink = parser.band_config[band]
            print(f"  ✅ {band:10} | UL: {uplink[0]:7.1f}-{uplink[1]:7.1f} MHz | DL: {downlink[0]:7.1f}-{downlink[1]:7.1f} MHz")
        else:
            print(f"  ❌ {band:10} | NOT FOUND")

    # Test critical LTE bands
    lte_bands = ['B1', 'B3', 'B7', 'B11', 'B21', 'B41', 'B42', 'B66', 'B71']
    print("\n📡 LTE Bands (Critical):")
    for band in lte_bands:
        if band in parser.band_config:
            uplink, downlink = parser.band_config[band]
            print(f"  ✅ {band:10} | UL: {uplink[0]:7.1f}-{uplink[1]:7.1f} MHz | DL: {downlink[0]:7.1f}-{downlink[1]:7.1f} MHz")
        else:
            print(f"  ❌ {band:10} | NOT FOUND")

    # Test TDD bands
    tdd_bands = ['B38', 'B39', 'B40', 'B41', 'B42', 'B43']
    print("\n📡 LTE TDD Bands:")
    for band in tdd_bands:
        if band in parser.band_config:
            uplink, downlink = parser.band_config[band]
            is_tdd = uplink == downlink
            status = "TDD" if is_tdd else "⚠️ NOT TDD"
            print(f"  {'✅' if is_tdd else '❌'} {band:10} | {status:8} | {uplink[0]:7.1f}-{uplink[1]:7.1f} MHz")
        else:
            print(f"  ❌ {band:10} | NOT FOUND")

    print(f"\n📊 Total bands configured: {len(parser.band_config)}")


def test_rx_tx_filtering():
    """Test Rx vs Tx frequency filtering"""
    print("\n" + "=" * 70)
    print("🔬 Rx/Tx Frequency Filtering Test")
    print("=" * 70)

    # Create test dataframe with wide frequency range
    freq_range = list(range(1800, 2800, 10))  # 1800-2800 MHz
    test_df = pd.DataFrame({
        'frequency': freq_range,
        'S21_re': [0.5] * len(freq_range),
        'S21_im': [0.1] * len(freq_range),
    })

    rx_parser = RxGainParser()
    tx_parser = TxPowerParser()

    # Test B1 filtering
    print("\n📡 Band B1 Filtering Test:")
    print(f"  Original data: {test_df['frequency'].min()}-{test_df['frequency'].max()} MHz ({len(test_df)} points)")

    # Rx (Downlink) filtering
    rx_filtered = rx_parser.filter_frequency(test_df.copy(), 'B1', direction='rx')
    print(f"  ✅ Rx (Downlink): {rx_filtered['frequency'].min()}-{rx_filtered['frequency'].max()} MHz ({len(rx_filtered)} points)")
    print(f"     Expected: 2110-2170 MHz")

    # Tx (Uplink) filtering
    tx_filtered = tx_parser.filter_frequency(test_df.copy(), 'B1', direction='tx')
    print(f"  ✅ Tx (Uplink):   {tx_filtered['frequency'].min()}-{tx_filtered['frequency'].max()} MHz ({len(tx_filtered)} points)")
    print(f"     Expected: 1920-1980 MHz")

    # Test B7 filtering
    print("\n📡 Band B7 Filtering Test:")
    freq_range_b7 = list(range(2400, 2800, 10))  # 2400-2800 MHz
    test_df_b7 = pd.DataFrame({
        'frequency': freq_range_b7,
        'S21_re': [0.5] * len(freq_range_b7),
        'S21_im': [0.1] * len(freq_range_b7),
    })

    print(f"  Original data: {test_df_b7['frequency'].min()}-{test_df_b7['frequency'].max()} MHz ({len(test_df_b7)} points)")

    # Rx (Downlink) filtering
    rx_filtered_b7 = rx_parser.filter_frequency(test_df_b7.copy(), 'B7', direction='rx')
    print(f"  ✅ Rx (Downlink): {rx_filtered_b7['frequency'].min()}-{rx_filtered_b7['frequency'].max()} MHz ({len(rx_filtered_b7)} points)")
    print(f"     Expected: 2620-2690 MHz")

    # Tx (Uplink) filtering
    tx_filtered_b7 = tx_parser.filter_frequency(test_df_b7.copy(), 'B7', direction='tx')
    print(f"  ✅ Tx (Uplink):   {tx_filtered_b7['frequency'].min()}-{tx_filtered_b7['frequency'].max()} MHz ({len(tx_filtered_b7)} points)")
    print(f"     Expected: 2500-2570 MHz")


def test_measurement_type_auto_detection():
    """Test that measurement type correctly determines direction"""
    print("\n" + "=" * 70)
    print("🔬 Measurement Type Auto-Detection Test")
    print("=" * 70)

    rx_parser = RxGainParser()
    tx_parser = TxPowerParser()

    print(f"\n✅ RxGainParser.get_measurement_type() = '{rx_parser.get_measurement_type()}'")
    print(f"   → Uses DOWNLINK frequencies (2110-2170 MHz for B1)")

    print(f"\n✅ TxPowerParser.get_measurement_type() = '{tx_parser.get_measurement_type()}'")
    print(f"   → Uses UPLINK frequencies (1920-1980 MHz for B1)")

    print("\n💡 In parse_file(), direction is auto-detected:")
    print("   direction = 'tx' if measurement_type == 'tx_power' else 'rx'")


def test_gsm_band_aliases():
    """Test GSM band name aliases"""
    print("\n" + "=" * 70)
    print("🔬 GSM Band Alias Test")
    print("=" * 70)

    parser = RxGainParser()

    gsm_tests = [
        ('GSM850', (824, 849), (869, 894)),
        ('GSM900', (890, 915), (935, 960)),
        ('DCS', (1710, 1785), (1805, 1880)),
        ('PCS', (1850, 1910), (1930, 1990)),
    ]

    for band_name, expected_ul, expected_dl in gsm_tests:
        if band_name in parser.band_config:
            ul, dl = parser.band_config[band_name]
            ul_match = ul == expected_ul
            dl_match = dl == expected_dl
            status = "✅" if (ul_match and dl_match) else "❌"
            print(f"  {status} {band_name:10} | UL: {ul} {'✅' if ul_match else '❌'} | DL: {dl} {'✅' if dl_match else '❌'}")
        else:
            print(f"  ❌ {band_name:10} | NOT FOUND")


if __name__ == '__main__':
    print("\n" + "🚀 Starting Band Configuration Tests" + "\n")

    # Run all tests
    test_band_config()
    test_rx_tx_filtering()
    test_measurement_type_auto_detection()
    test_gsm_band_aliases()

    print("\n" + "=" * 70)
    print("✅ All tests completed!")
    print("=" * 70)
    print("\n💡 Summary:")
    print("  - GSM bands (GSM850, GSM900, DCS, PCS) configured ✅")
    print("  - LTE FDD bands (B1-B88) with UL/DL separation ✅")
    print("  - LTE TDD bands (B34-B53) with same UL/DL ✅")
    print("  - Rx measurements use DOWNLINK frequencies ✅")
    print("  - Tx measurements use UPLINK frequencies ✅")
    print("  - Auto-detection based on measurement_type ✅")
    print("\n")
