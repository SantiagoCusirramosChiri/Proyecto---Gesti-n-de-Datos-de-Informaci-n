@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title Instalador Completo - Sistema de Documentos V3
color 0A

echo ===============================================
echo    INSTALADOR COMPLETO SISTEMA DOCUMENTOS V3
echo ===============================================
echo.

:: Configuración de rutas según tu estructura
set "PROJECT_ROOT=%~dp0.."
set "DATOS_DB=%PROJECT_ROOT%\datosDB"
set "SCRIPT_DIR=%DATOS_DB%"
set "VISTA_DIR=%~dp0"

:: Configuración de base de datos
set DB_NAME=sistema_documentos
set DB_USER=lolcito
set DB_PASS=12345678

:: Verificar que existe la carpeta datosDB
if not exist "!DATOS_DB!\" (
    echo ERROR: No se encuentra la carpeta datosDB
    echo Estructura esperada:
    echo V3/
    echo   vista/        ^<-- Este batch debe estar aquí^>
    echo   datosDB/      ^<-- Scripts SQL aquí^>
    echo.
    pause
    exit /b 1
)

echo Estructura de proyecto detectada:
echo Proyecto: !PROJECT_ROOT!
echo Scripts DB: !DATOS_DB!
echo.
 
:: Verificar archivos SQL necesarios
set FILES[0]=creacionPRev
set FILES[1]=base_datos
set FILES[2]=procedimientos
set FILES[3]=triggers
set FILES[4]=insertgod

echo Verificando archivos en datosDB...
for /l %%i in (0,1,4) do (
    set FILE_FOUND=false
    if exist "!SCRIPT_DIR!\!FILES[%%i]!.sql" set FILE_FOUND=true
    if exist "!SCRIPT_DIR!\!FILES[%%i]!.txt" set FILE_FOUND=true
    
    if "!FILE_FOUND!"=="false" (
        echo ERROR: No se encuentra !FILES[%%i]!.sql o .txt en datosDB
        pause
        exit /b 1
    ) else (
        echo ✓ !FILES[%%i]! encontrado
    )
)
echo.

:: Determinar extensión de archivos
set "FILE_EXT=.sql"
if not exist "!SCRIPT_DIR!\creacionPRev.sql" (
    if exist "!SCRIPT_DIR!\creacionPRev.txt" set "FILE_EXT=.txt"
)
echo Usando archivos con extension: !FILE_EXT!
echo.

:: ===============================================
:: CREACION DE USUARIO LOLCITO (TU SCRIPT)
:: ===============================================
echo ===============================================
echo        CREANDO USUARIO DE BASE DE DATOS
echo ===============================================
echo.

set /p CREATE_USER="¿Crear usuario lolcito? (S/N): "
if /i "!CREATE_USER!"=="S" (
    echo Ejecutando creacion de usuario...
    
    :: Buscar PostgreSQL en rutas comunes
    set PG_FOUND=0
    for %%p in (
        "C:\Program Files\PostgreSQL\17\bin"
        "C:\Program Files\PostgreSQL\16\bin" 
        "C:\Program Files\PostgreSQL\15\bin"
        "C:\Program Files\PostgreSQL\14\bin"
        "C:\Program Files\PostgreSQL\13\bin"
        "C:\Program Files\PostgreSQL\12\bin"
    ) do (
        if !PG_FOUND! equ 0 (
            if exist "%%p\psql.exe" (
                set "PGPATH=%%p"
                set PG_FOUND=1
                echo ✓ PostgreSQL encontrado en: %%p
            )
        )
    )
    
    if !PG_FOUND! equ 0 (
        echo Buscando PostgreSQL en PATH...
        where psql >nul 2>nul
        if !errorlevel! equ 0 (
            set PG_FOUND=1
            echo ✓ PostgreSQL encontrado en PATH
        ) else (
            echo ✗ PostgreSQL no encontrado
            goto SkipUserCreation
        )
    )
    
    echo [1/5] Terminando conexiones activas...
    "%PGPATH%\psql.exe" -U postgres -h localhost -p 5432 -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '!DB_NAME!' AND pid <> pg_backend_pid();" >nul 2>&1
    
    echo [2/5] Eliminando base de datos (si existe)...
    "%PGPATH%\psql.exe" -U postgres -h localhost -p 5432 -c "DROP DATABASE IF EXISTS !DB_NAME!;" >nul 2>&1
    
    echo [3/5] Eliminando usuario (si existe)...
    "%PGPATH%\psql.exe" -U postgres -h localhost -p 5432 -c "DROP USER IF EXISTS !DB_USER!;" >nul 2>&1
    
    echo [4/5] Creando usuario !DB_USER!...
    "%PGPATH%\psql.exe" -U postgres -h localhost -p 5432 -c "CREATE USER !DB_USER! WITH PASSWORD '!DB_PASS!' SUPERUSER CREATEDB CREATEROLE;"
    
    IF !ERRORLEVEL! NEQ 0 (
        echo.
        echo ✗ Error al crear el usuario
        goto SkipUserCreation
    )
    
    echo [5/5] Usuario creado exitosamente
    echo ✓ Usuario '!DB_USER!' creado con password '!DB_PASS!'
)

:SkipUserCreation
echo.

:: ===============================================
:: CONEXION E INSTALACION
:: ===============================================
echo ===============================================
echo        CONEXION E INSTALACION
echo ===============================================
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

:: Intentar conexiones automáticas
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
:: INSTALACION COMPLETA DE LA BASE DE DATOS
:: ===============================================
echo ===============================================
echo        INSTALACION BASE DE DATOS
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
psql -h !PG_HOST! -p !PG_PORT! -U !PG_USER! -f "!SCRIPT_DIR!\creacionPRev!FILE_EXT!"
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
psql -h !PG_HOST! -p !PG_PORT! -U !PG_USER! -d !DB_NAME! -f "!SCRIPT_DIR!\base_datos!FILE_EXT!"
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
psql -h !PG_HOST! -p !PG_PORT! -U !PG_USER! -d !DB_NAME! -f "!SCRIPT_DIR!\procedimientos!FILE_EXT!"
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
psql -h !PG_HOST! -p !PG_PORT! -U !PG_USER! -d !DB_NAME! -f "!SCRIPT_DIR!\triggers!FILE_EXT!"
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
psql -h !PG_HOST! -p !PG_PORT! -U !PG_USER! -d !DB_NAME! -f "!SCRIPT_DIR!\insertgod!FILE_EXT!"
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
:: VERIFICACION FINAL
:: ===============================================
echo ===============================================
echo        VERIFICACION FINAL
echo ===============================================
echo.

set /p VERIFY="¿Desea verificar la instalacion? (S/N): "
if /i "!VERIFY!"=="S" (
    echo.
    echo Ejecutando verificacion completa...
    
    :: Verificar con el usuario lolcito
    psql -h !PG_HOST! -p !PG_PORT! -U !DB_USER! -d !DB_NAME! -c "
    SELECT '✓ CONEXION EXITOSA' as resultado;
    
    SELECT 'TABLAS MAESTRAS: ' || COUNT(*) || ' tablas' as verificacion
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name LIKE 'mae_%'
    
    UNION ALL
    
    SELECT 'TABLAS TRANSACCIONALES: ' || COUNT(*) || ' tablas'
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name LIKE 'trs_%'
    
    UNION ALL
    
    SELECT 'PROCEDIMIENTOS: ' || COUNT(*) || ' funciones'
    FROM information_schema.routines 
    WHERE routine_schema = 'public'
    
    UNION ALL
    
    SELECT 'DATOS PRODUCTOS: ' || COUNT(*) || ' registros'
    FROM mae_producto;
    " 2>nul
    
    echo.
    echo ✅ VERIFICACION COMPLETADA
)

echo.
echo ===============================================
echo        RESUMEN FINAL
echo ===============================================
echo.
echo ✅ INSTALACION TERMINADA EXITOSAMENTE
echo.
echo Base de datos: !DB_NAME!
echo Usuario app: !DB_USER! 
echo Password: !DB_PASS!
echo Servidor: !PG_HOST!:!PG_PORT!
echo.
echo Para conectarse:
echo psql -h !PG_HOST! -p !PG_PORT! -U !DB_USER! -d !DB_NAME!
echo.
echo Ubicacion scripts: !SCRIPT_DIR!
echo.

:: Limpiar variable de entorno
set PGPASSWORD=

echo Presione cualquier tecla para salir...
pause >nul