"""Test script for Core functionality"""

from pathlib import Path
from core import ConversionService

def test_conversion():
    """Test SnP to CSV conversion with sample file"""

    # Use sample SnP file from target folder
    target_folder = Path(r'C:/Project/html_exporter/target')
    snp_files = list(target_folder.glob('*.s2p'))[:5]  # Test with first 5 files

    if not snp_files:
        print("❌ No SnP files found in target folder")
        return

    print(f"📂 Found {len(snp_files)} SnP files for testing")
    for f in snp_files:
        print(f"  - {f.name}")

    # Create service
    service = ConversionService('rx_gain')

    # Validate files
    validation = service.validate_files(snp_files)
    print(f"\n✅ Validation:")
    print(f"  Valid: {validation['file_count']} files")
    print(f"  Size: {validation['total_size_mb']:.2f} MB")

    # Convert with progress callback
    def progress(current, total, filename):
        percent = (current / total) * 100
        print(f"  [{current}/{total}] {percent:.0f}% - {filename}")

    output_csv = Path(r'C:/Project/html_exporter/rf_converter/test_output.csv')

    print(f"\n🚀 Converting to: {output_csv}")
    result = service.convert_files(
        snp_files,
        output_csv,
        options={'freq_filter': True, 'auto_band': True},
        progress_callback=progress
    )

    # Print result
    print(f"\n{result}")

    if result.success:
        print(f"✅ Output file: {result.output_path}")
        print(f"✅ Size: {result.output_size_kb:.1f} KB")

        # Show first few rows
        import pandas as pd
        df = pd.read_csv(output_csv)
        print(f"\n📊 Sample data ({len(df)} rows):")
        print(df.head(10))
        print(f"\n📋 Columns ({len(df.columns)}):")
        print(df.columns.tolist())
    else:
        print(f"❌ Conversion failed!")
        for error in result.errors:
            print(f"  - {error['file']}: {error['error']}")

if __name__ == '__main__':
    test_conversion()
