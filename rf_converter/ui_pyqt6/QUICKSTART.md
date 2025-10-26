# Quick Start Guide - RF SnP to CSV Converter

## Launch the Application

### Option 1: Using the batch file (Windows)
```bash
cd C:/Project/html_exporter/rf_converter
run_gui.bat
```

### Option 2: Using Python directly
```bash
cd C:/Project/html_exporter/rf_converter
C:/Project/html_exporter/.venv/Scripts/python.exe ui_pyqt6/main.py
```

## First Time Setup

1. **Check Dependencies**
   ```bash
   pip install PyQt6
   ```
   (Already installed if you followed the README)

2. **Verify Installation**
   ```bash
   python test_gui_simple.py
   ```
   You should see "SUCCESS: All tests passed!"

## Using the Application

### Step-by-Step Guide

1. **Launch the Application**
   - Double-click `run_gui.bat` or use command line

2. **Select Your Files**
   - **Drag-and-Drop**: Drag .s2p files or folders into the blue drop area
   - **Browse**: Click "Browse Folder..." to select a folder
   - The app will show: "X files selected (Y.YY MB)"

3. **Configure Settings**
   - **Measurement Type**: Currently "Rx Gain Measurement" (others coming soon)
   - **Frequency Filtering**: ✓ Enabled by default (band-specific filtering)
   - **Auto-detect Band**: ✓ Enabled by default (reads band from filename)
   - **Full Frequency Sweep**: ☐ Optional (includes all frequencies)

4. **Set Output Location**
   - Default: `Desktop/RF_Output.csv`
   - Click "Browse..." to change location

5. **Start Conversion**
   - Click the green "START CONVERSION" button
   - Watch real-time progress:
     - Progress bar shows percentage
     - File counter: "Processing 15/84 files..."
     - Current filename being processed

6. **View Results**
   - **Success**: Green checkmark with statistics
     - Files processed count
     - Total rows generated
     - Output file size
   - **Quick Actions**:
     - "Open CSV": Opens the CSV file
     - "Open Folder": Opens containing folder
     - "Convert More": Start a new conversion

## Tips and Tricks

### Selecting Files

**Drag-and-Drop Multiple Times**
- You can drag files multiple times
- Files are accumulated (not replaced)
- Click "Clear Files" to start over

**Mixed Selection**
- Drag individual files
- Drag entire folders
- Mix both methods

### Output Formatting

**Frequency Filtering**
- When enabled: Only relevant frequencies for each band
- When disabled: All measured frequencies

**Auto Band Detection**
- Reads band from filename (e.g., "B40", "N78")
- Automatically applies correct frequency ranges

**Full Sweep**
- Includes complete frequency sweep
- Useful for analysis beyond standard bands

### Keyboard Shortcuts

- **Tab**: Navigate between controls
- **Space**: Activate focused button
- **Enter**: Press focused button

## Troubleshooting

### "Application won't start"
**Solution**: Install PyQt6
```bash
pip install PyQt6
```

### "No files selected" warning
**Solution**:
- Make sure you're selecting .s2p files (or .s1p, .s3p, .s4p)
- Check file extensions are correct
- Files must have valid SnP format

### "Conversion failed" error
**Solution**:
- Check the error details in the results section
- Verify SnP files are not corrupted
- Ensure output folder has write permissions

### UI appears frozen
**Solution**:
- The conversion runs in a background thread
- UI should remain responsive during conversion
- If truly frozen, restart the application

### Output file not created
**Solution**:
- Check output path has write permissions
- Ensure parent folder exists
- Try changing output location to Desktop

## Sample Workflow

**Example: Converting PA Module Test Data**

1. Launch application: `run_gui.bat`

2. Drag folder: `C:/Project/html_exporter/target/`
   - Result: "84 files selected (2.45 MB)"

3. Settings:
   - ✓ Frequency filtering
   - ✓ Auto-detect band
   - ☐ Full frequency sweep

4. Output: `Desktop/PA_Module_Results.csv`

5. Click "START CONVERSION"

6. Wait for completion (progress updates every file)

7. Results:
   - "84/84 files processed"
   - "15,456 rows generated"
   - "245.3 KB"

8. Click "Open CSV" to view in Excel

## Performance Notes

- **Small batches (< 100 files)**: ~5-10 seconds
- **Medium batches (100-500 files)**: ~30-60 seconds
- **Large batches (> 500 files)**: ~2-5 minutes

Actual time depends on:
- File size
- Number of frequency points
- Computer speed
- Disk performance

## File Format Requirements

**Supported Formats**:
- `.s1p` - Single-port parameters
- `.s2p` - Two-port parameters (most common)
- `.s3p` - Three-port parameters
- `.s4p` - Four-port parameters

**Case Insensitive**: `.S2P` and `.s2p` both work

**Filename Convention** (for auto band detection):
- Must contain band identifier: `B40`, `N78`, etc.
- Example: `PA_Module_B40_Rx_Gain.s2p`

## Next Steps

- See `README.md` for detailed architecture
- Check `test_gui_simple.py` for validation tests
- Review core module documentation for conversion logic

## Support

For issues or questions:
1. Check error messages in the results section
2. Review this guide's troubleshooting section
3. Verify with `test_gui_simple.py`
4. Check core module documentation
