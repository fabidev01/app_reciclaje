-- 1 canjear_recompensa (Canje de Recompensas)
DELIMITER //
CREATE PROCEDURE canjear_recompensa(
    IN p_id_usuario INT,
    IN p_id_catalogo_recompensa INT,
    IN p_estado VARCHAR(35),
    IN p_fecha_canje DATE
)
BEGIN
    DECLARE puntos_necesarios INT;
    DECLARE puntos_usuario INT;
    DECLARE stock_disponible INT;

    SELECT puntos_coste, stock INTO puntos_necesarios, stock_disponible
    FROM Catalogo_Recompensa
    WHERE id_catalogo_recompensa = p_id_catalogo_recompensa;

    SELECT balance_puntos INTO puntos_usuario
    FROM Usuario
    WHERE id_usuario = p_id_usuario;

    IF puntos_usuario < puntos_necesarios THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: No tienes suficientes puntos para canjear esta recompensa.';
    END IF;

    IF stock_disponible <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: No hay stock disponible para esta recompensa.';
    END IF;

    UPDATE Usuario
    SET balance_puntos = balance_puntos - puntos_necesarios
    WHERE id_usuario = p_id_usuario;

    INSERT INTO Canje_Recompensa (id_usuario, id_catalogo_recompensa, estado, fecha_canje, puntos_descontados)
    VALUES (p_id_usuario, p_id_catalogo_recompensa, p_estado, p_fecha_canje, puntos_necesarios);

    IF p_estado = 'Completado' THEN
        UPDATE Catalogo_Recompensa
        SET stock = stock - 1
        WHERE id_catalogo_recompensa = p_id_catalogo_recompensa;
    END IF;
END //
DELIMITER ;
-- canje_donacion
DELIMITER //
CREATE PROCEDURE canjear_donacion(
    IN p_id_usuario INT,
    IN p_id_donacion INT,
    IN p_cantidad INT,
    IN p_estado VARCHAR(35),
    IN p_fecha_canje DATE
)
BEGIN
    DECLARE puntos_necesarios DECIMAL(10, 2);
    DECLARE puntos_usuario INT;

    SELECT monto_donacion INTO puntos_necesarios
    FROM Donacion
    WHERE id_donacion = p_id_donacion;

    SELECT balance_puntos INTO puntos_usuario
    FROM Usuario
    WHERE id_usuario = p_id_usuario;

    IF puntos_usuario < (puntos_necesarios * p_cantidad) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: No tienes suficientes puntos para esta donación.';
    END IF;

    UPDATE Usuario
    SET balance_puntos = balance_puntos - (puntos_necesarios * p_cantidad)
    WHERE id_usuario = p_id_usuario;

    INSERT INTO Canje_Donacion (id_usuario, id_donacion, estado, fecha_canje, puntos_descontados)
    VALUES (p_id_usuario, p_id_donacion, p_estado, p_fecha_canje, (puntos_necesarios * p_cantidad));

END //
DELIMITER ;
-- reporte de actividad de un usuario mediante su id
DELIMITER //
CREATE PROCEDURE reporte_actividad_reciclaje(
    IN p_id_usuario INT
)
BEGIN
    SELECT 
        u.nombre AS usuario,
        mr.nombre AS material,
        SUM(rr.cantidad_kg) AS total_kg,
        SUM(rr.puntos_obtenidos) AS total_puntos,
        SUM(rr.co2_reducido) AS total_co2_reducido
    FROM Registro_Reciclaje rr
    JOIN Usuario u ON rr.id_usuario = u.id_usuario
    JOIN Material_Reciclable mr ON rr.id_material_reciclable = mr.id_material_reciclable
    WHERE u.id_usuario = p_id_usuario
    GROUP BY u.id_usuario, mr.id_material_reciclable
    ORDER BY total_kg DESC;
END //
DELIMITER ;
-- registrar intentos de inicio de sesion de los usuarios
DELIMITER //
CREATE PROCEDURE registrar_intento_login(
    IN p_id_usuario INT, -- NULL si el login falla
    IN p_correo VARCHAR(50),
    IN p_resultado VARCHAR(35),
    IN p_detalle TEXT 
)
BEGIN
    INSERT INTO Bitacora_Acceso (id_usuario, tipo_acceso, fecha_acceso, resultado, detalle)
    VALUES (
        p_id_usuario,
        'Inicio',
        CURDATE(),
        p_resultado,
        CONCAT('Intento de login para ', p_correo, ': ', p_detalle)
    );
END //
DELIMITER ;