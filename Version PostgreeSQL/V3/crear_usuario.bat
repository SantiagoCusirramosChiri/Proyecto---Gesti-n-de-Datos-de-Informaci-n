@echo off
chcp 65001 >nul
echo ====================================
echo CREAR USUARIO LOLCITO
echo ====================================
echo.

:: Buscar automáticamente la ruta de PostgreSQL
set PGPATH=
for /d %%i in ("C:\Program Files\PostgreSQL\*") do (
    if exist "%%i\bin\psql.exe" set PGPATH=%%i\bin
)

if "%PGPATH%"=="" (
    echo ✗ No se encontró PostgreSQL instalado
    exit /b 1
)

echo [INFO] Usando PostgreSQL en: %PGPATH%
echo.

echo [1/5] Terminando conexiones activas...
"%PGPATH%\psql.exe" -U postgres -h localhost -p 5432 -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'sistema_documentos' AND pid <> pg_backend_pid();" >nul 2>&1

echo [2/5] Eliminando base de datos (si existe)...
"%PGPATH%\psql.exe" -U postgres -h localhost -p 5432 -c "DROP DATABASE IF EXISTS sistema_documentos;" >nul 2>&1

echo [3/5] Eliminando usuario (si existe)...
"%PGPATH%\psql.exe" -U postgres -h localhost -p 5432 -c "DROP USER IF EXISTS lolcito;" >nul 2>&1

echo [4/5] Creando usuario lolcito...
"%PGPATH%\psql.exe" -U postgres -h localhost -p 5432 -c "CREATE USER lolcito WITH PASSWORD '12345678' SUPERUSER CREATEDB CREATEROLE;"

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ✗ Error al crear el usuario
    exit /b 1
)

echo [5/5] Usuario creado exitosamente
echo.
echo ✓ Usuario 'lolcito' creado exitosamente
exit /b 0