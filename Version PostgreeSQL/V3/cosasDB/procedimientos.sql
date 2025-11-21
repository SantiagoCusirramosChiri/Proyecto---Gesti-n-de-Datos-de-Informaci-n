-- ============================================
-- PROCEDIMIENTOS ALMACENADOS CORREGIDOS
-- Sistema de Documentos
-- ============================================

-- LOGIN Y REGISTRO

CREATE OR REPLACE FUNCTION sp_login_empresa(
    p_usuario VARCHAR(50), 
    p_clave CHAR(11)
)
RETURNS TABLE(
    mensaje TEXT,
    id_empresa INTEGER,
    nombre_empresa VARCHAR(50),
    razon_social_empresa VARCHAR(100)
) AS $$
DECLARE
    v_empresa_existe INTEGER := 0;
    v_empresa_record RECORD;
BEGIN
    -- Verificar si la empresa existe y está activa
    SELECT COUNT(*) INTO v_empresa_existe 
    FROM mae_empresa emp
    WHERE emp.nombre = sp_login_empresa.p_usuario 
    AND emp.RUC = sp_login_empresa.p_clave 
    AND emp.activo = TRUE;
    
    IF v_empresa_existe > 0 THEN
        -- Obtener los datos completos de la empresa
        SELECT 
            emp.id_empresa,
            emp.nombre,
            emp.razon_social
        INTO v_empresa_record
        FROM mae_empresa emp
        WHERE emp.nombre = sp_login_empresa.p_usuario 
        AND emp.RUC = sp_login_empresa.p_clave;
        
        RETURN QUERY 
        SELECT 
            'LOGIN EXITOSO'::TEXT, 
            v_empresa_record.id_empresa, 
            v_empresa_record.nombre, 
            v_empresa_record.razon_social;
    ELSE
        RETURN QUERY 
        SELECT 
            'USUARIO O CONTRASEÑA INCORRECTA O EMPRESA INACTIVA'::TEXT,
            NULL::INTEGER, 
            NULL::VARCHAR(50), 
            NULL::VARCHAR(100);
    END IF;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_registrar_empresa(VARCHAR, VARCHAR, CHAR, INTEGER);
CREATE OR REPLACE FUNCTION sp_registrar_empresa(
    p_nombre VARCHAR(50), 
    p_razon_social VARCHAR(100), 
    p_ruc CHAR(11), 
    p_id_ubicacion INTEGER
)
RETURNS TABLE(mensaje TEXT, id_empresa INTEGER) AS $$
DECLARE
    v_id_ruc INTEGER := NULL;
    v_activo_ruc BOOLEAN := FALSE;
    v_id_nombre INTEGER := NULL;
    v_nombre_existente VARCHAR(50);
    v_new_id INTEGER;
    v_ubicacion_existe INTEGER := 0;
BEGIN
    -- Validar que la ubicación existe
    SELECT COUNT(*) INTO v_ubicacion_existe
    FROM mae_ubicacion
    WHERE id_ubicacion = sp_registrar_empresa.p_id_ubicacion
    AND activo = TRUE;
    
    IF v_ubicacion_existe = 0 THEN
        RETURN QUERY SELECT 'ERROR: LA UBICACIÓN SELECCIONADA NO EXISTE O ESTÁ INACTIVA'::TEXT, NULL::INTEGER;
        RETURN;
    END IF;
    
    -- Verificar si el RUC ya existe
    SELECT emp.id_empresa, emp.activo, emp.nombre 
    INTO v_id_ruc, v_activo_ruc, v_nombre_existente 
    FROM mae_empresa emp
    WHERE emp.RUC = sp_registrar_empresa.p_ruc 
    LIMIT 1;
    
    -- Verificar si el nombre ya existe con otro RUC
    SELECT emp.id_empresa 
    INTO v_id_nombre 
    FROM mae_empresa emp
    WHERE emp.nombre = sp_registrar_empresa.p_nombre 
    AND emp.RUC != sp_registrar_empresa.p_ruc 
    LIMIT 1;
    
    -- CASO 1: Nueva empresa (ni RUC ni nombre existen)
    IF v_id_ruc IS NULL AND v_id_nombre IS NULL THEN
        INSERT INTO mae_empresa(
            nombre, 
            razon_social, 
            RUC, 
            id_ubicacion, 
            activo
        ) 
        VALUES (
            sp_registrar_empresa.p_nombre, 
            sp_registrar_empresa.p_razon_social, 
            sp_registrar_empresa.p_ruc, 
            sp_registrar_empresa.p_id_ubicacion, 
            TRUE
        )
        RETURNING mae_empresa.id_empresa INTO v_new_id;
        
        RETURN QUERY SELECT 'EMPRESA CREADA'::TEXT, v_new_id;
        RETURN;
    END IF;
    
    -- CASO 2: El nombre ya existe con otro RUC
    IF v_id_nombre IS NOT NULL THEN
        RETURN QUERY SELECT 'ERROR: NOMBRE DE EMPRESA YA USADO CON OTRO RUC'::TEXT, NULL::INTEGER;
        RETURN;
    END IF;
    
    -- CASO 3: El RUC ya existe
    IF v_id_ruc IS NOT NULL THEN
        IF v_nombre_existente = sp_registrar_empresa.p_nombre THEN
            -- Mismo RUC y mismo nombre
            IF v_activo_ruc = FALSE THEN
                -- Reactivar empresa inactiva
                UPDATE mae_empresa 
                SET activo = TRUE, 
                    razon_social = sp_registrar_empresa.p_razon_social, 
                    id_ubicacion = sp_registrar_empresa.p_id_ubicacion 
                WHERE id_empresa = v_id_ruc;
                
                RETURN QUERY SELECT 'EMPRESA REACTIVADA'::TEXT, v_id_ruc;
            ELSE
                -- Empresa ya activa
                RETURN QUERY SELECT 'EMPRESA YA EXISTE (ACTIVA)'::TEXT, v_id_ruc;
            END IF;
        ELSE
            -- Mismo RUC pero diferente nombre
            RETURN QUERY SELECT CONCAT('ERROR: RUC YA REGISTRADO CON EL NOMBRE "', v_nombre_existente, '"')::TEXT, NULL::INTEGER;
        END IF;
        RETURN;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- LISTADO

DROP FUNCTION IF EXISTS sp_listar_guias_empresa(INTEGER);
CREATE OR REPLACE FUNCTION sp_listar_guias_empresa(p_id_empresa INTEGER)
RETURNS TABLE(
    id_guia INTEGER,
    nro_guia VARCHAR(20),
    fecha_emision DATE,
    fecha_inicio_traslado DATE,
    motivo_traslado VARCHAR(100),
    direccion_partida VARCHAR(150),
    direccion_llegada VARCHAR(150),
    conductor VARCHAR(50),
    vehiculo CHAR(8),
    estado_guia VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY 
    SELECT g.id_guia, 
        g.nro_guia, 
        g.fecha_emision, 
        g.fecha_inicio_traslado, 
        g.motivo_traslado, 
        g.direccion_partida, 
        g.direccion_llegada, 
        c.nombre::VARCHAR(50) AS conductor, 
        v.placa::CHAR(8) AS vehiculo, 
        g.estado_guia
    FROM trs_encabezado_guia g 
    JOIN trs_encabezado_documento d ON g.id_doc_venta = d.id_documento 
    JOIN mae_conductor c ON g.id_conductor = c.id_conductor 
    JOIN mae_vehiculo v ON g.id_vehiculo = v.id_vehiculo
    WHERE d.id_empresa = sp_listar_guias_empresa.p_id_empresa 
    ORDER BY g.fecha_emision DESC;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_listar_guias_pendientes_empresa(INTEGER);
CREATE OR REPLACE FUNCTION sp_listar_guias_pendientes_empresa(p_id_empresa INTEGER)
RETURNS TABLE(
    id_guia INTEGER,
    nro_guia VARCHAR(20),
    fecha_inicio_traslado DATE,
    conductor VARCHAR(50),
    vehiculo CHAR(8)
) AS $$
BEGIN
    RETURN QUERY 
    SELECT g.id_guia, 
        g.nro_guia, 
        g.fecha_inicio_traslado, 
        c.nombre::VARCHAR(50) AS conductor, 
        v.placa::CHAR(8) AS vehiculo
    FROM trs_encabezado_guia g 
    JOIN trs_encabezado_documento d ON g.id_doc_venta = d.id_documento 
    JOIN mae_conductor c ON g.id_conductor = c.id_conductor 
    JOIN mae_vehiculo v ON g.id_vehiculo = v.id_vehiculo
    WHERE d.id_empresa = sp_listar_guias_pendientes_empresa.p_id_empresa 
    AND g.estado_guia = 'PENDIENTE' 
    ORDER BY g.fecha_inicio_traslado ASC;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_detalle_productos_empresa(INTEGER);
CREATE OR REPLACE FUNCTION sp_detalle_productos_empresa(p_id_empresa INTEGER)
RETURNS TABLE(
    id_documento INTEGER,
    producto VARCHAR(50),
    cantidad INTEGER,
    precio_producto DECIMAL(10,2),
    importe DECIMAL(10,2)
) AS $$
BEGIN
    RETURN QUERY 
    SELECT d.id_documento, 
        p.nombre::VARCHAR(50) AS producto, 
        dt.cantidad, 
        p.precio_base AS precio_producto, 
        dt.importe
    FROM trs_detalle_documento dt 
    JOIN trs_encabezado_documento d ON dt.id_documento = d.id_documento 
    JOIN mae_producto p ON dt.id_producto = p.id_producto
    WHERE d.id_empresa = sp_detalle_productos_empresa.p_id_empresa 
    ORDER BY d.fecha_emision DESC;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_listar_clientes_empresa(INTEGER);
CREATE OR REPLACE FUNCTION sp_listar_clientes_empresa(p_id_empresa INTEGER)
RETURNS TABLE(
    id_cliente INTEGER,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    ubicacion VARCHAR(100),
    tipo_identificacion VARCHAR(20),
    codigo_documento VARCHAR(15)
) AS $$
BEGIN
    RETURN QUERY 
    SELECT DISTINCT 
        c.id_cliente, 
        c.nombre, 
        c.apellido, 
        u.descripcion::VARCHAR(100) AS ubicacion, 
        i.tipo_identificacion, 
        i.codigo_documento
    FROM mae_cliente c 
    JOIN mae_ubicacion u ON c.id_ubicacion = u.id_ubicacion 
    JOIN mae_identidad i ON c.id_identidad = i.id_identidad 
    JOIN trs_encabezado_documento d ON c.id_cliente = d.id_cliente
    WHERE d.id_empresa = sp_listar_clientes_empresa.p_id_empresa 
    AND c.activo = TRUE 
    ORDER BY c.nombre, c.apellido;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_listar_stock_empresa(INTEGER);
CREATE OR REPLACE FUNCTION sp_listar_stock_empresa(p_id_empresa INTEGER)
RETURNS TABLE(
    id_producto INTEGER,
    nombre VARCHAR(50),
    descripcion VARCHAR(100),
    stock INTEGER,
    unidad_medida VARCHAR(10)
) AS $$
BEGIN
    RETURN QUERY 
    SELECT p.id_producto, 
        p.nombre, 
        p.descripcion, 
        p.stock, 
        p.unidad_medida 
    FROM mae_producto p 
    WHERE p.activo = TRUE 
    ORDER BY p.nombre ASC;
END;
$$ LANGUAGE plpgsql;

-- INSERCIÓN - MAESTRAS

DROP FUNCTION IF EXISTS sp_insertar_ubicacion(VARCHAR);
CREATE OR REPLACE FUNCTION sp_insertar_ubicacion(p_descripcion VARCHAR(100))
RETURNS TABLE(id_ubicacion INTEGER) AS $$
DECLARE
    v_id INTEGER;
BEGIN
    INSERT INTO mae_ubicacion(descripcion) 
    VALUES (sp_insertar_ubicacion.p_descripcion)
    RETURNING mae_ubicacion.id_ubicacion INTO v_id;
    
    RETURN QUERY SELECT v_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al insertar ubicación: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_insertar_identidad(VARCHAR, VARCHAR);

CREATE OR REPLACE FUNCTION sp_insertar_identidad(
    p_tipo_identificacion VARCHAR(20),
    p_codigo_documento VARCHAR(15)
)
RETURNS TABLE(
    success BOOLEAN,
    message VARCHAR(255),
    id_identidad INTEGER
) AS $$
DECLARE
    v_id_identidad INTEGER;
    v_existe BOOLEAN;
BEGIN
    -- Validar que los campos no estén vacíos
    IF TRIM(p_tipo_identificacion) = '' OR p_codigo_documento IS NULL THEN
        RETURN QUERY SELECT FALSE, 'Tipo de identificación y código son requeridos'::VARCHAR(255), NULL::INTEGER;
        RETURN;
    END IF;

    -- Normalizar código (quitar espacios)
    p_codigo_documento := TRIM(p_codigo_documento);

    -- Validaciones según tipo de documento
    CASE UPPER(p_tipo_identificacion)
        WHEN 'DNI' THEN
            IF p_codigo_documento !~ '^\d{8}$' THEN
                RETURN QUERY SELECT FALSE, 'DNI debe tener exactamente 8 dígitos numéricos'::VARCHAR(255), NULL::INTEGER;
                RETURN;
            END IF;
            
        WHEN 'RUC' THEN
            IF p_codigo_documento !~ '^\d{11}$' THEN
                RETURN QUERY SELECT FALSE, 'RUC debe tener exactamente 11 dígitos numéricos'::VARCHAR(255), NULL::INTEGER;
                RETURN;
            END IF;
            
        WHEN 'CE' THEN
            IF p_codigo_documento !~ '^\d{9}$' THEN
                RETURN QUERY SELECT FALSE, 'CE debe tener exactamente 9 dígitos numéricos'::VARCHAR(255), NULL::INTEGER;
                RETURN;
            END IF;
            
        WHEN 'PASAPORTE' THEN
            IF LENGTH(p_codigo_documento) < 6 OR LENGTH(p_codigo_documento) > 12 THEN
                RETURN QUERY SELECT FALSE, 'Pasaporte debe tener entre 6 y 12 caracteres'::VARCHAR(255), NULL::INTEGER;
                RETURN;
            END IF;
            
        ELSE
            RETURN QUERY SELECT FALSE, 'Tipo de identificación debe ser DNI, RUC, CE o PASAPORTE'::VARCHAR(255), NULL::INTEGER;
            RETURN;
    END CASE;

    -- Validar unicidad del código_documento
    SELECT EXISTS(
        SELECT 1 FROM mae_identidad 
        WHERE codigo_documento = p_codigo_documento 
        AND activo = TRUE
    ) INTO v_existe;
    
    IF v_existe THEN
        RETURN QUERY SELECT FALSE, 'El documento ya está registrado'::VARCHAR(255), NULL::INTEGER;
        RETURN;
    END IF;

    -- ✅ CORREGIDO: Usar mae_identidad.id_identidad en lugar de solo id_identidad
    INSERT INTO mae_identidad (tipo_identificacion, codigo_documento)
    VALUES (UPPER(p_tipo_identificacion), p_codigo_documento)
    RETURNING mae_identidad.id_identidad INTO v_id_identidad;

    -- Retornar éxito
    RETURN QUERY SELECT TRUE, 'Identidad registrada exitosamente'::VARCHAR(255), v_id_identidad;
    
EXCEPTION
    WHEN OTHERS THEN
        RETURN QUERY SELECT FALSE, ('Error al registrar: ' || SQLERRM)::VARCHAR(255), NULL::INTEGER;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_insertar_empresa(VARCHAR, VARCHAR, CHAR, INTEGER);
CREATE OR REPLACE FUNCTION sp_insertar_empresa(
    p_nombre VARCHAR(50), 
    p_razon_social VARCHAR(100), 
    p_RUC CHAR(11), 
    p_id_ubicacion INTEGER
)
RETURNS TABLE(id_empresa INTEGER) AS $$
DECLARE
    v_id INTEGER;
BEGIN
    INSERT INTO mae_empresa(
        nombre, 
        razon_social, 
        RUC, 
        id_ubicacion
    ) 
    VALUES (
        sp_insertar_empresa.p_nombre, 
        sp_insertar_empresa.p_razon_social, 
        sp_insertar_empresa.p_RUC, 
        sp_insertar_empresa.p_id_ubicacion
    )
    RETURNING mae_empresa.id_empresa INTO v_id;
    
    RETURN QUERY SELECT v_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al insertar empresa: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_insertar_conductor(VARCHAR, CHAR);
CREATE OR REPLACE FUNCTION sp_insertar_conductor(
    p_nombre VARCHAR(50), 
    p_n_licencia CHAR(12)
)
RETURNS TABLE(id_conductor INTEGER) AS $$
DECLARE
    v_id INTEGER;
BEGIN
    INSERT INTO mae_conductor(
        nombre, 
        n_licencia
    ) 
    VALUES (
        sp_insertar_conductor.p_nombre, 
        sp_insertar_conductor.p_n_licencia
    )
    RETURNING mae_conductor.id_conductor INTO v_id;
    
    RETURN QUERY SELECT v_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al insertar conductor: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_insertar_vehiculo(VARCHAR, CHAR);
CREATE OR REPLACE FUNCTION sp_insertar_vehiculo(
    p_descripcion VARCHAR(50), 
    p_placa CHAR(8)
)
RETURNS TABLE(id_vehiculo INTEGER) AS $$
DECLARE
    v_id INTEGER;
BEGIN
    INSERT INTO mae_vehiculo(
        descripcion, 
        placa
    ) 
    VALUES (
        sp_insertar_vehiculo.p_descripcion, 
        sp_insertar_vehiculo.p_placa
    )
    RETURNING mae_vehiculo.id_vehiculo INTO v_id;
    
    RETURN QUERY SELECT v_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al insertar vehículo: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_insertar_producto(VARCHAR, VARCHAR, DECIMAL, INTEGER, VARCHAR);
CREATE OR REPLACE FUNCTION sp_insertar_producto(
    p_nombre VARCHAR(50), 
    p_descripcion VARCHAR(100), 
    p_precio_base DECIMAL(10,2), 
    p_stock INTEGER, 
    p_unidad_medida VARCHAR(10)
)
RETURNS TABLE(id_producto INTEGER) AS $$
DECLARE
    v_id INTEGER;
BEGIN
    INSERT INTO mae_producto(
        nombre, 
        descripcion, 
        precio_base, 
        stock, 
        unidad_medida
    ) 
    VALUES (
        sp_insertar_producto.p_nombre, 
        sp_insertar_producto.p_descripcion, 
        sp_insertar_producto.p_precio_base, 
        sp_insertar_producto.p_stock, 
        sp_insertar_producto.p_unidad_medida
    )
    RETURNING mae_producto.id_producto INTO v_id;
    
    RETURN QUERY SELECT v_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al insertar producto: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_insertar_forma_pago(VARCHAR, VARCHAR);
CREATE OR REPLACE FUNCTION sp_insertar_forma_pago(
    p_nombre VARCHAR(35), 
    p_descripcion VARCHAR(100)
)
RETURNS TABLE(id_forma_pago INTEGER) AS $$
DECLARE
    v_id INTEGER;
BEGIN
    INSERT INTO mae_forma_pago(
        nombre, 
        descripcion
    ) 
    VALUES (
        sp_insertar_forma_pago.p_nombre, 
        sp_insertar_forma_pago.p_descripcion
    )
    RETURNING mae_forma_pago.id_forma_pago INTO v_id;
    
    RETURN QUERY SELECT v_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al insertar forma de pago: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_insertar_moneda(CHAR, VARCHAR);
CREATE OR REPLACE FUNCTION sp_insertar_moneda(
    p_codigo_iso CHAR(3), 
    p_nombre VARCHAR(20)
)
RETURNS TABLE(id_moneda INTEGER) AS $$
DECLARE
    v_id INTEGER;
BEGIN
    INSERT INTO mae_moneda(
        codigo_iso, 
        nombre
    ) 
    VALUES (
        sp_insertar_moneda.p_codigo_iso, 
        sp_insertar_moneda.p_nombre
    )
    RETURNING mae_moneda.id_moneda INTO v_id;
    
    RETURN QUERY SELECT v_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al insertar moneda: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- INSERCIÓN - TRANSACCIONAL

DROP FUNCTION IF EXISTS sp_insertar_encabezado_documento(VARCHAR, DATE, INTEGER, INTEGER, INTEGER, INTEGER);
CREATE OR REPLACE FUNCTION sp_insertar_encabezado_documento(
    p_tipo_doc VARCHAR(20), 
    p_fecha_emision DATE, 
    p_id_empresa INTEGER, 
    p_id_cliente INTEGER, 
    p_id_forma_pago INTEGER, 
    p_id_moneda INTEGER
)
RETURNS TABLE(id_documento INTEGER) AS $$
DECLARE
    v_id INTEGER;
BEGIN
    INSERT INTO trs_encabezado_documento(
        tipo_doc, 
        fecha_emision, 
        id_empresa, 
        id_cliente, 
        id_forma_pago, 
        id_moneda
    ) 
    VALUES (
        sp_insertar_encabezado_documento.p_tipo_doc, 
        sp_insertar_encabezado_documento.p_fecha_emision, 
        sp_insertar_encabezado_documento.p_id_empresa, 
        sp_insertar_encabezado_documento.p_id_cliente, 
        sp_insertar_encabezado_documento.p_id_forma_pago, 
        sp_insertar_encabezado_documento.p_id_moneda
    )
    RETURNING trs_encabezado_documento.id_documento INTO v_id;
    
    RETURN QUERY SELECT v_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al insertar encabezado documento: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_insertar_detalle_documento(INTEGER, INTEGER, INTEGER, DECIMAL, DECIMAL, DECIMAL);
CREATE OR REPLACE FUNCTION sp_insertar_detalle_documento(
    p_id_documento INTEGER, 
    p_id_producto INTEGER, 
    p_cantidad INTEGER, 
    p_subtotal DECIMAL(10,2), 
    p_igv DECIMAL(10,2), 
    p_importe DECIMAL(10,2)
)
RETURNS TABLE(id_detalle INTEGER) AS $$
DECLARE
    v_id INTEGER;
BEGIN
    INSERT INTO trs_detalle_documento(
        id_documento, 
        id_producto, 
        cantidad, 
        subtotal, 
        igv, 
        importe
    ) 
    VALUES (
        sp_insertar_detalle_documento.p_id_documento, 
        sp_insertar_detalle_documento.p_id_producto, 
        sp_insertar_detalle_documento.p_cantidad, 
        sp_insertar_detalle_documento.p_subtotal, 
        sp_insertar_detalle_documento.p_igv, 
        sp_insertar_detalle_documento.p_importe
    )
    RETURNING trs_detalle_documento.id_detalle INTO v_id;
    
    RETURN QUERY SELECT v_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al insertar detalle documento: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_insertar_encabezado_guia(INTEGER, VARCHAR, DATE, DATE, VARCHAR, VARCHAR, VARCHAR, INTEGER, INTEGER);
CREATE OR REPLACE FUNCTION sp_insertar_encabezado_guia(
    p_id_doc_venta INTEGER, 
    p_nro_guia VARCHAR(20), 
    p_fecha_emision DATE, 
    p_fecha_inicio_traslado DATE, 
    p_motivo_traslado VARCHAR(100), 
    p_direccion_partida VARCHAR(150), 
    p_direccion_llegada VARCHAR(150), 
    p_id_conductor INTEGER, 
    p_id_vehiculo INTEGER
)
RETURNS TABLE(id_guia INTEGER) AS $$
DECLARE
    v_id INTEGER;
BEGIN
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
        sp_insertar_encabezado_guia.p_id_doc_venta, 
        sp_insertar_encabezado_guia.p_nro_guia, 
        sp_insertar_encabezado_guia.p_fecha_emision, 
        sp_insertar_encabezado_guia.p_fecha_inicio_traslado, 
        sp_insertar_encabezado_guia.p_motivo_traslado, 
        sp_insertar_encabezado_guia.p_direccion_partida, 
        sp_insertar_encabezado_guia.p_direccion_llegada, 
        sp_insertar_encabezado_guia.p_id_conductor, 
        sp_insertar_encabezado_guia.p_id_vehiculo
    )
    RETURNING trs_encabezado_guia.id_guia INTO v_id;
    
    RETURN QUERY SELECT v_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al insertar encabezado guía: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_insertar_detalle_guia(INTEGER, INTEGER, VARCHAR, VARCHAR, VARCHAR, DECIMAL, VARCHAR, CHAR, CHAR, CHAR, CHAR, INTEGER, INTEGER);
CREATE OR REPLACE FUNCTION sp_insertar_detalle_guia(
    p_id_guia INTEGER, 
    p_id_producto INTEGER, 
    p_descripcion VARCHAR(100), 
    p_unidad_medida VARCHAR(10), 
    p_unidad_peso_bruto VARCHAR(10), 
    p_peso_total_carga DECIMAL(10,2), 
    p_modalidad_trans VARCHAR(20), 
    p_transbordo_prog CHAR(2), 
    p_categoriaM1_L CHAR(2), 
    p_retorno_envases CHAR(2), 
    p_vehiculo_vacio CHAR(2), 
    p_id_conductor INTEGER, 
    p_id_vehiculo INTEGER
)
RETURNS TABLE(id_detalle_guia INTEGER) AS $$
DECLARE
    v_id INTEGER;
BEGIN
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
        sp_insertar_detalle_guia.p_id_guia, 
        sp_insertar_detalle_guia.p_id_producto, 
        sp_insertar_detalle_guia.p_descripcion, 
        sp_insertar_detalle_guia.p_unidad_medida, 
        sp_insertar_detalle_guia.p_unidad_peso_bruto, 
        sp_insertar_detalle_guia.p_peso_total_carga, 
        sp_insertar_detalle_guia.p_modalidad_trans, 
        sp_insertar_detalle_guia.p_transbordo_prog, 
        sp_insertar_detalle_guia.p_categoriaM1_L, 
        sp_insertar_detalle_guia.p_retorno_envases, 
        sp_insertar_detalle_guia.p_vehiculo_vacio, 
        sp_insertar_detalle_guia.p_id_conductor, 
        sp_insertar_detalle_guia.p_id_vehiculo
    )
    RETURNING trs_detalle_guia.id_detalle_guia INTO v_id;
    
    RETURN QUERY SELECT v_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al insertar detalle guía: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- CRUD - CONDUCTORES

DROP FUNCTION IF EXISTS sp_obtener_conductores_activos();
CREATE OR REPLACE FUNCTION sp_obtener_conductores_activos()
RETURNS TABLE(
    id_conductor INTEGER,
    nombre VARCHAR(50),
    n_licencia CHAR(12),
    activo BOOLEAN
) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.id_conductor, 
        c.nombre, 
        c.n_licencia, 
        c.activo 
    FROM mae_conductor c
    WHERE c.activo = TRUE 
    ORDER BY c.nombre;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_actualizar_conductor(INTEGER, VARCHAR, CHAR);
CREATE OR REPLACE FUNCTION sp_actualizar_conductor(
    p_id_conductor INTEGER, 
    p_nombre VARCHAR(50), 
    p_n_licencia CHAR(12)
)
RETURNS TABLE(mensaje TEXT) AS $$
BEGIN
    UPDATE mae_conductor 
    SET nombre = sp_actualizar_conductor.p_nombre, 
        n_licencia = sp_actualizar_conductor.p_n_licencia, 
        activo = TRUE 
    WHERE id_conductor = sp_actualizar_conductor.p_id_conductor;
    
    RETURN QUERY SELECT 'Conductor actualizado exitosamente'::TEXT;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al actualizar conductor: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_desactivar_conductor(INTEGER);
CREATE OR REPLACE FUNCTION sp_desactivar_conductor(p_id_conductor INTEGER)
RETURNS TABLE(mensaje TEXT) AS $$
BEGIN
    UPDATE mae_conductor 
    SET activo = FALSE 
    WHERE id_conductor = sp_desactivar_conductor.p_id_conductor;
    
    RETURN QUERY SELECT 'Conductor desactivado exitosamente'::TEXT;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al desactivar conductor: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- CRUD - VEHÍCULOS

DROP FUNCTION IF EXISTS sp_obtener_vehiculos_activos();
CREATE OR REPLACE FUNCTION sp_obtener_vehiculos_activos()
RETURNS TABLE(
    id_vehiculo INTEGER,
    descripcion VARCHAR(50),
    placa CHAR(8),
    activo BOOLEAN
) AS $$
BEGIN
    RETURN QUERY 
    SELECT v.id_vehiculo, 
        v.descripcion, 
        v.placa, 
        v.activo 
    FROM mae_vehiculo v
    WHERE v.activo = TRUE 
    ORDER BY v.descripcion;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_actualizar_vehiculo(INTEGER, VARCHAR, CHAR);
CREATE OR REPLACE FUNCTION sp_actualizar_vehiculo(
    p_id_vehiculo INTEGER, 
    p_descripcion VARCHAR(50), 
    p_placa CHAR(8)
)
RETURNS TABLE(mensaje TEXT) AS $$
BEGIN
    UPDATE mae_vehiculo 
    SET descripcion = sp_actualizar_vehiculo.p_descripcion, 
        placa = sp_actualizar_vehiculo.p_placa, 
        activo = TRUE 
    WHERE id_vehiculo = sp_actualizar_vehiculo.p_id_vehiculo;
    
    RETURN QUERY SELECT 'Vehículo actualizado exitosamente'::TEXT;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al actualizar vehículo: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_desactivar_vehiculo(INTEGER);
CREATE OR REPLACE FUNCTION sp_desactivar_vehiculo(p_id_vehiculo INTEGER)
RETURNS TABLE(mensaje TEXT) AS $$
BEGIN
    UPDATE mae_vehiculo 
    SET activo = FALSE 
    WHERE id_vehiculo = sp_desactivar_vehiculo.p_id_vehiculo;
    
    RETURN QUERY SELECT 'Vehículo desactivado exitosamente'::TEXT;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al desactivar vehículo: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- CRUD - FORMAS DE PAGO

DROP FUNCTION IF EXISTS sp_obtener_formas_pago_activas();
CREATE OR REPLACE FUNCTION sp_obtener_formas_pago_activas()
RETURNS TABLE(
    id_forma_pago INTEGER,
    nombre VARCHAR(35),
    descripcion VARCHAR(100),
    activo BOOLEAN
) AS $$
BEGIN
    RETURN QUERY 
    SELECT fp.id_forma_pago, 
        fp.nombre, 
        fp.descripcion, 
        fp.activo 
    FROM mae_forma_pago fp
    WHERE fp.activo = TRUE 
    ORDER BY fp.nombre;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_actualizar_forma_pago(INTEGER, VARCHAR, VARCHAR);
CREATE OR REPLACE FUNCTION sp_actualizar_forma_pago(
    p_id_forma_pago INTEGER, 
    p_nombre VARCHAR(35), 
    p_descripcion VARCHAR(100)
)
RETURNS TABLE(mensaje TEXT) AS $$
BEGIN
    UPDATE mae_forma_pago 
    SET nombre = sp_actualizar_forma_pago.p_nombre, 
        descripcion = sp_actualizar_forma_pago.p_descripcion, 
        activo = TRUE 
    WHERE id_forma_pago = sp_actualizar_forma_pago.p_id_forma_pago;
    
    RETURN QUERY SELECT 'Forma de pago actualizada exitosamente'::TEXT;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al actualizar forma de pago: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_desactivar_forma_pago(INTEGER);
CREATE OR REPLACE FUNCTION sp_desactivar_forma_pago(p_id_forma_pago INTEGER)
RETURNS TABLE(mensaje TEXT) AS $$
BEGIN
    UPDATE mae_forma_pago 
    SET activo = FALSE 
    WHERE id_forma_pago = sp_desactivar_forma_pago.p_id_forma_pago;
    
    RETURN QUERY SELECT 'Forma de pago desactivada exitosamente'::TEXT;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al desactivar forma de pago: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- CRUD - MONEDAS

DROP FUNCTION IF EXISTS sp_obtener_monedas_activas();
CREATE OR REPLACE FUNCTION sp_obtener_monedas_activas()
RETURNS TABLE(
    id_moneda INTEGER,
    codigo_iso CHAR(3),
    nombre VARCHAR(20),
    activo BOOLEAN
) AS $$
BEGIN
    RETURN QUERY 
    SELECT m.id_moneda, 
        m.codigo_iso, 
        m.nombre, 
        m.activo 
    FROM mae_moneda m
    WHERE m.activo = TRUE 
    ORDER BY m.nombre;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_actualizar_moneda(INTEGER, CHAR, VARCHAR);
CREATE OR REPLACE FUNCTION sp_actualizar_moneda(
    p_id_moneda INTEGER, 
    p_codigo_iso CHAR(3), 
    p_nombre VARCHAR(20)
)
RETURNS TABLE(mensaje TEXT) AS $$
BEGIN
    UPDATE mae_moneda 
    SET codigo_iso = sp_actualizar_moneda.p_codigo_iso, 
        nombre = sp_actualizar_moneda.p_nombre, 
        activo = TRUE 
    WHERE id_moneda = sp_actualizar_moneda.p_id_moneda;
    
    RETURN QUERY SELECT 'Moneda actualizada exitosamente'::TEXT;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al actualizar moneda: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_desactivar_moneda(INTEGER);
CREATE OR REPLACE FUNCTION sp_desactivar_moneda(p_id_moneda INTEGER)
RETURNS TABLE(mensaje TEXT) AS $$
BEGIN
    UPDATE mae_moneda 
    SET activo = FALSE 
    WHERE id_moneda = sp_desactivar_moneda.p_id_moneda;
    
    RETURN QUERY SELECT 'Moneda desactivada exitosamente'::TEXT;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al desactivar moneda: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- CRUD - UBICACIONES

DROP FUNCTION IF EXISTS sp_obtener_ubicaciones_activas();
CREATE OR REPLACE FUNCTION sp_obtener_ubicaciones_activas()
RETURNS TABLE(
    id_ubicacion INTEGER,
    descripcion VARCHAR(100),
    activo BOOLEAN
) AS $$
BEGIN
    RETURN QUERY 
    SELECT u.id_ubicacion, 
        u.descripcion, 
        u.activo 
    FROM mae_ubicacion u
    WHERE u.activo = TRUE 
    ORDER BY u.descripcion;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_actualizar_ubicacion(INTEGER, VARCHAR);
CREATE OR REPLACE FUNCTION sp_actualizar_ubicacion(
    p_id_ubicacion INTEGER, 
    p_descripcion VARCHAR(100)
)
RETURNS TABLE(mensaje TEXT) AS $$
BEGIN
    UPDATE mae_ubicacion 
    SET descripcion = sp_actualizar_ubicacion.p_descripcion, 
        activo = TRUE 
    WHERE id_ubicacion = sp_actualizar_ubicacion.p_id_ubicacion;
    
    RETURN QUERY SELECT 'Ubicación actualizada exitosamente'::TEXT;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al actualizar ubicación: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_desactivar_ubicacion(INTEGER);
CREATE OR REPLACE FUNCTION sp_desactivar_ubicacion(p_id_ubicacion INTEGER)
RETURNS TABLE(mensaje TEXT) AS $$
BEGIN
    UPDATE mae_ubicacion 
    SET activo = FALSE 
    WHERE id_ubicacion = sp_desactivar_ubicacion.p_id_ubicacion;
    
    RETURN QUERY SELECT 'Ubicación desactivada exitosamente'::TEXT;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al desactivar ubicación: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- CRUD - IDENTIDADES

DROP FUNCTION IF EXISTS sp_obtener_identidades_activas();
CREATE OR REPLACE FUNCTION sp_obtener_identidades_activas()
RETURNS TABLE(
    id_identidad INTEGER,
    tipo_identificacion VARCHAR(20),
    codigo_documento VARCHAR(15),
    activo BOOLEAN
) AS $$
BEGIN
    RETURN QUERY 
    SELECT i.id_identidad, 
        i.tipo_identificacion, 
        i.codigo_documento, 
        i.activo 
    FROM mae_identidad i
    WHERE i.activo = TRUE 
    ORDER BY i.tipo_identificacion, i.codigo_documento;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_actualizar_identidad(INTEGER, VARCHAR, VARCHAR);
CREATE OR REPLACE FUNCTION sp_actualizar_identidad(
    p_id_identidad INTEGER, 
    p_tipo_identificacion VARCHAR(20), 
    p_codigo_documento VARCHAR(15)
)
RETURNS TABLE(mensaje TEXT) AS $$
BEGIN
    UPDATE mae_identidad 
    SET tipo_identificacion = sp_actualizar_identidad.p_tipo_identificacion, 
        codigo_documento = sp_actualizar_identidad.p_codigo_documento, 
        activo = TRUE 
    WHERE id_identidad = sp_actualizar_identidad.p_id_identidad;
    
    RETURN QUERY SELECT 'Identidad actualizada exitosamente'::TEXT;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al actualizar identidad: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_desactivar_identidad(INTEGER);
CREATE OR REPLACE FUNCTION sp_desactivar_identidad(p_id_identidad INTEGER)
RETURNS TABLE(mensaje TEXT) AS $$
BEGIN
    UPDATE mae_identidad 
    SET activo = FALSE 
    WHERE id_identidad = sp_desactivar_identidad.p_id_identidad;
    
    RETURN QUERY SELECT 'Identidad desactivada exitosamente'::TEXT;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al desactivar identidad: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- CRUD - CLIENTES

DROP FUNCTION IF EXISTS sp_obtener_clientes_activos();
CREATE OR REPLACE FUNCTION sp_obtener_clientes_activos()
RETURNS TABLE(
    id_cliente INTEGER,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    ubicacion VARCHAR(100),
    tipo_identificacion VARCHAR(20),
    codigo_documento VARCHAR(15),
    activo BOOLEAN,
    id_ubicacion INTEGER,
    id_identidad INTEGER
) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.id_cliente, 
        c.nombre, 
        c.apellido, 
        u.descripcion::VARCHAR(100) AS ubicacion, 
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
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_actualizar_cliente(INTEGER, VARCHAR, VARCHAR, INTEGER, INTEGER);
CREATE OR REPLACE FUNCTION sp_actualizar_cliente(
    p_id_cliente INTEGER, 
    p_nombre VARCHAR(50), 
    p_apellido VARCHAR(50), 
    p_id_ubicacion INTEGER, 
    p_id_identidad INTEGER
)
RETURNS TABLE(mensaje TEXT) AS $$
BEGIN
    UPDATE mae_cliente 
    SET nombre = sp_actualizar_cliente.p_nombre, 
        apellido = sp_actualizar_cliente.p_apellido, 
        id_ubicacion = sp_actualizar_cliente.p_id_ubicacion, 
        id_identidad = sp_actualizar_cliente.p_id_identidad, 
        activo = TRUE 
    WHERE id_cliente = sp_actualizar_cliente.p_id_cliente;
    
    RETURN QUERY SELECT 'Cliente actualizado exitosamente'::TEXT;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al actualizar cliente: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_desactivar_cliente(INTEGER);
CREATE OR REPLACE FUNCTION sp_desactivar_cliente(p_id_cliente INTEGER)
RETURNS TABLE(mensaje TEXT) AS $$
BEGIN
    UPDATE mae_cliente 
    SET activo = FALSE 
    WHERE id_cliente = sp_desactivar_cliente.p_id_cliente;
    
    RETURN QUERY SELECT 'Cliente desactivado exitosamente'::TEXT;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al desactivar cliente: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- CRUD - PRODUCTOS

DROP FUNCTION IF EXISTS sp_obtener_productos_activos();
CREATE OR REPLACE FUNCTION sp_obtener_productos_activos()
RETURNS TABLE(
    id_producto INTEGER,
    nombre VARCHAR(50),
    descripcion VARCHAR(100),
    precio_base DECIMAL(10,2),
    stock INTEGER,
    unidad_medida VARCHAR(10),
    activo BOOLEAN
) AS $$
BEGIN
    RETURN QUERY 
    SELECT p.id_producto, 
        p.nombre, 
        p.descripcion, 
        p.precio_base, 
        p.stock, 
        p.unidad_medida, 
        p.activo 
    FROM mae_producto p
    WHERE p.activo = TRUE 
    ORDER BY p.nombre;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_actualizar_producto(INTEGER, VARCHAR, VARCHAR, DECIMAL, INTEGER, VARCHAR);
CREATE OR REPLACE FUNCTION sp_actualizar_producto(
    p_id_producto INTEGER, 
    p_nombre VARCHAR(50), 
    p_descripcion VARCHAR(100), 
    p_precio_base DECIMAL(10,2), 
    p_stock INTEGER, 
    p_unidad_medida VARCHAR(10)
)
RETURNS TABLE(mensaje TEXT) AS $$
BEGIN
    UPDATE mae_producto 
    SET nombre = sp_actualizar_producto.p_nombre, 
        descripcion = sp_actualizar_producto.p_descripcion, 
        precio_base = sp_actualizar_producto.p_precio_base, 
        stock = sp_actualizar_producto.p_stock, 
        unidad_medida = sp_actualizar_producto.p_unidad_medida, 
        activo = TRUE 
    WHERE id_producto = sp_actualizar_producto.p_id_producto;
    
    RETURN QUERY SELECT 'Producto actualizado exitosamente'::TEXT;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al actualizar producto: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_desactivar_producto(INTEGER);
CREATE OR REPLACE FUNCTION sp_desactivar_producto(p_id_producto INTEGER)
RETURNS TABLE(mensaje TEXT) AS $$
BEGIN
    UPDATE mae_producto 
    SET activo = FALSE 
    WHERE id_producto = sp_desactivar_producto.p_id_producto;
    
    RETURN QUERY SELECT 'Producto desactivado exitosamente'::TEXT;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al desactivar producto: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_ajustar_stock_producto(INTEGER, INTEGER, VARCHAR);
CREATE OR REPLACE FUNCTION sp_ajustar_stock_producto(
    p_id_producto INTEGER, 
    p_cantidad INTEGER, 
    p_tipo_movimiento VARCHAR(10)
)
RETURNS TABLE(mensaje TEXT, nuevo_stock INTEGER) AS $$
DECLARE
    v_stock_actual INTEGER;
BEGIN
    SELECT p.stock INTO v_stock_actual 
    FROM mae_producto p
    WHERE p.id_producto = sp_ajustar_stock_producto.p_id_producto;
    
    IF sp_ajustar_stock_producto.p_tipo_movimiento = 'ENTRADA' THEN
        UPDATE mae_producto 
        SET stock = stock + sp_ajustar_stock_producto.p_cantidad 
        WHERE id_producto = sp_ajustar_stock_producto.p_id_producto;
        
        RETURN QUERY 
        SELECT 'Stock incrementado exitosamente'::TEXT, 
            (v_stock_actual + sp_ajustar_stock_producto.p_cantidad)::INTEGER;
            
    ELSIF sp_ajustar_stock_producto.p_tipo_movimiento = 'SALIDA' THEN
        IF v_stock_actual < sp_ajustar_stock_producto.p_cantidad THEN
            RAISE EXCEPTION 'Stock insuficiente. Stock actual: %', v_stock_actual;
        ELSE
            UPDATE mae_producto 
            SET stock = stock - sp_ajustar_stock_producto.p_cantidad 
            WHERE id_producto = sp_ajustar_stock_producto.p_id_producto;
            
            RETURN QUERY 
            SELECT 'Stock reducido exitosamente'::TEXT, 
                (v_stock_actual - sp_ajustar_stock_producto.p_cantidad)::INTEGER;
        END IF;
    ELSE
        RAISE EXCEPTION 'Tipo de movimiento inválido. Use ENTRADA o SALIDA';
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        RAISE;
END;
$$ LANGUAGE plpgsql;

-- MOVIMIENTOS DE INVENTARIO

DROP FUNCTION IF EXISTS sp_obtener_movimientos_inventario();
CREATE OR REPLACE FUNCTION sp_obtener_movimientos_inventario()
RETURNS TABLE(
    id_documento INTEGER,
    tipo_doc VARCHAR(20),
    fecha_emision DATE,
    producto VARCHAR(50),
    cantidad INTEGER,
    estado_doc VARCHAR(20),
    tipo_movimiento TEXT
) AS $$
BEGIN
    RETURN QUERY 
    SELECT d.id_documento, 
        d.tipo_doc, 
        d.fecha_emision, 
        p.nombre::VARCHAR(50) AS producto, 
        dt.cantidad, 
        d.estado_doc, 
        'SALIDA'::TEXT AS tipo_movimiento
    FROM trs_detalle_documento dt 
    JOIN trs_encabezado_documento d ON dt.id_documento = d.id_documento 
    JOIN mae_producto p ON dt.id_producto = p.id_producto
    WHERE d.estado_doc = 'EMITIDO' 
    ORDER BY d.fecha_emision DESC 
    LIMIT 100;
END;
$$ LANGUAGE plpgsql;

-- DOCUMENTOS

DROP FUNCTION IF EXISTS sp_obtener_documentos_empresa(INTEGER);
CREATE OR REPLACE FUNCTION sp_obtener_documentos_empresa(p_id_empresa INTEGER)
RETURNS TABLE(
    id_documento INTEGER,
    tipo_doc VARCHAR(20),
    fecha_emision DATE,
    cliente TEXT,
    forma_pago VARCHAR(35),
    moneda CHAR(3),
    estado_doc VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY 
    SELECT d.id_documento, 
        d.tipo_doc, 
        d.fecha_emision, 
        (c.nombre || ' ' || c.apellido)::TEXT AS cliente, 
        fp.nombre::VARCHAR(35) AS forma_pago, 
        m.codigo_iso::CHAR(3) AS moneda, 
        d.estado_doc
    FROM trs_encabezado_documento d 
    JOIN mae_cliente c ON d.id_cliente = c.id_cliente 
    JOIN mae_forma_pago fp ON d.id_forma_pago = fp.id_forma_pago 
    JOIN mae_moneda m ON d.id_moneda = m.id_moneda
    WHERE d.id_empresa = sp_obtener_documentos_empresa.p_id_empresa 
    ORDER BY d.fecha_emision DESC, d.id_documento DESC;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_obtener_detalle_documento(INTEGER);
CREATE OR REPLACE FUNCTION sp_obtener_detalle_documento(p_id_documento INTEGER)
RETURNS TABLE(
    producto VARCHAR(50),
    cantidad INTEGER,
    subtotal DECIMAL(10,2),
    igv DECIMAL(10,2),
    importe DECIMAL(10,2)
) AS $$
BEGIN
    RETURN QUERY 
    SELECT p.nombre::VARCHAR(50) AS producto, 
        dt.cantidad, 
        dt.subtotal, 
        dt.igv, 
        dt.importe 
    FROM trs_detalle_documento dt 
    JOIN mae_producto p ON dt.id_producto = p.id_producto 
    WHERE dt.id_documento = sp_obtener_detalle_documento.p_id_documento;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_actualizar_estado_documento(INTEGER, VARCHAR);
CREATE OR REPLACE FUNCTION sp_actualizar_estado_documento(
    p_id_documento INTEGER, 
    p_nuevo_estado VARCHAR(20)
)
RETURNS TABLE(mensaje TEXT) AS $$
BEGIN
    UPDATE trs_encabezado_documento 
    SET estado_doc = sp_actualizar_estado_documento.p_nuevo_estado 
    WHERE id_documento = sp_actualizar_estado_documento.p_id_documento;
    
    RETURN QUERY SELECT 'Estado del documento actualizado exitosamente'::TEXT;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al actualizar estado del documento: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- GUÍAS DE REMISIÓN

DROP FUNCTION IF EXISTS sp_obtener_guias_empresa(INTEGER);
CREATE OR REPLACE FUNCTION sp_obtener_guias_empresa(p_id_empresa INTEGER)
RETURNS TABLE(
    id_guia INTEGER,
    nro_guia VARCHAR(20),
    fecha_emision DATE,
    fecha_inicio_traslado DATE,
    motivo_traslado VARCHAR(100),
    direccion_partida VARCHAR(150),
    direccion_llegada VARCHAR(150),
    conductor VARCHAR(50),
    vehiculo VARCHAR(50),
    estado_guia VARCHAR(20),
    tipo_doc VARCHAR(20),
    id_documento INTEGER
) AS $$
BEGIN
    RETURN QUERY 
    SELECT g.id_guia, 
        g.nro_guia, 
        g.fecha_emision, 
        g.fecha_inicio_traslado, 
        g.motivo_traslado, 
        g.direccion_partida, 
        g.direccion_llegada, 
        c.nombre::VARCHAR(50) AS conductor, 
        v.descripcion::VARCHAR(50) AS vehiculo, 
        g.estado_guia, 
        d.tipo_doc, 
        d.id_documento
    FROM trs_encabezado_guia g 
    JOIN trs_encabezado_documento d ON g.id_doc_venta = d.id_documento 
    JOIN mae_conductor c ON g.id_conductor = c.id_conductor 
    JOIN mae_vehiculo v ON g.id_vehiculo = v.id_vehiculo
    WHERE d.id_empresa = sp_obtener_guias_empresa.p_id_empresa 
    ORDER BY g.fecha_emision DESC, g.id_guia DESC;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_obtener_detalle_guia(INTEGER);
CREATE OR REPLACE FUNCTION sp_obtener_detalle_guia(p_id_guia INTEGER)
RETURNS TABLE(
    producto VARCHAR(50),
    descripcion VARCHAR(100),
    unidad_medida VARCHAR(10),
    peso_total_carga DECIMAL(10,2),
    modalidad_trans VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY 
    SELECT p.nombre::VARCHAR(50) AS producto, 
        dg.descripcion, 
        dg.unidad_medida, 
        dg.peso_total_carga, 
        dg.modalidad_trans 
    FROM trs_detalle_guia dg 
    JOIN mae_producto p ON dg.id_producto = p.id_producto 
    WHERE dg.id_guia = sp_obtener_detalle_guia.p_id_guia;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_actualizar_estado_guia(INTEGER, VARCHAR);
CREATE OR REPLACE FUNCTION sp_actualizar_estado_guia(
    p_id_guia INTEGER, 
    p_nuevo_estado VARCHAR(20)
)
RETURNS TABLE(mensaje TEXT) AS $$
BEGIN
    UPDATE trs_encabezado_guia 
    SET estado_guia = sp_actualizar_estado_guia.p_nuevo_estado 
    WHERE id_guia = sp_actualizar_estado_guia.p_id_guia;
    
    RETURN QUERY SELECT 'Estado de la guía actualizado exitosamente'::TEXT;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al actualizar estado de la guía: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- COMBOS

DROP FUNCTION IF EXISTS sp_obtener_ubicaciones_combo();
CREATE OR REPLACE FUNCTION sp_obtener_ubicaciones_combo()
RETURNS TABLE(
    id_ubicacion INTEGER,
    descripcion VARCHAR(100)
) AS $$
BEGIN
    RETURN QUERY 
    SELECT u.id_ubicacion, 
        u.descripcion 
    FROM mae_ubicacion u
    WHERE u.activo = TRUE 
    ORDER BY u.descripcion;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_obtener_identidades_combo();
CREATE OR REPLACE FUNCTION sp_obtener_identidades_combo()
RETURNS TABLE(
    id_identidad INTEGER,
    tipo_identificacion VARCHAR(20),
    codigo_documento VARCHAR(15)
) AS $$
BEGIN
    RETURN QUERY 
    SELECT i.id_identidad, 
        i.tipo_identificacion, 
        i.codigo_documento 
    FROM mae_identidad i
    WHERE i.activo = TRUE 
    ORDER BY i.tipo_identificacion, i.codigo_documento;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_obtener_clientes_combo();
CREATE OR REPLACE FUNCTION sp_obtener_clientes_combo()
RETURNS TABLE(
    id_cliente INTEGER,
    nombre VARCHAR(50),
    apellido VARCHAR(50)
) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.id_cliente, 
        c.nombre, 
        c.apellido 
    FROM mae_cliente c
    WHERE c.activo = TRUE 
    ORDER BY c.nombre, c.apellido;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_obtener_formas_pago_combo();
CREATE OR REPLACE FUNCTION sp_obtener_formas_pago_combo()
RETURNS TABLE(
    id_forma_pago INTEGER,
    nombre VARCHAR(35)
) AS $$
BEGIN
    RETURN QUERY 
    SELECT fp.id_forma_pago, 
        fp.nombre 
    FROM mae_forma_pago fp
    WHERE fp.activo = TRUE 
    ORDER BY fp.nombre;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_obtener_monedas_combo();
CREATE OR REPLACE FUNCTION sp_obtener_monedas_combo()
RETURNS TABLE(
    id_moneda INTEGER,
    codigo_iso CHAR(3),
    nombre VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY 
    SELECT m.id_moneda, 
        m.codigo_iso, 
        m.nombre 
    FROM mae_moneda m
    WHERE m.activo = TRUE 
    ORDER BY m.nombre;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_obtener_productos_combo();
CREATE OR REPLACE FUNCTION sp_obtener_productos_combo()
RETURNS TABLE(
    id_producto INTEGER,
    nombre VARCHAR(50),
    precio_base DECIMAL(10,2),
    stock INTEGER
) AS $$
BEGIN
    RETURN QUERY 
    SELECT p.id_producto, 
        p.nombre, 
        p.precio_base, 
        p.stock 
    FROM mae_producto p
    WHERE p.activo = TRUE 
    ORDER BY p.nombre;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_obtener_conductores_combo();
CREATE OR REPLACE FUNCTION sp_obtener_conductores_combo()
RETURNS TABLE(
    id_conductor INTEGER,
    nombre VARCHAR(50),
    n_licencia CHAR(12)
) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.id_conductor, 
        c.nombre, 
        c.n_licencia 
    FROM mae_conductor c
    WHERE c.activo = TRUE 
    ORDER BY c.nombre;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_obtener_vehiculos_combo();
CREATE OR REPLACE FUNCTION sp_obtener_vehiculos_combo()
RETURNS TABLE(
    id_vehiculo INTEGER,
    descripcion VARCHAR(50),
    placa CHAR(8)
) AS $$
BEGIN
    RETURN QUERY 
    SELECT v.id_vehiculo, 
        v.descripcion, 
        v.placa 
    FROM mae_vehiculo v
    WHERE v.activo = TRUE 
    ORDER BY v.descripcion;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_obtener_documentos_emitidos(INTEGER);
CREATE OR REPLACE FUNCTION sp_obtener_documentos_emitidos(p_id_empresa INTEGER)
RETURNS TABLE(
    id_documento INTEGER,
    tipo_doc VARCHAR(20),
    fecha_emision DATE,
    cliente TEXT
) AS $$
BEGIN
    RETURN QUERY 
    SELECT d.id_documento, 
        d.tipo_doc, 
        d.fecha_emision, 
        (c.nombre || ' ' || c.apellido)::TEXT AS cliente
    FROM trs_encabezado_documento d 
    JOIN mae_cliente c ON d.id_cliente = c.id_cliente
    WHERE d.id_empresa = sp_obtener_documentos_emitidos.p_id_empresa 
    AND d.estado_doc = 'EMITIDO' 
    AND d.id_documento NOT IN (
        SELECT id_doc_venta 
        FROM trs_encabezado_guia
    )
    ORDER BY d.fecha_emision DESC;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS sp_obtener_productos_documento(INTEGER);
CREATE OR REPLACE FUNCTION sp_obtener_productos_documento(p_id_documento INTEGER)
RETURNS TABLE(
    id_producto INTEGER,
    nombre VARCHAR(50),
    cantidad INTEGER,
    unidad_medida VARCHAR(10)
) AS $$
BEGIN
    RETURN QUERY 
    SELECT p.id_producto, 
        p.nombre, 
        dt.cantidad, 
        p.unidad_medida 
    FROM trs_detalle_documento dt 
    JOIN mae_producto p ON dt.id_producto = p.id_producto 
    WHERE dt.id_documento = sp_obtener_productos_documento.p_id_documento;
END;
$$ LANGUAGE plpgsql;

-- VALIDACIONES

DROP FUNCTION IF EXISTS sp_verificar_guia_existe(VARCHAR);
CREATE OR REPLACE FUNCTION sp_verificar_guia_existe(p_nro_guia VARCHAR(20))
RETURNS TABLE(existe BIGINT) AS $$
BEGIN
    RETURN QUERY 
    SELECT COUNT(*)::BIGINT AS existe 
    FROM trs_encabezado_guia 
    WHERE nro_guia = sp_verificar_guia_existe.p_nro_guia;
END;
$$ LANGUAGE plpgsql;