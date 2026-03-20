# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Conversor TOTVS - Production Build
# Professional desktop application with licensing and updates

import os
import sys
from pathlib import Path

# Get the application directory
app_dir = Path(SPECPATH).absolute()

# Application metadata
app_name = 'ConversorTOTVS'
app_version = '2.0.0'
app_author = 'Fa Maringa'
company_name = 'FA MARINGA LTDA'

# Add project root to Python path for imports
project_root = app_dir
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

block_cipher = None

a = Analysis(
    ['app/main.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tkinterdnd2',
        'app',
        'core',
        'services', 
        'ui',
        'utils',
        'core.parsers',
        'core.converter_engine',
        'core.exceptions',
        'services.license_service',
        'services.update_service',
        'ui.dialogs',
        'ui.ui_components',
        'utils.config_service',
        'utils.logger',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'PIL',
        'cv2',
        'jupyter',
        'notebook',
        'pytest',
        'sphinx',
        'django',
        'flask',
    ],
    noarchive=False,
    optimize=2,  # Optimize bytecode
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,  # Desabilitar strip
    upx=False,    # Desabilitar UPX
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(app_dir / 'logo.ico') if (app_dir / 'logo.ico').exists() else None,
)

# Optional: Create installer script (uncomment if needed)
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name=app_name
# )
