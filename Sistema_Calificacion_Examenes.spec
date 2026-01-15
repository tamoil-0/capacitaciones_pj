# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# Archivos de datos que deben incluirse en el EXE
datas = [
    ('poppler', 'poppler'),           # Poppler para procesar PDFs
    ('config.py', '.'),               # Configuración de la API
    ('api_client.py', '.'),           # Cliente de API Laravel
]

binaries = []

# Imports ocultos necesarios
hiddenimports = [
    'PIL._tkinter_finder',
    'customtkinter',
    'cv2',
    'numpy',
    'pdf2image',
    'reportlab',
    'reportlab.pdfgen',
    'reportlab.lib',
    'reportlab.lib.pagesizes',
    'reportlab.lib.units',
    'reportlab.lib.colors',
    'reportlab.lib.utils',
    'reportlab.pdfbase',
    'requests',
    'urllib3',
    'json',
    'datetime',
]

# Recolectar todos los archivos de customtkinter
tmp_ret = collect_all('customtkinter')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['completo.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['torch', 'tensorflow', 'tensorboard', 'ultralytics', 'pygame', 'matplotlib', 'scipy', 'pandas', 'sklearn', 'jinja2', 'notebook', 'IPython', 'jupyter'],
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
    name='Sistema_Calificacion_Examenes',
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
)
