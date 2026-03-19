# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Conversor TOTVS
# Production-ready configuration

import os
from pathlib import Path

# Get the application directory
app_dir = Path(SPECPATH).absolute()

# Application metadata
app_name = 'ConversorTOTVS'
app_version = '1.1.0'
app_author = 'Fa Maringa'
company_name = 'FA MARINGA LTDA'

block_cipher = None

a = Analysis(
    ['main_app.py'],
    pathex=[str(app_dir)],
    binaries=[],
    datas=[
        # Include logo files if they exist
        (str(app_dir / 'logo.png'), '.') if (app_dir / 'logo.png').exists() else None,
        (str(app_dir / 'logo.gif'), '.') if (app_dir / 'logo.gif').exists() else None,
    ],
    hiddenimports=[
        'tkinterdnd2',
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
    ],
    noarchive=False,
    optimize=2,  # Optimize bytecode
)

# Remove None entries from datas
a.datas = [item for item in a.datas if item is not None]

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
    strip=True,  # Strip debug symbols
    upx=True,   # Use UPX compression
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(app_dir / 'logo.ico') if (app_dir / 'logo.ico').exists() else None,
    version=f'''
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({app_version.replace('.', ',')}, 0),
    prodvers=({app_version.replace('.', ',')}, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', company_name),
        StringStruct(u'FileDescription', 'Conversor TXT para CSV - TOTVS'),
        StringStruct(u'FileVersion', app_version),
        StringStruct(u'InternalName', app_name),
        StringStruct(u'LegalCopyright', f'© {Path(__file__).stat().st_mtime.year} {company_name}'),
        StringStruct(u'OriginalFilename', f'{app_name}.exe'),
        StringStruct(u'ProductName', 'Conversor TOTVS'),
        StringStruct(u'ProductVersion', app_version)])
      ])
  ,
  VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
)
