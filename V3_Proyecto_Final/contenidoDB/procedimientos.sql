
USE sistema_documentos;

-- Procedures

-- Autenticación

DROP PROCEDURE IF EXISTS sp_login_empresa;
DELIMITER $$
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
        SELECT 'LOGIN EXITOSO' AS mensaje, 
               id_empresa, 
               nombre, 
               razon_social 
        FROM mae_empresa 
        WHERE nombre = p_usuario 
          AND RUC = p_clave;
    ELSE
        SELECT 'USUARIO O CONTRASEÑA INCORRECTA O EMPRESA INACTIVA' AS mensaje;
    END IF;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_registrar_empresa;
DELIMITER $$
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
    
    SELECT id_empresa, 
           activo, 
           nombre 
    INTO v_id_ruc, 
         v_activo_ruc, 
         v_nombre_existente 
    FROM mae_empresa 
    WHERE RUC = p_ruc 
    LIMIT 1;
    
    SELECT id_empresa 
    INTO v_id_nombre 
    FROM mae_empresa 
    WHERE nombre = p_nombre 
      AND RUC != p_ruc 
    LIMIT 1;
    
    IF v_id_ruc IS NULL AND v_id_nombre IS NULL THEN
        INSERT INTO mae_empresa (
            nombre, 
            razon_social, 
            RUC, 
            id_ubicacion, 
            activo
        ) 
        VALUES (
            p_nombre, 
            p_razon_social, 
            p_ruc, 
            p_id_ubicacion, 
            TRUE
        );
        
        SELECT 'EMPRESA CREADA' AS mensaje, 
               LAST_INSERT_ID() AS id_empresa;
        LEAVE proc_end;
    END IF;
    
    IF v_id_nombre IS NOT NULL THEN
        SELECT 'ERROR: NOMBRE DE EMPRESA YA USADO CON OTRO RUC' AS mensaje, 
               NULL AS id_empresa;
        LEAVE proc_end;
    END IF;
    
    IF v_id_ruc IS NOT NULL THEN
        IF v_nombre_existente = p_nombre THEN
            IF v_activo_ruc = FALSE THEN
                UPDATE mae_empresa 
                SET activo = TRUE, 
                    razon_social = p_razon_social, 
                    id_ubicacion = p_id_ubicacion 
                WHERE id_empresa = v_id_ruc;
                
                SELECT 'EMPRESA REACTIVADA' AS mensaje, 
                       v_id_ruc AS id_empresa;
            ELSE
                SELECT 'EMPRESA YA EXISTE (ACTIVA)' AS mensaje, 
                       v_id_ruc AS id_empresa;
            END IF;
        ELSE
            SELECT CONCAT('ERROR: RUC YA REGISTRADO CON EL NOMBRE "', v_nombre_existente, '"') AS mensaje, 
                   NULL AS id_empresa;
        END IF;
        LEAVE proc_end;
    END IF;
END$$
DELIMITER ;

-- Listado

DROP PROCEDURE IF EXISTS sp_listar_guias_empresa;
DELIMITER $$
CREATE PROCEDURE sp_listar_guias_empresa(IN p_id_empresa INT)
BEGIN
    SELECT g.id_guia, 
           g.nro_guia, 
           g.fecha_emision, 
           g.fecha_inicio_traslado, 
           g.motivo_traslado, 
           g.direccion_partida, 
           g.direccion_llegada, 
           c.nombre AS conductor, 
           v.placa AS vehiculo, 
           g.estado_guia
    FROM trs_encabezado_guia g 
    JOIN trs_encabezado_documento d ON g.id_doc_venta = d.id_documento 
    JOIN mae_conductor c ON g.id_conductor = c.id_conductor 
    JOIN mae_vehiculo v ON g.id_vehiculo = v.id_vehiculo
    WHERE d.id_empresa = p_id_empresa 
    ORDER BY g.fecha_emision DESC;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_listar_guias_pendientes_empresa;
DELIMITER $$
CREATE PROCEDURE sp_listar_guias_pendientes_empresa(IN p_id_empresa INT)
BEGIN
    SELECT g.id_guia, 
           g.nro_guia, 
           g.fecha_inicio_traslado, 
           c.nombre AS conductor, 
           v.placa AS vehiculo
    FROM trs_encabezado_guia g 
    JOIN trs_encabezado_documento d ON g.id_doc_venta = d.id_documento 
    JOIN mae_conductor c ON g.id_conductor = c.id_conductor 
    JOIN mae_vehiculo v ON g.id_vehiculo = v.id_vehiculo
    WHERE d.id_empresa = p_id_empresa 
      AND g.estado_guia = 'PENDIENTE' 
    ORDER BY g.fecha_inicio_traslado ASC;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_detalle_productos_empresa;
DELIMITER $$
CREATE PROCEDURE sp_detalle_productos_empresa(IN p_id_empresa INT)
BEGIN
    SELECT d.id_documento, 
           p.nombre AS producto, 
           dt.cantidad, 
           p.precio_base AS precio_producto, 
           dt.importe
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
    SELECT DISTINCT 
           c.id_cliente, 
           c.nombre, 
           c.apellido, 
           u.descripcion AS ubicacion, 
           i.tipo_identificacion, 
           i.codigo_documento
    FROM mae_cliente c 
    JOIN mae_ubicacion u ON c.id_ubicacion = u.id_ubicacion 
    JOIN mae_identidad i ON c.id_identidad = i.id_identidad 
    JOIN trs_encabezado_documento d ON c.id_cliente = d.id_cliente
    WHERE d.id_empresa = p_id_empresa 
      AND c.activo = TRUE 
    ORDER BY c.nombre, c.apellido;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_listar_stock_empresa;
DELIMITER $$
CREATE PROCEDURE sp_listar_stock_empresa(IN p_id_empresa INT)
BEGIN
    SELECT p.id_producto, 
           p.nombre, 
           p.descripcion, 
           p.stock, 
           p.unidad_medida 
    FROM mae_producto p 
    WHERE p.activo = TRUE 
    ORDER BY p.nombre ASC;
END$$
DELIMITER ;

-- Conteo y estadísticas

DROP PROCEDURE IF EXISTS sp_contar_documentos_emitidos;
DELIMITER $$
CREATE PROCEDURE sp_contar_documentos_emitidos(
    IN p_id_empresa INT, 
    OUT p_total INT
)
BEGIN
    SELECT COUNT(*) INTO p_total 
    FROM trs_encabezado_documento 
    WHERE id_empresa = p_id_empresa 
      AND estado_doc = 'EMITIDO';
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_contar_documentos_pendientes;
DELIMITER $$
CREATE PROCEDURE sp_contar_documentos_pendientes(
    IN p_id_empresa INT, 
    OUT p_total INT
)
BEGIN
    SELECT COUNT(*) INTO p_total 
    FROM trs_encabezado_documento 
    WHERE id_empresa = p_id_empresa 
      AND estado_doc = 'PENDIENTE';
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_contar_guias_pendientes;
DELIMITER $$
CREATE PROCEDURE sp_contar_guias_pendientes(
    IN p_id_empresa INT, 
    OUT p_total INT
)
BEGIN
    SELECT COUNT(*) INTO p_total 
    FROM trs_encabezado_guia g 
    JOIN trs_encabezado_documento d ON g.id_doc_venta = d.id_documento 
    WHERE d.id_empresa = p_id_empresa 
      AND g.estado_guia = 'PENDIENTE';
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_contar_clientes_activos;
DELIMITER $$
CREATE PROCEDURE sp_contar_clientes_activos(
    IN p_id_empresa INT, 
    OUT p_total_clientes INT
)
BEGIN
    SELECT COUNT(DISTINCT c.id_cliente) INTO p_total_clientes 
    FROM mae_cliente c 
    JOIN trs_encabezado_documento d ON c.id_cliente = d.id_cliente 
    WHERE d.id_empresa = p_id_empresa 
      AND c.activo = TRUE;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_stock_total_empresa;
DELIMITER $$
CREATE PROCEDURE sp_stock_total_empresa(
    IN p_id_empresa INT, 
    OUT p_total_stock INT
)
BEGIN
    SELECT COALESCE(SUM(p.stock), 0) INTO p_total_stock 
    FROM mae_producto p 
    WHERE p.activo = TRUE;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_total_ventas_empresa;
DELIMITER $$
CREATE PROCEDURE sp_total_ventas_empresa(
    IN p_id_empresa INT, 
    OUT p_total_ventas DECIMAL(15,2)
)
BEGIN
    SELECT COALESCE(SUM(dt.importe), 0.00) INTO p_total_ventas 
    FROM trs_detalle_documento dt 
    JOIN trs_encabezado_documento d ON dt.id_documento = d.id_documento 
    WHERE d.id_empresa = p_id_empresa 
      AND d.estado_doc = 'EMITIDO';
END$$
DELIMITER ;

-- Inserción - Maestras

DROP PROCEDURE IF EXISTS sp_insertar_ubicacion;
DELIMITER $$
CREATE PROCEDURE sp_insertar_ubicacion(IN p_descripcion VARCHAR(100))
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT 'Error al insertar ubicación' AS mensaje;
        ROLLBACK;
    END;
    
    START TRANSACTION;
        INSERT INTO mae_ubicacion(descripcion) 
        VALUES (p_descripcion);
        
        SELECT LAST_INSERT_ID() AS id_ubicacion;
    COMMIT;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_insertar_identidad;
DELIMITER $$
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
        INSERT INTO mae_identidad(
            tipo_identificacion, 
            codigo_documento
        ) 
        VALUES (
            p_tipo_identificacion, 
            p_codigo_documento
        );
        
        SELECT LAST_INSERT_ID() AS id_identidad;
    COMMIT;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_insertar_cliente;
DELIMITER $$
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
        INSERT INTO mae_cliente(
            nombre, 
            apellido, 
            id_ubicacion, 
            id_identidad
        ) 
        VALUES (
            p_nombre, 
            p_apellido, 
            p_id_ubicacion, 
            p_id_identidad
        );
        
        SELECT LAST_INSERT_ID() AS id_cliente;
    COMMIT;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_insertar_empresa;
DELIMITER $$
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
        INSERT INTO mae_empresa(
            nombre, 
            razon_social, 
            RUC, 
            id_ubicacion
        ) 
        VALUES (
            p_nombre, 
            p_razon_social, 
            p_RUC, 
            p_id_ubicacion
        );
        
        SELECT LAST_INSERT_ID() AS id_empresa;
    COMMIT;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_insertar_conductor;
DELIMITER $$
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
        INSERT INTO mae_conductor(
            nombre, 
            n_licencia
        ) 
        VALUES (
            p_nombre, 
            p_n_licencia
        );
        
        SELECT LAST_INSERT_ID() AS id_conductor;
    COMMIT;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_insertar_vehiculo;
DELIMITER $$
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
        INSERT INTO mae_vehiculo(
            descripcion, 
            placa
        ) 
        VALUES (
            p_descripcion, 
            p_placa
        );
        
        SELECT LAST_INSERT_ID() AS id_vehiculo;
    COMMIT;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_insertar_producto;
DELIMITER $$
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
        INSERT INTO mae_producto(
            nombre, 
            descripcion, 
            precio_base, 
            stock, 
            unidad_medida
        ) 
        VALUES (
            p_nombre, 
            p_descripcion, 
            p_precio_base, 
            p_stock, 
            p_unidad_medida
        );
        
        SELECT LAST_INSERT_ID() AS id_producto;
    COMMIT;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_insertar_forma_pago;
DELIMITER $$
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
        INSERT INTO mae_forma_pago(
            nombre, 
            descripcion
        ) 
        VALUES (
            p_nombre, 
            p_descripcion
        );
        
        SELECT LAST_INSERT_ID() AS id_forma_pago;
    COMMIT;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_insertar_moneda;
DELIMITER $$
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
        INSERT INTO mae_moneda(
            codigo_iso, 
            nombre
        ) 
        VALUES (
            p_codigo_iso, 
            p_nombre
        );
        
        SELECT LAST_INSERT_ID() AS id_moneda;
    COMMIT;
END$$
DELIMITER ;

-- Inserción - Transaccional

DROP PROCEDURE IF EXISTS sp_insertar_encabezado_documento;
DELIMITER $$
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
            tipo_doc, 
            fecha_emision, 
            id_empresa, 
            id_cliente, 
            id_forma_pago, 
            id_moneda
        ) 
        VALUES (
            p_tipo_doc, 
            p_fecha_emision, 
            p_id_empresa, 
            p_id_cliente, 
            p_id_forma_pago, 
            p_id_moneda
        );
        
        SELECT LAST_INSERT_ID() AS id_documento;
    COMMIT;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_insertar_detalle_documento;
DELIMITER $$
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
            id_documento, 
            id_producto, 
            cantidad, 
            subtotal, 
            igv, 
            importe
        ) 
        VALUES (
            p_id_documento, 
            p_id_producto, 
            p_cantidad, 
            p_subtotal, 
            p_igv, 
            p_importe
        );
        
        SELECT LAST_INSERT_ID() AS id_detalle;
    COMMIT;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_insertar_encabezado_guia;
DELIMITER $$
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
            id_doc_venta, 
            nro_guia, 
            fecha_emision, 
            fecha_inicio_traslado, 
            motivo_traslado, 
            direccion_partida, 
            direccion_llegada, 
            id_conductor, 
            id_vehiculo
        ) 
        VALUES (
            p_id_doc_venta, 
            p_nro_guia, 
            p_fecha_emision, 
            p_fecha_inicio_traslado, 
            p_motivo_traslado, 
            p_direccion_partida, 
            p_direccion_llegada, 
            p_id_conductor, 
            p_id_vehiculo
        );
        
        SELECT LAST_INSERT_ID() AS id_guia;
    COMMIT;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_insertar_detalle_guia;
DELIMITER $$
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
            id_guia, 
            id_producto, 
            descripcion, 
            unidad_medida, 
            unidad_peso_bruto, 
            peso_total_carga, 
            modalidad_trans, 
            transbordo_prog, 
            categoriaM1_L, 
            retorno_envases, 
            vehiculo_vacio, 
            id_conductor, 
            id_vehiculo
        ) 
        VALUES (
            p_id_guia, 
            p_id_producto, 
            p_descripcion, 
            p_unidad_medida, 
            p_unidad_peso_bruto, 
            p_peso_total_carga, 
            p_modalidad_trans, 
            p_transbordo_prog, 
            p_categoriaM1_L, 
            p_retorno_envases, 
            p_vehiculo_vacio, 
            p_id_conductor, 
            p_id_vehiculo
        );
        
        SELECT LAST_INSERT_ID() AS id_detalle_guia;
    COMMIT;
END$$
DELIMITER ;

-- CRUD - Conductores

DROP PROCEDURE IF EXISTS sp_obtener_conductores_activos;
DELIMITER $$
CREATE PROCEDURE sp_obtener_conductores_activos()
BEGIN
    SELECT id_conductor, 
           nombre, 
           n_licencia, 
           activo 
    FROM mae_conductor 
    WHERE activo = TRUE 
    ORDER BY nombre;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_actualizar_conductor;
DELIMITER $$
CREATE PROCEDURE sp_actualizar_conductor(
    IN p_id_conductor INT, 
    IN p_nombre VARCHAR(50), 
    IN p_n_licencia CHAR(12)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error al actualizar conductor' AS mensaje;
    END;
    
    START TRANSACTION;
        UPDATE mae_conductor 
        SET nombre = p_nombre, 
            n_licencia = p_n_licencia, 
            activo = TRUE 
        WHERE id_conductor = p_id_conductor;
        
        SELECT 'Conductor actualizado exitosamente' AS mensaje;
    COMMIT;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_desactivar_conductor;
DELIMITER $$
CREATE PROCEDURE sp_desactivar_conductor(IN p_id_conductor INT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error al desactivar conductor' AS mensaje;
    END;
    
    START TRANSACTION;
        UPDATE mae_conductor 
        SET activo = FALSE 
        WHERE id_conductor = p_id_conductor;
        
        SELECT 'Conductor desactivado exitosamente' AS mensaje;
    COMMIT;
END$$
DELIMITER ;

-- CRUD - Vehículos

DROP PROCEDURE IF EXISTS sp_obtener_vehiculos_activos;
DELIMITER $$
CREATE PROCEDURE sp_obtener_vehiculos_activos()
BEGIN
    SELECT id_vehiculo, 
           descripcion, 
           placa, 
           activo 
    FROM mae_vehiculo 
    WHERE activo = TRUE 
    ORDER BY descripcion;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_actualizar_vehiculo;
DELIMITER $$
CREATE PROCEDURE sp_actualizar_vehiculo(
    IN p_id_vehiculo INT, 
    IN p_descripcion VARCHAR(50), 
    IN p_placa CHAR(8)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error al actualizar vehículo' AS mensaje;
    END;
    
    START TRANSACTION;
        UPDATE mae_vehiculo 
        SET descripcion = p_descripcion, 
            placa = p_placa, 
            activo = TRUE 
        WHERE id_vehiculo = p_id_vehiculo;
        
        SELECT 'Vehículo actualizado exitosamente' AS mensaje;
    COMMIT;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_desactivar_vehiculo;
DELIMITER $$
CREATE PROCEDURE sp_desactivar_vehiculo(IN p_id_vehiculo INT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error al desactivar vehículo' AS mensaje;
    END;
    
    START TRANSACTION;
        UPDATE mae_vehiculo 
        SET activo = FALSE 
        WHERE id_vehiculo = p_id_vehiculo;
        
        SELECT 'Vehículo desactivado exitosamente' AS mensaje;
    COMMIT;
END$$
DELIMITER ;

-- CRUD - Formas de pago

DROP PROCEDURE IF EXISTS sp_obtener_formas_pago_activas;
DELIMITER $$
CREATE PROCEDURE sp_obtener_formas_pago_activas()
BEGIN
    SELECT id_forma_pago, 
           nombre, 
           descripcion, 
           activo 
    FROM mae_forma_pago 
    WHERE activo = TRUE 
    ORDER BY nombre;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_actualizar_forma_pago;
DELIMITER $$
CREATE PROCEDURE sp_actualizar_forma_pago(
    IN p_id_forma_pago INT, 
    IN p_nombre VARCHAR(35), 
    IN p_descripcion VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error al actualizar forma de pago' AS mensaje;
    END;
    
    START TRANSACTION;
        UPDATE mae_forma_pago 
        SET nombre = p_nombre, 
            descripcion = p_descripcion, 
            activo = TRUE 
        WHERE id_forma_pago = p_id_forma_pago;
        
        SELECT 'Forma de pago actualizada exitosamente' AS mensaje;
    COMMIT;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_desactivar_forma_pago;
DELIMITER $$
CREATE PROCEDURE sp_desactivar_forma_pago(IN p_id_forma_pago INT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error al desactivar forma de pago' AS mensaje;
    END;
    
    START TRANSACTION;
        UPDATE mae_forma_pago 
        SET activo = FALSE 
        WHERE id_forma_pago = p_id_forma_pago;
        
        SELECT 'Forma de pago desactivada exitosamente' AS mensaje;
    COMMIT;
END$$
DELIMITER ;

-- CRUD - Monedas

DROP PROCEDURE IF EXISTS sp_obtener_monedas_activas;
DELIMITER $$
CREATE PROCEDURE sp_obtener_monedas_activas()
BEGIN
    SELECT id_moneda, 
           codigo_iso, 
           nombre, 
           activo 
    FROM mae_moneda 
    WHERE activo = TRUE 
    ORDER BY nombre;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_actualizar_moneda;
DELIMITER $$
CREATE PROCEDURE sp_actualizar_moneda(
    IN p_id_moneda INT, 
    IN p_codigo_iso CHAR(3), 
    IN p_nombre VARCHAR(20)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error al actualizar moneda' AS mensaje;
    END;
    
    START TRANSACTION;
        UPDATE mae_moneda 
        SET codigo_iso = p_codigo_iso, 
            nombre = p_nombre, 
            activo = TRUE 
        WHERE id_moneda = p_id_moneda;
        
        SELECT 'Moneda actualizada exitosamente' AS mensaje;
    COMMIT;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_desactivar_moneda;
DELIMITER $
CREATE PROCEDURE sp_desactivar_moneda(IN p_id_moneda INT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error al desactivar moneda' AS mensaje;
    END;
    
    START TRANSACTION;
        UPDATE mae_moneda 
        SET activo = FALSE 
        WHERE id_moneda = p_id_moneda;
        
        SELECT 'Moneda desactivada exitosamente' AS mensaje;
    COMMIT;
END$
DELIMITER ;

-- CRUD - Ubicaciones

DROP PROCEDURE IF EXISTS sp_obtener_ubicaciones_activas;
DELIMITER $
CREATE PROCEDURE sp_obtener_ubicaciones_activas()
BEGIN
    SELECT id_ubicacion, 
           descripcion, 
           activo 
    FROM mae_ubicacion 
    WHERE activo = TRUE 
    ORDER BY descripcion;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_actualizar_ubicacion;
DELIMITER $
CREATE PROCEDURE sp_actualizar_ubicacion(
    IN p_id_ubicacion INT, 
    IN p_descripcion VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error al actualizar ubicación' AS mensaje;
    END;
    
    START TRANSACTION;
        UPDATE mae_ubicacion 
        SET descripcion = p_descripcion, 
            activo = TRUE 
        WHERE id_ubicacion = p_id_ubicacion;
        
        SELECT 'Ubicación actualizada exitosamente' AS mensaje;
    COMMIT;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_desactivar_ubicacion;
DELIMITER $
CREATE PROCEDURE sp_desactivar_ubicacion(IN p_id_ubicacion INT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error al desactivar ubicación' AS mensaje;
    END;
    
    START TRANSACTION;
        UPDATE mae_ubicacion 
        SET activo = FALSE 
        WHERE id_ubicacion = p_id_ubicacion;
        
        SELECT 'Ubicación desactivada exitosamente' AS mensaje;
    COMMIT;
END$
DELIMITER ;

-- CRUD - Identidades

DROP PROCEDURE IF EXISTS sp_obtener_identidades_activas;
DELIMITER $
CREATE PROCEDURE sp_obtener_identidades_activas()
BEGIN
    SELECT id_identidad, 
           tipo_identificacion, 
           codigo_documento, 
           activo 
    FROM mae_identidad 
    WHERE activo = TRUE 
    ORDER BY tipo_identificacion, codigo_documento;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_actualizar_identidad;
DELIMITER $
CREATE PROCEDURE sp_actualizar_identidad(
    IN p_id_identidad INT, 
    IN p_tipo_identificacion VARCHAR(20), 
    IN p_codigo_documento VARCHAR(15)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error al actualizar identidad' AS mensaje;
    END;
    
    START TRANSACTION;
        UPDATE mae_identidad 
        SET tipo_identificacion = p_tipo_identificacion, 
            codigo_documento = p_codigo_documento, 
            activo = TRUE 
        WHERE id_identidad = p_id_identidad;
        
        SELECT 'Identidad actualizada exitosamente' AS mensaje;
    COMMIT;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_desactivar_identidad;
DELIMITER $
CREATE PROCEDURE sp_desactivar_identidad(IN p_id_identidad INT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error al desactivar identidad' AS mensaje;
    END;
    
    START TRANSACTION;
        UPDATE mae_identidad 
        SET activo = FALSE 
        WHERE id_identidad = p_id_identidad;
        
        SELECT 'Identidad desactivada exitosamente' AS mensaje;
    COMMIT;
END$
DELIMITER ;

-- CRUD - Clientes

DROP PROCEDURE IF EXISTS sp_obtener_clientes_activos;
DELIMITER $
CREATE PROCEDURE sp_obtener_clientes_activos()
BEGIN
    SELECT c.id_cliente, 
           c.nombre, 
           c.apellido, 
           u.descripcion AS ubicacion, 
           i.tipo_identificacion, 
           i.codigo_documento, 
           c.activo, 
           c.id_ubicacion, 
           c.id_identidad
    FROM mae_cliente c 
    JOIN mae_ubicacion u ON c.id_ubicacion = u.id_ubicacion 
    JOIN mae_identidad i ON c.id_identidad = i.id_identidad 
    WHERE c.activo = TRUE 
    ORDER BY c.nombre, c.apellido;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_actualizar_cliente;
DELIMITER $
CREATE PROCEDURE sp_actualizar_cliente(
    IN p_id_cliente INT, 
    IN p_nombre VARCHAR(50), 
    IN p_apellido VARCHAR(50), 
    IN p_id_ubicacion INT, 
    IN p_id_identidad INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error al actualizar cliente' AS mensaje;
    END;
    
    START TRANSACTION;
        UPDATE mae_cliente 
        SET nombre = p_nombre, 
            apellido = p_apellido, 
            id_ubicacion = p_id_ubicacion, 
            id_identidad = p_id_identidad, 
            activo = TRUE 
        WHERE id_cliente = p_id_cliente;
        
        SELECT 'Cliente actualizado exitosamente' AS mensaje;
    COMMIT;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_desactivar_cliente;
DELIMITER $
CREATE PROCEDURE sp_desactivar_cliente(IN p_id_cliente INT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error al desactivar cliente' AS mensaje;
    END;
    
    START TRANSACTION;
        UPDATE mae_cliente 
        SET activo = FALSE 
        WHERE id_cliente = p_id_cliente;
        
        SELECT 'Cliente desactivado exitosamente' AS mensaje;
    COMMIT;
END$
DELIMITER ;

-- CRUD - Productos

DROP PROCEDURE IF EXISTS sp_obtener_productos_activos;
DELIMITER $
CREATE PROCEDURE sp_obtener_productos_activos()
BEGIN
    SELECT id_producto, 
           nombre, 
           descripcion, 
           precio_base, 
           stock, 
           unidad_medida, 
           activo 
    FROM mae_producto 
    WHERE activo = TRUE 
    ORDER BY nombre;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_actualizar_producto;
DELIMITER $
CREATE PROCEDURE sp_actualizar_producto(
    IN p_id_producto INT, 
    IN p_nombre VARCHAR(50), 
    IN p_descripcion VARCHAR(100), 
    IN p_precio_base DECIMAL(10,2), 
    IN p_stock INT, 
    IN p_unidad_medida VARCHAR(10)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error al actualizar producto' AS mensaje;
    END;
    
    START TRANSACTION;
        UPDATE mae_producto 
        SET nombre = p_nombre, 
            descripcion = p_descripcion, 
            precio_base = p_precio_base, 
            stock = p_stock, 
            unidad_medida = p_unidad_medida, 
            activo = TRUE 
        WHERE id_producto = p_id_producto;
        
        SELECT 'Producto actualizado exitosamente' AS mensaje;
    COMMIT;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_desactivar_producto;
DELIMITER $
CREATE PROCEDURE sp_desactivar_producto(IN p_id_producto INT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error al desactivar producto' AS mensaje;
    END;
    
    START TRANSACTION;
        UPDATE mae_producto 
        SET activo = FALSE 
        WHERE id_producto = p_id_producto;
        
        SELECT 'Producto desactivado exitosamente' AS mensaje;
    COMMIT;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_ajustar_stock_producto;
DELIMITER $
CREATE PROCEDURE sp_ajustar_stock_producto(
    IN p_id_producto INT, 
    IN p_cantidad INT, 
    IN p_tipo_movimiento VARCHAR(10)
)
BEGIN
    DECLARE v_stock_actual INT;
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error al ajustar stock' AS mensaje;
    END;
    
    START TRANSACTION;
        SELECT stock INTO v_stock_actual 
        FROM mae_producto 
        WHERE id_producto = p_id_producto;
        
        IF p_tipo_movimiento = 'ENTRADA' THEN
            UPDATE mae_producto 
            SET stock = stock + p_cantidad 
            WHERE id_producto = p_id_producto;
            
            SELECT 'Stock incrementado exitosamente' AS mensaje, 
                   (v_stock_actual + p_cantidad) AS nuevo_stock;
                   
        ELSEIF p_tipo_movimiento = 'SALIDA' THEN
            IF v_stock_actual < p_cantidad THEN
                ROLLBACK;
                SELECT CONCAT('Stock insuficiente. Stock actual: ', v_stock_actual) AS mensaje;
            ELSE
                UPDATE mae_producto 
                SET stock = stock - p_cantidad 
                WHERE id_producto = p_id_producto;
                
                SELECT 'Stock reducido exitosamente' AS mensaje, 
                       (v_stock_actual - p_cantidad) AS nuevo_stock;
            END IF;
        ELSE
            ROLLBACK;
            SELECT 'Tipo de movimiento inválido. Use ENTRADA o SALIDA' AS mensaje;
        END IF;
    COMMIT;
END$
DELIMITER ;

-- Movimientos de inventario

DROP PROCEDURE IF EXISTS sp_obtener_movimientos_inventario;
DELIMITER $
CREATE PROCEDURE sp_obtener_movimientos_inventario()
BEGIN
    SELECT d.id_documento, 
           d.tipo_doc, 
           d.fecha_emision, 
           p.nombre AS producto, 
           dt.cantidad, 
           d.estado_doc, 
           'SALIDA' AS tipo_movimiento
    FROM trs_detalle_documento dt 
    JOIN trs_encabezado_documento d ON dt.id_documento = d.id_documento 
    JOIN mae_producto p ON dt.id_producto = p.id_producto
    WHERE d.estado_doc = 'EMITIDO' 
    ORDER BY d.fecha_emision DESC 
    LIMIT 100;
END$
DELIMITER ;

-- Documentos

DROP PROCEDURE IF EXISTS sp_obtener_documentos_empresa;
DELIMITER $
CREATE PROCEDURE sp_obtener_documentos_empresa(IN p_id_empresa INT)
BEGIN
    SELECT d.id_documento, 
           d.tipo_doc, 
           d.fecha_emision, 
           CONCAT(c.nombre, ' ', c.apellido) AS cliente, 
           fp.nombre AS forma_pago, 
           m.codigo_iso AS moneda, 
           d.estado_doc
    FROM trs_encabezado_documento d 
    JOIN mae_cliente c ON d.id_cliente = c.id_cliente 
    JOIN mae_forma_pago fp ON d.id_forma_pago = fp.id_forma_pago 
    JOIN mae_moneda m ON d.id_moneda = m.id_moneda
    WHERE d.id_empresa = p_id_empresa 
    ORDER BY d.fecha_emision DESC, d.id_documento DESC;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_obtener_detalle_documento;
DELIMITER $
CREATE PROCEDURE sp_obtener_detalle_documento(IN p_id_documento INT)
BEGIN
    SELECT p.nombre AS producto, 
           dt.cantidad, 
           dt.subtotal, 
           dt.igv, 
           dt.importe 
    FROM trs_detalle_documento dt 
    JOIN mae_producto p ON dt.id_producto = p.id_producto 
    WHERE dt.id_documento = p_id_documento;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_actualizar_estado_documento;
DELIMITER $
CREATE PROCEDURE sp_actualizar_estado_documento(
    IN p_id_documento INT, 
    IN p_nuevo_estado VARCHAR(20)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error al actualizar estado del documento' AS mensaje;
    END;
    
    START TRANSACTION;
        UPDATE trs_encabezado_documento 
        SET estado_doc = p_nuevo_estado 
        WHERE id_documento = p_id_documento;
        
        SELECT 'Estado del documento actualizado exitosamente' AS mensaje;
    COMMIT;
END$
DELIMITER ;

-- Guías de remisión

DROP PROCEDURE IF EXISTS sp_obtener_guias_empresa;
DELIMITER $
CREATE PROCEDURE sp_obtener_guias_empresa(IN p_id_empresa INT)
BEGIN
    SELECT g.id_guia, 
           g.nro_guia, 
           g.fecha_emision, 
           g.fecha_inicio_traslado, 
           g.motivo_traslado, 
           g.direccion_partida, 
           g.direccion_llegada, 
           c.nombre AS conductor, 
           v.descripcion AS vehiculo, 
           g.estado_guia, 
           d.tipo_doc, 
           d.id_documento
    FROM trs_encabezado_guia g 
    JOIN trs_encabezado_documento d ON g.id_doc_venta = d.id_documento 
    JOIN mae_conductor c ON g.id_conductor = c.id_conductor 
    JOIN mae_vehiculo v ON g.id_vehiculo = v.id_vehiculo
    WHERE d.id_empresa = p_id_empresa 
    ORDER BY g.fecha_emision DESC, g.id_guia DESC;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_obtener_detalle_guia;
DELIMITER $
CREATE PROCEDURE sp_obtener_detalle_guia(IN p_id_guia INT)
BEGIN
    SELECT p.nombre AS producto, 
           dg.descripcion, 
           dg.unidad_medida, 
           dg.peso_total_carga, 
           dg.modalidad_trans 
    FROM trs_detalle_guia dg 
    JOIN mae_producto p ON dg.id_producto = p.id_producto 
    WHERE dg.id_guia = p_id_guia;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_actualizar_estado_guia;
DELIMITER $
CREATE PROCEDURE sp_actualizar_estado_guia(
    IN p_id_guia INT, 
    IN p_nuevo_estado VARCHAR(20)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error al actualizar estado de la guía' AS mensaje;
    END;
    
    START TRANSACTION;
        UPDATE trs_encabezado_guia 
        SET estado_guia = p_nuevo_estado 
        WHERE id_guia = p_id_guia;
        
        SELECT 'Estado de la guía actualizado exitosamente' AS mensaje;
    COMMIT;
END$
DELIMITER ;

-- Combos

DROP PROCEDURE IF EXISTS sp_obtener_ubicaciones_combo;
DELIMITER $
CREATE PROCEDURE sp_obtener_ubicaciones_combo()
BEGIN
    SELECT id_ubicacion, 
           descripcion 
    FROM mae_ubicacion 
    WHERE activo = TRUE 
    ORDER BY descripcion;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_obtener_identidades_combo;
DELIMITER $
CREATE PROCEDURE sp_obtener_identidades_combo()
BEGIN
    SELECT id_identidad, 
           tipo_identificacion, 
           codigo_documento 
    FROM mae_identidad 
    WHERE activo = TRUE 
    ORDER BY tipo_identificacion, codigo_documento;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_obtener_clientes_combo;
DELIMITER $
CREATE PROCEDURE sp_obtener_clientes_combo()
BEGIN
    SELECT id_cliente, 
           nombre, 
           apellido 
    FROM mae_cliente 
    WHERE activo = TRUE 
    ORDER BY nombre, apellido;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_obtener_formas_pago_combo;
DELIMITER $
CREATE PROCEDURE sp_obtener_formas_pago_combo()
BEGIN
    SELECT id_forma_pago, 
           nombre 
    FROM mae_forma_pago 
    WHERE activo = TRUE 
    ORDER BY nombre;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_obtener_monedas_combo;
DELIMITER $
CREATE PROCEDURE sp_obtener_monedas_combo()
BEGIN
    SELECT id_moneda, 
           codigo_iso, 
           nombre 
    FROM mae_moneda 
    WHERE activo = TRUE 
    ORDER BY nombre;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_obtener_productos_combo;
DELIMITER $
CREATE PROCEDURE sp_obtener_productos_combo()
BEGIN
    SELECT id_producto, 
           nombre, 
           precio_base, 
           stock 
    FROM mae_producto 
    WHERE activo = TRUE 
    ORDER BY nombre;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_obtener_conductores_combo;
DELIMITER $
CREATE PROCEDURE sp_obtener_conductores_combo()
BEGIN
    SELECT id_conductor, 
           nombre, 
           n_licencia 
    FROM mae_conductor 
    WHERE activo = TRUE 
    ORDER BY nombre;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_obtener_vehiculos_combo;
DELIMITER $
CREATE PROCEDURE sp_obtener_vehiculos_combo()
BEGIN
    SELECT id_vehiculo, 
           descripcion, 
           placa 
    FROM mae_vehiculo 
    WHERE activo = TRUE 
    ORDER BY descripcion;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_obtener_documentos_emitidos;
DELIMITER $
CREATE PROCEDURE sp_obtener_documentos_emitidos(IN p_id_empresa INT)
BEGIN
    SELECT d.id_documento, 
           d.tipo_doc, 
           d.fecha_emision, 
           CONCAT(c.nombre, ' ', c.apellido) AS cliente
    FROM trs_encabezado_documento d 
    JOIN mae_cliente c ON d.id_cliente = c.id_cliente
    WHERE d.id_empresa = p_id_empresa 
      AND d.estado_doc = 'EMITIDO' 
      AND d.id_documento NOT IN (
          SELECT id_doc_venta 
          FROM trs_encabezado_guia
      )
    ORDER BY d.fecha_emision DESC;
END$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_obtener_productos_documento;
DELIMITER $
CREATE PROCEDURE sp_obtener_productos_documento(IN p_id_documento INT)
BEGIN
    SELECT p.id_producto, 
           p.nombre, 
           dt.cantidad, 
           p.unidad_medida 
    FROM trs_detalle_documento dt 
    JOIN mae_producto p ON dt.id_producto = p.id_producto 
    WHERE dt.id_documento = p_id_documento;
END$
DELIMITER ;

-- Validaciones

DROP PROCEDURE IF EXISTS sp_verificar_guia_existe;
DELIMITER $
CREATE PROCEDURE sp_verificar_guia_existe(IN p_nro_guia VARCHAR(20))
BEGIN
    SELECT COUNT(*) AS existe 
    FROM trs_encabezado_guia 
    WHERE nro_guia = p_nro_guia;
END$
DELIMITER ;