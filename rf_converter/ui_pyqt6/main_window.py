"""
Main Window for RF SnP to CSV Converter
Professional PyQt6 UI with modern design
"""

from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QLabel, QRadioButton, QCheckBox, QLineEdit,
    QProgressBar, QFileDialog, QMessageBox, QButtonGroup, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSettings
from PyQt6.QtGui import QFont

from rf_converter.core import ConversionService, ConversionResult
from rf_converter.core.logger import get_logger
from rf_converter.core.band_mapper import BandMapper
from rf_converter.ui_pyqt6.widgets.file_selector import FileSelector
from rf_converter.ui_pyqt6.widgets.progress_widget import ProgressWidget

# Import version from package
try:
    from rf_converter import __version__, __app_name__
except ImportError:
    __version__ = "1.1.0"
    __app_name__ = "RF Converter"


class ConversionWorker(QThread):
    """
    Worker thread for file conversion
    Prevents UI freezing during conversion process
    """

    # Signals for thread-safe communication
    progress_updated = pyqtSignal(int, int, str)  # current, total, filename
    conversion_complete = pyqtSignal(object)  # ConversionResult

    def __init__(self, service, snp_files, output_csv, options):
        super().__init__()
        self.service = service
        self.snp_files = snp_files
        self.output_csv = output_csv
        self.options = options

    def run(self):
        """Execute conversion in separate thread"""
        def progress_callback(current, total, filename):
            self.progress_updated.emit(current, total, filename)

        result = self.service.convert_files(
            self.snp_files,
            self.output_csv,
            self.options,
            progress_callback
        )

        self.conversion_complete.emit(result)


class MainWindow(QMainWindow):
    """
    Main application window
    Provides comprehensive UI for SnP to CSV conversion

    Layout Design Philosophy:
    - Always-visible result section (no sudden layout jumps)
    - Fixed, predictable layout height optimized for 1080p screens
    - State-based content display (empty → converting → complete)
    - Scroll support for content overflow
    """

    def __init__(self):
        super().__init__()
        self.snp_files = []
        self.conversion_service = None
        self.worker = None

        # Initialize settings and logger
        self.settings = QSettings("RF Analyzer", "RF Converter")
        self.logger = get_logger()
        self.logger.log_info("Application started")

        # Initialize BandMapper singleton
        self.band_mapper = BandMapper.get_instance()

        self.setup_ui()
        self.apply_styling()
        self.connect_signals()

        # Restore last settings
        self.restore_settings()

    def setup_ui(self):
        """Initialize UI components and layouts"""
        self.setWindowTitle(f"{__app_name__} v{__version__}")

        # Set window icon - must be set here for PyInstaller taskbar icon support
        # Handle both development (source) and PyInstaller (bundled) paths
        import sys
        from pathlib import Path
        from PyQt6.QtGui import QIcon

        if getattr(sys, 'frozen', False):
            # Running as PyInstaller bundle - icon is at _MEIPASS root
            icon_path = Path(sys._MEIPASS) / "icon.ico"
        else:
            # Running from source - icon is in rf_converter/
            icon_path = Path(__file__).parent.parent / "icon.ico"

        if icon_path.exists():
            # Store as instance variable to prevent garbage collection
            self._window_icon = QIcon(str(icon_path))
            self.setWindowIcon(self._window_icon)

        # Further increased window size for complete visibility (no scroll)
        # Height: 1020px to ensure conversion result fully visible
        self.setGeometry(100, 50, 850, 1020)
        self.setMinimumSize(850, 980)  # Increased minimum height
        self.setMaximumSize(850, 1050)  # Increased maximum height

        # Create scroll area for content overflow protection
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setCentralWidget(scroll_area)

        # Content widget inside scroll area
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        main_layout = QVBoxLayout(content_widget)
        main_layout.setSpacing(8)  # Reduced from 16 to 10
        main_layout.setContentsMargins(20, 20, 20, 20)  # Reduced margins

        # Title section
        title_label = QLabel("RF SnP to CSV Converter")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # File selection section
        self.file_selector = FileSelector()
        main_layout.addWidget(self.file_selector)
        main_layout.addSpacing(8)  # Reduced from 15 to 8

        # Measurement type selection
        measurement_group = self.create_measurement_section()
        main_layout.addWidget(measurement_group)
        main_layout.addSpacing(8)  # Reduced from 15 to 8

        # Options panel
        options_group = self.create_options_section()
        main_layout.addWidget(options_group)
        main_layout.addSpacing(8)  # Reduced from 15 to 8

        # Band Mapping section (NEW)
        mapping_group = self.create_mapping_section()
        main_layout.addWidget(mapping_group)
        main_layout.addSpacing(8)

        # Output selection
        output_group = self.create_output_section()
        main_layout.addWidget(output_group)
        main_layout.addSpacing(10)  # Slightly more space before convert button

        # Conversion button
        self.convert_btn = QPushButton("START CONVERSION")
        self.convert_btn.setMinimumHeight(50)
        self.convert_btn.setEnabled(False)
        main_layout.addWidget(self.convert_btn)

        # Progress display
        self.progress_widget = ProgressWidget()
        self.progress_widget.setVisible(False)
        main_layout.addWidget(self.progress_widget)

        # Result section - ALWAYS VISIBLE with state-based content
        # This ensures no layout jump when results appear
        self.result_widget = self.create_result_section()
        main_layout.addWidget(self.result_widget)

        # Initialize to empty state (ready to convert)
        self.set_result_empty_state()

        # Add bottom spacing to ensure buttons are always visible
        main_layout.addSpacing(20)

    def create_measurement_section(self):
        """Create measurement type selection group"""
        group = QGroupBox("Measurement Type")
        layout = QVBoxLayout(group)

        self.meas_button_group = QButtonGroup()

        # Rx Gain (enabled)
        self.rx_gain_radio = QRadioButton("Rx Gain Measurement")
        self.rx_gain_radio.setChecked(True)
        self.meas_button_group.addButton(self.rx_gain_radio)
        layout.addWidget(self.rx_gain_radio)

        # Tx Power (disabled for future)
        self.tx_power_radio = QRadioButton("Tx Power (Coming Soon)")
        self.tx_power_radio.setEnabled(False)
        self.meas_button_group.addButton(self.tx_power_radio)
        layout.addWidget(self.tx_power_radio)

        # Isolation (disabled for future)
        self.isolation_radio = QRadioButton("Isolation (Coming Soon)")
        self.isolation_radio.setEnabled(False)
        self.meas_button_group.addButton(self.isolation_radio)
        layout.addWidget(self.isolation_radio)

        return group

    def create_options_section(self):
        """Create conversion options panel"""
        group = QGroupBox("Conversion Options")
        layout = QVBoxLayout(group)

        self.freq_filter_check = QCheckBox("Frequency filtering (band-specific)")
        self.freq_filter_check.setChecked(True)
        layout.addWidget(self.freq_filter_check)

        self.auto_band_check = QCheckBox("Auto-detect band from filename")
        self.auto_band_check.setChecked(True)
        layout.addWidget(self.auto_band_check)

        self.full_sweep_check = QCheckBox("Include full frequency sweep")
        self.full_sweep_check.setChecked(False)
        layout.addWidget(self.full_sweep_check)

        return group

    def create_mapping_section(self):
        """Create band notation mapping section"""
        group = QGroupBox("Band Mapping (Optional)")
        layout = QVBoxLayout(group)

        # Enable mapping checkbox
        self.mapping_enabled_check = QCheckBox("Enable N-plexer bank mapping")
        self.mapping_enabled_check.setToolTip(
            "Convert filename band notation (e.g., B41[CN]) to\n"
            "N-plexer bank notation (e.g., 34_39+41) using JSON mapping file"
        )
        self.mapping_enabled_check.setChecked(False)
        self.mapping_enabled_check.stateChanged.connect(self.on_mapping_enabled_changed)
        layout.addWidget(self.mapping_enabled_check)

        # File selector row
        file_layout = QHBoxLayout()

        self.mapping_file_edit = QLineEdit()
        self.mapping_file_edit.setPlaceholderText("Select JSON mapping file...")
        self.mapping_file_edit.setEnabled(False)
        self.mapping_file_edit.textChanged.connect(self.on_mapping_file_changed)
        file_layout.addWidget(self.mapping_file_edit)

        self.mapping_browse_btn = QPushButton("Browse...")
        self.mapping_browse_btn.setEnabled(False)
        self.mapping_browse_btn.clicked.connect(self.browse_mapping_file)
        file_layout.addWidget(self.mapping_browse_btn)

        layout.addLayout(file_layout)

        # Status label
        self.mapping_status_label = QLabel("Disabled")
        self.mapping_status_label.setStyleSheet("color: gray; font-style: italic;")
        self.mapping_status_label.setWordWrap(True)
        layout.addWidget(self.mapping_status_label)

        return group

    def create_output_section(self):
        """Create output file selection section"""
        group = QGroupBox("Output Location")
        layout = QHBoxLayout(group)

        # Default output path (Desktop)
        desktop = Path.home() / "Desktop" / "RF_Output.csv"

        self.output_path_edit = QLineEdit(str(desktop))
        layout.addWidget(self.output_path_edit)

        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_output)
        layout.addWidget(browse_btn)

        return group

    def create_result_section(self):
        """
        Create result display section
        Always visible with three states:
        1. Empty state (before conversion): Placeholder content
        2. Converting state (during): Progress shown elsewhere, buttons disabled
        3. Complete state (after): Actual results with enabled buttons
        """
        group = QGroupBox("Conversion Results")
        group.setMinimumHeight(250)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        # Result status label
        self.result_status = QLabel()
        result_font = QFont()
        result_font.setPointSize(12)
        result_font.setBold(True)
        self.result_status.setFont(result_font)
        self.result_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_status)
        layout.addSpacing(8)

        # Statistics labels
        self.stats_label = QLabel()
        self.stats_label.setMinimumHeight(80)
        self.stats_label.setWordWrap(True)
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.stats_label)

        layout.addSpacing(8)

        # Action buttons (always visible, enabled/disabled based on state)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        self.open_csv_btn = QPushButton("Open CSV")
        self.open_csv_btn.setMinimumHeight(45)
        self.open_csv_btn.setMinimumWidth(120)
        self.open_csv_btn.clicked.connect(self.open_output_csv)
        button_layout.addWidget(self.open_csv_btn)

        self.open_folder_btn = QPushButton("Open Folder")
        self.open_folder_btn.setMinimumHeight(45)
        self.open_folder_btn.setMinimumWidth(120)
        self.open_folder_btn.clicked.connect(self.open_output_folder)
        button_layout.addWidget(self.open_folder_btn)

        self.convert_more_btn = QPushButton("Convert More")
        self.convert_more_btn.setMinimumHeight(45)
        self.convert_more_btn.setMinimumWidth(120)
        self.convert_more_btn.clicked.connect(self.reset_ui)
        button_layout.addWidget(self.convert_more_btn)

        layout.addLayout(button_layout)

        return group

    def set_result_empty_state(self):
        """
        Set result section to empty state (before conversion)
        Shows placeholder content to make the UI intentional, not broken
        """
        self.result_status.setText("Ready to Convert")
        self.result_status.setStyleSheet("color: #95a5a6;")  # Gray for inactive state

        self.stats_label.setText("Select SnP files and click START CONVERSION to begin")
        self.stats_label.setStyleSheet("color: #7f8c8d;")

        # Disable all action buttons
        self.open_csv_btn.setEnabled(False)
        self.open_folder_btn.setEnabled(False)
        self.convert_more_btn.setEnabled(False)

    def set_result_converting_state(self):
        """
        Set result section to converting state (during conversion)
        Buttons remain disabled, shows processing status
        """
        self.result_status.setText("Converting...")
        self.result_status.setStyleSheet("color: #3498db;")  # Blue for active state

        self.stats_label.setText("Processing files... Please wait")
        self.stats_label.setStyleSheet("color: #7f8c8d;")

        # Keep buttons disabled during conversion
        self.open_csv_btn.setEnabled(False)
        self.open_folder_btn.setEnabled(False)
        self.convert_more_btn.setEnabled(False)

    def set_result_complete_state(self, result):
        """
        Set result section to complete state (after conversion)
        Shows actual results and enables appropriate buttons
        """
        if result.success:
            self.result_status.setText("✅ Conversion Successful!")
            self.result_status.setStyleSheet("color: #27ae60;")  # Green for success

            stats_text = f"""
            <b>Files Processed:</b> {result.files_processed}/{result.total_files}<br>
            <b>Rows Generated:</b> {result.rows_generated:,}<br>
            <b>Output Size:</b> {result.output_size_kb:.1f} KB<br>
            <b>Success Rate:</b> {result.success_rate:.1f}%
            """

            if result.has_errors:
                stats_text += f"<br><b style='color: #e74c3c;'>Errors:</b> {len(result.errors)}"

            self.stats_label.setText(stats_text)
            self.stats_label.setStyleSheet("")

            # Enable all action buttons
            self.open_csv_btn.setEnabled(True)
            self.open_folder_btn.setEnabled(True)
            self.convert_more_btn.setEnabled(True)
        else:
            self.result_status.setText("❌ Conversion Failed")
            self.result_status.setStyleSheet("color: #e74c3c;")  # Red for failure

            stats_text = f"<b>Errors:</b> {len(result.errors)}"
            if result.errors:
                stats_text += "<br><br><b>Error Details:</b><br>"
                for error in result.errors[:5]:  # Show first 5 errors
                    stats_text += f"• {error.get('file', 'Unknown')}: {error.get('error', 'Unknown error')}<br>"

            self.stats_label.setText(stats_text)
            self.stats_label.setStyleSheet("")

            # Enable only "Convert More" button on failure
            self.open_csv_btn.setEnabled(False)
            self.open_folder_btn.setEnabled(False)
            self.convert_more_btn.setEnabled(True)

    def apply_styling(self):
        """Apply modern styling to the application"""
        # Main window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }

            QGroupBox {
                font-weight: bold;
                font-size: 12pt;
                border: 2px solid #dcdde1;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
                background-color: white;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 4px 8px;
                color: #2f3640;
                font-size: 12pt;
            }

            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 11pt;
            }

            QPushButton:hover {
                background-color: #45a049;
            }

            QPushButton:pressed {
                background-color: #3d8b40;
            }

            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }

            QPushButton#start_conversion {
                background-color: #27ae60;
                font-size: 13pt;
            }

            QPushButton#start_conversion:hover {
                background-color: #229954;
            }

            QLineEdit {
                border: 2px solid #dcdde1;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
                font-size: 10pt;
            }

            QLineEdit:focus {
                border-color: #3498db;
            }

            QCheckBox, QRadioButton {
                font-size: 10pt;
                spacing: 8px;
            }

            QProgressBar {
                border: 2px solid #dcdde1;
                border-radius: 6px;
                text-align: center;
                background-color: #ecf0f1;
                height: 30px;
            }

            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 4px;
            }
        """)

        # Set object name for specific styling
        self.convert_btn.setObjectName("start_conversion")

    def connect_signals(self):
        """Connect signals to slots for event handling"""
        self.file_selector.files_changed.connect(self.on_files_changed)
        self.convert_btn.clicked.connect(self.start_conversion)

    def browse_output(self):
        """Open file dialog to select output CSV location"""
        current_path = self.output_path_edit.text()

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Select Output CSV File",
            current_path,
            "CSV Files (*.csv);;All Files (*)"
        )

        if file_path:
            self.output_path_edit.setText(file_path)

    def browse_mapping_file(self):
        """Open file dialog to select JSON mapping file"""
        # Default to mappings directory if exists
        default_dir = Path(__file__).parent.parent / "core" / "mappings"
        if not default_dir.exists():
            default_dir = Path.home()

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select JSON Mapping File",
            str(default_dir),
            "JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            self.mapping_file_edit.setText(file_path)
            # Load mapping immediately
            self.load_mapping_file(file_path)

    def on_mapping_enabled_changed(self, state):
        """Handle mapping enable/disable checkbox state change"""
        is_enabled = (state == Qt.CheckState.Checked.value)

        # Enable/disable controls
        self.mapping_file_edit.setEnabled(is_enabled)
        self.mapping_browse_btn.setEnabled(is_enabled)

        if is_enabled:
            # If file already specified, try to load it
            file_path = self.mapping_file_edit.text()
            if file_path:
                self.load_mapping_file(file_path)
            else:
                self.mapping_status_label.setText("⚠️ Please select a mapping file")
                self.mapping_status_label.setStyleSheet("color: orange; font-style: italic;")
        else:
            # Clear mapping
            self.band_mapper.clear()
            self.mapping_status_label.setText("Disabled")
            self.mapping_status_label.setStyleSheet("color: gray; font-style: italic;")
            self.logger.log_info("Band mapping disabled")

    def on_mapping_file_changed(self, file_path):
        """Handle mapping file path text change"""
        # This is called when text is changed programmatically or by user typing
        # We only auto-load when Browse button is used (handled in browse_mapping_file)
        pass

    def load_mapping_file(self, file_path):
        """Load mapping file and update status"""
        if not file_path:
            return

        success, message = self.band_mapper.load_mapping(file_path)

        if success:
            self.mapping_status_label.setText(message)
            self.mapping_status_label.setStyleSheet("color: green; font-weight: bold;")
            self.logger.log_info(f"Band mapping loaded: {message}")
        else:
            self.mapping_status_label.setText(message)
            self.mapping_status_label.setStyleSheet("color: red; font-weight: bold;")
            self.logger.log_error(f"Band mapping failed: {message}")

            # Show error dialog
            QMessageBox.warning(
                self,
                "Mapping Load Error",
                f"Failed to load mapping file:\n\n{message}\n\n"
                "Please check the file format and try again."
            )

    def on_files_changed(self, files, total_size_mb):
        """Handle file selection changes"""
        self.snp_files = files

        # Enable/disable conversion button based on file selection
        self.convert_btn.setEnabled(len(files) > 0)

        # Update file selector display
        self.file_selector.update_display(len(files), total_size_mb)

    def start_conversion(self):
        """Initiate the conversion process"""
        # Validate inputs
        if not self.snp_files:
            QMessageBox.warning(self, "No Files", "Please select SnP files to convert.")
            return

        output_path = Path(self.output_path_edit.text())

        # Create parent directory if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Prepare conversion options
        options = {
            'freq_filter': self.freq_filter_check.isChecked(),
            'auto_band': self.auto_band_check.isChecked(),
            'full_sweep': self.full_sweep_check.isChecked(),
            'band_mapper': self.band_mapper if self.mapping_enabled_check.isChecked() else None
        }

        # Get measurement type
        measurement_type = 'rx_gain'  # Currently only this is supported

        # Create conversion service
        try:
            self.conversion_service = ConversionService(measurement_type)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to initialize converter: {e}")
            return

        # Update UI state - NO layout changes, only content updates
        self.convert_btn.setEnabled(False)
        self.progress_widget.setVisible(True)
        self.progress_widget.reset()

        # Update result section to converting state (stays visible)
        self.set_result_converting_state()

        # Log conversion start
        self.logger.log_conversion_start(self.snp_files, output_path, options)

        # Create and start worker thread
        self.worker = ConversionWorker(
            self.conversion_service,
            self.snp_files,
            output_path,
            options
        )

        self.worker.progress_updated.connect(self.on_progress_update)
        self.worker.conversion_complete.connect(self.on_conversion_complete)
        self.worker.start()

    def on_progress_update(self, current, total, filename):
        """Handle progress updates from worker thread"""
        # Calculate percentage
        percent = int((current / total) * 100)

        # Update progress widget
        self.progress_widget.update_progress(percent, current, total, filename)

    def on_conversion_complete(self, result):
        """
        Handle conversion completion
        Updates content only, no layout changes
        """
        # Hide progress widget
        self.progress_widget.setVisible(False)

        # Update result section to complete state (already visible)
        self.set_result_complete_state(result)

        # Log conversion completion
        self.logger.log_conversion_complete(result)

        # Re-enable conversion button
        self.convert_btn.setEnabled(True)

        # Clean up worker
        self.worker = None

    def open_output_csv(self):
        """Open the output CSV file in default application"""
        output_path = Path(self.output_path_edit.text())

        if output_path.exists():
            import os
            os.startfile(output_path)
        else:
            QMessageBox.warning(self, "File Not Found", "Output CSV file does not exist.")

    def open_output_folder(self):
        """Open the folder containing the output CSV"""
        output_path = Path(self.output_path_edit.text())

        if output_path.parent.exists():
            import os
            os.startfile(output_path.parent)
        else:
            QMessageBox.warning(self, "Folder Not Found", "Output folder does not exist.")

    def reset_ui(self):
        """Reset UI for another conversion"""
        self.file_selector.clear_files()
        self.progress_widget.reset()

        # Reset to empty state (no visibility changes)
        self.set_result_empty_state()

        self.convert_btn.setEnabled(False)

    def save_settings(self):
        """Save current settings to registry/config file"""
        # Save checkbox states
        self.settings.setValue("freq_filter", self.freq_filter_check.isChecked())
        self.settings.setValue("auto_band", self.auto_band_check.isChecked())
        self.settings.setValue("full_sweep", self.full_sweep_check.isChecked())

        # Save measurement type
        if self.rx_gain_radio.isChecked():
            self.settings.setValue("measurement_type", "rx_gain")
        elif self.tx_power_radio.isChecked():
            self.settings.setValue("measurement_type", "tx_power")
        elif self.isolation_radio.isChecked():
            self.settings.setValue("measurement_type", "isolation")

        # Save last output path
        output_path = self.output_path_edit.text()
        if output_path:
            self.settings.setValue("last_output_path", output_path)
            # Save output directory for next time
            self.settings.setValue("last_output_dir", str(Path(output_path).parent))

        # Save band mapping settings
        self.settings.setValue("mapping_enabled", self.mapping_enabled_check.isChecked())
        self.settings.setValue("mapping_file_path", self.mapping_file_edit.text())

        self.logger.log_info("Settings saved")

    def restore_settings(self):
        """Restore settings from last session"""
        # Restore checkbox states (default to True)
        freq_filter = self.settings.value("freq_filter", True, type=bool)
        auto_band = self.settings.value("auto_band", True, type=bool)
        full_sweep = self.settings.value("full_sweep", False, type=bool)

        self.freq_filter_check.setChecked(freq_filter)
        self.auto_band_check.setChecked(auto_band)
        self.full_sweep_check.setChecked(full_sweep)

        # Restore measurement type
        measurement_type = self.settings.value("measurement_type", "rx_gain", type=str)
        if measurement_type == "rx_gain":
            self.rx_gain_radio.setChecked(True)
        elif measurement_type == "tx_power":
            self.tx_power_radio.setChecked(True)
        elif measurement_type == "isolation":
            self.isolation_radio.setChecked(True)

        # Restore last output directory (for file dialog)
        last_output_dir = self.settings.value("last_output_dir", str(Path.home()), type=str)
        if Path(last_output_dir).exists():
            suggested_filename = f"rx_gain_{Path.home().name}.csv"
            suggested_path = Path(last_output_dir) / suggested_filename
            self.output_path_edit.setText(str(suggested_path))

        # Restore band mapping settings
        mapping_enabled = self.settings.value("mapping_enabled", False, type=bool)
        mapping_file_path = self.settings.value("mapping_file_path", "", type=str)

        self.mapping_enabled_check.setChecked(mapping_enabled)
        if mapping_file_path:
            self.mapping_file_edit.setText(mapping_file_path)
            # Try to load the mapping file if enabled
            if mapping_enabled and Path(mapping_file_path).exists():
                self.load_mapping_file(mapping_file_path)

        self.logger.log_info("Settings restored")

    def closeEvent(self, event):
        """Override close event to save settings before exit"""
        self.save_settings()
        self.logger.log_info("Application closed")
        event.accept()
