DROP DATABASE IF EXISTS sistema_documentos;

CREATE DATABASE sistema_documentos;

CREATE TABLE mae_ubicacion (
    id_ubicacion SERIAL PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE mae_identidad (
    id_identidad SERIAL PRIMARY KEY,
    tipo_identificacion VARCHAR(20) NOT NULL,
    codigo_documento VARCHAR(15) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE mae_cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    id_ubicacion INT NOT NULL,
    id_identidad INT NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_ubicacion) REFERENCES mae_ubicacion(id_ubicacion)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (id_identidad) REFERENCES mae_identidad(id_identidad)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE mae_empresa (
    id_empresa SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    razon_social VARCHAR(100) NOT NULL,
    RUC CHAR(11) NOT NULL UNIQUE,
    id_ubicacion INT NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_ubicacion) REFERENCES mae_ubicacion(id_ubicacion)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE mae_conductor (
    id_conductor SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    n_licencia CHAR(12) NOT NULL UNIQUE,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE mae_vehiculo (
    id_vehiculo SERIAL PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL,
    placa CHAR(8) NOT NULL UNIQUE,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE mae_producto (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(100) NOT NULL,
    precio_base DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    unidad_medida VARCHAR(10) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE mae_forma_pago (
    id_forma_pago SERIAL PRIMARY KEY,
    nombre VARCHAR(35) NOT NULL,
    descripcion VARCHAR(100) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE mae_moneda (
    id_moneda SERIAL PRIMARY KEY,
    codigo_iso CHAR(3) NOT NULL,
    nombre VARCHAR(20) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- TABLAS TRANSACCIONALES

CREATE TABLE trs_encabezado_documento (
    id_documento SERIAL PRIMARY KEY,
    tipo_doc VARCHAR(20) NOT NULL,
    fecha_emision DATE NOT NULL,
    id_empresa INT NOT NULL,
    id_cliente INT NOT NULL,
    id_forma_pago INT NOT NULL,
    id_moneda INT NOT NULL,
    estado_doc VARCHAR(20) NOT NULL DEFAULT 'PENDIENTE',
    FOREIGN KEY (id_empresa) REFERENCES mae_empresa(id_empresa)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (id_cliente) REFERENCES mae_cliente(id_cliente)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (id_forma_pago) REFERENCES mae_forma_pago(id_forma_pago)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (id_moneda) REFERENCES mae_moneda(id_moneda)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE trs_detalle_documento (
    id_detalle SERIAL PRIMARY KEY,
    id_documento INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    igv DECIMAL(10,2) NOT NULL,
    importe DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_documento) REFERENCES trs_encabezado_documento(id_documento)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES mae_producto(id_producto)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE trs_encabezado_guia (
    id_guia SERIAL PRIMARY KEY,
    id_doc_venta INT NOT NULL,
    nro_guia VARCHAR(20) NOT NULL UNIQUE,
    fecha_emision DATE NOT NULL,
    fecha_inicio_traslado DATE NOT NULL,
    motivo_traslado VARCHAR(100) NOT NULL,
    direccion_partida VARCHAR(150) NOT NULL,
    direccion_llegada VARCHAR(150) NOT NULL,
    id_conductor INT NOT NULL,
    id_vehiculo INT NOT NULL,
    estado_guia VARCHAR(20) NOT NULL DEFAULT 'PENDIENTE',
    FOREIGN KEY (id_doc_venta) REFERENCES trs_encabezado_documento(id_documento)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (id_conductor) REFERENCES mae_conductor(id_conductor)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (id_vehiculo) REFERENCES mae_vehiculo(id_vehiculo)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE trs_detalle_guia (
    id_detalle_guia SERIAL PRIMARY KEY,
    id_guia INT NOT NULL,
    id_producto INT NOT NULL,
    descripcion VARCHAR(100),
    unidad_medida VARCHAR(10),
    unidad_peso_bruto VARCHAR(10),
    peso_total_carga DECIMAL(10,2),
    modalidad_trans VARCHAR(20),
    transbordo_prog CHAR(2),
    categoriaM1_L CHAR(2),
    retorno_envases CHAR(2),
    vehiculo_vacio CHAR(2),
    id_conductor INT,
    id_vehiculo INT,
    FOREIGN KEY (id_guia) REFERENCES trs_encabezado_guia(id_guia)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES mae_producto(id_producto)
        ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE log_eliminaciones (
    id_log SERIAL PRIMARY KEY,
    tabla VARCHAR(50) NOT NULL,
    id_registro INT NOT NULL,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);