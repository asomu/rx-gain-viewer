"""
PyQt6 GUI for RF SnP to CSV Converter
"""

# Lazy import to avoid importing PyQt6 at package level
# This allows rf_converter package to be imported without PyQt6 installed
__all__ = ['MainWindow']

def __getattr__(name):
    """Lazy import for MainWindow"""
    if name == 'MainWindow':
        from .main_window import MainWindow
        return MainWindow
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
