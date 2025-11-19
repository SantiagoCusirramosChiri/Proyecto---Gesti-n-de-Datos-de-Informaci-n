import os
import sys

def ruta_recurso(rel_path):
    try:
        base_path = sys._MEIPASS  # Carpeta temporal donde PyInstaller descomprime
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))  # Modo normal
    return os.path.join(base_path, rel_path)
