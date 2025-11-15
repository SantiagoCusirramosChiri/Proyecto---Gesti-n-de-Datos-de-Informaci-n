USE sistema_documentos;

-- 1️⃣ Insertar ubicaciones
INSERT INTO mae_ubicacion (descripcion) VALUES
('Avenida San Martín 507'),
('Avenida Bolognesi 312'),
('Avenida Coronel Mendoza 210'),
('Avenida Gustavo Pinto 459'),
('Avenida Justo Arias Aragüez 189'),
('Avenida 28 de Agosto 356'),
('Avenida Hoyos Rubio 202'),
('Calle Alto Lima 134'),
('Calle Francisco Laso 221'),
('Pasaje Las Bugambillas 89');

-- 2️⃣ Insertar identidades
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

-- 3️⃣ Insertar clientes
INSERT INTO mae_cliente (nombre, apellido, id_ubicacion, id_identidad) VALUES
('Carlos', 'Ramírez', 1, 1),
('María', 'Torres', 2, 2),
('Luis', 'Gómez', 3, 3),
('Ana', 'Quispe', 4, 4),
('Jorge', 'Mamani', 5, 5),
('Rosa', 'Paredes', 6, 6),
('Pedro', 'Huanca', 7, 7),
('Lucía', 'Flores', 8, 8),
('Miguel', 'Valdez', 9, 9),
('Carmen', 'Chávez', 10, 10);

-- 4️⃣ Insertar empresas
INSERT INTO mae_empresa (nombre, razon_social, RUC, id_ubicacion) VALUES
('LIBRERÍA DISTRIBUIDORA ANILU S.R.L.', 'LIBRERÍA DISTRIBUIDORA ANILU S.R.L.', '20600026748', 1);

-- 5️⃣ Insertar conductores
INSERT INTO mae_conductor (nombre, n_licencia) VALUES
('Juan Pérez', 'B12345678'),
('Marcos Rojas', 'B87654321'),
('Daniel López', 'B13579246'),
('José Aguilar', 'B24681357'),
('Ricardo Castillo', 'B99887766');

-- 6️⃣ Insertar vehículos
INSERT INTO mae_vehiculo (descripcion, placa) VALUES
('Camioneta Toyota Hilux Blanca', 'ABC-123'),
('Furgón Hyundai H1 Gris', 'XYZ-456'),
('Camión Mitsubishi Canter', 'KLM-789'),
('Motocicleta Honda Cargo', 'HND-321'),
('Camioneta Nissan Frontier Roja', 'NSN-654');

-- 7️⃣ Insertar productos
INSERT INTO mae_producto (nombre, descripcion, precio_base, stock, unidad_medida) VALUES
('Cuaderno College 100 hojas', 'Cuaderno A4 de 100 hojas, marca Justus', 8.50, 120, 'UND'),
('Lapicero BIC Azul', 'Lapicero azul punta fina', 1.50, 500, 'UND'),
('Borrador Pelikan', 'Borrador blanco para lápiz', 2.00, 200, 'UND'),
('Tajador Maped', 'Tajador doble con depósito', 3.50, 150, 'UND'),
('Regla 30 cm Arti', 'Regla plástica transparente', 2.50, 300, 'UND'),
('Cartulina Duplex', 'Cartulina tamaño A3 color blanco', 1.80, 400, 'UND'),
('Resaltador Stabilo Amarillo', 'Resaltador color amarillo', 3.00, 250, 'UND'),
('Témpera Vinifan 6 colores', 'Set de témperas escolares', 10.00, 100, 'UND'),
('Corrector Líquido Pelikan', 'Corrector blanco con brocha', 4.50, 180, 'UND'),
('Folder Manila A4', 'Folder tamaño A4 color manila', 1.20, 350, 'UND');

-- 8️⃣ Insertar formas de pago
INSERT INTO mae_forma_pago (nombre, descripcion) VALUES
('Efectivo', 'Pago en moneda física'),
('Tarjeta de Crédito', 'Pago con tarjeta VISA o MasterCard'),
('Transferencia Bancaria', 'Depósito o transferencia en cuenta'),
('Yape', 'Pago digital mediante aplicativo Yape'),
('Plin', 'Pago digital mediante aplicativo Plin');

-- 9️⃣ Insertar monedas
INSERT INTO mae_moneda (codigo_iso, nombre) VALUES
('PEN', 'Soles'),
('USD', 'Dólares');

--  🔟 Insertar encabezados de documentos
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

-- 1️⃣1️⃣ Insertar detalle de documentos (precio_producto → precio_unitario)
INSERT INTO trs_detalle_documento (id_documento, id_producto, cantidad) VALUES
(1, 1, 2),
(1, 3, 4),
(2, 2, 5),
(2, 7, 3),
(3, 4, 5),
(4, 5, 4),
(4, 9, 2),
(5, 6, 10),
(5, 8, 2),
(6, 1, 1),
(6, 10, 5),
(7, 7, 5),
(7, 8, 1),
(8, 3, 2),
(8, 2, 4),
(9, 5, 4),
(9, 4, 3),
(10, 1, 3),
(10, 6, 2);

-- 1️⃣2️⃣ Insertar encabezado de guías
INSERT INTO trs_encabezado_guia (id_doc_venta, nro_guia, fecha_emision, fecha_inicio_traslado, motivo_traslado, direccion_partida, direccion_llegada, id_conductor, id_vehiculo) VALUES
(2, 'GR-0001', '2025-10-02', '2025-10-02', 'Entrega de material educativo', 'Avenida San Martín 507', 'Calle Mariano Santos 315', 1, 1),
(4, 'GR-0002', '2025-10-02', '2025-10-03', 'Reparto de libros a institución educativa', 'Avenida Bolognesi 312', 'Calle Cajamarca 188', 2, 2),
(7, 'GR-0003', '2025-10-05', '2025-10-06', 'Despacho de productos a sucursal', 'Avenida Coronel Mendoza 210', 'Pasaje Las Bugambillas 89', 3, 3),
(9, 'GR-0004', '2025-10-06', '2025-10-07', 'Entrega a cliente corporativo', 'Avenida 28 de Agosto 356', 'Calle Francisco Laso 221', 4, 1),
(10, 'GR-0005', '2025-10-07', '2025-10-07', 'Envío de útiles escolares', 'Calle Alto Lima 134', 'Avenida Justo Arias Aragüez 189', 5, 2);

-- 1️⃣3️⃣ Insertar detalle de guías
INSERT INTO trs_detalle_guia (id_guia, id_producto, descripcion, unidad_medida, unidad_peso_bruto, peso_total_carga, modalidad_trans, transbordo_prog, categoriaM1_L, retorno_envases, vehiculo_vacio, id_conductor, id_vehiculo) VALUES
(1, 2, 'Lapiceros BIC', 'UND', 'KG', 2.5, 'Privado', 'NO', 'M1', 'NO', 'NO', 1, 1),
(1, 7, 'Resaltadores Amarillos', 'UND', 'KG', 0.8, 'Privado', 'NO', 'M1', 'NO', 'NO', 1, 1),
(2, 5, 'Reglas Plásticas', 'UND', 'KG', 3.2, 'Privado', 'NO', 'M1', 'NO', 'NO', 2, 2),
(3, 8, 'Témperas Escolares', 'UND', 'KG', 1.5, 'Privado', 'NO', 'M1', 'NO', 'NO', 3, 3),
(3, 9, 'Correctores Líquidos', 'UND', 'KG', 5.0, 'Privado', 'NO', 'M1', 'NO', 'NO', 3, 3),
(4, 5, 'Reglas 30 cm', 'UND', 'KG', 4.5, 'Privado', 'NO', 'M1', 'NO', 'NO', 4, 1),
(5, 1, 'Cuadernos A4', 'UND', 'KG', 0.5, 'Privado', 'NO', 'M1', 'NO', 'NO', 5, 2),
(5, 6, 'Cartulinas Blancas', 'UND', 'KG', 2.0, 'Privado', 'NO', 'M1', 'NO', 'NO', 5, 2);
