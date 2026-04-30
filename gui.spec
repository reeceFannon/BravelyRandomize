# -*- mode: python -*-

block_cipher = None

a = Analysis(
    [
        'gui.py',
        'src/Classes.py',
        'src/Utilities.py',
    ],
    pathex=[],
    binaries=[],
    datas=[
        ('json/*.json', 'json'),
        ('imgs/BD/Portraits/*', 'imgs/BD/Portraits'),
        ('imgs/BD/Icons/*', 'imgs/BD/Icons'),
        ('imgs/BS/Portraits/*', 'imgs/BS/Portraits'),
        ('imgs/BS/Icons/*', 'imgs/BS/Icons'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
    name='mybuild'
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BravelyRandomize.exe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False
)
