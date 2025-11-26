SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'sistema_documentos' AND pid <> pg_backend_pid();

DROP DATABASE IF EXISTS sistema_documentos;

DROP USER IF EXISTS lolcito;

CREATE USER lolcito WITH PASSWORD '12345678' SUPERUSER CREATEDB CREATEROLE;