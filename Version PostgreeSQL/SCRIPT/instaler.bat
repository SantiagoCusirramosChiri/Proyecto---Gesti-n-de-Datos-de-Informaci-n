@echo off
chcp 65001 >nul
title Instalador de Dependencias Python
echo ========================================
echo    INSTALADOR AUTOMATICO DE PAQUETES
echo ========================================
echo.

echo Instalando paquetes Python...
echo.

echo [1/5] Instalando psycopg2...
pip install psycopg2
if %errorlevel% neq 0 (
    echo Error al instalar psycopg2
    pause
    exit /b 1
)

echo.
echo [2/5] Instalando sqlalchemy...
pip install sqlalchemy
if %errorlevel% neq 0 (
    echo Error al instalar sqlalchemy
    pause
    exit /b 1
)

echo.
echo [3/5] Instalando customtkinter...
pip install customtkinter
if %errorlevel% neq 0 (
    echo Error al instalar customtkinter
    pause
    exit /b 1
)

echo.
echo [4/5] Instalando pillow...
pip install pillow
if %errorlevel% neq 0 (
    echo Error al instalar pillow
    pause
    exit /b 1
)

echo.
echo [5/5] Instalando ttkbootstrap...
pip install ttkbootstrap
if %errorlevel% neq 0 (
    echo Error al instalar ttkbootstrap
    pause
    exit /b 1
)

echo.
echo ========================================
echo    INSTALACION COMPLETADA EXITOSAMENTE
echo ========================================
echo.
echo Paquetes instalados:
echo   - psycopg2
echo   - sqlalchemy
echo   - customtkinter
echo   - pillow
echo   - ttkbootstrap
echo.
pause