

USE sistema_documentos;


DELIMITER $$

DROP PROCEDURE IF EXISTS sp_login_empresa $$
CREATE PROCEDURE sp_login_empresa(
    IN p_usuario VARCHAR(50),
    IN p_clave CHAR(11)
)
BEGIN
    DECLARE v_existe INT DEFAULT 0;

    SELECT COUNT(*) INTO v_existe
    FROM mae_empresa
    WHERE nombre = p_usuario
      AND RUC = p_clave
      AND activo = TRUE;

    IF v_existe > 0 THEN
        SELECT 'LOGIN EXITOSO' AS mensaje, id_empresa, nombre, razon_social
        FROM mae_empresa
        WHERE nombre = p_usuario AND RUC = p_clave;
    ELSE
        SELECT 'USUARIO O CONTRASEÑA INCORRECTA O EMPRESA INACTIVA' AS mensaje;
    END IF;
END$$

DELIMITER ;

DELIMITER $$

DROP PROCEDURE IF EXISTS sp_registrar_empresa$$

CREATE PROCEDURE sp_registrar_empresa(
    IN p_nombre VARCHAR(50),
    IN p_razon_social VARCHAR(100),
    IN p_ruc CHAR(11),
    IN p_id_ubicacion INT
)
proc_end: BEGIN
    DECLARE v_id_ruc INT DEFAULT NULL;
    DECLARE v_activo_ruc BOOLEAN DEFAULT FALSE;
    DECLARE v_id_nombre INT DEFAULT NULL;
    DECLARE v_nombre_existente VARCHAR(50);
    
    -- Verificar si el RUC ya existe
    SELECT id_empresa, activo, nombre 
    INTO v_id_ruc, v_activo_ruc, v_nombre_existente
    FROM mae_empresa
    WHERE RUC = p_ruc
    LIMIT 1;x
    
    -- Verificar si el nombre ya existe con otro RUC
    SELECT id_empresa 
    INTO v_id_nombre
    FROM mae_empresa
    WHERE nombre = p_nombre AND RUC != p_ruc
    LIMIT 1;
    
    -- CASO 1: Ni el RUC ni el nombre existen -> CREAR NUEVA EMPRESA
    IF v_id_ruc IS NULL AND v_id_nombre IS NULL THEN
        INSERT INTO mae_empresa (nombre, razon_social, RUC, id_ubicacion, activo)
        VALUES (p_nombre, p_razon_social, p_ruc, p_id_ubicacion, TRUE);
        
        SELECT 'EMPRESA CREADA' AS mensaje, LAST_INSERT_ID() AS id_empresa;
        LEAVE proc_end;
    END IF;
    
    -- CASO 2: El nombre ya existe con otro RUC -> ERROR
    IF v_id_nombre IS NOT NULL THEN
        SELECT 'ERROR: NOMBRE DE EMPRESA YA USADO CON OTRO RUC' AS mensaje, 
               NULL AS id_empresa;
        LEAVE proc_end;
    END IF;
    
    -- CASO 3: El RUC existe
    IF v_id_ruc IS NOT NULL THEN
        -- CASO 3A: RUC existe con el mismo nombre
        IF v_nombre_existente = p_nombre THEN
            IF v_activo_ruc = FALSE THEN
                -- Reactivar empresa
                UPDATE mae_empresa
                SET activo = TRUE,
                    razon_social = p_razon_social,
                    id_ubicacion = p_id_ubicacion
                WHERE id_empresa = v_id_ruc;
                
                SELECT 'EMPRESA REACTIVADA' AS mensaje, v_id_ruc AS id_empresa;
            ELSE
                -- Ya existe y está activa
                SELECT 'EMPRESA YA EXISTE (ACTIVA)' AS mensaje, v_id_ruc AS id_empresa;
            END IF;
        ELSE
            -- CASO 3B: RUC existe pero con otro nombre -> ERROR
            SELECT CONCAT('ERROR: RUC YA REGISTRADO CON EL NOMBRE "', 
                         v_nombre_existente, '"') AS mensaje,
                   NULL AS id_empresa;
        END IF;
        LEAVE proc_end;
    END IF;
    
END$$

DELIMITER ;

DROP PROCEDURE IF EXISTS sp_listar_guias_empresa;
DELIMITER $$
CREATE PROCEDURE sp_listar_guias_empresa(IN p_id_empresa INT)
BEGIN
    SELECT g.id_guia, g.nro_guia, g.fecha_emision, g.fecha_inicio_traslado,
           g.motivo_traslado, g.direccion_partida, g.direccion_llegada,
           c.nombre AS conductor, v.placa AS vehiculo, g.estado_guia
    FROM trs_encabezado_guia g
    JOIN trs_encabezado_documento d ON g.id_doc_venta = d.id_documento
    JOIN mae_conductor c ON g.id_conductor = c.id_conductor
    JOIN mae_vehiculo v ON g.id_vehiculo = v.id_vehiculo
    WHERE d.id_empresa = p_id_empresa
    ORDER BY g.fecha_emision DESC;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_detalle_productos_empresa;
DELIMITER $$
CREATE PROCEDURE sp_detalle_productos_empresa(IN p_id_empresa INT)
BEGIN
    SELECT d.id_documento, p.nombre AS producto, dt.cantidad, 
           p.precio_base AS precio_producto, dt.importe
    FROM trs_detalle_documento dt
    JOIN trs_encabezado_documento d ON dt.id_documento = d.id_documento
    JOIN mae_producto p ON dt.id_producto = p.id_producto
    WHERE d.id_empresa = p_id_empresa
    ORDER BY d.fecha_emision DESC;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_listar_clientes_empresa;
DELIMITER $$
CREATE PROCEDURE sp_listar_clientes_empresa(IN p_id_empresa INT)
BEGIN
    SELECT c.id_cliente, c.nombre, c.apellido, u.descripcion AS ubicacion, i.tipo_identificacion, i.codigo_documento
    FROM mae_cliente c
    JOIN mae_ubicacion u ON c.id_ubicacion = u.id_ubicacion
    JOIN mae_identidad i ON c.id_identidad = i.id_identidad
    JOIN trs_encabezado_documento d ON c.id_cliente = d.id_cliente
    WHERE d.id_empresa = p_id_empresa
    GROUP BY c.id_cliente;
END$$
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_listar_stock_empresa;
DELIMITER $$
CREATE PROCEDURE sp_listar_stock_empresa(IN p_id_empresa INT)
BEGIN
    SELECT p.id_producto, p.nombre, p.descripcion, p.stock, p.unidad_medida
    FROM mae_producto p
    JOIN trs_detalle_documento dt ON p.id_producto = dt.id_producto
    JOIN trs_encabezado_documento d ON dt.id_documento = d.id_documento
    WHERE d.id_empresa = p_id_empresa AND p.activo = TRUE
    GROUP BY p.id_producto;
END$$
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_listar_guias_pendientes_empresa;
DELIMITER $$
CREATE PROCEDURE sp_listar_guias_pendientes_empresa(IN p_id_empresa INT)
BEGIN
    SELECT g.id_guia, g.nro_guia, g.fecha_inicio_traslado, c.nombre AS conductor, v.placa AS vehiculo
    FROM trs_encabezado_guia g
    JOIN trs_encabezado_documento d ON g.id_doc_venta = d.id_documento
    JOIN mae_conductor c ON g.id_conductor = c.id_conductor
    JOIN mae_vehiculo v ON g.id_vehiculo = v.id_vehiculo
    WHERE d.id_empresa = p_id_empresa AND g.estado_guia = 'PENDIENTE'
    ORDER BY g.fecha_inicio_traslado ASC;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_contar_documentos_emitidos;
DELIMITER $$
CREATE PROCEDURE sp_contar_documentos_emitidos(IN p_id_empresa INT, OUT p_total INT)
BEGIN
    SELECT COUNT(*) INTO p_total
    FROM trs_encabezado_documento
    WHERE id_empresa = p_id_empresa AND estado_doc = 'EMITIDO';
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_contar_documentos_pendientes;
DELIMITER $$
CREATE PROCEDURE sp_contar_documentos_pendientes(IN p_id_empresa INT, OUT p_total INT)
BEGIN
    SELECT COUNT(*) INTO p_total
    FROM trs_encabezado_documento
    WHERE id_empresa = p_id_empresa AND estado_doc = 'PENDIENTE';
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_contar_guias_pendientes;
DELIMITER $$
CREATE PROCEDURE sp_contar_guias_pendientes(IN p_id_empresa INT, OUT p_total INT)
BEGIN
    SELECT COUNT(*) INTO p_total
    FROM trs_encabezado_guia g
    JOIN trs_encabezado_documento d ON g.id_doc_venta = d.id_documento
    WHERE d.id_empresa = p_id_empresa AND g.estado_guia = 'PENDIENTE';
END$$
DELIMITER ;



DROP PROCEDURE IF EXISTS sp_stock_total_empresa;
DELIMITER $$
CREATE PROCEDURE sp_stock_total_empresa(IN p_id_empresa INT, OUT p_total_stock INT)
BEGIN
    SELECT SUM(p.stock) INTO p_total_stock
    FROM mae_producto p
    JOIN trs_detalle_documento dt ON p.id_producto = dt.id_producto
    JOIN trs_encabezado_documento d ON dt.id_documento = d.id_documento
    WHERE d.id_empresa = p_id_empresa;
END$$
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_total_ventas_empresa;
DELIMITER $$
CREATE PROCEDURE sp_total_ventas_empresa(IN p_id_empresa INT, OUT p_total_ventas DECIMAL(15,2))
BEGIN
    SELECT SUM(importe) INTO p_total_ventas
    FROM trs_detalle_documento dt
    JOIN trs_encabezado_documento d ON dt.id_documento = d.id_documento
    WHERE d.id_empresa = p_id_empresa AND d.estado_doc = 'EMITIDO';
END$$
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_contar_clientes_activos;
DELIMITER $$
CREATE PROCEDURE sp_contar_clientes_activos(IN p_id_empresa INT, OUT p_total_clientes INT)
BEGIN
    SELECT COUNT(DISTINCT c.id_cliente) INTO p_total_clientes
    FROM mae_cliente c
    JOIN trs_encabezado_documento d ON c.id_cliente = d.id_cliente
    WHERE d.id_empresa = p_id_empresa AND c.activo = TRUE;
END$$
DELIMITER ;

