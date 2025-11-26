-- 1.1 mae_ubicacion: Reactivar ubicación inactiva
DROP TRIGGER IF EXISTS trg_recuperar_ubicacion ON mae_ubicacion;
DROP FUNCTION IF EXISTS trg_recuperar_ubicacion();

CREATE OR REPLACE FUNCTION trg_recuperar_ubicacion()
RETURNS TRIGGER AS $$
DECLARE
    v_id INTEGER;
BEGIN
    SELECT id_ubicacion INTO v_id
    FROM mae_ubicacion
    WHERE descripcion = NEW.descripcion AND activo = FALSE
    LIMIT 1;

    IF v_id IS NOT NULL THEN
        UPDATE mae_ubicacion SET activo = TRUE WHERE id_ubicacion = v_id;
        RAISE NOTICE 'Ubicación reactivada con ID: %', v_id;
        RETURN NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_recuperar_ubicacion
    BEFORE INSERT ON mae_ubicacion
    FOR EACH ROW
    EXECUTE FUNCTION trg_recuperar_ubicacion();

-- 1.2 mae_identidad: Reactivar identidad inactiva
DROP TRIGGER IF EXISTS trg_recuperar_identidad ON mae_identidad;
DROP FUNCTION IF EXISTS trg_recuperar_identidad();

CREATE OR REPLACE FUNCTION trg_recuperar_identidad()
RETURNS TRIGGER AS $$
DECLARE
    v_id INTEGER;
BEGIN
    SELECT id_identidad INTO v_id
    FROM mae_identidad
    WHERE tipo_identificacion = NEW.tipo_identificacion
      AND codigo_documento = NEW.codigo_documento
      AND activo = FALSE
    LIMIT 1;

    IF v_id IS NOT NULL THEN
        UPDATE mae_identidad SET activo = TRUE WHERE id_identidad = v_id;
        RAISE NOTICE 'Identidad reactivada con ID: %', v_id;
        RETURN NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_recuperar_identidad
    BEFORE INSERT ON mae_identidad
    FOR EACH ROW
    EXECUTE FUNCTION trg_recuperar_identidad();

-- 1.3 mae_conductor: Reactivar conductor inactivo
DROP TRIGGER IF EXISTS trg_recuperar_conductor ON mae_conductor;
DROP FUNCTION IF EXISTS trg_recuperar_conductor();

CREATE OR REPLACE FUNCTION trg_recuperar_conductor()
RETURNS TRIGGER AS $$
DECLARE
    v_id INTEGER;
BEGIN
    SELECT id_conductor INTO v_id
    FROM mae_conductor
    WHERE n_licencia = NEW.n_licencia AND activo = FALSE
    LIMIT 1;

    IF v_id IS NOT NULL THEN
        UPDATE mae_conductor 
        SET activo = TRUE, nombre = NEW.nombre
        WHERE id_conductor = v_id;
        RAISE NOTICE 'Conductor reactivado con ID: %', v_id;
        RETURN NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_recuperar_conductor
    BEFORE INSERT ON mae_conductor
    FOR EACH ROW
    EXECUTE FUNCTION trg_recuperar_conductor();

-- 1.4 mae_vehiculo: Reactivar vehículo inactivo
DROP TRIGGER IF EXISTS trg_recuperar_vehiculo ON mae_vehiculo;
DROP FUNCTION IF EXISTS trg_recuperar_vehiculo();

CREATE OR REPLACE FUNCTION trg_recuperar_vehiculo()
RETURNS TRIGGER AS $$
DECLARE
    v_id INTEGER;
BEGIN
    SELECT id_vehiculo INTO v_id
    FROM mae_vehiculo
    WHERE placa = NEW.placa AND activo = FALSE
    LIMIT 1;

    IF v_id IS NOT NULL THEN
        UPDATE mae_vehiculo 
        SET activo = TRUE, descripcion = NEW.descripcion
        WHERE id_vehiculo = v_id;
        RAISE NOTICE 'Vehículo reactivado con ID: %', v_id;
        RETURN NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_recuperar_vehiculo
    BEFORE INSERT ON mae_vehiculo
    FOR EACH ROW
    EXECUTE FUNCTION trg_recuperar_vehiculo();

-- 1.5 mae_forma_pago: Reactivar forma de pago inactiva
DROP TRIGGER IF EXISTS trg_recuperar_forma_pago ON mae_forma_pago;
DROP FUNCTION IF EXISTS trg_recuperar_forma_pago();

CREATE OR REPLACE FUNCTION trg_recuperar_forma_pago()
RETURNS TRIGGER AS $$
DECLARE
    v_id INTEGER;
BEGIN
    SELECT id_forma_pago INTO v_id
    FROM mae_forma_pago
    WHERE nombre = NEW.nombre AND activo = FALSE
    LIMIT 1;

    IF v_id IS NOT NULL THEN
        UPDATE mae_forma_pago 
        SET activo = TRUE, descripcion = NEW.descripcion
        WHERE id_forma_pago = v_id;
        RAISE NOTICE 'Forma de pago reactivada con ID: %', v_id;
        RETURN NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_recuperar_forma_pago
    BEFORE INSERT ON mae_forma_pago
    FOR EACH ROW
    EXECUTE FUNCTION trg_recuperar_forma_pago();

-- 1.6 mae_moneda: Reactivar moneda inactiva
DROP TRIGGER IF EXISTS trg_recuperar_moneda ON mae_moneda;
DROP FUNCTION IF EXISTS trg_recuperar_moneda();

CREATE OR REPLACE FUNCTION trg_recuperar_moneda()
RETURNS TRIGGER AS $$
DECLARE
    v_id INTEGER;
BEGIN
    SELECT id_moneda INTO v_id
    FROM mae_moneda
    WHERE codigo_iso = NEW.codigo_iso AND activo = FALSE
    LIMIT 1;

    IF v_id IS NOT NULL THEN
        UPDATE mae_moneda 
        SET activo = TRUE, nombre = NEW.nombre
        WHERE id_moneda = v_id;
        RAISE NOTICE 'Moneda reactivada con ID: %', v_id;
        RETURN NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_recuperar_moneda
    BEFORE INSERT ON mae_moneda
    FOR EACH ROW
    EXECUTE FUNCTION trg_recuperar_moneda();

-- 1.7 mae_producto: Reactivar producto inactivo
DROP TRIGGER IF EXISTS trg_before_insert_mae_producto ON mae_producto;
DROP FUNCTION IF EXISTS trg_before_insert_mae_producto();

CREATE OR REPLACE FUNCTION trg_before_insert_mae_producto()
RETURNS TRIGGER AS $$
DECLARE
    v_id INTEGER;
    v_activo BOOLEAN;
    v_stock_actual INTEGER;
BEGIN
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
        RAISE NOTICE 'Producto reactivado con ID: %', v_id;
        RETURN NULL;
    END IF;

    IF v_id IS NOT NULL AND v_activo = TRUE THEN
        RAISE EXCEPTION 'El producto ya existe y está activo.';
    END IF;

    IF NEW.stock < 0 THEN
        RAISE EXCEPTION 'No se permite registrar productos con stock negativo.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_before_insert_mae_producto
    BEFORE INSERT ON mae_producto
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_insert_mae_producto();

-- 1.8 mae_empresa: Reactivar empresa inactiva
DROP TRIGGER IF EXISTS trg_before_insert_mae_empresa ON mae_empresa;
DROP FUNCTION IF EXISTS trg_before_insert_mae_empresa();

CREATE OR REPLACE FUNCTION trg_before_insert_mae_empresa()
RETURNS TRIGGER AS $$
DECLARE
    v_id_ruc INTEGER;
    v_activo_ruc BOOLEAN;
    v_id_nombre INTEGER;
BEGIN
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
            RAISE NOTICE 'Empresa reactivada con ID: %', v_id_ruc;
            RETURN NULL;
        ELSE
            RAISE EXCEPTION 'ERROR: RUC ya registrado (conflicto de nombre).';
        END IF;
    END IF;

    IF v_id_nombre IS NOT NULL AND v_id_ruc IS NULL THEN
        RAISE EXCEPTION 'ERROR: Nombre de empresa ya usado con otro RUC.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_before_insert_mae_empresa
    BEFORE INSERT ON mae_empresa
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_insert_mae_empresa();


-- 2.1 mae_ubicacion
CREATE OR REPLACE FUNCTION trg_before_delete_mae_ubicacion()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO log_eliminaciones (id_registro, tabla, fecha_hora)
    VALUES (OLD.id_ubicacion, 'mae_ubicacion', NOW());
    RAISE EXCEPTION 'No se permite eliminar ubicaciones. Use activo=FALSE y log.';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_before_delete_mae_ubicacion ON mae_ubicacion;
CREATE TRIGGER trg_before_delete_mae_ubicacion
    BEFORE DELETE ON mae_ubicacion
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_delete_mae_ubicacion();

-- 2.2 mae_identidad
CREATE OR REPLACE FUNCTION trg_before_delete_mae_identidad()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO log_eliminaciones (id_registro, tabla, fecha_hora)
    VALUES (OLD.id_identidad, 'mae_identidad', NOW());
    RAISE EXCEPTION 'No se permite eliminar identidades. Use activo=FALSE y log.';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_before_delete_mae_identidad ON mae_identidad;
CREATE TRIGGER trg_before_delete_mae_identidad
    BEFORE DELETE ON mae_identidad
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_delete_mae_identidad();

-- 2.3 mae_cliente
CREATE OR REPLACE FUNCTION trg_before_delete_mae_cliente()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO log_eliminaciones (id_registro, tabla, fecha_hora)
    VALUES (OLD.id_cliente, 'mae_cliente', NOW());
    RAISE EXCEPTION 'No se permite eliminar clientes. Use activo=FALSE y log.';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_before_delete_mae_cliente ON mae_cliente;
CREATE TRIGGER trg_before_delete_mae_cliente
    BEFORE DELETE ON mae_cliente
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_delete_mae_cliente();

-- 2.4 mae_empresa
CREATE OR REPLACE FUNCTION trg_before_delete_mae_empresa()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO log_eliminaciones (id_registro, tabla, fecha_hora)
    VALUES (OLD.id_empresa, 'mae_empresa', NOW());
    RAISE EXCEPTION 'No se permite eliminar empresas. Use activo=FALSE y log.';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_before_delete_mae_empresa ON mae_empresa;
CREATE TRIGGER trg_before_delete_mae_empresa
    BEFORE DELETE ON mae_empresa
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_delete_mae_empresa();

-- 2.5 mae_conductor
CREATE OR REPLACE FUNCTION trg_before_delete_mae_conductor()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO log_eliminaciones (id_registro, tabla, fecha_hora)
    VALUES (OLD.id_conductor, 'mae_conductor', NOW());
    RAISE EXCEPTION 'No se permite eliminar conductores. Use activo=FALSE y log.';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_before_delete_mae_conductor ON mae_conductor;
CREATE TRIGGER trg_before_delete_mae_conductor
    BEFORE DELETE ON mae_conductor
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_delete_mae_conductor();

-- 2.6 mae_vehiculo
CREATE OR REPLACE FUNCTION trg_before_delete_mae_vehiculo()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO log_eliminaciones (id_registro, tabla, fecha_hora)
    VALUES (OLD.id_vehiculo, 'mae_vehiculo', NOW());
    RAISE EXCEPTION 'No se permite eliminar vehículos. Use activo=FALSE y log.';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_before_delete_mae_vehiculo ON mae_vehiculo;
CREATE TRIGGER trg_before_delete_mae_vehiculo
    BEFORE DELETE ON mae_vehiculo
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_delete_mae_vehiculo();

-- 2.7 mae_producto
CREATE OR REPLACE FUNCTION trg_before_delete_mae_producto()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO log_eliminaciones (id_registro, tabla, fecha_hora)
    VALUES (OLD.id_producto, 'mae_producto', NOW());
    RAISE EXCEPTION 'No se permite eliminar productos. Use activo=FALSE y log.';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_before_delete_mae_producto ON mae_producto;
CREATE TRIGGER trg_before_delete_mae_producto
    BEFORE DELETE ON mae_producto
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_delete_mae_producto();


-- 3.1 RUC único para empresas activas
CREATE OR REPLACE FUNCTION trg_before_insert_mae_empresa_ruc_unico()
RETURNS TRIGGER AS $$
DECLARE
    v_activo BOOLEAN;
BEGIN
    SELECT activo INTO v_activo
    FROM mae_empresa
    WHERE RUC = NEW.RUC
    LIMIT 1;

    IF FOUND AND v_activo = TRUE THEN
        RAISE EXCEPTION 'Error: El RUC ingresado ya pertenece a una empresa activa.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_before_insert_mae_empresa_ruc_unico ON mae_empresa;
CREATE TRIGGER trg_before_insert_mae_empresa_ruc_unico
    BEFORE INSERT ON mae_empresa
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_insert_mae_empresa_ruc_unico();

-- 3.2 Stock no negativo en actualización
CREATE OR REPLACE FUNCTION trg_before_update_mae_producto_stock()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.stock < 0 THEN
        RAISE EXCEPTION 'El stock no puede ser negativo.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_before_update_mae_producto_stock ON mae_producto;
CREATE TRIGGER trg_before_update_mae_producto_stock
    BEFORE UPDATE ON mae_producto
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_update_mae_producto_stock();

-- 3.3 Precio no puede bajar más del 50%
CREATE OR REPLACE FUNCTION trg_before_update_precio_producto()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.precio_base < (OLD.precio_base * 0.5) THEN
        RAISE EXCEPTION 'El nuevo precio no puede ser inferior al 50%% del precio anterior.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_before_update_precio_producto ON mae_producto;
CREATE TRIGGER trg_before_update_precio_producto
    BEFORE UPDATE ON mae_producto
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_update_precio_producto();

-- 3.4 Alerta de stock bajo
CREATE OR REPLACE FUNCTION trg_after_update_stock_minimo()
RETURNS TRIGGER AS $$
DECLARE
    v_stock_inicial INTEGER := 100;
BEGIN
    IF NEW.stock <= (v_stock_inicial * 0.25) AND NEW.stock < OLD.stock THEN
        RAISE NOTICE 'ALERTA: Stock bajo para producto ID %', NEW.id_producto;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_after_update_stock_minimo ON mae_producto;
CREATE TRIGGER trg_after_update_stock_minimo
    AFTER UPDATE ON mae_producto
    FOR EACH ROW
    EXECUTE FUNCTION trg_after_update_stock_minimo();

-- 3.5 Cantidad positiva en detalle documento
CREATE OR REPLACE FUNCTION trg_before_insert_detalle_documento_cantidad()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.cantidad <= 0 THEN
        RAISE EXCEPTION 'La cantidad del detalle debe ser mayor que 0.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_before_insert_detalle_documento_cantidad ON trs_detalle_documento;
CREATE TRIGGER trg_before_insert_detalle_documento_cantidad
    BEFORE INSERT ON trs_detalle_documento
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_insert_detalle_documento_cantidad();

-- 4.1 Asignar fecha automática si no se proporciona
CREATE OR REPLACE FUNCTION trg_before_insert_documento()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.fecha_emision IS NULL THEN
        NEW.fecha_emision := CURRENT_DATE;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_before_insert_documento ON trs_encabezado_documento;
CREATE TRIGGER trg_before_insert_documento
    BEFORE INSERT ON trs_encabezado_documento
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_insert_documento();

-- 4.2 Evitar cambios de fecha si documento está pendiente
CREATE OR REPLACE FUNCTION trg_before_update_documento_fecha()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.estado_doc = 'PENDIENTE' THEN
        IF NEW.fecha_emision IS NULL THEN
            NEW.fecha_emision := OLD.fecha_emision;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_before_update_documento_fecha ON trs_encabezado_documento;
CREATE TRIGGER trg_before_update_documento_fecha
    BEFORE UPDATE ON trs_encabezado_documento
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_update_documento_fecha();

-- 4.3 Solo documentos pendientes pueden anularse
CREATE OR REPLACE FUNCTION trg_before_update_documento_estado()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.estado_doc = 'ANULADO' AND OLD.estado_doc <> 'PENDIENTE' THEN
        RAISE EXCEPTION 'Solo se pueden anular documentos pendientes.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_before_update_documento_estado ON trs_encabezado_documento;
CREATE TRIGGER trg_before_update_documento_estado
    BEFORE UPDATE ON trs_encabezado_documento
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_update_documento_estado();

-- 4.4 Bloquear modificaciones de documentos emitidos/anulados
CREATE OR REPLACE FUNCTION trg_before_update_documento_bloqueo()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.estado_doc IN ('EMITIDO', 'ANULADO') THEN
        RAISE EXCEPTION 'No se puede modificar un documento que ya está emitido o anulado';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_before_update_documento_bloqueo ON trs_encabezado_documento;
CREATE TRIGGER trg_before_update_documento_bloqueo
    BEFORE UPDATE ON trs_encabezado_documento
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_update_documento_bloqueo();

-- 4.5 Validar stock antes de emitir documento
CREATE OR REPLACE FUNCTION trg_before_update_documento_emitido()
RETURNS TRIGGER AS $$
DECLARE
    v_producto INTEGER;
    v_cantidad INTEGER;
    v_stock_actual INTEGER;
    v_nombre_producto VARCHAR(50);
    cur_detalle CURSOR FOR 
        SELECT id_producto, cantidad 
        FROM trs_detalle_documento
        WHERE id_documento = NEW.id_documento;
BEGIN
    IF NEW.estado_doc = 'EMITIDO' AND OLD.estado_doc != 'EMITIDO' THEN
        OPEN cur_detalle;
        LOOP
            FETCH cur_detalle INTO v_producto, v_cantidad;
            EXIT WHEN NOT FOUND;
            
            SELECT stock, nombre 
            INTO v_stock_actual, v_nombre_producto
            FROM mae_producto 
            WHERE id_producto = v_producto;
            
            IF v_stock_actual < v_cantidad THEN
                CLOSE cur_detalle;
                RAISE EXCEPTION 'Stock insuficiente para emitir el documento';
            END IF;
        END LOOP;
        CLOSE cur_detalle;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_before_update_documento_emitido ON trs_encabezado_documento;
CREATE TRIGGER trg_before_update_documento_emitido
    BEFORE UPDATE ON trs_encabezado_documento
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_update_documento_emitido();

-- 4.6 Actualizar stock al emitir o anular documento
CREATE OR REPLACE FUNCTION trg_after_update_documento_emitido()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.estado_doc = 'EMITIDO' AND OLD.estado_doc != 'EMITIDO' THEN
        UPDATE mae_producto p
        SET stock = p.stock - d.cantidad
        FROM trs_detalle_documento d
        WHERE p.id_producto = d.id_producto
          AND d.id_documento = NEW.id_documento;
    END IF;
    
    IF NEW.estado_doc = 'ANULADO' AND OLD.estado_doc = 'EMITIDO' THEN
        UPDATE mae_producto p
        SET stock = p.stock + d.cantidad
        FROM trs_detalle_documento d
        WHERE p.id_producto = d.id_producto
          AND d.id_documento = NEW.id_documento;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_after_update_documento_emitido ON trs_encabezado_documento;
CREATE TRIGGER trg_after_update_documento_emitido
    AFTER UPDATE ON trs_encabezado_documento
    FOR EACH ROW
    EXECUTE FUNCTION trg_after_update_documento_emitido();


-- 5.1 Impedir crear guía con número usado
CREATE OR REPLACE FUNCTION trg_before_insert_guia()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.fecha_emision IS NULL THEN
        NEW.fecha_emision := CURRENT_DATE;
    END IF;

    IF EXISTS (SELECT 1 FROM trs_encabezado_guia WHERE nro_guia = NEW.nro_guia) THEN
        RAISE EXCEPTION 'Número de guía ya existe. Ingrese uno diferente.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_before_insert_guia ON trs_encabezado_guia;
CREATE TRIGGER trg_before_insert_guia
    BEFORE INSERT ON trs_encabezado_guia
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_insert_guia();

-- 5.2 Evitar cambios de fecha si guía está pendiente
CREATE OR REPLACE FUNCTION trg_before_update_guia_fecha()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.estado_guia = 'PENDIENTE' THEN
        IF NEW.fecha_emision IS NULL THEN
            NEW.fecha_emision := OLD.fecha_emision;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_before_update_guia_fecha ON trs_encabezado_guia;
CREATE TRIGGER trg_before_update_guia_fecha
    BEFORE UPDATE ON trs_encabezado_guia
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_update_guia_fecha();

-- 5.3 Solo guías pendientes pueden anularse
CREATE OR REPLACE FUNCTION trg_before_update_guia_estado()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.estado_guia = 'ANULADO' AND OLD.estado_guia <> 'PENDIENTE' THEN
        RAISE EXCEPTION 'Solo se pueden anular guías pendientes.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_before_update_guia_estado ON trs_encabezado_guia;
CREATE TRIGGER trg_before_update_guia_estado
    BEFORE UPDATE ON trs_encabezado_guia
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_update_guia_estado();

-- 5.4 Bloquear modificaciones de guías emitidas/anuladas
CREATE OR REPLACE FUNCTION trg_before_update_guia_bloqueo()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.estado_guia IN ('EMITIDO', 'ANULADO') THEN
        RAISE EXCEPTION 'No se puede modificar una guía que ya está emitida o anulada';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_before_update_guia_bloqueo ON trs_encabezado_guia;
CREATE TRIGGER trg_before_update_guia_bloqueo
    BEFORE UPDATE ON trs_encabezado_guia
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_update_guia_bloqueo();
