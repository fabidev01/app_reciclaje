-- Insertar datos en Rol
INSERT INTO Rol (nombre, descripcion) VALUES
('Administrador', 'Gestiona todo el sistema'),
('Usuario Regular', 'Recicla y canjea puntos'),
('Moderador', 'Gestiona puntos y recompensas'),
('Auditor', 'Revisa bitácoras y accesos'),
('Soporte', 'Asiste a usuarios');

-- Insertar datos en Permiso
INSERT INTO Permiso (nombre) VALUES
('Crear Recompensa'),
('Eliminar Recompensa'),
('Gestionar Puntos'),
('Gestionar Usuarios'),
('Gestionar Donaciones');

-- Insertar datos en Rol_Permiso
INSERT INTO Rol_Permiso (id_rol, id_permiso) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),  
(2, 3),  
(3, 3), (3, 1), (3, 2), 
(4, 4); 

-- Insertar datos en Usuario
INSERT INTO Usuario (nombre, correo, telefono, balance_puntos, fecha_registro, contraseña, ip, id_rol) VALUES
('Administrador', 'admin@gmail.com', '77712345', 100, STR_TO_DATE('01/03/2025', '%d/%m/%Y'), '123', '192.168.1.1', 1),
('Ana Quispe', 'ana.quispe@gmail.com', '66654321', 50, STR_TO_DATE('02/03/2025', '%d/%m/%Y'), '123', '192.168.1.2', 2),
('Pedro Vargas', 'pedro.vargas@gmail.com', '77765432', 200, STR_TO_DATE('03/03/2025', '%d/%m/%Y'), '123', '192.168.1.3', 2),
('María Rojas', 'maria.rojas@gmail.com', '66612345', 80, STR_TO_DATE('04/03/2025', '%d/%m/%Y'), '123', '192.168.1.4', 3),
('Carlos Mamani', 'carlos.mamani@gmail.com', '77798765', 150, STR_TO_DATE('05/03/2025', '%d/%m/%Y'), '123', '192.168.1.5', 4);

-- Insertar datos en Material_Reciclable
INSERT INTO Material_Reciclable (nombre, puntos_por_unidad, co2_por_unidad, unidad_medida) VALUES
('Plástico', 10, 0.5, 'kg'),
('Papel', 5, 0.2, 'kg'),
('Vidrio', 15, 0.8, 'kg'),
('Metal', 20, 1.0, 'kg'),
('Cartón', 8, 0.3, 'kg'),
('Orgánico', 3, 0.1, 'kg'),
('Electrónico', 50, 2.5, 'kg');

-- Insertar datos en Punto_Reciclaje
INSERT INTO Punto_Reciclaje (nombre, capacidad_maxima, hora_apertura, hora_cierre, latitud, longitud, estado_punto) VALUES
('Punto Central', 1000, '08:00:00', '18:00:00', -17.3833, -66.1568, 'Disponible'),
('Punto Norte', 800, '09:00:00', '17:00:00', -17.3667, -66.1333, 'Disponible'),
('Punto Sur', 1200, '07:00:00', '19:00:00', -17.4000, -66.1667, 'Disponible'),
('Punto Este', 900, '08:30:00', '17:30:00', -17.3667, -66.1167, 'Disponible'),
('Punto Oeste', 700, '09:00:00', '18:00:00', -17.3667, -66.1833, 'Disponible'),
('Punto Rural 1', 500, '08:00:00', '16:00:00', -17.4333, -66.1500, 'Mantenimiento'),
('Punto Rural 2', 600, '07:30:00', '17:30:00', -17.4167, -66.1667, 'Cerrado'),
('Punto Urbano', 1100, '08:00:00', '18:00:00', -17.3833, -66.1333, 'Mantenimiento');

-- Insertar datos en Material_Punto_Reciclaje
INSERT INTO Material_Punto_Reciclaje (id_material_reciclable, id_punto_reciclaje, condiciones_especificas) VALUES
(1, 1, 'Limpiar antes de depositar'),
(2, 1, NULL),
(3, 2, 'Solo envases'),
(4, 3, NULL),
(5, 4, 'Sin humedad'),
(6, 5, NULL),
(7, 6, 'Desarmar componentes'),
(1, 7, NULL),
(2, 8, 'Sin grapas');

-- Insertar datos en Registro_Reciclaje
INSERT INTO Registro_Reciclaje (id_usuario, id_punto_reciclaje, id_material_reciclable, cantidad_kg, puntos_obtenidos, co2_reducido, fecha_registro, nombre_subtipo) VALUES
(2, 1, 1, 2.0, 20, 1.0, STR_TO_DATE('01/03/2025', '%d/%m/%Y'), 'Botellas de plástico'),
(2, 2, 2, 1.5, 7.5, 0.3, STR_TO_DATE('02/03/2025', '%d/%m/%Y'), 'Papel de oficina'),
(3, 3, 3, 3.0, 45, 2.4, STR_TO_DATE('03/03/2025', '%d/%m/%Y'), 'Botellas de vidrio'),
(4, 4, 4, 1.0, 20, 1.0, STR_TO_DATE('04/03/2025', '%d/%m/%Y'), 'Latas de aluminio'),
(5, 5, 5, 2.5, 20, 0.75, STR_TO_DATE('05/03/2025', '%d/%m/%Y'), 'Cajas de cartón');

-- Insertar datos en Catalogo_Recompensa
INSERT INTO Catalogo_Recompensa (nombre, puntos_coste, disponible, stock, descuento, categoria, ruta_imagen) VALUES
('Descuento 10%', 50, TRUE, 100, 10.0, 'Descuento', 'img/catalogo/img-1.png'),
('Planta Ecológica', 30, TRUE, 50, 0.0, 'Producto', 'img/catalogo/img-2.png'),
('Bolsa Reutilizable', 20, TRUE, 200, 0.0, 'Producto', 'img/catalogo/img-3.png'),
('Donación Árbol', 100, TRUE, 30, 0.0, 'Donación', 'img/catalogo/img-4.png'),
('Cupón 5%', 40, TRUE, 150, 5.0, 'Descuento', 'img/catalogo/img-5.png');

-- Insertar datos en Donacion
INSERT INTO Donacion (nombre, entidad_donacion, monto_donacion, ruta_imagen) VALUES
('Donación Escolar', 'Fundación Educativa', 50.0, 'img/donacion/img-1.png'),
('Donación Médica', 'Cruz Roja', 100.0, 'img/donacion/img-2.png'),
('Donación Ambiental', 'Green Earth', 75.0, 'img/donacion/img-3.png'),
('Donación Comida', 'Banco de Alimentos', 60.0, 'img/donacion/img-4.png'),
('Donación Infraestructura', 'Municipio Cochabamba', 200.0, 'img/donacion/img-5.png');

-- Insertar datos en Canje_Recompensa
INSERT INTO Canje_Recompensa (id_usuario, id_catalogo_recompensa, estado, fecha_canje, puntos_descontados) VALUES
(2, 1, 'Completado', STR_TO_DATE('01/03/2025', '%d/%m/%Y'), 50),
(2, 2, 'Pendiente', STR_TO_DATE('02/03/2025', '%d/%m/%Y'), 30),
(3, 3, 'Completado', STR_TO_DATE('03/03/2025', '%d/%m/%Y'), 20),
(4, 4, 'Pendiente', STR_TO_DATE('04/03/2025', '%d/%m/%Y'), 100),
(5, 5, 'Completado', STR_TO_DATE('05/03/2025', '%d/%m/%Y'), 40);

-- Insertar datos en Canje_Donacion
INSERT INTO Canje_Donacion (id_usuario, id_donacion, estado, fecha_canje, puntos_descontados) VALUES
(2, 1, 'Completado', STR_TO_DATE('01/03/2025', '%d/%m/%Y'), 50),
(2, 2, 'Pendiente', STR_TO_DATE('02/03/2025', '%d/%m/%Y'), 100),
(3, 3, 'Completado', STR_TO_DATE('03/03/2025', '%d/%m/%Y'), 75),
(4, 4, 'Pendiente', STR_TO_DATE('04/03/2025', '%d/%m/%Y'), 60),
(5, 5, 'Completado', STR_TO_DATE('05/03/2025', '%d/%m/%Y'), 200);

-- Insertar datos en Bitacora_Acceso
INSERT INTO Bitacora_Acceso (id_usuario, tipo_acceso, fecha_acceso, resultado, detalle) VALUES
(1, 'Inicio', STR_TO_DATE('01/03/2025 08:00:00', '%d/%m/%Y %H:%i:%s'), 'Éxito', 'Intento de login para luis.morales@email.com: Inicio de sesión exitoso'),
(2, 'Inicio', STR_TO_DATE('02/03/2025 08:00:00', '%d/%m/%Y %H:%i:%s'), 'Fallido', 'Intento de login para ana.quispe@email.com: Credenciales incorrectas'),
(3, 'Inicio', STR_TO_DATE('03/03/2025 08:00:00', '%d/%m/%Y %H:%i:%s'), 'Éxito', 'Intento de login para pedro.vargas@email.com: Inicio de sesión exitoso'),
(NULL, 'Inicio', STR_TO_DATE('04/03/2025 08:00:00', '%d/%m/%Y %H:%i:%s'), 'Fallido', 'Intento de login para usuario.inexistente@email.com: Credenciales incorrectas'),
(5, 'Inicio', STR_TO_DATE('05/03/2025 09:00:00', '%d/%m/%Y %H:%i:%s'), 'Éxito', 'Intento de login para carlos.mamani@email.com: Inicio de sesión exitoso');

-- Insertar datos en Bitacora_Catalogo
INSERT INTO Bitacora_Catalogo (ip, id_catalogo_recompensa, accion, fecha_accion, detalle) VALUES
('192.168.1.1', 1, 'INSERT', STR_TO_DATE('01/03/2025 08:00:00', '%d/%m/%Y %H:%i:%s'), 'Recompensa creada'),
('192.168.1.2', 2, 'UPDATE', STR_TO_DATE('02/03/2025 08:00:00', '%d/%m/%Y %H:%i:%s'), 'Stock actualizado'),
('192.168.1.3', 3, 'DELETE', STR_TO_DATE('03/03/2025 08:00:00', '%d/%m/%Y %H:%i:%s'), 'Recompensa eliminada'),
('192.168.1.4', 4, 'INSERT', STR_TO_DATE('04/03/2025 08:00:00', '%d/%m/%Y %H:%i:%s'), 'Nueva recompensa'),
('192.168.1.5', 5, 'UPDATE', STR_TO_DATE('05/03/2025 08:00:00', '%d/%m/%Y %H:%i:%s'), 'Descuento modificado');


-- Insertar datos en Bitacora_Reciclaje
INSERT INTO Bitacora_Reciclaje (ip, id_registro_reciclaje, accion, fecha_accion, detalle) VALUES
('192.168.1.1', 1, 'UPDATE', STR_TO_DATE('01/03/2025 08:00:00', '%d/%m/%Y %H:%i:%s'), 'Cantidad modificada'),
('192.168.1.2', 2, 'DELETE', STR_TO_DATE('02/03/2025 08:00:00', '%d/%m/%Y %H:%i:%s'), 'Registro eliminado'),
('192.168.1.3', 3, 'UPDATE', STR_TO_DATE('03/03/2025 08:00:00', '%d/%m/%Y %H:%i:%s'), 'Subtipo cambiado'),
('192.168.1.4', 4, 'DELETE', STR_TO_DATE('04/03/2025 08:00:00', '%d/%m/%Y %H:%i:%s'), 'Registro eliminado'),
('192.168.1.5', 5, 'UPDATE', STR_TO_DATE('05/03/2025 08:00:00', '%d/%m/%Y %H:%i:%s'), 'Cantidad ajustada');

-- Insertar datos en Bitacora_Canje
INSERT INTO Bitacora_Canje (ip, id_canje_recompensa, id_catalogo_recompensa, accion, fecha_accion, detalle) VALUES
('192.168.1.1', 1, 1, 'UPDATE', STR_TO_DATE('01/03/2025 08:00:00', '%d/%m/%Y %H:%i:%s'), 'Estado cambiado'),
('192.168.1.2', 2, 2, 'DELETE', STR_TO_DATE('02/03/2025 08:00:00', '%d/%m/%Y %H:%i:%s'), 'Canje eliminado'),
('192.168.1.3', 3, 3, 'UPDATE', STR_TO_DATE('03/03/2025 08:00:00', '%d/%m/%Y %H:%i:%s'), 'Puntos ajustados'),
('192.168.1.4', 4, 4, 'DELETE', STR_TO_DATE('04/03/2025 08:00:00', '%d/%m/%Y %H:%i:%s'), 'Canje eliminado'),
('192.168.1.5', 5, 5, 'UPDATE', STR_TO_DATE('05/03/2025 08:00:00', '%d/%m/%Y %H:%i:%s'), 'Estado modificado');


INSERT INTO Impacto_Ambiental_Diario (fecha_dia, tipo_basura, unidad_medida, cantidad_reciclada_por_tipo, co2_reducido_por_tipo) VALUES
(STR_TO_DATE('01/03/2025', '%d/%m/%Y'), 'Plástico', 'kg', 2.0, 1.0),
(STR_TO_DATE('02/03/2025', '%d/%m/%Y'), 'Metal', 'kg', 1.5, 0.3),
(STR_TO_DATE('03/03/2025', '%d/%m/%Y'), 'Vidrio', 'kg', 3.0, 2.4),
(STR_TO_DATE('04/03/2025', '%d/%m/%Y'), 'Papel', 'kg', 1.0, 1.0),
(STR_TO_DATE('05/03/2025', '%d/%m/%Y'), 'Cartón', 'kg', 2.5, 0.75);