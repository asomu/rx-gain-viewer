# Band Mapping Configuration Files

This directory contains JSON configuration files for translating band notation
between filename format and N-plexer bank format.

## Purpose

Different test sites and projects may use different notation for the same RF bands.
For example:
- SnP filename: "B41[CN]"
- N-plexer bank: "34_39+41"

These mapping files allow RF Converter to automatically translate notations so that
measurement data from different sources can be compared on the same graph.

## File Format

JSON files with the following structure:

```json
{
  "version": "1.0",
  "description": "Brief description of this mapping set",
  "project": "Project name (optional)",
  "created_date": "YYYY-MM-DD (optional)",
  "mappings": {
    "B41[CN]": "34_39+41",
    "B41[SA]": "41",
    "B41[NA]": "25_30_66+41"
  }
}
```

## Schema Requirements

- **version** (required): Must be "1.0"
- **mappings** (required): Dictionary of string key-value pairs
  - Key: Band notation from SnP filename (e.g., "B41[CN]", "B1", "N77")
  - Value: N-plexer bank notation (e.g., "34_39+41", "TM01_A")
- **description** (optional): Human-readable description
- **project** (optional): Project or site name
- **created_date** (optional): Creation date in YYYY-MM-DD format

## Usage

1. Create a JSON file in this directory with your project-specific mappings
2. In RF Converter GUI, check "Enable N-plexer bank mapping"
3. Click "Browse..." and select your mapping file
4. Status will show "✅ Loaded N mappings from filename.json"
5. Converted CSV files will include both columns:
   - `ca_config`: Original filename notation (e.g., "B41[CN]")
   - `debug-nplexer_bank`: Mapped N-plexer notation (e.g., "34_39+41")

## Example Files

- `example_alpha1c_evb1.json`: Alpha-1C EVB#1 project mappings
- `example_basic.json`: Simple mapping example
- `example_comprehensive.json`: Full 48-band mapping

## Tips

- Only map the bands you actually use in your project
- Use descriptive filenames: `{project}_{site}_mapping.json`
- Keep mappings in version control with your test data
- Review logs for "No mapping found" warnings to identify missing entries

## File Location Options

You can store mapping files in:
1. This directory (`rf_converter/core/mappings/`) - Shared mappings
2. User home directory (`~/.rf_converter/mappings/`) - Personal mappings
3. Project data directory - Project-specific mappings

RF Converter will remember your last used mapping file in settings.
