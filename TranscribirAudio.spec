# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'kivy.deps.angle',
        'kivy.deps.glew',
        'kivy.deps.sdl2',
        'speech_recognition',
        'pydub',
        'kivy.core.window',
        'kivy.core.audio',
        'kivy.core.clipboard',
        'kivy.uix.popup',
        'kivy.uix.gridlayout',
        'kivy.clock',
        'threading'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'PIL',
        'matplotlib',
        'numpy',
        'scipy'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TranscribirAudio',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False para interfaz gráfica
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None  # Puedes agregar un icono aquí si lo tienes
)