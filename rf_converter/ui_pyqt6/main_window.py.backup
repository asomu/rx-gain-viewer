"""
Main Window for RF SnP to CSV Converter
Professional PyQt6 UI with modern design
"""

from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QLabel, QRadioButton, QCheckBox, QLineEdit,
    QProgressBar, QFileDialog, QMessageBox, QButtonGroup
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

from core import ConversionService, ConversionResult
from widgets.file_selector import FileSelector
from widgets.progress_widget import ProgressWidget


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
    """

    def __init__(self):
        super().__init__()
        self.snp_files = []
        self.conversion_service = None
        self.worker = None

        self.setup_ui()
        self.apply_styling()
        self.connect_signals()

    def setup_ui(self):
        """Initialize UI components and layouts"""
        self.setWindowTitle("RF SnP to CSV Converter")
        self.setMinimumSize(750, 1050)
        self.setMinimumSize(750, 1050)

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(24, 24, 24, 24)

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
        main_layout.addSpacing(15)

        # Measurement type selection
        measurement_group = self.create_measurement_section()
        main_layout.addWidget(measurement_group)
        main_layout.addSpacing(15)

        # Options panel
        options_group = self.create_options_section()
        main_layout.addWidget(options_group)
        main_layout.addSpacing(15)

        # Output selection
        output_group = self.create_output_section()
        main_layout.addWidget(output_group)
        main_layout.addSpacing(15)

        # Conversion button
        self.convert_btn = QPushButton("START CONVERSION")
        self.convert_btn.setMinimumHeight(50)
        self.convert_btn.setEnabled(False)
        main_layout.addWidget(self.convert_btn)

        # Progress display
        self.progress_widget = ProgressWidget()
        self.progress_widget.setVisible(False)
        main_layout.addWidget(self.progress_widget)

        # Result section (initially hidden)
        self.result_widget = self.create_result_section()
        self.result_widget.setVisible(False)
        main_layout.addWidget(self.result_widget)

        # Add stretch at bottom to push everything up
        main_layout.addStretch()

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
        """Create result display section"""
        group = QGroupBox("Conversion Results")
        group.setMinimumHeight(280)
        layout = QVBoxLayout(group)

        # Result status label
        self.result_status = QLabel()
        result_font = QFont()
        result_font.setPointSize(12)
        result_font.setBold(True)
        self.result_status.setFont(result_font)
        layout.addWidget(self.result_status)
        layout.addSpacing(10)

        # Statistics labels
        self.stats_label = QLabel()
        self.stats_label.setMinimumHeight(80)
        self.stats_label.setWordWrap(True)
        layout.addWidget(self.stats_label)

        # Action buttons
        button_layout = QHBoxLayout()

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

    def apply_styling(self):
        """Apply modern styling to the application"""
        # Main window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }

            QGroupBox {
                font-weight: bold;
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
            'full_sweep': self.full_sweep_check.isChecked()
        }

        # Get measurement type
        measurement_type = 'rx_gain'  # Currently only this is supported

        # Create conversion service
        try:
            self.conversion_service = ConversionService(measurement_type)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to initialize converter: {e}")
            return

        # Update UI state
        self.convert_btn.setEnabled(False)
        self.progress_widget.setVisible(True)
        self.progress_widget.reset()
        self.result_widget.setVisible(False)

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
        """Handle conversion completion"""
        # Hide progress widget
        self.progress_widget.setVisible(False)

        # Show result widget
        self.result_widget.setVisible(True)

        # Update result display
        if result.success:
            self.result_status.setText("✅ Conversion Successful!")
            self.result_status.setStyleSheet("color: #27ae60;")

            stats_text = f"""
            <b>Files Processed:</b> {result.files_processed}/{result.total_files}<br>
            <b>Rows Generated:</b> {result.rows_generated:,}<br>
            <b>Output Size:</b> {result.output_size_kb:.1f} KB<br>
            <b>Success Rate:</b> {result.success_rate:.1f}%
            """

            if result.has_errors:
                stats_text += f"<br><b style='color: #e74c3c;'>Errors:</b> {len(result.errors)}"
        else:
            self.result_status.setText("❌ Conversion Failed")
            self.result_status.setStyleSheet("color: #e74c3c;")

            stats_text = f"<b>Errors:</b> {len(result.errors)}"
            if result.errors:
                stats_text += "<br><br><b>Error Details:</b><br>"
                for error in result.errors[:5]:  # Show first 5 errors
                    stats_text += f"• {error.get('file', 'Unknown')}: {error.get('error', 'Unknown error')}<br>"

        self.stats_label.setText(stats_text)

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
        self.result_widget.setVisible(False)
        self.convert_btn.setEnabled(False)
