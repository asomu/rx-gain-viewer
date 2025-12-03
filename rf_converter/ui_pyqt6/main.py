"""
RF SnP to CSV Converter - PyQt6 GUI Application
Entry point for the desktop application
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt, QLockFile, QStandardPaths
from PyQt6.QtGui import QIcon

# Windows taskbar icon support
import ctypes

# Use absolute imports for PyInstaller compatibility
from rf_converter.ui_pyqt6.main_window import MainWindow


def main():
    """Application entry point"""
    # Windows taskbar icon: Set AppUserModelID BEFORE QApplication creation
    # This ensures Windows uses our custom icon instead of Python's default
    if sys.platform == 'win32':
        try:
            # AppUserModelID format: CompanyName.ProductName.SubProduct.VersionInformation
            myappid = 'RFAnalyzer.RFConverter.Desktop.1'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

            # Note: Windows icon cache issues may still occur due to OS-level caching.
            # Workaround: Right-click taskbar icon → "Pin to taskbar" for persistence.
            # See: https://github.com/pyinstaller/pyinstaller/issues/1430
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

    # Single instance check using secure app-specific directory
    # Use AppLocalDataLocation instead of system temp for security
    lock_dir = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.AppLocalDataLocation
    )
    lock_file_path = Path(lock_dir) / "RFConverter.lock"

    # Ensure directory exists
    lock_file_path.parent.mkdir(parents=True, exist_ok=True)

    lock_file = QLockFile(str(lock_file_path))

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
