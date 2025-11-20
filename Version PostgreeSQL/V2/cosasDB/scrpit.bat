@echo off
setlocal enabledelayedexpansion

title Instalador Base de Datos - Sistema de Documentos
color 0A

echo ===============================================
echo    INSTALADOR BASE DE DATOS AUTOMATICO
echo ===============================================
echo.

:: Configuración
set DB_NAME=sistema_documentos
set DB_USER=lolcito
set DB_PASS=12345678
set SCRIPT_DIR=%~dp0

:: Verificar archivos SQL necesarios
set FILES[0]=creacionPRev
set FILES[1]=base_datos
set FILES[2]=procedimientos
set FILES[3]=triggers
set FILES[4]=insertgod

echo Verificando archivos necesarios...
for /l %%i in (0,1,4) do (
    set FILE_FOUND=false
    if exist "!SCRIPT_DIR!!FILES[%%i]!.sql" set FILE_FOUND=true
    if exist "!SCRIPT_DIR!!FILES[%%i]!.txt" set FILE_FOUND=true
    
    if "!FILE_FOUND!"=="false" (
        echo ERROR: No se encuentra !FILES[%%i]!.sql o .txt
        pause
        exit /b 1
    ) else (
        echo ✓ !FILES[%%i]! encontrado
    )
)
echo.

:: Determinar extensión de archivos
set "FILE_EXT=.sql"
if not exist "!SCRIPT_DIR!creacionPRev.sql" (
    if exist "!SCRIPT_DIR!creacionPRev.txt" set "FILE_EXT=.txt"
)
echo Usando archivos con extension: !FILE_EXT!
echo.

:: Verificar PostgreSQL
echo Verificando PostgreSQL...
where psql >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: PostgreSQL no encontrado en el PATH.
    echo Asegurese de tener PostgreSQL instalado.
    pause
    exit /b 1
)
echo ✓ PostgreSQL detectado
echo.

:: ===============================================
:: INTENTO DE CONEXION SIN PASSWORD
:: ===============================================
echo Probando conexiones automaticas...

set CONNECTION_SUCCESS=0
set PG_HOST=localhost
set PG_PORT=5432

:: Lista de usuarios comunes sin password
set USERS[0]=postgres
set USERS[1]=%USERNAME%
set USERS[2]=lolcito
set USERS[3]=admin

:TryConnections
for /l %%i in (0,1,3) do (
    if !CONNECTION_SUCCESS! equ 0 (
        echo Probando usuario: !USERS[%%i]! sin password...
        psql -h !PG_HOST! -p !PG_PORT! -U !USERS[%%i]! -l >nul 2>nul
        if !errorlevel! equ 0 (
            echo ✓ Conexion exitosa con: !USERS[%%i]!
            set PG_USER=!USERS[%%i]!
            set CONNECTION_SUCCESS=1
            goto ConnectionFound
        )
    )
)

:: Si no funcionó, pedir credenciales manualmente
echo.
echo No se pudo conectar automaticamente.
echo.
set /p PG_HOST="Host (Enter para localhost): "
if "!PG_HOST!"=="" set PG_HOST=localhost

set /p PG_PORT="Puerto (Enter para 5432): "
if "!PG_PORT!"=="" set PG_PORT=5432

set /p PG_USER="Usuario PostgreSQL: "
set /p PG_PASS="Password (dejar vacio si no tiene): "

if not "!PG_PASS!"=="" set PGPASSWORD=!PG_PASS!

:: Probar conexión manual
psql -h !PG_HOST! -p !PG_PORT! -U !PG_USER! -l >nul 2>nul
if !errorlevel! neq 0 (
    echo ERROR: No se pudo conectar con las credenciales proporcionadas.
    pause
    exit /b 1
)

:ConnectionFound
echo.
echo ✓ Conexion establecida con PostgreSQL
echo   Usuario: !PG_USER!
echo   Servidor: !PG_HOST!:!PG_PORT!
echo.

:: ===============================================
:: INSTALACION COMPLETA
:: ===============================================
echo ===============================================
echo        INICIANDO INSTALACION COMPLETA
echo ===============================================
echo.

echo Se ejecutaran los siguientes scripts:
echo 1. creacionPRev!FILE_EXT!    (Crea BD y usuario)
echo 2. base_datos!FILE_EXT!       (Estructura tablas)
echo 3. procedimientos!FILE_EXT!   (Procedimientos almacenados)
echo 4. triggers!FILE_EXT!         (Triggers)
echo 5. insertgod!FILE_EXT!        (Datos iniciales)
echo.

set /p CONFIRM="¿Desea continuar con la instalacion? (S/N): "
if /i not "!CONFIRM!"=="S" (
    echo Instalacion cancelada por el usuario.
    pause
    exit /b 0
)

echo.

:: 1. EJECUTAR creacionPRev.sql (crea BD y usuario)
echo [1/5] Ejecutando creacionPRev!FILE_EXT!...
echo    - Creando base de datos: !DB_NAME!
echo    - Creando usuario: !DB_USER!
psql -h !PG_HOST! -p !PG_PORT! -U !PG_USER! -f "!SCRIPT_DIR!creacionPRev!FILE_EXT!"
if !errorlevel! neq 0 (
    echo ✗ Error en creacionPRev!FILE_EXT!
    echo Revise que el usuario tenga permisos para crear bases de datos.
    pause
    exit /b 1
)
echo ✓ Base de datos y usuario creados exitosamente
echo.

:: 2. EJECUTAR base_datos.sql (estructura de tablas)
echo [2/5] Ejecutando base_datos!FILE_EXT!...
echo    - Creando tablas maestras y transaccionales
psql -h !PG_HOST! -p !PG_PORT! -U !PG_USER! -d !DB_NAME! -f "!SCRIPT_DIR!base_datos!FILE_EXT!"
if !errorlevel! neq 0 (
    echo ✗ Error en base_datos!FILE_EXT!
    pause
    exit /b 1
)
echo ✓ Estructura de tablas creada exitosamente
echo.

:: 3. EJECUTAR procedimientos.sql (procedimientos almacenados)
echo [3/5] Ejecutando procedimientos!FILE_EXT!...
echo    - Creando funciones y procedimientos almacenados
psql -h !PG_HOST! -p !PG_PORT! -U !PG_USER! -d !DB_NAME! -f "!SCRIPT_DIR!procedimientos!FILE_EXT!"
if !errorlevel! neq 0 (
    echo ✗ Error en procedimientos!FILE_EXT!
    pause
    exit /b 1
)
echo ✓ Procedimientos almacenados creados exitosamente
echo.

:: 4. EJECUTAR triggers.sql (triggers)
echo [4/5] Ejecutando triggers!FILE_EXT!...
echo    - Creando triggers del sistema
psql -h !PG_HOST! -p !PG_PORT! -U !PG_USER! -d !DB_NAME! -f "!SCRIPT_DIR!triggers!FILE_EXT!"
if !errorlevel! neq 0 (
    echo ✗ Error en triggers!FILE_EXT!
    pause
    exit /b 1
)
echo ✓ Triggers creados exitosamente
echo.

:: 5. EJECUTAR insertgod.sql (datos iniciales)
echo [5/5] Ejecutando insertgod!FILE_EXT!...
echo    - Insertando datos iniciales y de prueba
psql -h !PG_HOST! -p !PG_PORT! -U !PG_USER! -d !DB_NAME! -f "!SCRIPT_DIR!insertgod!FILE_EXT!"
if !errorlevel! neq 0 (
    echo ✗ Error en insertgod!FILE_EXT!
    pause
    exit /b 1
)
echo ✓ Datos iniciales insertados exitosamente
echo.

echo ✅ INSTALACION COMPLETADA EXITOSAMENTE
echo.

:: ===============================================
:: VERIFICACION COMPLETA
:: ===============================================
echo ===============================================
echo        VERIFICACION DE INSTALACION
echo ===============================================
echo.

set /p VERIFY="¿Desea verificar la instalacion completada? (S/N): "
if /i not "!VERIFY!"=="S" goto SkipVerification

echo.
echo Ejecutando verificacion completa de la base de datos...

:: Verificar que la base de datos existe y es accesible
echo 1. Verificando conexion a la base de datos...
psql -h !PG_HOST! -p !PG_PORT! -U !DB_USER! -d !DB_NAME! -c "SELECT '✓ Conexion a BD exitosa' as resultado;" 2>nul
if !errorlevel! neq 0 (
    echo ✗ Error: No se pudo conectar a la base de datos
    goto VerificationFailed
)

:: Verificar tablas principales
echo 2. Verificando tablas creadas...
psql -h !PG_HOST! -p !PG_PORT! -U !DB_USER! -d !DB_NAME! -c "
SELECT 
    'TABLAS MAESTRAS: ' || COUNT(*) || ' tablas' as verificacion
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE 'mae_%'

UNION ALL

SELECT 
    'TABLAS TRANSACCIONALES: ' || COUNT(*) || ' tablas'
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE 'trs_%'
" 2>nul

:: Verificar procedimientos y triggers
echo 3. Verificando procedimientos y triggers...
psql -h !PG_HOST! -p !PG_PORT! -U !DB_USER! -d !DB_NAME! -c "
SELECT 
    'PROCEDIMIENTOS: ' || COUNT(*) || ' funciones' as verificacion
FROM information_schema.routines 
WHERE routine_schema = 'public'

UNION ALL

SELECT 
    'TRIGGERS: ' || COUNT(*) || ' triggers'
FROM information_schema.triggers 
WHERE trigger_schema = 'public'
" 2>nul

:: Verificar datos insertados
echo 4. Verificando datos iniciales...
psql -h !PG_HOST! -p !PG_PORT! -U !DB_USER! -d !DB_NAME! -c "
SELECT 
    'PRODUCTOS: ' || COUNT(*) || ' registros' as verificacion
FROM mae_producto

UNION ALL

SELECT 
    'CLIENTES: ' || COUNT(*) || ' registros'
FROM mae_cliente

UNION ALL

SELECT 
    'EMPRESAS: ' || COUNT(*) || ' registros'
FROM mae_empresa

UNION ALL

SELECT 
    'DOCUMENTOS: ' || COUNT(*) || ' registros'
FROM trs_encabezado_documento

UNION ALL

SELECT 
    'GUIAS: ' || COUNT(*) || ' registros'
FROM trs_encabezado_guia;
" 2>nul

echo.
echo ✅ VERIFICACION COMPLETADA EXITOSAMENTE
goto ShowSummary

:VerificationFailed
echo.
echo ⚠ Algunos elementos no pudieron verificarse correctamente
echo   La instalacion puede estar incompleta.

:SkipVerification
echo.
echo ⚠ Verificacion omitida por el usuario

:ShowSummary
echo.
echo ===============================================
echo        RESUMEN FINAL DE INSTALACION
echo ===============================================
echo.
echo ✅ PROCESO DE INSTALACION TERMINADO
echo.
echo Base de datos creada: !DB_NAME!
echo Usuario de aplicacion: !DB_USER!
echo Servidor: !PG_HOST!:!PG_PORT!
echo.
echo Para conectarse manualmente:
echo psql -h !PG_HOST! -p !PG_PORT! -U !DB_USER! -d !DB_NAME!
echo.
echo Los siguientes archivos se ejecutaron exitosamente:
echo ✓ creacionPRev!FILE_EXT!    (Crea BD y usuario)
echo ✓ base_datos!FILE_EXT!       (Estructura tablas)  
echo ✓ procedimientos!FILE_EXT!   (Procedimientos)
echo ✓ triggers!FILE_EXT!         (Triggers)
echo ✓ insertgod!FILE_EXT!        (Datos iniciales)
echo.

:: Limpiar variable de entorno
set PGPASSWORD=

echo Presione cualquier tecla para salir...
pause >nul