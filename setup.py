import sys
import os
from cx_Freeze import setup, Executable

files = [ 'requirements.txt', 'conexion.py', 'Fondo.png', 'sort.py']

exe = Executable(script="ContadorCTP.py", base="Win32GUI")

setup(
    name="Contador de Personas | Tiendas Cortitelas",
    version="0.1",
    author="Tania Villanueva",
    options={'build_exe': {'include_files': files}},
    executables=[exe]
)
