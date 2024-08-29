# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['WallpaperOS.py'],
    pathex=[],
    binaries=[('Back.png', '.'), ('loading.gif', '.'), ('Lock.png', '.'), ('Select_Image.png', '.'), ('tray_icon.png', '.'), ('tray_icon_light.png', '.'), ('Unlock.png', '.'), ('Yesterday.png', '.')],
    datas=[],
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
    name='WallpaperOS',
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
    icon=['WallpaperOS.ico'],
)
