SET session_replication_role = replica;

TRUNCATE TABLE trs_detalle_guia CASCADE;
TRUNCATE TABLE trs_encabezado_guia CASCADE;
TRUNCATE TABLE trs_detalle_documento CASCADE;
TRUNCATE TABLE trs_encabezado_documento CASCADE;

TRUNCATE TABLE mae_producto CASCADE;
TRUNCATE TABLE mae_vehiculo CASCADE;
TRUNCATE TABLE mae_conductor CASCADE;
TRUNCATE TABLE mae_empresa CASCADE;
TRUNCATE TABLE mae_cliente CASCADE;
TRUNCATE TABLE mae_identidad CASCADE;
TRUNCATE TABLE mae_ubicacion CASCADE;
TRUNCATE TABLE mae_forma_pago CASCADE;
TRUNCATE TABLE mae_moneda CASCADE;

SET session_replication_role = DEFAULT;

ALTER SEQUENCE mae_ubicacion_id_ubicacion_seq RESTART WITH 1;
ALTER SEQUENCE mae_identidad_id_identidad_seq RESTART WITH 1;
ALTER SEQUENCE mae_cliente_id_cliente_seq RESTART WITH 1;
ALTER SEQUENCE mae_empresa_id_empresa_seq RESTART WITH 1;
ALTER SEQUENCE mae_conductor_id_conductor_seq RESTART WITH 1;
ALTER SEQUENCE mae_vehiculo_id_vehiculo_seq RESTART WITH 1;
ALTER SEQUENCE mae_producto_id_producto_seq RESTART WITH 1;
ALTER SEQUENCE mae_forma_pago_id_forma_pago_seq RESTART WITH 1;
ALTER SEQUENCE mae_moneda_id_moneda_seq RESTART WITH 1;
ALTER SEQUENCE trs_encabezado_documento_id_documento_seq RESTART WITH 1;
ALTER SEQUENCE trs_detalle_documento_id_detalle_seq RESTART WITH 1;
ALTER SEQUENCE trs_encabezado_guia_id_guia_seq RESTART WITH 1;
ALTER SEQUENCE trs_detalle_guia_id_detalle_guia_seq RESTART WITH 1;

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

INSERT INTO mae_empresa (nombre, razon_social, RUC, id_ubicacion) VALUES
('LIBRERIA DISTRIBUIDORA ANILU S.R.L.', 'LIBRERIA DISTRIBUIDORA ANILU S.R.L.', '20600026748', 1);

INSERT INTO mae_conductor (nombre, n_licencia) VALUES
('Juan Perez', 'B12345678123'),
('Marcos Rojas', 'B87654321123'),
('Daniel Lopez', 'B13579246123'),
('Jose Aguilar', 'B24681357123'),
('Ricardo Castillo', 'B99887766123');

INSERT INTO mae_vehiculo (descripcion, placa) VALUES
('Camioneta Toyota Hilux Blanca', 'ABC-123'),
('Furgon Hyundai H1 Gris', 'XYZ-456'),
('Camion Mitsubishi Canter', 'KLM-789'),
('Motocicleta Honda Cargo', 'HND-321'),
('Camioneta Nissan Frontier Roja', 'NSN-654');

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

INSERT INTO mae_forma_pago (nombre, descripcion) VALUES
('Efectivo', 'Pago en moneda fisica'),
('Tarjeta de Credito', 'Pago con tarjeta VISA o MasterCard'),
('Transferencia Bancaria', 'Deposito o transferencia en cuenta'),
('Yape', 'Pago digital mediante aplicativo Yape'),
('Plin', 'Pago digital mediante aplicativo Plin');

INSERT INTO mae_moneda (codigo_iso, nombre) VALUES
('PEN', 'Soles'),
('USD', 'Dolares');

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

INSERT INTO trs_encabezado_guia (id_doc_venta, nro_guia, fecha_emision, fecha_inicio_traslado, motivo_traslado, direccion_partida, direccion_llegada, id_conductor, id_vehiculo) VALUES
(2, 'GR-0001', '2025-10-02', '2025-10-02', 'Entrega de material educativo', 'Avenida San Martin 507', 'Calle Mariano Santos 315', 1, 1),
(4, 'GR-0002', '2025-10-02', '2025-10-03', 'Reparto de libros a institucion educativa', 'Avenida Bolognesi 312', 'Calle Cajamarca 188', 2, 2),
(7, 'GR-0003', '2025-10-05', '2025-10-06', 'Despacho de productos a sucursal', 'Avenida Coronel Mendoza 210', 'Pasaje Las Bugambillas 89', 3, 3),
(9, 'GR-0004', '2025-10-06', '2025-10-07', 'Entrega a cliente corporativo', 'Avenida 28 de Agosto 356', 'Calle Francisco Laso 221', 4, 1),
(10, 'GR-0005', '2025-10-07', '2025-10-07', 'Envio de utiles escolares', 'Calle Alto Lima 134', 'Avenida Justo Arias Araquez 189', 5, 2);

INSERT INTO trs_detalle_guia (id_guia, id_producto, descripcion, unidad_medida, unidad_peso_bruto, peso_total_carga, modalidad_trans, transbordo_prog, categoriaM1_L, retorno_envases, vehiculo_vacio, id_conductor, id_vehiculo) VALUES
(1, 2, 'Lapiceros BIC', 'UND', 'KG', 2.5, 'Privado', 'NO', 'M1', 'NO', 'NO', 1, 1),
(1, 7, 'Resaltadores Amarillos', 'UND', 'KG', 0.8, 'Privado', 'NO', 'M1', 'NO', 'NO', 1, 1),
(2, 5, 'Reglas Plasticas', 'UND', 'KG', 3.2, 'Privado', 'NO', 'M1', 'NO', 'NO', 2, 2),
(3, 8, 'Temperas Escolares', 'UND', 'KG', 1.5, 'Privado', 'NO', 'M1', 'NO', 'NO', 3, 3),
(3, 9, 'Correctores Liquidos', 'UND', 'KG', 5.0, 'Privado', 'NO', 'M1', 'NO', 'NO', 3, 3),
(4, 5, 'Reglas 30 cm', 'UND', 'KG', 4.5, 'Privado', 'NO', 'M1', 'NO', 'NO', 4, 1),
(5, 1, 'Cuadernos A4', 'UND', 'KG', 0.5, 'Privado', 'NO', 'M1', 'NO', 'NO', 5, 2),
(5, 6, 'Cartulinas Blancas', 'UND', 'KG', 2.0, 'Privado', 'NO', 'M1', 'NO', 'NO', 5, 2);