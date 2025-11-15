
USE sistema_documentos;

-- Índices

-- Índices únicos

CREATE UNIQUE INDEX UQ_mae_empresa_RUC ON mae_empresa(RUC);

CREATE UNIQUE INDEX UQ_mae_conductor_licencia ON mae_conductor(n_licencia);

CREATE UNIQUE INDEX UQ_mae_vehiculo_placa ON mae_vehiculo(placa);

CREATE UNIQUE INDEX UQ_trs_encabezado_guia_nro_guia ON trs_encabezado_guia(nro_guia);

CREATE UNIQUE INDEX UQ_mae_producto_nombre ON mae_producto(nombre);

CREATE UNIQUE INDEX UQ_mae_moneda_codigo_iso ON mae_moneda(codigo_iso);

CREATE UNIQUE INDEX UQ_mae_identidad_codigo_documento ON mae_identidad(codigo_documento);

-- Índices de optimización de búsqueda

CREATE INDEX IDX_trs_encabezado_documento_fecha ON trs_encabezado_documento(fecha_emision);

CREATE INDEX IDX_trs_encabezado_documento_cliente ON trs_encabezado_documento(id_cliente);

CREATE INDEX IDX_trs_encabezado_documento_tipo ON trs_encabezado_documento(tipo_doc);

CREATE INDEX IDX_trs_detalle_documento_producto ON trs_detalle_documento(id_producto);

CREATE INDEX IDX_trs_encabezado_guia_fecha ON trs_encabezado_guia(fecha_emision);

CREATE INDEX IDX_trs_encabezado_guia_doc_venta ON trs_encabezado_guia(id_doc_venta);

CREATE INDEX IDX_mae_cliente_nombre ON mae_cliente(nombre);

CREATE INDEX IDX_mae_cliente_identidad ON mae_cliente(id_identidad);

CREATE INDEX IDX_trs_detalle_guia_producto ON trs_detalle_guia(id_producto);

-- Triggers

-- Evita insertar productos con nombre duplicado o stock negativo

DROP TRIGGER IF EXISTS trg_before_insert_mae_producto;
DELIMITER $$
CREATE TRIGGER trg_before_insert_mae_producto
BEFORE INSERT ON mae_producto
FOR EACH ROW
BEGIN
    DECLARE v_id INT;
    DECLARE v_activo BOOLEAN;
    DECLARE v_stock_actual INT;

    SELECT id_producto, activo, stock INTO v_id, v_activo, v_stock_actual
    FROM mae_producto
    WHERE nombre = NEW.nombre
    LIMIT 1;

    IF v_id IS NOT NULL AND v_activo = FALSE THEN
        UPDATE mae_producto
        SET stock = v_stock_actual + NEW.stock,
            activo = TRUE,
            descripcion = NEW.descripcion,
            precio_base = NEW.precio_base,
            unidad_medida = NEW.unidad_medida
        WHERE id_producto = v_id;

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Producto reactivado automáticamente. Inserción cancelada.';
    END IF;

    IF v_id IS NOT NULL AND v_activo = TRUE THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El producto ya existe y está activo.';
    END IF;

    IF NEW.stock < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se permite registrar productos con stock negativo.';
    END IF;
END$$
DELIMITER ;

-- Evita actualizaciones de stock negativo

DROP TRIGGER IF EXISTS trg_before_update_mae_producto_stock;
DELIMITER $$
CREATE TRIGGER trg_before_update_mae_producto_stock
BEFORE UPDATE ON mae_producto
FOR EACH ROW
BEGIN
    IF NEW.stock < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El stock no puede ser negativo.';
    END IF;
END$$
DELIMITER ;

-- Evita reducciones extremas de precio base

DROP TRIGGER IF EXISTS trg_before_update_precio_producto;
DELIMITER $$
CREATE TRIGGER trg_before_update_precio_producto
BEFORE UPDATE ON mae_producto
FOR EACH ROW
BEGIN
    IF NEW.precio_base < (OLD.precio_base * 0.5) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El nuevo precio no puede ser inferior al 50% del precio anterior.';
    END IF;
END$$
DELIMITER ;

-- Eliminación Lógica Cliente

DROP TRIGGER IF EXISTS trg_before_delete_mae_cliente;
DELIMITER $$
CREATE TRIGGER trg_before_delete_mae_cliente
BEFORE DELETE ON mae_cliente
FOR EACH ROW
BEGIN
    INSERT INTO log_eliminaciones (id_registro, tabla, fecha_hora)
    VALUES (OLD.id_cliente, 'mae_cliente', NOW());

    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'No se permite eliminar clientes. Use activo=FALSE y log.';
END$$
DELIMITER ;

-- Eliminación Lógica Empresa

DROP TRIGGER IF EXISTS trg_before_delete_mae_empresa;
DELIMITER $$
CREATE TRIGGER trg_before_delete_mae_empresa
BEFORE DELETE ON mae_empresa
FOR EACH ROW
BEGIN
    INSERT INTO log_eliminaciones (id_registro, tabla, fecha_hora)
    VALUES (OLD.id_empresa, 'mae_empresa', NOW());

    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'No se permite eliminar empresas. Use activo=FALSE y log.';
END$$
DELIMITER ;

-- Eliminación Lógica Ubicación

DROP TRIGGER IF EXISTS trg_before_delete_mae_ubicacion;
DELIMITER $$
CREATE TRIGGER trg_before_delete_mae_ubicacion
BEFORE DELETE ON mae_ubicacion
FOR EACH ROW
BEGIN
    INSERT INTO log_eliminaciones (id_registro, tabla, fecha_hora)
    VALUES (OLD.id_ubicacion, 'mae_ubicacion', NOW());

    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'No se permite eliminar ubicaciones. Use activo=FALSE y log.';
END$$
DELIMITER ;

-- Eliminación Lógica Identidad

DROP TRIGGER IF EXISTS trg_before_delete_mae_identidad;
DELIMITER $$
CREATE TRIGGER trg_before_delete_mae_identidad
BEFORE DELETE ON mae_identidad
FOR EACH ROW
BEGIN
    INSERT INTO log_eliminaciones (id_registro, tabla, fecha_hora)
    VALUES (OLD.id_identidad, 'mae_identidad', NOW());

    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'No se permite eliminar identidades. Use activo=FALSE y log.';
END$$
DELIMITER ;

-- Eliminación Lógica Conductor

DROP TRIGGER IF EXISTS trg_before_delete_mae_conductor;
DELIMITER $$
CREATE TRIGGER trg_before_delete_mae_conductor
BEFORE DELETE ON mae_conductor
FOR EACH ROW
BEGIN
    INSERT INTO log_eliminaciones (id_registro, tabla, fecha_hora)
    VALUES (OLD.id_conductor, 'mae_conductor', NOW());

    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'No se permite eliminar conductores. Use activo=FALSE y log.';
END$$
DELIMITER ;

-- Eliminación Lógica Vehículo

DROP TRIGGER IF EXISTS trg_before_delete_mae_vehiculo;
DELIMITER $$
CREATE TRIGGER trg_before_delete_mae_vehiculo
BEFORE DELETE ON mae_vehiculo
FOR EACH ROW
BEGIN
    INSERT INTO log_eliminaciones (id_registro, tabla, fecha_hora)
    VALUES (OLD.id_vehiculo, 'mae_vehiculo', NOW());

    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'No se permite eliminar vehículos. Use activo=FALSE y log.';
END$$
DELIMITER ;

-- Eliminación Lógica Producto

DROP TRIGGER IF EXISTS trg_before_delete_mae_producto;
DELIMITER $$
CREATE TRIGGER trg_before_delete_mae_producto
BEFORE DELETE ON mae_producto
FOR EACH ROW
BEGIN
    INSERT INTO log_eliminaciones (id_registro, tabla, fecha_hora)
    VALUES (OLD.id_producto, 'mae_producto', NOW());

    SIGNAL SQLSTATE '45000' 
    SET MESSAGE_TEXT = 'No se permite eliminar productos. Use activo=FALSE y log.';
END$$
DELIMITER ;

-- Fecha automática si no se proporciona

DROP TRIGGER IF EXISTS trg_before_insert_documento;
DELIMITER $$
CREATE TRIGGER trg_before_insert_documento
BEFORE INSERT ON trs_encabezado_documento
FOR EACH ROW
BEGIN
    IF NEW.fecha_emision IS NULL THEN
        SET NEW.fecha_emision = CURDATE();
    END IF;
END$$
DELIMITER ;

-- Impide Crear guía con nro usado

DROP TRIGGER IF EXISTS trg_before_insert_guia;
DELIMITER $$
CREATE TRIGGER trg_before_insert_guia
BEFORE INSERT ON trs_encabezado_guia
FOR EACH ROW
BEGIN
    IF NEW.fecha_emision IS NULL THEN
        SET NEW.fecha_emision = CURDATE();
    END IF;

    IF EXISTS (SELECT 1 FROM trs_encabezado_guia WHERE nro_guia = NEW.nro_guia) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Número de guía ya existe. Ingrese uno diferente.';
    END IF;
END$$
DELIMITER ;

-- Evita cambios de fecha si documento está pendiente

DROP TRIGGER IF EXISTS trg_before_update_documento_fecha;
DELIMITER $$
CREATE TRIGGER trg_before_update_documento_fecha
BEFORE UPDATE ON trs_encabezado_documento
FOR EACH ROW
BEGIN
    IF OLD.estado_doc = 'PENDIENTE' THEN
        IF NEW.fecha_emision IS NULL THEN
            SET NEW.fecha_emision = OLD.fecha_emision;
        END IF;
    END IF;
END$$
DELIMITER ;

-- Evita cambios de fecha si guía está pendiente

DROP TRIGGER IF EXISTS trg_before_update_guia_fecha;
DELIMITER $$
CREATE TRIGGER trg_before_update_guia_fecha
BEFORE UPDATE ON trs_encabezado_guia
FOR EACH ROW
BEGIN
    IF OLD.estado_guia = 'PENDIENTE' THEN
        IF NEW.fecha_emision IS NULL THEN
            SET NEW.fecha_emision = OLD.fecha_emision;
        END IF;
    END IF;
END$$
DELIMITER ;

-- Validación de estados - solo pendientes pueden anularse

DROP TRIGGER IF EXISTS trg_before_update_guia_estado;
DELIMITER $$
CREATE TRIGGER trg_before_update_guia_estado
BEFORE UPDATE ON trs_encabezado_guia
FOR EACH ROW
BEGIN
    IF NEW.estado_guia = 'ANULADO' AND OLD.estado_guia <> 'PENDIENTE' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Solo se pueden anular guías pendientes.';
    END IF;
END$$
DELIMITER ;

-- Validación de estados - solo documentos pendientes pueden anularse

DROP TRIGGER IF EXISTS trg_before_update_documento_estado;
DELIMITER $$
CREATE TRIGGER trg_before_update_documento_estado
BEFORE UPDATE ON trs_encabezado_documento
FOR EACH ROW
BEGIN
    IF NEW.estado_doc = 'ANULADO' AND OLD.estado_doc <> 'PENDIENTE' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Solo se pueden anular documentos pendientes.';
    END IF;
END$$
DELIMITER ;

-- Valida stock antes de emitir documento

DROP TRIGGER IF EXISTS trg_before_update_documento_emitido;
DELIMITER $$
CREATE TRIGGER trg_before_update_documento_emitido
BEFORE UPDATE ON trs_encabezado_documento
FOR EACH ROW
BEGIN
    DECLARE v_producto INT;
    DECLARE v_cantidad INT;
    DECLARE v_stock_actual INT;
    DECLARE v_terminado INT DEFAULT 0;
    DECLARE v_nombre_producto VARCHAR(50);
    
    IF NEW.estado_doc = 'EMITIDO' AND OLD.estado_doc != 'EMITIDO' THEN
        BEGIN
            DECLARE cur_detalle CURSOR FOR 
                SELECT id_producto, cantidad 
                FROM trs_detalle_documento
                WHERE id_documento = NEW.id_documento;
            
            DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_terminado = 1;
            
            OPEN cur_detalle;
            
            read_loop: LOOP
                FETCH cur_detalle INTO v_producto, v_cantidad;
                
                IF v_terminado = 1 THEN
                    LEAVE read_loop;
                END IF;
                
                SELECT stock, nombre 
                INTO v_stock_actual, v_nombre_producto
                FROM mae_producto 
                WHERE id_producto = v_producto;
                
                IF v_stock_actual < v_cantidad THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Stock insuficiente para emitir el documento';
                END IF;
                
            END LOOP;
            
            CLOSE cur_detalle;
        END;
    END IF;
END$$
DELIMITER ;

-- Actualiza stock al emitir o anular documento

DROP TRIGGER IF EXISTS trg_after_update_documento_emitido;
DELIMITER $$
CREATE TRIGGER trg_after_update_documento_emitido
AFTER UPDATE ON trs_encabezado_documento
FOR EACH ROW
BEGIN
   
    IF NEW.estado_doc = 'EMITIDO' AND OLD.estado_doc != 'EMITIDO' THEN
        
        UPDATE mae_producto p
        INNER JOIN trs_detalle_documento d ON p.id_producto = d.id_producto
        SET p.stock = p.stock - d.cantidad
        WHERE d.id_documento = NEW.id_documento;
        
    END IF;
    
    
    IF NEW.estado_doc = 'ANULADO' AND OLD.estado_doc = 'EMITIDO' THEN
        
        UPDATE mae_producto p
        INNER JOIN trs_detalle_documento d ON p.id_producto = d.id_producto
        SET p.stock = p.stock + d.cantidad
        WHERE d.id_documento = NEW.id_documento;
        
    END IF;
END$$
DELIMITER ;

-- Alerta de stock bajo (25% del stock inicial)

DROP TRIGGER IF EXISTS trg_after_update_stock_minimo;
DELIMITER $$
CREATE TRIGGER trg_after_update_stock_minimo
AFTER UPDATE ON mae_producto
FOR EACH ROW
BEGIN
    DECLARE v_stock_inicial INT;
    
    SET v_stock_inicial = 100; 
    
    IF NEW.stock <= (v_stock_inicial * 0.25) AND NEW.stock < OLD.stock THEN
        
        SIGNAL SQLSTATE '01000'
        SET MESSAGE_TEXT = 'ALERTA: Stock bajo para producto';
    END IF;
END$$
DELIMITER ;

-- Bloquea modificaciones de documentos emitidos o anulados

DROP TRIGGER IF EXISTS trg_before_update_documento_bloqueo;
DELIMITER $$
CREATE TRIGGER trg_before_update_documento_bloqueo
BEFORE UPDATE ON trs_encabezado_documento
FOR EACH ROW
BEGIN
    IF OLD.estado_doc IN ('EMITIDO', 'ANULADO') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede modificar un documento que ya esta emitido o anulado';
    END IF;
END$$
DELIMITER ;

-- Bloquea modificaciones de guías emitidas o anuladas

DROP TRIGGER IF EXISTS trg_before_update_guia_bloqueo;
DELIMITER $$
CREATE TRIGGER trg_before_update_guia_bloqueo
BEFORE UPDATE ON trs_encabezado_guia
FOR EACH ROW
BEGIN
    IF OLD.estado_guia IN ('EMITIDO', 'ANULADO') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede modificar una guia que ya esta emitida o anulada';
    END IF;
END$$
DELIMITER ;

-- Valida cantidad positiva en detalle documento

DROP TRIGGER IF EXISTS trg_before_insert_detalle_documento_cantidad;
DELIMITER $$
CREATE TRIGGER trg_before_insert_detalle_documento_cantidad
BEFORE INSERT ON trs_detalle_documento
FOR EACH ROW
BEGIN
    IF NEW.cantidad <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La cantidad del detalle debe ser mayor que 0.';
    END IF;
END$$
DELIMITER ;

-- Valida RUC único para empresas activas

DELIMITER $$
DROP TRIGGER IF EXISTS trg_before_insert_mae_empresa_ruc_unico;
DELIMITER $$
CREATE TRIGGER trg_before_insert_mae_empresa_ruc_unico
BEFORE INSERT ON mae_empresa
FOR EACH ROW
BEGIN
    DECLARE v_activo BOOLEAN;

    SELECT activo INTO v_activo
    FROM mae_empresa
    WHERE RUC = NEW.RUC
    LIMIT 1;

    IF v_activo IS TRUE THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: El RUC ingresado ya pertenece a una empresa activa.';
    END IF;
END$$
DELIMITER ;

-- Maneja reactivación de empresa inactiva o previene duplicados

DROP TRIGGER IF EXISTS trg_before_insert_mae_empresa;
DELIMITER $$
CREATE TRIGGER trg_before_insert_mae_empresa
BEFORE INSERT ON mae_empresa
FOR EACH ROW
BEGIN
    DECLARE v_id_ruc INT;
    DECLARE v_activo_ruc BOOLEAN;
    DECLARE v_id_nombre INT;

    SELECT id_empresa, activo INTO v_id_ruc, v_activo_ruc
    FROM mae_empresa
    WHERE RUC = NEW.RUC
    LIMIT 1;

    SELECT id_empresa INTO v_id_nombre
    FROM mae_empresa
    WHERE nombre = NEW.nombre
    LIMIT 1;

    IF v_id_ruc IS NOT NULL THEN
        IF EXISTS (SELECT 1 FROM mae_empresa WHERE RUC = NEW.RUC AND nombre = NEW.nombre AND activo = FALSE) THEN
            UPDATE mae_empresa
            SET activo = TRUE,
                razon_social = NEW.razon_social,
                id_ubicacion = NEW.id_ubicacion
            WHERE id_empresa = v_id_ruc;

            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Empresa reactivada automáticamente. Inserción cancelada.';
        ELSE
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'ERROR: RUC ya registrado (conflicto de nombre).';
        END IF;
    END IF;

    IF v_id_nombre IS NOT NULL AND v_id_ruc IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'ERROR: Nombre de empresa ya usado con otro RUC.';
    END IF;
END$$
DELIMITER ;

-- Calcula subtotal, IGV e importe al insertar detalle documento

DROP TRIGGER IF EXISTS trg_before_insert_detalle_documento_calc;
DELIMITER $$
CREATE TRIGGER trg_before_insert_detalle_documento_calc
BEFORE INSERT ON trs_detalle_documento
FOR EACH ROW
BEGIN
    DECLARE v_igv DECIMAL(10,2);
    DECLARE v_subtotal DECIMAL(10,2);
    DECLARE v_precio_base DECIMAL(10,2);

    SET v_igv = 0.18;

    SELECT precio_base INTO v_precio_base
    FROM mae_producto
    WHERE id_producto = NEW.id_producto;

    IF NEW.subtotal IS NULL OR NEW.subtotal = 0 THEN
        SET v_subtotal = NEW.cantidad * v_precio_base;
        SET NEW.subtotal = v_subtotal;
        SET NEW.igv = v_subtotal * v_igv;
        SET NEW.importe = v_subtotal + (v_subtotal * v_igv);
    END IF;
END$$
DELIMITER ;

-- Recalcula valores al actualizar cantidad en detalle documento

DROP TRIGGER IF EXISTS trg_before_update_detalle_documento_calc;
DELIMITER $$
CREATE TRIGGER trg_before_update_detalle_documento_calc
BEFORE UPDATE ON trs_detalle_documento
FOR EACH ROW
BEGIN
    DECLARE v_igv DECIMAL(10,2);
    DECLARE v_subtotal DECIMAL(10,2);
    DECLARE v_estado_doc VARCHAR(20);
    DECLARE v_precio_base DECIMAL(10,2);

    SET v_igv = 0.18;

    SELECT estado_doc INTO v_estado_doc
    FROM trs_encabezado_documento
    WHERE id_documento = OLD.id_documento;

    IF v_estado_doc = 'EMITIDO' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se puede modificar un detalle de documento emitido.';
    END IF;

    SELECT precio_base INTO v_precio_base
    FROM mae_producto
    WHERE id_producto = NEW.id_producto;

    IF NEW.cantidad <> OLD.cantidad THEN
        SET v_subtotal = NEW.cantidad * v_precio_base;
        SET NEW.subtotal = v_subtotal;
        SET NEW.igv = v_subtotal * v_igv;
        SET NEW.importe = v_subtotal + (v_subtotal * v_igv);
    END IF;
END$$
DELIMITER ;

-- Reactiva ubicación inactiva si se intenta insertar duplicada

DROP TRIGGER IF EXISTS trg_recuperar_ubicacion;
DELIMITER $$
CREATE TRIGGER trg_recuperar_ubicacion
BEFORE INSERT ON mae_ubicacion
FOR EACH ROW
BEGIN
    DECLARE v_id INT;
    SELECT id_ubicacion INTO v_id
    FROM mae_ubicacion
    WHERE descripcion = NEW.descripcion AND activo = FALSE
    LIMIT 1;

    IF v_id IS NOT NULL THEN
        UPDATE mae_ubicacion SET activo = TRUE WHERE id_ubicacion = v_id;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Registro existente reactivado (ubicación).';
    END IF;
END$$
DELIMITER ;

-- Reactiva identidad inactiva si se intenta insertar duplicada

DROP TRIGGER IF EXISTS trg_recuperar_identidad;
DELIMITER $$
CREATE TRIGGER trg_recuperar_identidad
BEFORE INSERT ON mae_identidad
FOR EACH ROW
BEGIN
    DECLARE v_id INT;
    SELECT id_identidad INTO v_id
    FROM mae_identidad
    WHERE tipo_identificacion = NEW.tipo_identificacion
      AND codigo_documento = NEW.codigo_documento
      AND activo = FALSE
    LIMIT 1;

    IF v_id IS NOT NULL THEN
        UPDATE mae_identidad SET activo = TRUE WHERE id_identidad = v_id;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Registro existente reactivado (identidad).';
    END IF;
END$$
DELIMITER ;

-- Reactiva conductor inactivo si se intenta insertar duplicado

DROP TRIGGER IF EXISTS trg_recuperar_conductor;
DELIMITER $$
CREATE TRIGGER trg_recuperar_conductor
BEFORE INSERT ON mae_conductor
FOR EACH ROW
BEGIN
    DECLARE v_id INT;
    SELECT id_conductor INTO v_id
    FROM mae_conductor
    WHERE n_licencia = NEW.n_licencia AND activo = FALSE
    LIMIT 1;

    IF v_id IS NOT NULL THEN
        UPDATE mae_conductor SET activo = TRUE WHERE id_conductor = v_id;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Registro existente reactivado (conductor).';
    END IF;
END$$
DELIMITER ;

-- Reactiva vehículo inactivo si se intenta insertar duplicado

DROP TRIGGER IF EXISTS trg_recuperar_vehiculo;
DELIMITER $$
CREATE TRIGGER trg_recuperar_vehiculo
BEFORE INSERT ON mae_vehiculo
FOR EACH ROW
BEGIN
    DECLARE v_id INT;
    SELECT id_vehiculo INTO v_id
    FROM mae_vehiculo
    WHERE placa = NEW.placa AND activo = FALSE
    LIMIT 1;

    IF v_id IS NOT NULL THEN
        UPDATE mae_vehiculo SET activo = TRUE WHERE id_vehiculo = v_id;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Registro existente reactivado (vehículo).';
    END IF;
END$$
DELIMITER ;

-- Reactiva forma de pago inactiva si se intenta insertar duplicada

DROP TRIGGER IF EXISTS trg_recuperar_forma_pago;
DELIMITER $$
CREATE TRIGGER trg_recuperar_forma_pago
BEFORE INSERT ON mae_forma_pago
FOR EACH ROW
BEGIN
    DECLARE v_id INT;
    SELECT id_forma_pago INTO v_id
    FROM mae_forma_pago
    WHERE nombre = NEW.nombre AND activo = FALSE
    LIMIT 1;

    IF v_id IS NOT NULL THEN
        UPDATE mae_forma_pago SET activo = TRUE WHERE id_forma_pago = v_id;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Registro existente reactivado (forma de pago).';
    END IF;
END$$
DELIMITER ;

-- Reactiva moneda inactiva si se intenta insertar duplicada

DROP TRIGGER IF EXISTS trg_recuperar_moneda;
DELIMITER $$
CREATE TRIGGER trg_recuperar_moneda
BEFORE INSERT ON mae_moneda
FOR EACH ROW
BEGIN
    DECLARE v_id INT;
    SELECT id_moneda INTO v_id
    FROM mae_moneda
    WHERE codigo_iso = NEW.codigo_iso AND activo = FALSE
    LIMIT 1;

    IF v_id IS NOT NULL THEN
        UPDATE mae_moneda SET activo = TRUE WHERE id_moneda = v_id;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Registro existente reactivado (moneda).';
    END IF;
END$$
DELIMITER ;