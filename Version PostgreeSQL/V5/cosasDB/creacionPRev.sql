-- 5. QUINTO: Crear la base de datos con encoding UTF-8
CREATE DATABASE sistema_documentos
WITH 
    OWNER = lolcito
    ENCODING = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    TEMPLATE = template0;

-- 6. SEXTO: Configurar el usuario para usar UTF-8 por defecto
ALTER USER lolcito SET client_encoding TO 'utf8';