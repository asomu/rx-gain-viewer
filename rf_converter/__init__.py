"""
RF Converter - S-parameter to CSV Converter with 3GPP Band Mapping

A PyQt6 desktop application for converting RF S-parameter files to CSV
with automatic 3GPP band detection and filtering.
"""

__version__ = "1.1.0"
__app_name__ = "RF Converter"

try:
    from importlib.metadata import version
    __version__ = version("rf-converter")
except Exception:
    # Fallback to hardcoded version if package not installed
    pass

__all__ = ["__version__", "__app_name__"]
