import sys
import os
from cx_Freeze import setup, Executable

files = ['requirements.txt', 'conexion.py', 'dashboard.py', 'data.py', 'sort.py']

exe = Executable(script="ContadorCTPv2.py", base="Win32GUI")


class recursion_depth:
    def __init__(self, limit):
        self.limit = limit
        self.default_limit = sys.getrecursionlimit()

    def __enter__(self):
        sys.setrecursionlimit(self.limit)

    def __exit__(self, type, value, traceback):
        sys.setrecursionlimit(self.default_limit)


def setup_():
    setup(
        name="Contador de Personas | Tiendas Cortitelas",
        version="0.1",
        author="Tania Villanueva",
        options={'build_exe': {'include_files': files}},
        executables=[exe]
    )


with recursion_depth(5000):
    setup_()
