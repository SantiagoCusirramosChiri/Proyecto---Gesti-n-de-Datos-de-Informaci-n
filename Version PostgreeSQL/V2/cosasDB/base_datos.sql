DROP TABLE IF EXISTS log_eliminaciones CASCADE;
DROP TABLE IF EXISTS trs_detalle_guia CASCADE;
DROP TABLE IF EXISTS trs_encabezado_guia CASCADE;
DROP TABLE IF EXISTS trs_detalle_documento CASCADE;
DROP TABLE IF EXISTS trs_encabezado_documento CASCADE;
DROP TABLE IF EXISTS mae_cliente CASCADE;
DROP TABLE IF EXISTS mae_empresa CASCADE;
DROP TABLE IF EXISTS mae_producto CASCADE;
DROP TABLE IF EXISTS mae_forma_pago CASCADE;
DROP TABLE IF EXISTS mae_moneda CASCADE;
DROP TABLE IF EXISTS mae_vehiculo CASCADE;
DROP TABLE IF EXISTS mae_conductor CASCADE;
DROP TABLE IF EXISTS mae_identidad CASCADE;
DROP TABLE IF EXISTS mae_ubicacion CASCADE;

-- ============================================
-- PASO 2: CREAR ESTRUCTURA DE TABLAS
-- ============================================

-- TABLAS MAESTRAS

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

-- TABLA DE LOG
CREATE TABLE log_eliminaciones (
    id_log SERIAL PRIMARY KEY,
    tabla VARCHAR(50) NOT NULL,
    id_registro INT NOT NULL,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- PASO 3: INSERTAR DATOS INICIALES
-- ============================================

-- Insertar ubicaciones
INSERT INTO mae_ubicacion (descripcion) VALUES
('Avenida San Martin 507'),
('Avenida Bolognesi 312'),
('Avenida Coronel Mendoza 210'),
('Avenida Gustavo Pinto 459'),
('Avenida Justo Arias Araquez 189'),
('Avenida 28 de Agosto 356'),
('Avenida Hoyos Rubio 202'),
('Calle Alto Lima 134'),
('Calle Francisco Laso 221'),
('Pasaje Las Bugambillas 89');

-- Insertar identidades
INSERT INTO mae_identidad (tipo_identificacion, codigo_documento) VALUES
('DNI', '76543211'),
('DNI', '76234567'),
('DNI', '75432123'),
('DNI', '74561234'),
('DNI', '73678901'),
('DNI', '72890123'),
('DNI', '71987654'),
('DNI', '71023456'),
('DNI', '70123456'),
('DNI', '70098765');

-- Insertar clientes
INSERT INTO mae_cliente (nombre, apellido, id_ubicacion, id_identidad) VALUES
('Carlos', 'Ramirez', 1, 1),
('Maria', 'Torres', 2, 2),
('Luis', 'Gomez', 3, 3),
('Ana', 'Quispe', 4, 4),
('Jorge', 'Mamani', 5, 5),
('Rosa', 'Paredes', 6, 6),
('Pedro', 'Huanca', 7, 7),
('Lucia', 'Flores', 8, 8),
('Miguel', 'Valdez', 9, 9),
('Carmen', 'Chavez', 10, 10);

-- Insertar empresas
INSERT INTO mae_empresa (nombre, razon_social, RUC, id_ubicacion) VALUES
('LIBRERIA DISTRIBUIDORA ANILU S.R.L.', 'LIBRERIA DISTRIBUIDORA ANILU S.R.L.', '20600026748', 1);

-- Insertar conductores
INSERT INTO mae_conductor (nombre, n_licencia) VALUES
('Juan Perez', 'B12345678123'),
('Marcos Rojas', 'B87654321123'),
('Daniel Lopez', 'B13579246123'),
('Jose Aguilar', 'B24681357123'),
('Ricardo Castillo', 'B99887766123');

-- Insertar vehiculos
INSERT INTO mae_vehiculo (descripcion, placa) VALUES
('Camioneta Toyota Hilux Blanca', 'ABC-123'),
('Furgon Hyundai H1 Gris', 'XYZ-456'),
('Camion Mitsubishi Canter', 'KLM-789'),
('Motocicleta Honda Cargo', 'HND-321'),
('Camioneta Nissan Frontier Roja', 'NSN-654');

-- Insertar productos
INSERT INTO mae_producto (nombre, descripcion, precio_base, stock, unidad_medida) VALUES
('Cuaderno College 100 hojas', 'Cuaderno A4 de 100 hojas, marca Justus', 8.50, 120, 'UND'),
('Lapicero BIC Azul', 'Lapicero azul punta fina', 1.50, 500, 'UND'),
('Borrador Pelikan', 'Borrador blanco para lapiz', 2.00, 200, 'UND'),
('Tajador Maped', 'Tajador doble con deposito', 3.50, 150, 'UND'),
('Regla 30 cm Arti', 'Regla plastica transparente', 2.50, 300, 'UND'),
('Cartulina Duplex', 'Cartulina tamaño A3 color blanco', 1.80, 400, 'UND'),
('Resaltador Stabilo Amarillo', 'Resaltador color amarillo', 3.00, 250, 'UND'),
('Tempera Vinifan 6 colores', 'Set de temperas escolares', 10.00, 100, 'UND'),
('Corrector Liquido Pelikan', 'Corrector blanco con brocha', 4.50, 180, 'UND'),
('Folder Manila A4', 'Folder tamaño A4 color manila', 1.20, 350, 'UND');

-- Insertar formas de pago
INSERT INTO mae_forma_pago (nombre, descripcion) VALUES
('Efectivo', 'Pago en moneda fisica'),
('Tarjeta de Credito', 'Pago con tarjeta VISA o MasterCard'),
('Transferencia Bancaria', 'Deposito o transferencia en cuenta'),
('Yape', 'Pago digital mediante aplicativo Yape'),
('Plin', 'Pago digital mediante aplicativo Plin');

-- Insertar monedas
INSERT INTO mae_moneda (codigo_iso, nombre) VALUES
('PEN', 'Soles'),
('USD', 'Dolares');

-- Insertar encabezados de documentos
INSERT INTO trs_encabezado_documento (tipo_doc, fecha_emision, id_empresa, id_cliente, id_forma_pago, id_moneda) VALUES
('Boleta', '2025-10-01', 1, 1, 1, 1),
('Factura', '2025-10-01', 1, 2, 2, 1),
('Boleta', '2025-10-02', 1, 3, 1, 1),
('Factura', '2025-10-02', 1, 4, 3, 1),
('Boleta', '2025-10-03', 1, 5, 1, 1),
('Boleta', '2025-10-04', 1, 6, 1, 1),
('Factura', '2025-10-05', 1, 7, 2, 1),
('Boleta', '2025-10-06', 1, 8, 1, 1),
('Factura', '2025-10-06', 1, 9, 3, 1),
('Boleta', '2025-10-07', 1, 10, 1, 1);

-- Insertar detalle de documentos 
INSERT INTO trs_detalle_documento (id_documento, id_producto, cantidad, subtotal, igv, importe) VALUES
(1, 1, 2, 0, 0, 0),
(1, 3, 4, 0, 0, 0),
(2, 2, 5, 0, 0, 0),
(2, 7, 3, 0, 0, 0),
(3, 4, 5, 0, 0, 0),
(4, 5, 4, 0, 0, 0),
(4, 9, 2, 0, 0, 0),
(5, 6, 10, 0, 0, 0),
(5, 8, 2, 0, 0, 0),
(6, 1, 1, 0, 0, 0),
(6, 10, 5, 0, 0, 0),
(7, 7, 5, 0, 0, 0),
(7, 8, 1, 0, 0, 0),
(8, 3, 2, 0, 0, 0),
(8, 2, 4, 0, 0, 0),
(9, 5, 4, 0, 0, 0),
(9, 4, 3, 0, 0, 0),
(10, 1, 3, 0, 0, 0),
(10, 6, 2, 0, 0, 0);

-- Insertar encabezado de guias
INSERT INTO trs_encabezado_guia (id_doc_venta, nro_guia, fecha_emision, fecha_inicio_traslado, motivo_traslado, direccion_partida, direccion_llegada, id_conductor, id_vehiculo) VALUES
(2, 'GR-0001', '2025-10-02', '2025-10-02', 'Entrega de material educativo', 'Avenida San Martin 507', 'Calle Mariano Santos 315', 1, 1),
(4, 'GR-0002', '2025-10-02', '2025-10-03', 'Reparto de libros a institucion educativa', 'Avenida Bolognesi 312', 'Calle Cajamarca 188', 2, 2),
(7, 'GR-0003', '2025-10-05', '2025-10-06', 'Despacho de productos a sucursal', 'Avenida Coronel Mendoza 210', 'Pasaje Las Bugambillas 89', 3, 3),
(9, 'GR-0004', '2025-10-06', '2025-10-07', 'Entrega a cliente corporativo', 'Avenida 28 de Agosto 356', 'Calle Francisco Laso 221', 4, 1),
(10, 'GR-0005', '2025-10-07', '2025-10-07', 'Envio de utiles escolares', 'Calle Alto Lima 134', 'Avenida Justo Arias Araquez 189', 5, 2);

-- Insertar detalle de guias
INSERT INTO trs_detalle_guia (id_guia, id_producto, descripcion, unidad_medida, unidad_peso_bruto, peso_total_carga, modalidad_trans, transbordo_prog, categoriaM1_L, retorno_envases, vehiculo_vacio, id_conductor, id_vehiculo) VALUES
(1, 2, 'Lapiceros BIC', 'UND', 'KG', 2.5, 'Privado', 'NO', 'M1', 'NO', 'NO', 1, 1),
(1, 7, 'Resaltadores Amarillos', 'UND', 'KG', 0.8, 'Privado', 'NO', 'M1', 'NO', 'NO', 1, 1),
(2, 5, 'Reglas Plasticas', 'UND', 'KG', 3.2, 'Privado', 'NO', 'M1', 'NO', 'NO', 2, 2),
(3, 8, 'Temperas Escolares', 'UND', 'KG', 1.5, 'Privado', 'NO', 'M1', 'NO', 'NO', 3, 3),
(3, 9, 'Correctores Liquidos', 'UND', 'KG', 5.0, 'Privado', 'NO', 'M1', 'NO', 'NO', 3, 3),
(4, 5, 'Reglas 30 cm', 'UND', 'KG', 4.5, 'Privado', 'NO', 'M1', 'NO', 'NO', 4, 1),
(5, 1, 'Cuadernos A4', 'UND', 'KG', 0.5, 'Privado', 'NO', 'M1', 'NO', 'NO', 5, 2),
(5, 6, 'Cartulinas Blancas', 'UND', 'KG', 2.0, 'Privado', 'NO', 'M1', 'NO', 'NO', 5, 2);

