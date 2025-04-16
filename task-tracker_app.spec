import os
from pathlib import Path

# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/task-tracker_app.py'],
    pathex=[os.path.abspath('.')],
    binaries=[],
    datas=[
        ('resources/th-1828655096.ico', 'resources'),
        ('resources/crumpled-paper-1-1969922722.jpg', 'resources'),
    ],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='task-tracker_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='task-tracker_app',
)
