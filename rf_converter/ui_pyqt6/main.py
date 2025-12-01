"""
RF SnP to CSV Converter - PyQt6 GUI Application
Entry point for the desktop application
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt, QLockFile, QDir
from PyQt6.QtGui import QIcon

# Windows taskbar icon support
import ctypes

# Use absolute imports for PyInstaller compatibility
from rf_converter.ui_pyqt6.main_window import MainWindow


def main():
    """Application entry point"""
    # Windows taskbar icon fix: Set AppUserModelID
    # This ensures Windows uses our custom icon instead of Python's default
    if sys.platform == 'win32':
        try:
            # AppUserModelID format: CompanyName.ProductName.SubProduct.VersionInformation
            myappid = 'RFAnalyzer.RFConverter.Desktop.1'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass  # Non-critical, just continue

    # Enable high DPI scaling for modern displays
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("RF Converter")
    app.setOrganizationName("RF Analyzer")

    # Set application-level icon for consistent taskbar display
    # Store icon as persistent reference to prevent garbage collection
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller bundle
        icon_path = Path(sys._MEIPASS) / "icon.ico"
    else:
        # Running from source
        icon_path = Path(__file__).parent.parent / "icon.ico"

    if icon_path.exists():
        app_icon = QIcon(str(icon_path))
        app.setWindowIcon(app_icon)
        # Keep reference alive for app lifetime (prevents garbage collection)
        app.app_icon = app_icon

    # Single instance check
    lock_file_path = QDir.temp().filePath("RFConverter.lock")
    lock_file = QLockFile(lock_file_path)

    if not lock_file.tryLock(100):
        # Already running
        QMessageBox.warning(
            None,
            "이미 실행 중",
            "RF Converter가 이미 실행 중입니다.",
            QMessageBox.StandardButton.Ok
        )
        sys.exit(0)

    # Create and show main window
    # Note: Window icon is set in MainWindow.__init__() for PyInstaller compatibility
    window = MainWindow()

    window.show()

    try:
        return app.exec()
    finally:
        # Release lock file on exit
        lock_file.unlock()


if __name__ == '__main__':
    main()
