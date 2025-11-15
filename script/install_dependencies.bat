@echo off
echo ============================================
echo   Instalador automatico de dependencias
echo ============================================
echo.

echo Actualizando pip...
python -m pip install --upgrade pip

echo Instalando customtkinter...
pip install customtkinter

echo Instalando mysql-connector-python...
pip install mysql-connector-python

echo Instalando pillow...
pip install pillow

echo.
echo ============================================
echo   Instalación completada
echo ============================================
pause
