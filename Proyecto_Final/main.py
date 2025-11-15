# main.py

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vista.login import abrir_login

if __name__ == "__main__":
    abrir_login()