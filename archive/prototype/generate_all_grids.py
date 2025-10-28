"""
Batch generation script for all grid combinations
Generates 462 grid charts (22 bands × 7 LNA states × 3 input ports)
"""

import sys
from pathlib import Path
from datetime import datetime
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

from prototype.parsers.csv_parser import CsvParser
from prototype.utils.chart_generator import ChartGenerator


def generate_all_grids(
    output_dir: str = None,
    file_format: str = 'html',
    dry_run: bool = False
):
    """
    Generate all possible grid combinations

    Args:
        output_dir: Output directory path (default: prototype/output_grids)
        file_format: 'html' or 'png' (PNG requires kaleido)
        dry_run: If True, only show what would be generated without actually generating
    """

    # Setup output directory
    if output_dir is None:
        output_dir = Path(__file__).parent / "output_grids"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(exist_ok=True)

    # Load CSV
    print("="*70)
    print("Batch Grid Generation")
    print("="*70)
    print(f"\nOutput directory: {output_dir}")
    print(f"File format: {file_format.upper()}")
    print(f"Mode: {'DRY RUN' if dry_run else 'FULL GENERATION'}")

    csv_path = Path(__file__).parent.parent / "data" / "Bellagio_POC_Rx.csv"
    print(f"\nLoading CSV: {csv_path.name}...")

    parser = CsvParser(str(csv_path))
    parser.load_consolidated()

    print(f"[OK] CSV loaded: {parser}")

    # Get all combinations
    bands = parser.get_available_bands()
    lna_states = parser.get_lna_gain_states()
    input_ports = parser.get_input_ports()

    total_combinations = len(bands) * len(lna_states) * len(input_ports)

    print(f"\n{'='*70}")
    print("Generation Plan:")
    print(f"  Bands: {len(bands)}")
    print(f"    {', '.join(bands[:10])}...")
    print(f"  LNA Gain States: {len(lna_states)}")
    print(f"    {', '.join(lna_states)}")
    print(f"  Input Ports: {len(input_ports)}")
    print(f"    {', '.join(input_ports)}")
    print(f"\n  Total combinations: {total_combinations}")
    print(f"{'='*70}")

    if dry_run:
        print("\n[DRY RUN] Showing first 10 files that would be generated:")
        count = 0
        for band in bands:
            for lna in lna_states:
                for port in input_ports:
                    filename = f"{band}_{lna}_{port}.{file_format}"
                    print(f"  {count+1:3}. {filename}")
                    count += 1
                    if count >= 10:
                        break
                if count >= 10:
                    break
            if count >= 10:
                break
        print(f"\n  ... and {total_combinations - 10} more files")
        print("\n[DRY RUN] Use dry_run=False to actually generate files")
        return

    # Generate all grids
    print(f"\n{'='*70}")
    print("Starting generation...")
    print(f"{'='*70}\n")

    start_time = time.time()
    generated_count = 0
    skipped_count = 0
    error_count = 0

    for band_idx, band in enumerate(bands, 1):
        print(f"\n[{band_idx}/{len(bands)}] Processing Band: {band}")

        for lna_idx, lna in enumerate(lna_states, 1):
            for port_idx, port in enumerate(input_ports, 1):

                filename = f"{band}_{lna}_{port}.{file_format}"
                filepath = output_dir / filename

                try:
                    # Get grid data
                    grid_data = parser.get_grid_data(
                        band=band,
                        lna_gain_state=lna,
                        input_port=port
                    )

                    # Check if data exists
                    has_data = False
                    for ca_combo in grid_data.values():
                        for rx_port in ca_combo.values():
                            if rx_port['count'] > 0:
                                has_data = True
                                break
                        if has_data:
                            break

                    if not has_data:
                        print(f"  [{lna_idx}/{len(lna_states)}][{port_idx}/{len(input_ports)}] SKIP: {filename} (no data)")
                        skipped_count += 1
                        continue

                    # Generate chart
                    fig = ChartGenerator.create_compact_grid(
                        grid_data=grid_data,
                        band=band,
                        lna_gain_state=lna,
                        input_port=port,
                        compact_size=(250, 150)
                    )

                    # Save chart
                    if file_format == 'html':
                        ChartGenerator.export_to_html(fig, str(filepath), auto_open=False)
                    elif file_format == 'png':
                        ChartGenerator.export_to_image(fig, str(filepath))
                    else:
                        raise ValueError(f"Unsupported format: {file_format}")

                    generated_count += 1
                    print(f"  [{lna_idx}/{len(lna_states)}][{port_idx}/{len(input_ports)}] OK: {filename}")

                except Exception as e:
                    error_count += 1
                    print(f"  [{lna_idx}/{len(lna_states)}][{port_idx}/{len(input_ports)}] ERROR: {filename}")
                    print(f"    {str(e)}")

    # Summary
    elapsed_time = time.time() - start_time

    print(f"\n{'='*70}")
    print("Generation Complete!")
    print(f"{'='*70}")
    print(f"  Total combinations: {total_combinations}")
    print(f"  Generated: {generated_count}")
    print(f"  Skipped (no data): {skipped_count}")
    print(f"  Errors: {error_count}")
    print(f"  Time elapsed: {elapsed_time:.1f} seconds")
    print(f"  Average: {elapsed_time/max(generated_count,1):.2f} sec/file")
    print(f"\n  Output directory: {output_dir.absolute()}")
    print(f"{'='*70}")


def generate_summary_index(output_dir: str = None):
    """
    Generate HTML index page listing all generated grids
    """

    if output_dir is None:
        output_dir = Path(__file__).parent / "output_grids"
    else:
        output_dir = Path(output_dir)

    if not output_dir.exists():
        print(f"[ERROR] Output directory not found: {output_dir}")
        return

    # Find all HTML files
    html_files = sorted(output_dir.glob("*.html"))

    if not html_files:
        print(f"[ERROR] No HTML files found in {output_dir}")
        return

    # Parse filenames
    grids_by_band = {}
    for filepath in html_files:
        filename = filepath.stem  # Without extension
        parts = filename.split('_')

        if len(parts) >= 3:
            band = parts[0]
            lna = parts[1]
            port = parts[2]

            if band not in grids_by_band:
                grids_by_band[band] = []

            grids_by_band[band].append({
                'filename': filepath.name,
                'lna': lna,
                'port': port
            })

    # Generate index HTML
    index_path = output_dir / "index.html"

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Grid Chart Index</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #666; margin-top: 30px; }}
        table {{ border-collapse: collapse; width: 100%; margin-bottom: 30px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        a {{ color: #1976d2; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .summary {{ background-color: #e3f2fd; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <h1>RF S-parameter Grid Chart Index</h1>

    <div class="summary">
        <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
        <strong>Total Bands:</strong> {len(grids_by_band)}<br>
        <strong>Total Grids:</strong> {len(html_files)}
    </div>

"""

    for band in sorted(grids_by_band.keys()):
        html_content += f"    <h2>Band: {band}</h2>\n"
        html_content += "    <table>\n"
        html_content += "        <tr><th>LNA Gain State</th><th>Input Port</th><th>Chart</th></tr>\n"

        for grid in sorted(grids_by_band[band], key=lambda x: (x['lna'], x['port'])):
            html_content += f"        <tr>\n"
            html_content += f"            <td>{grid['lna']}</td>\n"
            html_content += f"            <td>{grid['port']}</td>\n"
            html_content += f"            <td><a href=\"{grid['filename']}\" target=\"_blank\">View Chart</a></td>\n"
            html_content += f"        </tr>\n"

        html_content += "    </table>\n"

    html_content += """
</body>
</html>
"""

    index_path.write_text(html_content, encoding='utf-8')

    print(f"\n[OK] Index page generated: {index_path}")
    print(f"  Open this file in a browser to navigate all grids")


if __name__ == "__main__":
    import argparse

    parser_args = argparse.ArgumentParser(description="Generate all grid combinations")
    parser_args.add_argument('--output-dir', '-o', type=str, help='Output directory path')
    parser_args.add_argument('--format', '-f', choices=['html', 'png'], default='html', help='Output file format')
    parser_args.add_argument('--dry-run', '-d', action='store_true', help='Dry run mode (show plan only)')
    parser_args.add_argument('--index', '-i', action='store_true', help='Generate index page after completion')

    args = parser_args.parse_args()

    # Generate grids
    generate_all_grids(
        output_dir=args.output_dir,
        file_format=args.format,
        dry_run=args.dry_run
    )

    # Generate index if requested
    if args.index and not args.dry_run:
        generate_summary_index(args.output_dir)

    print("\nUsage examples:")
    print("  # Dry run (show plan)")
    print("  python generate_all_grids.py --dry-run")
    print("\n  # Generate all HTML files")
    print("  python generate_all_grids.py")
    print("\n  # Generate all HTML files with index")
    print("  python generate_all_grids.py --index")
    print("\n  # Generate PNG files (requires kaleido)")
    print("  python generate_all_grids.py --format png")
