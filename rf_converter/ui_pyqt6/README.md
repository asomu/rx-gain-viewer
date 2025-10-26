# RF SnP to CSV Converter - PyQt6 GUI

Modern desktop application for converting RF SnP files to CSV format.

## Features

- **Drag-and-Drop Support**: Simply drag .s2p files or folders into the application
- **Folder Browser**: Browse and select folders containing SnP files
- **Real-time Progress**: Live progress bar and file counter during conversion
- **Measurement Types**: Currently supports Rx Gain measurement (more coming soon)
- **Conversion Options**:
  - Frequency filtering (band-specific)
  - Auto-detect band from filename
  - Include full frequency sweep
- **Result Statistics**: Detailed conversion results with success metrics
- **Quick Actions**: Open CSV file or folder directly from the app

## Installation

Ensure you have the required dependencies:

```bash
pip install PyQt6
```

The application uses the existing `core` module for conversion logic.

## Running the Application

From the project root directory:

```bash
cd C:/Project/html_exporter/rf_converter
C:/Project/html_exporter/.venv/Scripts/python.exe ui_pyqt6/main.py
```

Or from the ui_pyqt6 directory:

```bash
python main.py
```

## Usage

1. **Select Files**:
   - Drag and drop .s2p files onto the drag area, OR
   - Click "Browse Folder" to select a folder containing SnP files

2. **Configure Options**:
   - Choose measurement type (currently Rx Gain only)
   - Enable/disable frequency filtering
   - Configure band detection settings

3. **Set Output Location**:
   - Default location is Desktop/RF_Output.csv
   - Click "Browse..." to change output location

4. **Start Conversion**:
   - Click the "START CONVERSION" button
   - Monitor progress in real-time
   - View results when complete

5. **Post-Conversion Actions**:
   - Click "Open CSV" to view the converted file
   - Click "Open Folder" to browse the output location
   - Click "Convert More" to start a new conversion

## Architecture

```
ui_pyqt6/
├── main.py              # Application entry point
├── main_window.py       # Main window class
├── widgets/
│   ├── __init__.py
│   ├── file_selector.py # Drag-drop widget for file selection
│   └── progress_widget.py # Progress display widget
└── README.md
```

### Key Components

- **MainWindow**: Primary application window with all UI controls
- **ConversionWorker**: QThread worker for background conversion (prevents UI freeze)
- **FileSelector**: Custom widget with drag-and-drop support
- **ProgressWidget**: Real-time progress display

### Integration with Core Module

The GUI integrates with the `core` module:

```python
from core import ConversionService, ConversionResult

# Create service
service = ConversionService('rx_gain')

# Convert with progress callback
result = service.convert_files(
    snp_files,
    output_csv,
    options={'freq_filter': True, 'auto_band': True},
    progress_callback=progress_callback
)
```

## Design Principles

- **Separation of Concerns**: UI code is completely separate from business logic
- **Thread Safety**: Conversion runs in QThread to prevent UI freezing
- **Signal-Slot Architecture**: Clean event-driven communication
- **Modern UX**: Professional styling with clear visual hierarchy
- **Accessibility**: Keyboard navigation, proper tab order, tooltips

## Customization

### Styling

The application uses embedded QSS styling in `main_window.py`. The color scheme can be customized by modifying the `apply_styling()` method.

Key colors:
- Primary: #4CAF50 (green)
- Success: #27ae60
- Error: #e74c3c
- Info: #3498db
- Background: #f5f6fa

### Adding New Measurement Types

When new measurement types are added to the core module:

1. Enable the corresponding radio button in `create_measurement_section()`
2. Update the `start_conversion()` method to use the selected type
3. Add any type-specific options to the options panel

## Troubleshooting

### Application won't start
- Verify PyQt6 is installed: `pip install PyQt6`
- Ensure Python path is correct in the run command

### Conversion fails
- Check that SnP files are valid
- Verify output folder has write permissions
- Review error messages in the result section

### UI freezes during conversion
- This should not happen - conversion runs in a separate thread
- If it occurs, report as a bug

## Future Enhancements

- [ ] Support for Tx Power measurement type
- [ ] Support for Isolation measurement type
- [ ] Multi-file output options
- [ ] Conversion history and presets
- [ ] Chart preview of SnP data
- [ ] Batch conversion profiles

## License

Part of the RF Analyzer project.
