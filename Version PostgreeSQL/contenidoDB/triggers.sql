-- Conectarse a la base de datos (esto se hace fuera del script en PostgreSQL)
-- \c sistema_documentos;

-- Índices

-- Índices únicos
CREATE UNIQUE INDEX IF NOT EXISTS uq_mae_empresa_ruc ON mae_empresa(ruc);
CREATE UNIQUE INDEX IF NOT EXISTS uq_mae_conductor_licencia ON mae_conductor(n_licencia);
CREATE UNIQUE INDEX IF NOT EXISTS uq_mae_vehiculo_placa ON mae_vehiculo(placa);
CREATE UNIQUE INDEX IF NOT EXISTS uq_trs_encabezado_guia_nro_guia ON trs_encabezado_guia(nro_guia);
CREATE UNIQUE INDEX IF NOT EXISTS uq_mae_producto_nombre ON mae_producto(nombre);
CREATE UNIQUE INDEX IF NOT EXISTS uq_mae_moneda_codigo_iso ON mae_moneda(codigo_iso);
CREATE UNIQUE INDEX IF NOT EXISTS uq_mae_identidad_codigo_documento ON mae_identidad(codigo_documento);

-- Índices de optimización de búsqueda
CREATE INDEX IF NOT EXISTS idx_trs_encabezado_documento_fecha ON trs_encabezado_documento(fecha_emision);
CREATE INDEX IF NOT EXISTS idx_trs_encabezado_documento_cliente ON trs_encabezado_documento(id_cliente);
CREATE INDEX IF NOT EXISTS idx_trs_encabezado_documento_tipo ON trs_encabezado_documento(tipo_doc);
CREATE INDEX IF NOT EXISTS idx_trs_detalle_documento_producto ON trs_detalle_documento(id_producto);
CREATE INDEX IF NOT EXISTS idx_trs_encabezado_guia_fecha ON trs_encabezado_guia(fecha_emision);
CREATE INDEX IF NOT EXISTS idx_trs_encabezado_guia_doc_venta ON trs_encabezado_guia(id_doc_venta);
CREATE INDEX IF NOT EXISTS idx_mae_cliente_nombre ON mae_cliente(nombre);
CREATE INDEX IF NOT EXISTS idx_mae_cliente_identidad ON mae_cliente(id_identidad);
CREATE INDEX IF NOT EXISTS idx_trs_detalle_guia_producto ON trs_detalle_guia(id_producto);

-- Triggers

-- Función para evitar insertar productos con nombre duplicado o stock negativo
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

        RAISE EXCEPTION 'Producto reactivado automáticamente. Inserción cancelada.';
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

DROP TRIGGER IF EXISTS trg_before_insert_mae_producto ON mae_producto;
CREATE TRIGGER trg_before_insert_mae_producto
    BEFORE INSERT ON mae_producto
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_insert_mae_producto();

-- Evita actualizaciones de stock negativo
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

-- Evita reducciones extremas de precio base
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

-- Funciones de eliminación lógica
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

-- Fecha automática si no se proporciona
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

-- Impide crear guía con número usado
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

-- Evita cambios de fecha si documento está pendiente
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

-- Evita cambios de fecha si guía está pendiente
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

-- Validación de estados - solo pendientes pueden anularse
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

-- Validación de estados - solo documentos pendientes pueden anularse
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

-- Valida stock antes de emitir documento
CREATE OR REPLACE FUNCTION trg_before_update_documento_emitido()
RETURNS TRIGGER AS $$
DECLARE
    v_producto INTEGER;
    v_cantidad INTEGER;
    v_stock_actual INTEGER;
    v_nombre_producto VARCHAR(50);
    v_terminado BOOLEAN := FALSE;
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

-- Actualiza stock al emitir o anular documento
CREATE OR REPLACE FUNCTION trg_after_update_documento_emitido()
RETURNS TRIGGER AS $$
BEGIN
    -- Emitir documento: reducir stock
    IF NEW.estado_doc = 'EMITIDO' AND OLD.estado_doc != 'EMITIDO' THEN
        UPDATE mae_producto p
        SET stock = p.stock - d.cantidad
        FROM trs_detalle_documento d
        WHERE p.id_producto = d.id_producto
          AND d.id_documento = NEW.id_documento;
    END IF;
    
    -- Anular documento: restaurar stock
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

-- Alerta de stock bajo (25% del stock inicial)
CREATE OR REPLACE FUNCTION trg_after_update_stock_minimo()
RETURNS TRIGGER AS $$
DECLARE
    v_stock_inicial INTEGER := 100; -- Valor por defecto
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

-- Bloquea modificaciones de documentos emitidos o anulados
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

-- Bloquea modificaciones de guías emitidas o anuladas
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

-- Valida cantidad positiva en detalle documento
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

-- Valida RUC único para empresas activas
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

-- Maneja reactivación de empresa inactiva o previene duplicados
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

            RAISE EXCEPTION 'Empresa reactivada automáticamente. Inserción cancelada.';
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

DROP TRIGGER IF EXISTS trg_before_insert_mae_empresa ON mae_empresa;
CREATE TRIGGER trg_before_insert_mae_empresa
    BEFORE INSERT ON mae_empresa
    FOR EACH ROW
    EXECUTE FUNCTION trg_before_insert_mae_empresa();

-- Funciones de reactivación para registros inactivos
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
        RAISE EXCEPTION 'Registro existente reactivado (ubicación).';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_recuperar_ubicacion ON mae_ubicacion;
CREATE TRIGGER trg_recuperar_ubicacion
    BEFORE INSERT ON mae_ubicacion
    FOR EACH ROW
    EXECUTE FUNCTION trg_recuperar_ubicacion();

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
        RAISE EXCEPTION 'Registro existente reactivado (identidad).';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_recuperar_identidad ON mae_identidad;
CREATE TRIGGER trg_recuperar_identidad
    BEFORE INSERT ON mae_identidad
    FOR EACH ROW
    EXECUTE FUNCTION trg_recuperar_identidad();

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
        UPDATE mae_conductor SET activo = TRUE WHERE id_conductor = v_id;
        RAISE EXCEPTION 'Registro existente reactivado (conductor).';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_recuperar_conductor ON mae_conductor;
CREATE TRIGGER trg_recuperar_conductor
    BEFORE INSERT ON mae_conductor
    FOR EACH ROW
    EXECUTE FUNCTION trg_recuperar_conductor();

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
        UPDATE mae_vehiculo SET activo = TRUE WHERE id_vehiculo = v_id;
        RAISE EXCEPTION 'Registro existente reactivado (vehículo).';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_recuperar_vehiculo ON mae_vehiculo;
CREATE TRIGGER trg_recuperar_vehiculo
    BEFORE INSERT ON mae_vehiculo
    FOR EACH ROW
    EXECUTE FUNCTION trg_recuperar_vehiculo();

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
        UPDATE mae_forma_pago SET activo = TRUE WHERE id_forma_pago = v_id;
        RAISE EXCEPTION 'Registro existente reactivado (forma de pago).';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_recuperar_forma_pago ON mae_forma_pago;
CREATE TRIGGER trg_recuperar_forma_pago
    BEFORE INSERT ON mae_forma_pago
    FOR EACH ROW
    EXECUTE FUNCTION trg_recuperar_forma_pago();

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
        UPDATE mae_moneda SET activo = TRUE WHERE id_moneda = v_id;
        RAISE EXCEPTION 'Registro existente reactivado (moneda).';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_recuperar_moneda ON mae_moneda;
CREATE TRIGGER trg_recuperar_moneda
    BEFORE INSERT ON mae_moneda
    FOR EACH ROW
    EXECUTE FUNCTION trg_recuperar_moneda();