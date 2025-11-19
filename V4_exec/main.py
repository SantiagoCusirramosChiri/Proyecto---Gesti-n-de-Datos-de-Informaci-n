# main.py

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vista.mysql_config import abrir_config_mysql

if __name__ == "__main__":
    abrir_config_mysql()