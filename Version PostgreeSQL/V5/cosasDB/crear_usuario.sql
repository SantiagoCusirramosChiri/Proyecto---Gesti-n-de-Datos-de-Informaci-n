-- 1. PRIMERO: Terminar todas las conexiones activas a la base de datos
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'sistema_documentos' AND pid <> pg_backend_pid();

-- 2. SEGUNDO: Eliminar la base de datos
DROP DATABASE IF EXISTS sistema_documentos;

-- 3. TERCERO: Eliminar el usuario (ahora que no tiene dependencias)
DROP USER IF EXISTS lolcito;

-- 4. CUARTO: Crear el usuario con permisos
CREATE USER lolcito WITH PASSWORD '12345678' SUPERUSER CREATEDB CREATEROLE;