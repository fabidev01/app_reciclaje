 -- insertar 50 usuarios
 INSERT INTO Usuario (nombre, correo, telefono, balance_puntos, fecha_registro, contraseña, ip, id_rol) VALUES
('Luis Morales', 'luis.morales@gmail.com', '77711122', 120, STR_TO_DATE('06/03/2025', '%d/%m/%Y'), '123', '192.168.1.6', 2),
('Sofía Pérez', 'sofia.perez@gmail.com', '66622233', 90, STR_TO_DATE('07/03/2025', '%d/%m/%Y'), '123', '192.168.1.7', 2),
('Juan Torres', 'juan.torres@gmail.com', '77733344', 160, STR_TO_DATE('08/03/2025', '%d/%m/%Y'), '123', '192.168.1.8', 3),
('Elena Gómez', 'elena.gomez@gmail.com', '66644455', 70, STR_TO_DATE('09/03/2025', '%d/%m/%Y'), '123', '192.168.1.9', 4),
('Carlos López', 'carlos.lopez@gmail.com', '77755566', 200, STR_TO_DATE('10/03/2025', '%d/%m/%Y'), '123', '192.168.1.10', 2),
('María Sánchez', 'maria.sanchez@gmail.com', '66666677', 85, STR_TO_DATE('11/03/2025', '%d/%m/%Y'), '123', '192.168.1.11', 2),
('Pedro Ramírez', 'pedro.ramirez@gmail.com', '77777788', 140, STR_TO_DATE('12/03/2025', '%d/%m/%Y'), '123', '192.168.1.12', 3),
('Ana Martínez', 'ana.martinez@gmail.com', '66688899', 110, STR_TO_DATE('13/03/2025', '%d/%m/%Y'), '123', '192.168.1.13', 2),
('Jorge Castillo', 'jorge.castillo@gmail.com', '77799900', 95, STR_TO_DATE('14/03/2025', '%d/%m/%Y'), '123', '192.168.1.14', 4),
('Lucía Fernández', 'lucia.fernandez@gmail.com', '66600011', 175, STR_TO_DATE('15/03/2025', '%d/%m/%Y'), '123', '192.168.1.15', 2),
('Diego Rojas', 'diego.rojas@gmail.com', '77711133', 130, STR_TO_DATE('16/03/2025', '%d/%m/%Y'), '123', '192.168.1.16', 3),
('Paula Guzmán', 'paula.guzman@gmail.com', '66622244', 60, STR_TO_DATE('17/03/2025', '%d/%m/%Y'), '123', '192.168.1.17', 2),
('Ricardo Pérez', 'ricardo.perez@gmail.com', '77733355', 150, STR_TO_DATE('18/03/2025', '%d/%m/%Y'), '123', '192.168.1.18', 2),
('Carolina López', 'carolina.lopez@gmail.com', '66644466', 80, STR_TO_DATE('19/03/2025', '%d/%m/%Y'), '123', '192.168.1.19', 4),
('Héctor Morales', 'hector.morales@gmail.com', '77755577', 190, STR_TO_DATE('20/03/2025', '%d/%m/%Y'), '123', '192.168.1.20', 2),
('Valeria Torres', 'valeria.torres@gmail.com', '66666688', 100, STR_TO_DATE('21/03/2025', '%d/%m/%Y'), '123', '192.168.1.21', 3),
('Gabriel Gómez', 'gabriel.gomez@gmail.com', '77777799', 125, STR_TO_DATE('22/03/2025', '%d/%m/%Y'), '123', '192.168.1.22', 2),
('Isabel Sánchez', 'isabel.sanchez@gmail.com', '66688800', 70, STR_TO_DATE('23/03/2025', '%d/%m/%Y'), '123', '192.168.1.23', 4),
('Fernando Castillo', 'fernando.castillo@gmail.com', '77799911', 160, STR_TO_DATE('24/03/2025', '%d/%m/%Y'), '123', '192.168.1.24', 2),
('Beatriz Fernández', 'beatriz.fernandez@gmail.com', '66600022', 90, STR_TO_DATE('25/03/2025', '%d/%m/%Y'), '123', '192.168.1.25', 3),
('Oscar Rojas', 'oscar.rojas@gmail.com', '77711144', 140, STR_TO_DATE('26/03/2025', '%d/%m/%Y'), '123', '192.168.1.26', 2),
('Silvia Guzmán', 'silvia.guzman@gmail.com', '66622255', 110, STR_TO_DATE('27/03/2025', '%d/%m/%Y'), '123', '192.168.1.27', 4),
('Raúl Pérez', 'raul.perez@gmail.com', '77733366', 85, STR_TO_DATE('28/03/2025', '%d/%m/%Y'), '123', '192.168.1.28', 2),
('Teresa López', 'teresa.lopez@gmail.com', '66644477', 170, STR_TO_DATE('29/03/2025', '%d/%m/%Y'), '123', '192.168.1.29', 3),
('Víctor Morales', 'victor.morales@gmail.com', '77755588', 95, STR_TO_DATE('30/03/2025', '%d/%m/%Y'), '123', '192.168.1.30', 2),
('Laura Torres', 'laura.torres@gmail.com', '66666699', 130, STR_TO_DATE('31/03/2025', '%d/%m/%Y'), '123', '192.168.1.31', 4),
('Miguel Gómez', 'miguel.gomez@gmail.com', '77777700', 75, STR_TO_DATE('01/04/2025', '%d/%m/%Y'), '123', '192.168.1.32', 2),
('Patricia Sánchez', 'patricia.sanchez@gmail.com', '66688811', 150, STR_TO_DATE('02/04/2025', '%d/%m/%Y'), '123', '192.168.1.33', 3),
('Javier Castillo', 'javier.castillo@gmail.com', '77799922', 110, STR_TO_DATE('03/04/2025', '%d/%m/%Y'), '123', '192.168.1.34', 2),
('Rosa Fernández', 'rosa.fernandez@gmail.com', '66600033', 180, STR_TO_DATE('04/04/2025', '%d/%m/%Y'), '123', '192.168.1.35', 4),
('Eduardo Rojas', 'eduardo.rojas@gmail.com', '77711155', 90, STR_TO_DATE('05/04/2025', '%d/%m/%Y'), '123', '192.168.1.36', 2),
('Clara Guzmán', 'clara.guzman@gmail.com', '66622266', 140, STR_TO_DATE('06/04/2025', '%d/%m/%Y'), '123', '192.168.1.37', 3),
('Andrés Pérez', 'andres.perez@gmail.com', '77733377', 65, STR_TO_DATE('07/04/2025', '%d/%m/%Y'), '123', '192.168.1.38', 2),
('Monica López', 'monica.lopez@gmail.com', '66644488', 160, STR_TO_DATE('08/04/2025', '%d/%m/%Y'), '123', '192.168.1.39', 4),
('Hugo Morales', 'hugo.morales@gmail.com', '77755599', 105, STR_TO_DATE('09/04/2025', '%d/%m/%Y'), '123', '192.168.1.40', 2),
('Natalia Torres', 'natalia.torres@gmail.com', '66666600', 135, STR_TO_DATE('10/04/2025', '%d/%m/%Y'), '123', '192.168.1.41', 3),
('Pablo Gómez', 'pablo.gomez@gmail.com', '77777711', 80, STR_TO_DATE('11/04/2025', '%d/%m/%Y'), '123', '192.168.1.42', 2),
('Sandra Sánchez', 'sandra.sanchez@gmail.com', '66688822', 150, STR_TO_DATE('12/04/2025', '%d/%m/%Y'), '123', '192.168.1.43', 4),
('Rafael Castillo', 'rafael.castillo@gmail.com', '77799933', 95, STR_TO_DATE('13/04/2025', '%d/%m/%Y'), '123', '192.168.1.44', 2),
('Liliana Fernández', 'liliana.fernandez@gmail.com', '66600044', 170, STR_TO_DATE('14/04/2025', '%d/%m/%Y'), '123', '192.168.1.45', 3),
('Gustavo Rojas', 'gustavo.rojas@gmail.com', '77711166', 100, STR_TO_DATE('15/04/2025', '%d/%m/%Y'), '123', '192.168.1.46', 2),
('Yolanda Guzmán', 'yolanda.guzman@gmail.com', '66622277', 130, STR_TO_DATE('16/04/2025', '%d/%m/%Y'), '123', '192.168.1.47', 4),
('Felipe Pérez', 'felipe.perez@gmail.com', '77733388', 75, STR_TO_DATE('17/04/2025', '%d/%m/%Y'), '123', '192.168.1.48', 2),
('Carmen López', 'carmen.lopez@gmail.com', '66644499', 160, STR_TO_DATE('18/04/2025', '%d/%m/%Y'), '123', '192.168.1.49', 3),
('Alberto Morales', 'alberto.morales@gmail.com', '77755500', 90, STR_TO_DATE('19/04/2025', '%d/%m/%Y'), '123', '192.168.1.50', 2),
('Julia Torres', 'julia.torres@gmail.com', '66666611', 140, STR_TO_DATE('20/04/2025', '%d/%m/%Y'), '123', '192.168.1.51', 4),
('Enrique Gómez', 'enrique.gomez@gmail.com', '77777722', 110, STR_TO_DATE('21/04/2025', '%d/%m/%Y'), '123', '192.168.1.52', 2),
('Lucía Sánchez', 'lucia.sanchez@gmail.com', '66688833', 85, STR_TO_DATE('22/04/2025', '%d/%m/%Y'), '123', '192.168.1.53', 3),
('Mario Castillo', 'mario.castillo@gmail.com', '77799944', 170, STR_TO_DATE('23/04/2025', '%d/%m/%Y'), '123', '192.168.1.54', 2),
('Sofía Fernández', 'sofia.fernandez@gmail.com', '66600055', 95, STR_TO_DATE('24/04/2025', '%d/%m/%Y'), '123', '192.168.1.55', 4);
-- registros reciclajes
INSERT INTO Registro_Reciclaje (id_usuario, id_punto_reciclaje, id_material_reciclable, cantidad_kg, puntos_obtenidos, co2_reducido, fecha_registro, nombre_subtipo) VALUES
(2, 1, 1, 2.0, 20, 1.0, STR_TO_DATE('01/03/2025', '%d/%m/%Y'), 'Botellas de plástico'),
(2, 2, 2, 1.5, 7.5, 0.3, STR_TO_DATE('02/03/2025', '%d/%m/%Y'), 'Papel de oficina'),
(3, 3, 3, 3.0, 45, 2.4, STR_TO_DATE('03/03/2025', '%d/%m/%Y'), 'Botellas de vidrio'),
(3, 4, 4, 1.0, 20, 1.0, STR_TO_DATE('04/03/2025', '%d/%m/%Y'), 'Latas de aluminio'),
(3, 5, 5, 2.5, 20, 0.75, STR_TO_DATE('05/03/2025', '%d/%m/%Y'), 'Cajas de cartón'),
(6, 1, 1, 1.5, 15, 0.75, STR_TO_DATE('06/03/2025', '%d/%m/%Y'), 'Botellas PET'),
(6, 2, 2, 2.0, 10, 0.4, STR_TO_DATE('07/03/2025', '%d/%m/%Y'), 'Papel blanco'),
(10, 3, 3, 2.5, 37.5, 2.0, STR_TO_DATE('08/03/2025', '%d/%m/%Y'), 'Frascos vidrio'),
(10, 4, 4, 1.0, 20, 1.0, STR_TO_DATE('09/03/2025', '%d/%m/%Y'), 'Latas aluminio'),
(10, 5, 5, 3.0, 24, 0.9, STR_TO_DATE('10/03/2025', '%d/%m/%Y'), 'Cajas cartón'),
(13, 1, 6, 1.5, 4.5, 0.15, STR_TO_DATE('11/03/2025', '%d/%m/%Y'), 'Residuos orgánicos'),
(13, 2, 7, 0.5, 25, 1.25, STR_TO_DATE('12/03/2025', '%d/%m/%Y'), 'Teléfonos'),
(15, 3, 1, 2.0, 20, 1.0, STR_TO_DATE('13/03/2025', '%d/%m/%Y'), 'Envases plástico'),
(15, 4, 2, 1.8, 9, 0.36, STR_TO_DATE('14/03/2025', '%d/%m/%Y'), 'Periódicos'),
(20, 5, 3, 2.2, 33, 1.76, STR_TO_DATE('15/03/2025', '%d/%m/%Y'), 'Botellas vidrio'),
(20, 1, 4, 1.2, 24, 1.2, STR_TO_DATE('16/03/2025', '%d/%m/%Y'), 'Latas metal'),
(20, 2, 5, 2.5, 20, 0.75, STR_TO_DATE('17/03/2025', '%d/%m/%Y'), 'Cajas corrugadas'),
(6, 3, 6, 1.0, 3, 0.1, STR_TO_DATE('18/03/2025', '%d/%m/%Y'), 'Restos orgánicos'),
(6, 4, 7, 0.8, 40, 2.0, STR_TO_DATE('19/03/2025', '%d/%m/%Y'), 'Computadoras'),
(10, 5, 1, 1.7, 17, 0.85, STR_TO_DATE('20/03/2025', '%d/%m/%Y'), 'Bolsas plástico'),
(10, 1, 2, 2.3, 11.5, 0.46, STR_TO_DATE('21/03/2025', '%d/%m/%Y'), 'Papel reciclado'),
(13, 2, 3, 2.8, 42, 2.24, STR_TO_DATE('22/03/2025', '%d/%m/%Y'), 'Frascos vidrio'),
(13, 3, 4, 1.1, 22, 1.1, STR_TO_DATE('23/03/2025', '%d/%m/%Y'), 'Latas acero'),
(15, 4, 5, 3.2, 25.6, 0.96, STR_TO_DATE('24/03/2025', '%d/%m/%Y'), 'Cajas pequeñas'),
(15, 5, 6, 1.6, 4.8, 0.16, STR_TO_DATE('25/03/2025', '%d/%m/%Y'), 'Desechos orgánicos'),
(20, 1, 7, 0.6, 30, 1.5, STR_TO_DATE('26/03/2025', '%d/%m/%Y'), 'Televisores'),
(20, 2, 1, 1.9, 19, 0.95, STR_TO_DATE('27/03/2025', '%d/%m/%Y'), 'Envases PET'),
(6, 3, 2, 2.1, 10.5, 0.42, STR_TO_DATE('28/03/2025', '%d/%m/%Y'), 'Papel kraft'),
(6, 4, 3, 2.4, 36, 1.92, STR_TO_DATE('29/03/2025', '%d/%m/%Y'), 'Botellas vidrio'),
(10, 5, 4, 1.3, 26, 1.3, STR_TO_DATE('30/03/2025', '%d/%m/%Y'), 'Latas metal'),
(10, 1, 5, 2.7, 21.6, 0.81, STR_TO_DATE('31/03/2025', '%d/%m/%Y'), 'Cajas cartón'),
(13, 2, 6, 1.1, 3.3, 0.11, STR_TO_DATE('01/04/2025', '%d/%m/%Y'), 'Restos orgánicos'),
(13, 3, 7, 0.7, 35, 1.75, STR_TO_DATE('02/04/2025', '%d/%m/%Y'), 'Monitores'),
(15, 4, 1, 1.6, 16, 0.8, STR_TO_DATE('03/04/2025', '%d/%m/%Y'), 'Bolsas plástico'),
(15, 5, 2, 2.2, 11, 0.44, STR_TO_DATE('04/04/2025', '%d/%m/%Y'), 'Papel usado'),
(20, 1, 3, 2.6, 39, 2.08, STR_TO_DATE('05/04/2025', '%d/%m/%Y'), 'Frascos vidrio'),
(20, 2, 4, 1.4, 28, 1.4, STR_TO_DATE('06/04/2025', '%d/%m/%Y'), 'Latas aluminio'),
(6, 3, 5, 3.1, 24.8, 0.93, STR_TO_DATE('07/04/2025', '%d/%m/%Y'), 'Cajas corrugadas'),
(6, 4, 6, 1.3, 3.9, 0.13, STR_TO_DATE('08/04/2025', '%d/%m/%Y'), 'Desechos orgánicos'),
(10, 5, 7, 0.9, 45, 2.25, STR_TO_DATE('09/04/2025', '%d/%m/%Y'), 'Impresoras'),
(10, 1, 1, 1.8, 18, 0.9, STR_TO_DATE('10/04/2025', '%d/%m/%Y'), 'Envases plástico'),
(13, 2, 2, 2.0, 10, 0.4, STR_TO_DATE('11/04/2025', '%d/%m/%Y'), 'Papel reciclado'),
(13, 3, 3, 2.3, 34.5, 1.84, STR_TO_DATE('12/04/2025', '%d/%m/%Y'), 'Botellas vidrio'),
(15, 4, 4, 1.2, 24, 1.2, STR_TO_DATE('13/04/2025', '%d/%m/%Y'), 'Latas metal'),
(15, 5, 5, 2.6, 20.8, 0.78, STR_TO_DATE('14/04/2025', '%d/%m/%Y'), 'Cajas cartón'),
(20, 1, 6, 1.4, 4.2, 0.14, STR_TO_DATE('15/04/2025', '%d/%m/%Y'), 'Restos orgánicos'),
(20, 2, 7, 0.5, 25, 1.25, STR_TO_DATE('16/04/2025', '%d/%m/%Y'), 'Televisores'),
(6, 3, 1, 1.7, 17, 0.85, STR_TO_DATE('17/04/2025', '%d/%m/%Y'), 'Bolsas plástico'),
(6, 4, 2, 2.1, 10.5, 0.42, STR_TO_DATE('18/04/2025', '%d/%m/%Y'), 'Papel kraft'),
(10, 5, 3, 2.5, 37.5, 2.0, STR_TO_DATE('19/04/2025', '%d/%m/%Y'), 'Frascos vidrio'),
(10, 1, 4, 1.0, 20, 1.0, STR_TO_DATE('20/04/2025', '%d/%m/%Y'), 'Latas aluminio'),
(13, 2, 5, 3.0, 24, 0.9, STR_TO_DATE('21/04/2025', '%d/%m/%Y'), 'Cajas cartón'),
(13, 3, 6, 1.5, 4.5, 0.15, STR_TO_DATE('22/04/2025', '%d/%m/%Y'), 'Residuos orgánicos'),
(15, 4, 7, 0.6, 30, 1.5, STR_TO_DATE('23/04/2025', '%d/%m/%Y'), 'Computadoras'),
(15, 5, 1, 1.9, 19, 0.95, STR_TO_DATE('24/04/2025', '%d/%m/%Y'), 'Envases PET'),
(20, 1, 2, 2.2, 11, 0.44, STR_TO_DATE('25/04/2025', '%d/%m/%Y'), 'Papel blanco'),
(20, 2, 3, 2.4, 36, 1.92, STR_TO_DATE('26/04/2025', '%d/%m/%Y'), 'Botellas vidrio'),
(6, 3, 4, 1.3, 26, 1.3, STR_TO_DATE('27/04/2025', '%d/%m/%Y'), 'Latas metal'),
(6, 4, 5, 2.7, 21.6, 0.81, STR_TO_DATE('28/04/2025', '%d/%m/%Y'), 'Cajas corrugadas'),
(10, 5, 6, 1.2, 3.6, 0.12, STR_TO_DATE('29/04/2025', '%d/%m/%Y'), 'Desechos orgánicos'),
(10, 1, 7, 0.7, 35, 1.75, STR_TO_DATE('30/04/2025', '%d/%m/%Y'), 'Monitors'),
(13, 2, 1, 1.6, 16, 0.8, STR_TO_DATE('01/05/2025', '%d/%m/%Y'), 'Bolsas plástico'),
(13, 3, 2, 2.0, 10, 0.4, STR_TO_DATE('02/05/2025', '%d/%m/%Y'), 'Papel reciclado'),
(15, 4, 3, 2.6, 39, 2.08, STR_TO_DATE('03/05/2025', '%d/%m/%Y'), 'Frascos vidrio'),
(15, 5, 4, 1.1, 22, 1.1, STR_TO_DATE('04/05/2025', '%d/%m/%Y'), 'Latas acero'),
(20, 1, 5, 3.2, 25.6, 0.96, STR_TO_DATE('05/05/2025', '%d/%m/%Y'), 'Cajas pequeñas'),
(20, 2, 6, 1.6, 4.8, 0.16, STR_TO_DATE('06/05/2025', '%d/%m/%Y'), 'Restos orgánicos'),
(6, 3, 7, 0.8, 40, 2.0, STR_TO_DATE('07/05/2025', '%d/%m/%Y'), 'Impresoras'),
(6, 4, 1, 1.8, 18, 0.9, STR_TO_DATE('08/05/2025', '%d/%m/%Y'), 'Envases plástico'),
(10, 5, 2, 2.1, 10.5, 0.42, STR_TO_DATE('09/05/2025', '%d/%m/%Y'), 'Papel kraft'),
(10, 1, 3, 2.3, 34.5, 1.84, STR_TO_DATE('10/05/2025', '%d/%m/%Y'), 'Botellas vidrio'),
(13, 2, 4, 1.4, 28, 1.4, STR_TO_DATE('11/05/2025', '%d/%m/%Y'), 'Latas metal'),
(13, 3, 5, 2.6, 20.8, 0.78, STR_TO_DATE('12/05/2025', '%d/%m/%Y'), 'Cajas cartón'),
(15, 4, 6, 1.3, 3.9, 0.13, STR_TO_DATE('13/05/2025', '%d/%m/%Y'), 'Desechos orgánicos'),
(15, 5, 7, 0.6, 30, 1.5, STR_TO_DATE('14/05/2025', '%d/%m/%Y'), 'Computadoras'),
(20, 1, 1, 1.7, 17, 0.85, STR_TO_DATE('15/05/2025', '%d/%m/%Y'), 'Bolsas plástico'),
(20, 2, 2, 2.0, 10, 0.4, STR_TO_DATE('16/05/2025', '%d/%m/%Y'), 'Papel reciclado'),
(6, 3, 3, 2.6, 39, 2.08, STR_TO_DATE('17/05/2025', '%d/%m/%Y'), 'Frascos vidrio'),
(6, 4, 4, 1.1, 22, 1.1, STR_TO_DATE('18/05/2025', '%d/%m/%Y'), 'Latas acero'),
(10, 5, 5, 3.2, 25.6, 0.96, STR_TO_DATE('19/05/2025', '%d/%m/%Y'), 'Cajas pequeñas'),
(10, 1, 6, 1.6, 4.8, 0.16, STR_TO_DATE('20/05/2025', '%d/%m/%Y'), 'Restos orgánicos'),
(13, 2, 7, 0.8, 40, 2.0, STR_TO_DATE('21/05/2025', '%d/%m/%Y'), 'Impresoras'),
(13, 3, 1, 1.9, 19, 0.95, STR_TO_DATE('22/05/2025', '%d/%m/%Y'), 'Envases plástico'),
(15, 4, 2, 2.2, 11, 0.44, STR_TO_DATE('23/05/2025', '%d/%m/%Y'), 'Papel blanco'),
(15, 5, 3, 2.4, 36, 1.92, STR_TO_DATE('24/05/2025', '%d/%m/%Y'), 'Botellas vidrio'),
(20, 1, 4, 1.3, 26, 1.3, STR_TO_DATE('25/05/2025', '%d/%m/%Y'), 'Latas metal'),
(20, 2, 5, 2.7, 21.6, 0.81, STR_TO_DATE('26/05/2025', '%d/%m/%Y'), 'Cajas corrugadas'),
(6, 3, 6, 1.5, 4.5, 0.15, STR_TO_DATE('27/05/2025', '%d/%m/%Y'), 'Desechos orgánicos'),
(6, 4, 7, 0.9, 45, 2.25, STR_TO_DATE('28/05/2025', '%d/%m/%Y'), 'Televisores'),
(10, 5, 1, 1.6, 16, 0.8, STR_TO_DATE('29/05/2025', '%d/%m/%Y'), 'Bolsas plástico'),
(10, 1, 2, 2.0, 10, 0.4, STR_TO_DATE('30/05/2025', '%d/%m/%Y'), 'Papel reciclado'),
(13, 2, 3, 2.6, 39, 2.08, STR_TO_DATE('31/05/2025', '%d/%m/%Y'), 'Frascos vidrio'),
(13, 3, 4, 1.1, 22, 1.1, STR_TO_DATE('01/06/2025', '%d/%m/%Y'), 'Latas acero'),
(15, 4, 5, 3.2, 25.6, 0.96, STR_TO_DATE('02/06/2025', '%d/%m/%Y'), 'Cajas pequeñas'),
(15, 5, 6, 1.4, 4.2, 0.14, STR_TO_DATE('03/06/2025', '%d/%m/%Y'), 'Restos orgánicos'),
(20, 1, 7, 0.7, 35, 1.75, STR_TO_DATE('04/06/2025', '%d/%m/%Y'), 'Monitors'),
(20, 2, 1, 1.8, 18, 0.9, STR_TO_DATE('05/06/2025', '%d/%m/%Y'), 'Envases plástico'),
(6, 3, 2, 2.1, 10.5, 0.42, STR_TO_DATE('06/06/2025', '%d/%m/%Y'), 'Papel kraft'),
(6, 4, 3, 2.5, 37.5, 2.0, STR_TO_DATE('07/06/2025', '%d/%m/%Y'), 'Botellas vidrio'),
(10, 5, 4, 1.2, 24, 1.2, STR_TO_DATE('08/06/2025', '%d/%m/%Y'), 'Latas aluminio'),
(10, 1, 5, 3.0, 24, 0.9, STR_TO_DATE('09/06/2025', '%d/%m/%Y'), 'Cajas cartón'),
(13, 2, 6, 1.6, 4.8, 0.16, STR_TO_DATE('10/06/2025', '%d/%m/%Y'), 'Residuos orgánicos'),
(13, 3, 7, 0.8, 40, 2.0, STR_TO_DATE('11/06/2025', '%d/%m/%Y'), 'Impresoras'),
(15, 4, 1, 1.9, 19, 0.95, STR_TO_DATE('12/06/2025', '%d/%m/%Y'), 'Envases PET'),
(15, 5, 2, 2.2, 11, 0.44, STR_TO_DATE('13/06/2025', '%d/%m/%Y'), 'Papel blanco'),
(20, 1, 3, 2.4, 36, 1.92, STR_TO_DATE('14/06/2025', '%d/%m/%Y'), 'Botellas vidrio'),
(20, 2, 4, 1.3, 26, 1.3, STR_TO_DATE('15/06/2025', '%d/%m/%Y'), 'Latas metal'),
(6, 3, 5, 2.7, 21.6, 0.81, STR_TO_DATE('16/06/2025', '%d/%m/%Y'), 'Cajas corrugadas'),
(6, 4, 6, 1.5, 4.5, 0.15, STR_TO_DATE('17/06/2025', '%d/%m/%Y'), 'Desechos orgánicos'),
(10, 5, 7, 0.9, 45, 2.25, STR_TO_DATE('18/06/2025', '%d/%m/%Y'), 'Televisores'),
(10, 1, 1, 1.6, 16, 0.8, STR_TO_DATE('19/06/2025', '%d/%m/%Y'), 'Bolsas plástico'),
(13, 2, 2, 2.0, 10, 0.4, STR_TO_DATE('20/06/2025', '%d/%m/%Y'), 'Papel reciclado'),
(13, 3, 3, 2.6, 39, 2.08, STR_TO_DATE('21/06/2025', '%d/%m/%Y'), 'Frascos vidrio'),
(15, 4, 4, 1.1, 22, 1.1, STR_TO_DATE('22/06/2025', '%d/%m/%Y'), 'Latas acero'),
(15, 5, 5, 3.2, 25.6, 0.96, STR_TO_DATE('23/06/2025', '%d/%m/%Y'), 'Cajas pequeñas'),
(20, 1, 6, 1.6, 4.8, 0.16, STR_TO_DATE('24/06/2025', '%d/%m/%Y'), 'Restos orgánicos'),
(20, 2, 7, 0.8, 40, 2.0, STR_TO_DATE('25/06/2025', '%d/%m/%Y'), 'Impresoras'),
(6, 3, 1, 1.8, 18, 0.9, STR_TO_DATE('26/06/2025', '%d/%m/%Y'), 'Envases plástico'),
(6, 4, 2, 2.1, 10.5, 0.42, STR_TO_DATE('27/06/2025', '%d/%m/%Y'), 'Papel kraft'),
(10, 5, 3, 2.5, 37.5, 2.0, STR_TO_DATE('28/06/2025', '%d/%m/%Y'), 'Botellas vidrio'),
(10, 1, 4, 1.2, 24, 1.2, STR_TO_DATE('29/06/2025', '%d/%m/%Y'), 'Latas aluminio'),
(13, 2, 5, 3.0, 24, 0.9, STR_TO_DATE('30/06/2025', '%d/%m/%Y'), 'Cajas cartón'),
(13, 3, 6, 1.6, 4.8, 0.16, STR_TO_DATE('01/07/2025', '%d/%m/%Y'), 'Residuos orgánicos'),
(15, 4, 7, 0.7, 35, 1.75, STR_TO_DATE('02/07/2025', '%d/%m/%Y'), 'Monitors'),
(15, 5, 1, 1.9, 19, 0.95, STR_TO_DATE('03/07/2025', '%d/%m/%Y'), 'Envases plástico'),
(20, 1, 2, 2.2, 11, 0.44, STR_TO_DATE('04/07/2025', '%d/%m/%Y'), 'Papel blanco'),
(20, 2, 3, 2.4, 36, 1.92, STR_TO_DATE('05/07/2025', '%d/%m/%Y'), 'Botellas vidrio'),
(6, 3, 4, 1.3, 26, 1.3, STR_TO_DATE('06/07/2025', '%d/%m/%Y'), 'Latas metal'),
(6, 4, 5, 2.7, 21.6, 0.81, STR_TO_DATE('07/07/2025', '%d/%m/%Y'), 'Cajas corrugadas'),
(10, 5, 6, 1.5, 4.5, 0.15, STR_TO_DATE('08/07/2025', '%d/%m/%Y'), 'Desechos orgánicos'),
(10, 1, 7, 0.9, 45, 2.25, STR_TO_DATE('09/07/2025', '%d/%m/%Y'), 'Televisores'),
(13, 2, 1, 1.6, 16, 0.8, STR_TO_DATE('10/07/2025', '%d/%m/%Y'), 'Bolsas plástico'),
(13, 3, 2, 2.0, 10, 0.4, STR_TO_DATE('11/07/2025', '%d/%m/%Y'), 'Papel reciclado'),
(15, 4, 3, 2.6, 39, 2.08, STR_TO_DATE('12/07/2025', '%d/%m/%Y'), 'Frascos vidrio'),
(15, 5, 4, 1.1, 22, 1.1, STR_TO_DATE('13/07/2025', '%d/%m/%Y'), 'Latas acero'),
(20, 1, 5, 3.2, 25.6, 0.96, STR_TO_DATE('14/07/2025', '%d/%m/%Y'), 'Cajas pequeñas'),
(20, 2, 6, 1.6, 4.8, 0.16, STR_TO_DATE('15/07/2025', '%d/%m/%Y'), 'Restos orgánicos'),
(6, 3, 7, 0.8, 40, 2.0, STR_TO_DATE('16/07/2025', '%d/%m/%Y'), 'Impresoras'),
(6, 4, 1, 1.9, 19, 0.95, STR_TO_DATE('17/07/2025', '%d/%m/%Y'), 'Envases plástico'),
(10, 5, 2, 2.2, 11, 0.44, STR_TO_DATE('18/07/2025', '%d/%m/%Y'), 'Papel blanco'),
(10, 1, 3, 2.4, 36, 1.92, STR_TO_DATE('19/07/2025', '%d/%m/%Y'), 'Botellas vidrio'),
(13, 2, 4, 1.3, 26, 1.3, STR_TO_DATE('20/07/2025', '%d/%m/%Y'), 'Latas metal'),
(13, 3, 5, 2.7, 21.6, 0.81, STR_TO_DATE('21/07/2025', '%d/%m/%Y'), 'Cajas corrugadas'),
(15, 4, 6, 1.5, 4.5, 0.15, STR_TO_DATE('22/07/2025', '%d/%m/%Y'), 'Desechos orgánicos'),
(15, 5, 7, 0.9, 45, 2.25, STR_TO_DATE('23/07/2025', '%d/%m/%Y'), 'Televisores'),
(20, 1, 1, 1.6, 16, 0.8, STR_TO_DATE('24/07/2025', '%d/%m/%Y'), 'Bolsas plástico'),
(20, 2, 2, 2.0, 10, 0.4, STR_TO_DATE('25/07/2025', '%d/%m/%Y'), 'Papel reciclado'),
(6, 3, 3, 2.6, 39, 2.08, STR_TO_DATE('26/07/2025', '%d/%m/%Y'), 'Frascos vidrio'),
(6, 4, 4, 1.1, 22, 1.1, STR_TO_DATE('27/07/2025', '%d/%m/%Y'), 'Latas acero'),
(10, 5, 5, 3.2, 25.6, 0.96, STR_TO_DATE('28/07/2025', '%d/%m/%Y'), 'Cajas pequeñas'),
(10, 1, 6, 1.6, 4.8, 0.16, STR_TO_DATE('29/07/2025', '%d/%m/%Y'), 'Restos orgánicos'),
(13, 2, 7, 0.8, 40, 2.0, STR_TO_DATE('30/07/2025', '%d/%m/%Y'), 'Impresoras'),
(13, 3, 1, 1.9, 19, 0.95, STR_TO_DATE('31/07/2025', '%d/%m/%Y'), 'Envases plástico'),
(15, 4, 2, 2.2, 11, 0.44, STR_TO_DATE('01/08/2025', '%d/%m/%Y'), 'Papel blanco'),
(15, 5, 3, 2.4, 36, 1.92, STR_TO_DATE('02/08/2025', '%d/%m/%Y'), 'Botellas vidrio'),
(20, 1, 4, 1.3, 26, 1.3, STR_TO_DATE('03/08/2025', '%d/%m/%Y'), 'Latas metal'),
(20, 2, 5, 2.7, 21.6, 0.81, STR_TO_DATE('04/08/2025', '%d/%m/%Y'), 'Cajas corrugadas'),
(6, 3, 6, 1.5, 4.5, 0.15, STR_TO_DATE('05/08/2025', '%d/%m/%Y'), 'Desechos orgánicos'),
(6, 4, 7, 0.9, 45, 2.25, STR_TO_DATE('06/08/2025', '%d/%m/%Y'), 'Televisores'),
(10, 5, 1, 1.6, 16, 0.8, STR_TO_DATE('07/08/2025', '%d/%m/%Y'), 'Bolsas plástico'),
(10, 1, 2, 2.0, 10, 0.4, STR_TO_DATE('08/08/2025', '%d/%m/%Y'), 'Papel reciclado'),
(13, 2, 3, 2.6, 39, 2.08, STR_TO_DATE('09/08/2025', '%d/%m/%Y'), 'Frascos vidrio'),
(13, 3, 4, 1.1, 22, 1.1, STR_TO_DATE('10/08/2025', '%d/%m/%Y'), 'Latas acero'),
(15, 4, 5, 3.2, 25.6, 0.96, STR_TO_DATE('11/08/2025', '%d/%m/%Y'), 'Cajas pequeñas'),
(15, 5, 6, 1.4, 4.2, 0.14, STR_TO_DATE('12/08/2025', '%d/%m/%Y'), 'Restos orgánicos'),
(20, 1, 7, 0.7, 35, 1.75, STR_TO_DATE('13/08/2025', '%d/%m/%Y'), 'Monitors'),
(20, 2, 1, 1.8, 18, 0.9, STR_TO_DATE('14/08/2025', '%d/%m/%Y'), 'Envases plástico'),
(6, 3, 2, 2.1, 10.5, 0.42, STR_TO_DATE('15/08/2025', '%d/%m/%Y'), 'Papel kraft'),
(6, 4, 3, 2.5, 37.5, 2.0, STR_TO_DATE('16/08/2025', '%d/%m/%Y'), 'Botellas vidrio'),
(10, 5, 4, 1.2, 24, 1.2, STR_TO_DATE('17/08/2025', '%d/%m/%Y'), 'Latas aluminio'),
(10, 1, 5, 3.0, 24, 0.9, STR_TO_DATE('18/08/2025', '%d/%m/%Y'), 'Cajas cartón'),
(13, 2, 6, 1.6, 4.8, 0.16, STR_TO_DATE('19/08/2025', '%d/%m/%Y'), 'Residuos orgánicos'),
(13, 3, 7, 0.8, 40, 2.0, STR_TO_DATE('20/08/2025', '%d/%m/%Y'), 'Impresoras'),
(15, 4, 1, 1.9, 19, 0.95, STR_TO_DATE('21/08/2025', '%d/%m/%Y'), 'Envases plástico'),
(15, 5, 2, 2.2, 11, 0.44, STR_TO_DATE('22/08/2025', '%d/%m/%Y'), 'Papel blanco'),
(20, 1, 3, 2.4, 36, 1.92, STR_TO_DATE('23/08/2025', '%d/%m/%Y'), 'Botellas vidrio'),
(20, 2, 4, 1.3, 26, 1.3, STR_TO_DATE('24/08/2025', '%d/%m/%Y'), 'Latas metal'),
(6, 3, 5, 2.7, 21.6, 0.81, STR_TO_DATE('25/08/2025', '%d/%m/%Y'), 'Cajas corrugadas'),
(6, 4, 6, 1.5, 4.5, 0.15, STR_TO_DATE('26/08/2025', '%d/%m/%Y'), 'Desechos orgánicos'),
(10, 5, 7, 0.9, 45, 2.25, STR_TO_DATE('27/08/2025', '%d/%m/%Y'), 'Televisores'),
(10, 1, 1, 1.6, 16, 0.8, STR_TO_DATE('28/08/2025', '%d/%m/%Y'), 'Bolsas plástico'),
(13, 2, 2, 2.0, 10, 0.4, STR_TO_DATE('29/08/2025', '%d/%m/%Y'), 'Papel reciclado'),
(13, 3, 3, 2.6, 39, 2.08, STR_TO_DATE('30/08/2025', '%d/%m/%Y'), 'Frascos vidrio'),
(15, 4, 4, 1.1, 22, 1.1, STR_TO_DATE('31/08/2025', '%d/%m/%Y'), 'Latas acero');
SET SQL_SAFE_UPDATES = 0;
select * FROM punto_reciclaje;
select * from Permiso;
select * from rol;
select* from rol_permiso;
select * from usuario_permiso;
select * from usuario;

select * from Material_Reciclable;


CALL insertar_registro_reciclaje(1, 1, 2, 2.0, '2025-05-02', 'B');
select * from registro_reciclaje;
-- Verificar balance de puntos inicial
SELECT * FROM Usuario 
where id_usuario=7;
SELECT * FROM Impacto_ambiental_diario;
INSERT INTO Registro_Reciclaje (id_usuario, id_punto_reciclaje, id_material_reciclable, cantidad_kg, fecha_registro, nombre_subtipo)
VALUES (1, 2, 2, 2.0, '2025-05-04', 'papeles');
CALL insertar_registro_reciclaje(
    1,
    1,
    3,
    2,
    '2025-05-04',
    "botellas"
)

-- Registro y actualizacion de impacto ambiental diario
SELECT * FROM Impacto_Ambiental_Diario fecha_dia;

-- Verificar la bitácora
SELECT * FROM Bitacora_Reciclaje;
SELECT * FROM Registro_reciclaje;
-- Actualizar un registro existente
UPDATE Registro_Reciclaje SET cantidad_kg = 3.0 WHERE id_registro_reciclaje = 1;


-- Verificar puntos del usuario
SELECT * FROM Usuario;

CALL  (1, 1, 'Completado', '2025-05-02');

-- Verificar la bitácora
SELECT * FROM Canje_Recompensa;
SELECT * FROM Bitacora_canje;




-- reporte de actividad de un usuario
CALL reporte_actividad_reciclaje(1);

CALL registrar_intento_login(1, 'luis.morales@email.com', 'Éxito', 'Inicio de sesión exitoso');
CALL registrar_intento_login(NULL, 'correo inexistente', 'Fallido', 'Credenciales incorrectas');

-- Verificar la bitácora
SELECT * FROM Bitacora_Acceso ORDER BY id_bitacora_acceso DESC LIMIT 2;

