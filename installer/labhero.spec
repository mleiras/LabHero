# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for LabHero
# Run from repo root:
#   Windows: py -m PyInstaller --noconfirm --clean installer/labhero.spec
#   macOS:   python -m PyInstaller --noconfirm --clean installer/labhero.spec

import os
import sys
from PyInstaller.utils.hooks import collect_all, collect_submodules

# Paths in this spec are resolved relative to the spec file's directory, so we
# anchor everything to the project root one level up.
PROJ = os.path.dirname(SPECPATH)
IS_MACOS = sys.platform == 'darwin'

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
    (os.path.join(PROJ, 'LabHero-icon.png'), '.'),
]

# Pick the platform's native icon format. .icns is generated at build time on
# macOS (see .github/workflows/macos-build.yml); .ico is checked in for Windows.
if IS_MACOS:
    icon_path = os.path.join(PROJ, 'LabHero.icns')
else:
    icon_path = os.path.join(PROJ, 'LabHero.ico')

# target_arch is only honoured on macOS. We set it from an env var so CI can
# pin the Mach-O header to arm64 or x86_64 matching the runner's native arch.
target_arch = os.environ.get('PYI_TARGET_ARCH') if IS_MACOS else None

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
    target_arch=target_arch,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
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

# On macOS, wrap the collected output in a .app bundle so users get the
# expected double-clickable application instead of a folder of files.
if IS_MACOS:
    app = BUNDLE(
        coll,
        name='LabHero.app',
        icon=icon_path,
        bundle_identifier='io.github.mleiras.labhero',
        info_plist={
            'NSHighResolutionCapable': True,
            'CFBundleShortVersionString': '0.1.0',
            'CFBundleVersion': '0.1.0',
            'LSMinimumSystemVersion': '11.0',
            'NSHumanReadableCopyright': 'Copyright (c) 2024-2026 Monica Leiras. CC BY-SA 4.0.',
        },
    )
