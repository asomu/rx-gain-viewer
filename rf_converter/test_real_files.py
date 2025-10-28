"""Test real SnP files from Alpha-1C EVB#1 25 folder"""

from pathlib import Path
from core.parsers.rx_parser import RxGainParser
from collections import defaultdict


def test_real_files():
    """Test parsing of real SnP files"""

    parser = RxGainParser()
    folder = Path(r"C:\Python\Project\CplShow\sample\data\Alpha-1C EVB#1 25")

    if not folder.exists():
        print(f"❌ Folder not found: {folder}")
        return

    snp_files = list(folder.glob("*.s*p"))
    print("=" * 80)
    print(f"Found {len(snp_files)} SnP files in:")
    print(f"  {folder}")
    print("=" * 80)

    # Group by CA config
    ca_configs = defaultdict(list)
    port_outs = set()
    lna_states = set()
    parsing_errors = []

    print("\n📊 Parsing Results:\n")

    # Test first 10 files in detail
    for i, file_path in enumerate(snp_files[:10], 1):
        filename = file_path.name
        print(f"{i}. {filename}")

        try:
            metadata = parser.parse_filename(filename)

            print(f"   ✓ port_in:    {metadata.get('port_in', 'NOT FOUND')}")
            print(f"   ✓ band:       {metadata.get('band', 'NOT FOUND')}")
            print(f"   ✓ ca_config:  {metadata.get('ca_config', 'NOT FOUND')}")
            print(f"   ✓ port_out:   {metadata.get('port_out', 'NOT FOUND')}")
            print(f"   ✓ lna_state:  {metadata.get('lna_state', 'NOT FOUND')}")
            print()

            # Collect stats
            ca_config = metadata.get('ca_config', 'Unknown')
            ca_configs[ca_config].append(filename)

            if 'port_out' in metadata:
                port_outs.add(metadata['port_out'])
            if 'lna_state' in metadata:
                lna_states.add(metadata['lna_state'])

        except Exception as e:
            print(f"   ❌ ERROR: {e}\n")
            parsing_errors.append((filename, str(e)))

    # Process remaining files for statistics
    for file_path in snp_files[10:]:
        filename = file_path.name
        try:
            metadata = parser.parse_filename(filename)
            ca_config = metadata.get('ca_config', 'Unknown')
            ca_configs[ca_config].append(filename)

            if 'port_out' in metadata:
                port_outs.add(metadata['port_out'])
            if 'lna_state' in metadata:
                lna_states.add(metadata['lna_state'])
        except Exception as e:
            parsing_errors.append((filename, str(e)))

    # Statistics
    print("\n" + "=" * 80)
    print("📈 STATISTICS")
    print("=" * 80)

    print(f"\n✅ Total files processed: {len(snp_files)}")
    print(f"✅ Successfully parsed: {len(snp_files) - len(parsing_errors)}")
    if parsing_errors:
        print(f"❌ Parsing errors: {len(parsing_errors)}")

    print(f"\n📊 CA Configurations found ({len(ca_configs)}):")
    for ca_config, files in sorted(ca_configs.items()):
        print(f"   {ca_config:15} → {len(files):3} files")

    print(f"\n📊 Port Outputs found ({len(port_outs)}):")
    for port in sorted(port_outs):
        print(f"   {port}")

    print(f"\n📊 LNA States found ({len(lna_states)}):")
    for state in sorted(lna_states):
        print(f"   {state}")

    # Validation checks
    print("\n" + "=" * 80)
    print("✅ VALIDATION CHECKS")
    print("=" * 80)

    # Check if all B41[XX] patterns are recognized
    b41_patterns = [ca for ca in ca_configs.keys() if ca.startswith('B41[')]
    print(f"\n✅ B41[XX] patterns recognized: {len(b41_patterns)}")
    for pattern in sorted(b41_patterns):
        print(f"   {pattern}")

    # Check port_out coverage
    expected_ports = {'RXOUT1', 'RXOUT2', 'RXOUT3', 'RXOUT4'}
    found_ports = port_outs
    print(f"\n✅ Port coverage: {len(found_ports)}/{len(expected_ports)}")
    missing = expected_ports - found_ports
    if missing:
        print(f"   ⚠️ Missing: {missing}")

    # Check LNA state parsing
    print(f"\n✅ LNA states recognized: {len(lna_states)}")
    if 'G0_H' in lna_states:
        print("   ✅ G0H → G0_H conversion working")

    if parsing_errors:
        print("\n❌ PARSING ERRORS:")
        for filename, error in parsing_errors[:5]:  # Show first 5 errors
            print(f"   {filename}: {error}")
        if len(parsing_errors) > 5:
            print(f"   ... and {len(parsing_errors) - 5} more errors")

    print("\n" + "=" * 80)


if __name__ == '__main__':
    test_real_files()
