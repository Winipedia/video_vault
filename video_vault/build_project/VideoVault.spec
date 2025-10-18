# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
import winipedia_utils
from video_vault.core.consts import APP_NAME
import video_vault

# Get the project root directory from video_vault package
project_root = Path(video_vault.__file__).parent.parent

# Get winipedia_utils package path
winipedia_utils_path = Path(winipedia_utils.__file__).parent

a = Analysis(
    [str(project_root / 'video_vault' / 'main.py')],
    pathex=[],
    binaries=[],
    datas=[
        # Include migrations
        (str(project_root / 'video_vault' / 'db' / 'migrations'), 'video_vault/db/migrations'),
        # Include SVG resources from winipedia_utils
        (str(winipedia_utils_path / 'resources' / 'svgs'), 'winipedia_utils/resources/svgs'),
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
    a.binaries,
    a.datas,
    [],
    name=APP_NAME,
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
    icon=str(project_root / 'video_vault' / 'build_project' / 'app_icon.ico'),
)







