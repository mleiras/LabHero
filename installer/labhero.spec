# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for LabHero
# Run from repo root: py -m PyInstaller --noconfirm --clean installer/labhero.spec

import os
from PyInstaller.utils.hooks import collect_all, collect_submodules

# Paths in this spec are resolved relative to the spec file's directory, so we
# anchor everything to the project root one level up.
PROJ = os.path.dirname(SPECPATH)

datas = []
binaries = []
hiddenimports = []

# Packages with dynamic imports / data files that PyInstaller cannot fully
# discover by static analysis. collect_all grabs submodules, data files, and
# binary extensions in one go. numpy is included explicitly to ensure a single
# coherent copy is bundled (avoids the NumPy 2.x "cannot load module more
# than once per process" error under PyInstaller).
for pkg in ('numpy', 'mewpy', 'cobra', 'optlang', 'reframed', 'libsbml', 'swiglpk'):
    d, b, h = collect_all(pkg)
    datas += d
    binaries += b
    hiddenimports += h

# These two are pulled in indirectly by mewpy and use dynamic imports.
hiddenimports += collect_submodules('inspyred')
hiddenimports += collect_submodules('jmetalpy')

# Game assets bundled as read-only resources. (source_path, dest_inside_bundle)
datas += [
    (os.path.join(PROJ, 'graphics'), 'graphics'),
    (os.path.join(PROJ, 'audio'), 'audio'),
    (os.path.join(PROJ, 'font'), 'font'),
    (os.path.join(PROJ, 'data'), 'data'),
    (os.path.join(PROJ, 'code', 'player_history', 'mission01.txt'), 'code/player_history'),
]

a = Analysis(
    [os.path.join(PROJ, 'LabHero.py')],
    pathex=[os.path.join(PROJ, 'code')],  # so 'from settings import *' etc. resolve inside code/
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'PyQt5', 'PyQt6', 'PySide2', 'PySide6',
        'IPython', 'jupyter', 'notebook',
        'pytest',
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='LabHero',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
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
    upx=False,
    upx_exclude=[],
    name='LabHero',
)
