"""
Progress Widget
Real-time conversion progress display
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QGroupBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ProgressWidget(QGroupBox):
    """
    Custom widget for displaying conversion progress
    Shows progress bar, file counter, and current file being processed
    """

    def __init__(self):
        super().__init__("Conversion Progress")
        self.setup_ui()

    def setup_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        layout.addWidget(self.progress_bar)

        # File counter label
        self.counter_label = QLabel("Processing files...")
        self.counter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        counter_font = QFont()
        counter_font.setPointSize(11)
        counter_font.setBold(True)
        self.counter_label.setFont(counter_font)
        layout.addWidget(self.counter_label)

        # Current file label
        self.current_file_label = QLabel("")
        self.current_file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.current_file_label.setStyleSheet("color: #7f8c8d; font-size: 9pt;")
        self.current_file_label.setWordWrap(True)
        layout.addWidget(self.current_file_label)

    def update_progress(self, percent, current, total, filename):
        """
        Update progress display

        Args:
            percent: Progress percentage (0-100)
            current: Current file number
            total: Total number of files
            filename: Name of file being processed
        """
        # Update progress bar
        self.progress_bar.setValue(percent)

        # Update counter
        self.counter_label.setText(f"Processing {current}/{total} files...")

        # Update current file (truncate if too long)
        if len(filename) > 60:
            display_name = filename[:30] + "..." + filename[-27:]
        else:
            display_name = filename

        self.current_file_label.setText(f"Current: {display_name}")

    def reset(self):
        """Reset progress display to initial state"""
        self.progress_bar.setValue(0)
        self.counter_label.setText("Processing files...")
        self.current_file_label.setText("")
