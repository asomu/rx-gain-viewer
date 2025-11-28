# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for RF Converter
Optimized for single-file exe with icon and minimal size
"""

import sys
from pathlib import Path

block_cipher = None

# Project paths
project_root = Path('.').absolute()
rf_converter_path = project_root / 'rf_converter'

# Data files to include
datas = [
    # Icon file
    (str(rf_converter_path / 'icon.ico'), '.'),
    # Mapping examples (optional, user can create their own)
    (str(rf_converter_path / 'core' / 'mappings'), 'core/mappings'),
]

# Hidden imports that PyInstaller might miss
hiddenimports = [
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'pandas',
    'numpy',
    'pathlib',
    'json',
    'logging',
]

a = Analysis(
    [str(rf_converter_path / 'ui_pyqt6' / 'main.py')],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'tkinter',
        'matplotlib',
        'IPython',
        'jupyter',
        'notebook',
        'PIL',
        'scipy',
        'pytest',
        'unittest',
        'test',
        'tests',
        'setuptools',
        'distutils',
        # Exclude Django since it's not used in the exe
        'django',
        'sqlalchemy',
        'sphinx',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove duplicate files to reduce size
a.datas = list({tuple(map(str, t)) for t in a.datas})

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='RF_Converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,  # Keep False for Windows
    upx=True,  # Enable UPX compression for smaller size
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (GUI app)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(rf_converter_path / 'icon.ico'),  # Application icon
    version_file=None,
    # Optimization flags
    optimize=2,  # Maximum Python optimization
)
