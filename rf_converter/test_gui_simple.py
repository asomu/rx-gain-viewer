"""
Test script for PyQt6 GUI application - ASCII only
Validates that all components can be imported and instantiated
"""

import sys
from pathlib import Path

# Add ui_pyqt6 to path
sys.path.insert(0, str(Path(__file__).parent / 'ui_pyqt6'))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")

    try:
        from PyQt6.QtWidgets import QApplication
        print("[OK] PyQt6.QtWidgets imported")
    except ImportError as e:
        print(f"[FAIL] Failed to import PyQt6.QtWidgets: {e}")
        return False

    try:
        from core import ConversionService, ConversionResult
        print("[OK] Core module imported")
    except ImportError as e:
        print(f"[FAIL] Failed to import core module: {e}")
        return False

    try:
        from widgets.file_selector import FileSelector
        print("[OK] FileSelector widget imported")
    except ImportError as e:
        print(f"[FAIL] Failed to import FileSelector: {e}")
        return False

    try:
        from widgets.progress_widget import ProgressWidget
        print("[OK] ProgressWidget imported")
    except ImportError as e:
        print(f"[FAIL] Failed to import ProgressWidget: {e}")
        return False

    try:
        from main_window import MainWindow
        print("[OK] MainWindow imported")
    except ImportError as e:
        print(f"[FAIL] Failed to import MainWindow: {e}")
        return False

    return True


def test_instantiation():
    """Test that main components can be instantiated"""
    print("\nTesting component instantiation...")

    from PyQt6.QtWidgets import QApplication

    # Create QApplication (required for Qt widgets)
    app = QApplication([])

    try:
        from main_window import MainWindow
        window = MainWindow()
        print("[OK] MainWindow created successfully")

        # Check key attributes
        assert hasattr(window, 'file_selector'), "Missing file_selector"
        assert hasattr(window, 'progress_widget'), "Missing progress_widget"
        assert hasattr(window, 'convert_btn'), "Missing convert_btn"
        print("[OK] All required attributes present")

        return True
    except Exception as e:
        print(f"[FAIL] Failed to create MainWindow: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_core_integration():
    """Test integration with core module"""
    print("\nTesting core module integration...")

    try:
        from core import ConversionService

        # Create service
        service = ConversionService('rx_gain')
        print("[OK] ConversionService created")

        # Check methods
        assert hasattr(service, 'convert_files'), "Missing convert_files method"
        assert hasattr(service, 'validate_files'), "Missing validate_files method"
        print("[OK] Required methods present")

        # Test with sample files
        target_folder = Path(r'C:/Project/html_exporter/target')
        if target_folder.exists():
            snp_files = list(target_folder.glob('*.s2p'))[:3]
            if snp_files:
                validation = service.validate_files(snp_files)
                print(f"[OK] File validation works: {validation['file_count']} valid files")
            else:
                print("[WARN] No .s2p files found for testing")
        else:
            print("[WARN] Target folder not found for testing")

        return True
    except Exception as e:
        print(f"[FAIL] Core integration test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("RF SnP to CSV Converter - PyQt6 GUI Test Suite")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Import Test", test_imports()))
    results.append(("Instantiation Test", test_instantiation()))
    results.append(("Core Integration Test", test_core_integration()))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        print(f"{test_name}: {status}")

    all_passed = all(result for _, result in results)

    print("\n" + "=" * 60)
    if all_passed:
        print("SUCCESS: All tests passed! Application is ready to run.")
        print("\nTo launch the GUI, run:")
        print("  python ui_pyqt6/main.py")
        print("  or")
        print("  run_gui.bat")
    else:
        print("WARNING: Some tests failed. Please check the errors above.")

    print("=" * 60)

    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
