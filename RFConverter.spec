# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['rf_converter\\ui_pyqt6\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('rf_converter/icon.ico', '.'), ('rf_converter/core/mappings', 'core/mappings')],
    hiddenimports=['PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets', 'pandas', 'numpy', 'rf_converter.core', 'rf_converter.core.services.conversion_service', 'rf_converter.core.logger', 'rf_converter.core.band_mapper', 'rf_converter.core.parsers.base_parser', 'rf_converter.core.parsers.rx_parser', 'rf_converter.core.parsers.snp_reader', 'rf_converter.core.converters.csv_writer', 'rf_converter.core.models.conversion_result', 'rf_converter.ui_pyqt6', 'rf_converter.ui_pyqt6.widgets', 'rf_converter.ui_pyqt6.widgets.file_selector', 'rf_converter.ui_pyqt6.widgets.progress_widget'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='RFConverter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['rf_converter\\icon.ico'],
)
