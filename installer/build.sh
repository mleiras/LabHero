#!/usr/bin/env bash
# Build LabHero with PyInstaller.
# Usage from repo root:
#   ./installer/build.sh            # incremental build
#   ./installer/build.sh --clean    # wipe dist/ and build/ first
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Locate the venv Python (Windows uses Scripts/, Unix uses bin/)
if [[ -x ".venv/Scripts/python.exe" ]]; then
    PY=".venv/Scripts/python.exe"
elif [[ -x ".venv/bin/python" ]]; then
    PY=".venv/bin/python"
else
    echo "[build] venv Python not found. Run scripts/setup.ps1 first." >&2
    exit 1
fi

echo "[build] Installing build deps..."
"$PY" -m pip install -q -r installer/requirements-build.txt

if [[ "${1:-}" == "--clean" ]]; then
    echo "[build] Cleaning dist/ and build/..."
    rm -rf dist build
fi

echo "[build] Running PyInstaller..."
"$PY" -m PyInstaller --noconfirm --clean installer/labhero.spec

if [[ -f "dist/LabHero/LabHero.exe" ]]; then
    EXE="dist/LabHero/LabHero.exe"
elif [[ -f "dist/LabHero/LabHero" ]]; then
    EXE="dist/LabHero/LabHero"
else
    echo "[build] Build finished but no LabHero binary in dist/" >&2
    exit 1
fi

BUNDLE_MB=$(du -sm "dist/LabHero" | cut -f1)
echo "[build] Done. $EXE  (bundle: ${BUNDLE_MB} MB)"
