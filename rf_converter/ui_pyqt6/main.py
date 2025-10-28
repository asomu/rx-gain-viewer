"""
RF SnP to CSV Converter - PyQt6 GUI Application
Entry point for the desktop application
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# Add parent directory to path for core module import
sys.path.insert(0, str(Path(__file__).parent.parent))

from main_window import MainWindow


def main():
    """Application entry point"""
    # Enable high DPI scaling for modern displays
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("RF SnP to CSV Converter")
    app.setOrganizationName("RF Analyzer")

    # Set application icon (for taskbar)
    icon_path = Path(__file__).parent.parent / "icon.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    # Create and show main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
