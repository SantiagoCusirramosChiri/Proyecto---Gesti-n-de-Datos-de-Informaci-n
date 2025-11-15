

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
    LIMIT 1;
    
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
    SELECT 
        p.id_producto, 
        p.nombre, 
        p.descripcion, 
        p.stock, 
        p.unidad_medida
    FROM mae_producto p
    WHERE p.activo = TRUE
    ORDER BY p.id_producto DESC;
END$$
DELIMITER ;


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


-- =========================
-- PROCEDIMIENTOS MAESTROS
-- =========================

DELIMITER $$

-- Insertar Ubicación
CREATE PROCEDURE sp_insertar_ubicacion(
    IN p_descripcion VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT 'Error al insertar ubicación' AS mensaje;
        ROLLBACK;
    END;
    START TRANSACTION;
        INSERT INTO mae_ubicacion(descripcion) VALUES (p_descripcion);
        SELECT LAST_INSERT_ID() AS id_ubicacion;
    COMMIT;
END$$


-- Insertar Identidad
CREATE PROCEDURE sp_insertar_identidad(
    IN p_tipo_identificacion VARCHAR(20),
    IN p_codigo_documento VARCHAR(15)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT 'Error al insertar identidad' AS mensaje;
        ROLLBACK;
    END;
    START TRANSACTION;
        INSERT INTO mae_identidad(tipo_identificacion, codigo_documento)
        VALUES (p_tipo_identificacion, p_codigo_documento);
        SELECT LAST_INSERT_ID() AS id_identidad;
    COMMIT;
END$$


-- Insertar Cliente
CREATE PROCEDURE sp_insertar_cliente(
    IN p_nombre VARCHAR(50),
    IN p_apellido VARCHAR(50),
    IN p_id_ubicacion INT,
    IN p_id_identidad INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT 'Error al insertar cliente' AS mensaje;
        ROLLBACK;
    END;
    START TRANSACTION;
        INSERT INTO mae_cliente(nombre, apellido, id_ubicacion, id_identidad)
        VALUES (p_nombre, p_apellido, p_id_ubicacion, p_id_identidad);
        SELECT LAST_INSERT_ID() AS id_cliente;
    COMMIT;
END$$


-- Insertar Empresa
CREATE PROCEDURE sp_insertar_empresa(
    IN p_nombre VARCHAR(50),
    IN p_razon_social VARCHAR(100),
    IN p_RUC CHAR(11),
    IN p_id_ubicacion INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT 'Error al insertar empresa' AS mensaje;
        ROLLBACK;
    END;
    START TRANSACTION;
        INSERT INTO mae_empresa(nombre, razon_social, RUC, id_ubicacion)
        VALUES (p_nombre, p_razon_social, p_RUC, p_id_ubicacion);
        SELECT LAST_INSERT_ID() AS id_empresa;
    COMMIT;
END$$


-- Insertar Conductor
CREATE PROCEDURE sp_insertar_conductor(
    IN p_nombre VARCHAR(50),
    IN p_n_licencia CHAR(12)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT 'Error al insertar conductor' AS mensaje;
        ROLLBACK;
    END;
    START TRANSACTION;
        INSERT INTO mae_conductor(nombre, n_licencia)
        VALUES (p_nombre, p_n_licencia);
        SELECT LAST_INSERT_ID() AS id_conductor;
    COMMIT;
END$$


-- Insertar Vehículo
CREATE PROCEDURE sp_insertar_vehiculo(
    IN p_descripcion VARCHAR(50),
    IN p_placa CHAR(8)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT 'Error al insertar vehículo' AS mensaje;
        ROLLBACK;
    END;
    START TRANSACTION;
        INSERT INTO mae_vehiculo(descripcion, placa)
        VALUES (p_descripcion, p_placa);
        SELECT LAST_INSERT_ID() AS id_vehiculo;
    COMMIT;
END$$


-- Insertar Producto
CREATE PROCEDURE sp_insertar_producto(
    IN p_nombre VARCHAR(50),
    IN p_descripcion VARCHAR(100),
    IN p_precio_base DECIMAL(10,2),
    IN p_stock INT,
    IN p_unidad_medida VARCHAR(10)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT 'Error al insertar producto' AS mensaje;
        ROLLBACK;
    END;
    START TRANSACTION;
        INSERT INTO mae_producto(nombre, descripcion, precio_base, stock, unidad_medida)
        VALUES (p_nombre, p_descripcion, p_precio_base, p_stock, p_unidad_medida);
        SELECT LAST_INSERT_ID() AS id_producto;
    COMMIT;
END$$


-- Insertar Forma de Pago
CREATE PROCEDURE sp_insertar_forma_pago(
    IN p_nombre VARCHAR(35),
    IN p_descripcion VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT 'Error al insertar forma de pago' AS mensaje;
        ROLLBACK;
    END;
    START TRANSACTION;
        INSERT INTO mae_forma_pago(nombre, descripcion)
        VALUES (p_nombre, p_descripcion);
        SELECT LAST_INSERT_ID() AS id_forma_pago;
    COMMIT;
END$$


-- Insertar Moneda
CREATE PROCEDURE sp_insertar_moneda(
    IN p_codigo_iso CHAR(3),
    IN p_nombre VARCHAR(20)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT 'Error al insertar moneda' AS mensaje;
        ROLLBACK;
    END;
    START TRANSACTION;
        INSERT INTO mae_moneda(codigo_iso, nombre)
        VALUES (p_codigo_iso, p_nombre);
        SELECT LAST_INSERT_ID() AS id_moneda;
    COMMIT;
END$$


-- =========================
-- PROCEDIMIENTOS TRANSACCIONALES
-- =========================

-- Insertar Encabezado Documento
CREATE PROCEDURE sp_insertar_encabezado_documento(
    IN p_tipo_doc VARCHAR(20),
    IN p_fecha_emision DATE,
    IN p_id_empresa INT,
    IN p_id_cliente INT,
    IN p_id_forma_pago INT,
    IN p_id_moneda INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT 'Error al insertar encabezado documento' AS mensaje;
        ROLLBACK;
    END;
    START TRANSACTION;
        INSERT INTO trs_encabezado_documento(
            tipo_doc, fecha_emision, id_empresa, id_cliente, id_forma_pago, id_moneda
        )
        VALUES (p_tipo_doc, p_fecha_emision, p_id_empresa, p_id_cliente, p_id_forma_pago, p_id_moneda);
        SELECT LAST_INSERT_ID() AS id_documento;
    COMMIT;
END$$


-- Insertar Detalle Documento
CREATE PROCEDURE sp_insertar_detalle_documento(
    IN p_id_documento INT,
    IN p_id_producto INT,
    IN p_cantidad INT,
    IN p_subtotal DECIMAL(10,2),
    IN p_igv DECIMAL(10,2),
    IN p_importe DECIMAL(10,2)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT 'Error al insertar detalle documento' AS mensaje;
        ROLLBACK;
    END;
    START TRANSACTION;
        INSERT INTO trs_detalle_documento(
            id_documento, id_producto, cantidad, subtotal, igv, importe
        ) VALUES (p_id_documento, p_id_producto, p_cantidad, p_subtotal, p_igv, p_importe);
        SELECT LAST_INSERT_ID() AS id_detalle;
    COMMIT;
END$$


-- Insertar Encabezado Guía
CREATE PROCEDURE sp_insertar_encabezado_guia(
    IN p_id_doc_venta INT,
    IN p_nro_guia VARCHAR(20),
    IN p_fecha_emision DATE,
    IN p_fecha_inicio_traslado DATE,
    IN p_motivo_traslado VARCHAR(100),
    IN p_direccion_partida VARCHAR(150),
    IN p_direccion_llegada VARCHAR(150),
    IN p_id_conductor INT,
    IN p_id_vehiculo INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT 'Error al insertar encabezado guía' AS mensaje;
        ROLLBACK;
    END;
    START TRANSACTION;
        INSERT INTO trs_encabezado_guia(
            id_doc_venta, nro_guia, fecha_emision, fecha_inicio_traslado, motivo_traslado,
            direccion_partida, direccion_llegada, id_conductor, id_vehiculo
        )
        VALUES (
            p_id_doc_venta, p_nro_guia, p_fecha_emision, p_fecha_inicio_traslado,
            p_motivo_traslado, p_direccion_partida, p_direccion_llegada, p_id_conductor, p_id_vehiculo
        );
        SELECT LAST_INSERT_ID() AS id_guia;
    COMMIT;
END$$


-- Insertar Detalle Guía
CREATE PROCEDURE sp_insertar_detalle_guia(
    IN p_id_guia INT,
    IN p_id_producto INT,
    IN p_descripcion VARCHAR(100),
    IN p_unidad_medida VARCHAR(10),
    IN p_unidad_peso_bruto VARCHAR(10),
    IN p_peso_total_carga DECIMAL(10,2),
    IN p_modalidad_trans VARCHAR(20),
    IN p_transbordo_prog CHAR(2),
    IN p_categoriaM1_L CHAR(2),
    IN p_retorno_envases CHAR(2),
    IN p_vehiculo_vacio CHAR(2),
    IN p_id_conductor INT,
    IN p_id_vehiculo INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT 'Error al insertar detalle guía' AS mensaje;
        ROLLBACK;
    END;
    START TRANSACTION;
        INSERT INTO trs_detalle_guia(
            id_guia, id_producto, descripcion, unidad_medida, unidad_peso_bruto,
            peso_total_carga, modalidad_trans, transbordo_prog, categoriaM1_L,
            retorno_envases, vehiculo_vacio, id_conductor, id_vehiculo
        )
        VALUES (
            p_id_guia, p_id_producto, p_descripcion, p_unidad_medida, p_unidad_peso_bruto,
            p_peso_total_carga, p_modalidad_trans, p_transbordo_prog, p_categoriaM1_L,
            p_retorno_envases, p_vehiculo_vacio, p_id_conductor, p_id_vehiculo
        );
        SELECT LAST_INSERT_ID() AS id_detalle_guia;
    COMMIT;
END$$

DELIMITER ;
