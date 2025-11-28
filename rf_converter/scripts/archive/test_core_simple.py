"""Test script for Core functionality - No Unicode"""

from pathlib import Path
from core import ConversionService

# Use sample SnP file from target folder
target_folder = Path(r'C:/Project/html_exporter/target')
snp_files = list(target_folder.glob('*.s2p'))[:3]  # Test with first 3 files

print(f"Found {len(snp_files)} SnP files")

# Create service
service = ConversionService('rx_gain')

# Convert
output_csv = Path(r'C:/Project/html_exporter/rf_converter/test_output.csv')

def progress(current, total, filename):
    print(f"[{current}/{total}] {filename[:40]}")

result = service.convert_files(
    snp_files,
    output_csv,
    options={'freq_filter': True, 'auto_band': True},
    progress_callback=progress
)

print(f"\nSuccess: {result.success}")
print(f"Files: {result.files_processed}/{result.total_files}")
print(f"Rows: {result.rows_generated}")
print(f"Size: {result.output_size_kb:.1f} KB")

if result.errors:
    print("\nErrors:")
    for error in result.errors:
        print(f"  {error}")
