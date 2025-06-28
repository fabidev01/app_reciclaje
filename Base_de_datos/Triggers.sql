DELIMITER //

-- 1. para el impacto ambiental diario
CREATE TRIGGER after_registro_reciclaje_insert_impacto
AFTER INSERT ON Registro_Reciclaje
FOR EACH ROW
BEGIN
    DECLARE impacto_id INT;
    DECLARE nombre_material VARCHAR(35);
    DECLARE unidad VARCHAR(10);
    
    SELECT nombre, unidad_medida INTO nombre_material, unidad
    FROM Material_Reciclable
    WHERE id_material_reciclable = NEW.id_material_reciclable;
    
    SELECT id_impacto_ambiental_diario INTO impacto_id
    FROM Impacto_Ambiental_Diario 
    WHERE fecha_dia = NEW.fecha_registro
    AND tipo_basura = nombre_material;
    
    IF impacto_id IS NOT NULL THEN
        UPDATE Impacto_Ambiental_Diario
        SET cantidad_reciclada_por_tipo = cantidad_reciclada_por_tipo + NEW.cantidad_kg,
            co2_reducido_por_tipo = co2_reducido_por_tipo + NEW.co2_reducido
        WHERE id_impacto_ambiental_diario = impacto_id;
    ELSE
        INSERT INTO Impacto_Ambiental_Diario (fecha_dia, tipo_basura, unidad_medida, cantidad_reciclada_por_tipo, co2_reducido_por_tipo)
        VALUES (NEW.fecha_registro, nombre_material, unidad, NEW.cantidad_kg, NEW.co2_reducido);
    END IF;
END //

-- para actualizar el balance de puntos del usuario al registrar un nuevo registro reciclaje
DELIMITER //
CREATE TRIGGER before_registro_reciclaje_insert
BEFORE INSERT ON Registro_Reciclaje
FOR EACH ROW
BEGIN
    DECLARE puntos INT;
    DECLARE co2 FLOAT;
    DECLARE capacidad_usada FLOAT;
    DECLARE capacidad_max INT;

    SELECT puntos_por_unidad, co2_por_unidad
    INTO puntos, co2
    FROM Material_Reciclable
    WHERE id_material_reciclable = NEW.id_material_reciclable;

    SET NEW.puntos_obtenidos = puntos * NEW.cantidad_kg;
    SET NEW.co2_reducido = co2 * NEW.cantidad_kg;

    -- Calcular capacidad usada en el punto
    SELECT COALESCE(SUM(cantidad_kg), 0), pr.capacidad_maxima
    INTO capacidad_usada, capacidad_max
    FROM Registro_Reciclaje rr
    JOIN Punto_Reciclaje pr ON rr.id_punto_reciclaje = pr.id_punto_reciclaje
    WHERE rr.id_punto_reciclaje = NEW.id_punto_reciclaje
    GROUP BY pr.capacidad_maxima;

    IF (capacidad_usada + NEW.cantidad_kg) > capacidad_max THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: La capacidad máxima del punto de reciclaje ha sido excedida.';
    END IF;

    UPDATE Usuario 
    SET balance_puntos = balance_puntos + (puntos * NEW.cantidad_kg)
    WHERE id_usuario = NEW.id_usuario;
END //
DELIMITER ;

-- bitacora INSERT Registro_Reciclaje
CREATE TRIGGER after_registro_reciclaje_insert_bitacora
AFTER INSERT ON Registro_Reciclaje
FOR EACH ROW
BEGIN
    DECLARE nombre_usuario VARCHAR(35);
    SELECT nombre INTO nombre_usuario
    FROM Usuario
    WHERE id_usuario = NEW.id_usuario;
    
    INSERT INTO Bitacora_Reciclaje (ip, id_registro_reciclaje, accion, fecha_accion, detalle)
    VALUES (
        NULL,
        NEW.id_registro_reciclaje,
        'INSERT',
        NOW(),
        CONCAT('Registro creado por ', COALESCE(nombre_usuario, 'Desconocido'), ': ', NEW.cantidad_kg, ' kg de ', NEW.nombre_subtipo)
    );
END //

-- after_registro_reciclaje_update_bitacora (Auditoría UPDATE en Bitacora_Reciclaje)
CREATE TRIGGER after_registro_reciclaje_update_bitacora
AFTER UPDATE ON Registro_Reciclaje
FOR EACH ROW
BEGIN
    DECLARE nombre_usuario VARCHAR(35);
    SELECT nombre INTO nombre_usuario
    FROM Usuario
    WHERE id_usuario = NEW.id_usuario;
    
    INSERT INTO Bitacora_Reciclaje (ip, id_registro_reciclaje, accion, fecha_accion, detalle)
    VALUES (
        NULL,
        OLD.id_registro_reciclaje,
        'UPDATE',
        NOW(),
        CONCAT('Registro actualizado por ', COALESCE(nombre_usuario, 'Desconocido'), ': cantidad_kg de ', OLD.cantidad_kg, ' a ', NEW.cantidad_kg)
    );
END //

-- after_registro_reciclaje_delete_bitacora (Auditoría DELETE en Bitacora_Reciclaje)
CREATE TRIGGER after_registro_reciclaje_delete_bitacora
AFTER DELETE ON Registro_Reciclaje
FOR EACH ROW
BEGIN
    DECLARE nombre_usuario VARCHAR(35);
    SELECT nombre INTO nombre_usuario
    FROM Usuario
    WHERE id_usuario = OLD.id_usuario;
    
    INSERT INTO Bitacora_Reciclaje (ip, id_registro_reciclaje, accion, fecha_accion, detalle)
    VALUES (
        NULL,
        OLD.id_registro_reciclaje,
        'DELETE',
        NOW(),
        CONCAT('Registro eliminado por ', COALESCE(nombre_usuario, 'Desconocido'), ': ', OLD.cantidad_kg, ' kg de ', OLD.nombre_subtipo)
    );
END //

-- after_canje_recompensa_insert_bitacora (Auditoría INSERT en Bitacora_Canje)
CREATE TRIGGER after_canje_recompensa_insert_bitacora
AFTER INSERT ON Canje_Recompensa
FOR EACH ROW
BEGIN
    DECLARE nombre_usuario VARCHAR(35);
    SELECT nombre INTO nombre_usuario
    FROM Usuario
    WHERE id_usuario = NEW.id_usuario;
    
    INSERT INTO Bitacora_Canje (ip, id_canje_recompensa, id_catalogo_recompensa, accion, fecha_accion, detalle)
    VALUES (
        NULL,
        NEW.id_canje_recompensa,
        NEW.id_catalogo_recompensa,
        'INSERT',
        NOW(),
        CONCAT('Canje creado por ', COALESCE(nombre_usuario, 'Desconocido'), ': ', NEW.puntos_descontados, ' puntos (', NEW.estado, ')')
    );
END //

-- after_canje_recompensa_update_bitacora (Auditoría UPDATE en Bitacora_Canje)
CREATE TRIGGER after_canje_recompensa_update_bitacora
AFTER UPDATE ON Canje_Recompensa
FOR EACH ROW
BEGIN
    DECLARE nombre_usuario VARCHAR(35);
    SELECT nombre INTO nombre_usuario
    FROM Usuario
    WHERE id_usuario = NEW.id_usuario; -- Corregido de @current_user_id a NEW.id_usuario
    
    INSERT INTO Bitacora_Canje (ip, id_canje_recompensa, id_catalogo_recompensa, accion, fecha_accion, detalle)
    VALUES (
        NULL, -- Corregido de @current_user_ip a NULL
        OLD.id_canje_recompensa,
        OLD.id_catalogo_recompensa,
        'UPDATE',
        NOW(),
        CONCAT('Canje actualizado por ', COALESCE(nombre_usuario, 'Desconocido'), ': estado de ', OLD.estado, ' a ', NEW.estado)
    );
END //

-- after_canje_recompensa_delete_bitacora (Auditoría DELETE en Bitacora_Canje)
CREATE TRIGGER after_canje_recompensa_delete_bitacora
AFTER DELETE ON Canje_Recompensa
FOR EACH ROW
BEGIN
    DECLARE nombre_usuario VARCHAR(35);
    SELECT nombre INTO nombre_usuario
    FROM Usuario
    WHERE id_usuario = OLD.id_usuario; -- Corregido de @current_user_id a OLD.id_usuario
    
    INSERT INTO Bitacora_Canje (ip, id_canje_recompensa, id_catalogo_recompensa, accion, fecha_accion, detalle)
    VALUES (
        NULL, -- Corregido de @current_user_ip a NULL
        OLD.id_canje_recompensa,
        OLD.id_catalogo_recompensa,
        'DELETE',
        NOW(),
        CONCAT('Canje eliminado por ', COALESCE(nombre_usuario, 'Desconocido'), ': ', OLD.puntos_descontados, ' puntos (', OLD.estado, ')')
    );
END //

-- after_catalogo_recompensa_insert_bitacora (Auditoría INSERT en Bitacora_Catalogo)
CREATE TRIGGER after_catalogo_recompensa_insert_bitacora
AFTER INSERT ON Catalogo_Recompensa
FOR EACH ROW
BEGIN
    DECLARE nombre_usuario VARCHAR(35);
    -- Nota: No hay id_usuario directo en Catalogo_Recompensa, asumimos un usuario por defecto o de la sesión
    INSERT INTO Bitacora_Catalogo (ip, id_catalogo_recompensa, accion, fecha_accion, detalle)
    VALUES (
        NULL,
        NEW.id_catalogo_recompensa,
        'INSERT',
        NOW(),
        CONCAT('Recompensa creada por ', COALESCE(nombre_usuario, 'Desconocido'), ': ', NEW.nombre)
    );
END //

-- after_catalogo_recompensa_update_bitacora (Auditoría UPDATE en Bitacora_Catalogo)
CREATE TRIGGER after_catalogo_recompensa_update_bitacora
AFTER UPDATE ON Catalogo_Recompensa
FOR EACH ROW
BEGIN
    DECLARE nombre_usuario VARCHAR(35);
    -- Nota: No hay id_usuario directo, usamos COALESCE para manejar casos nulos
    INSERT INTO Bitacora_Catalogo (ip, id_catalogo_recompensa, accion, fecha_accion, detalle)
    VALUES (
        NULL,
        NEW.id_catalogo_recompensa,
        'UPDATE',
        NOW(),
        CONCAT('Recompensa actualizada por ', COALESCE(nombre_usuario, 'Desconocido'), ': ', OLD.nombre, ' a ', NEW.nombre)
    );
END //

-- after_catalogo_recompensa_delete_bitacora (Auditoría DELETE en Bitacora_Catalogo)
CREATE TRIGGER after_catalogo_recompensa_delete_bitacora
AFTER DELETE ON Catalogo_Recompensa
FOR EACH ROW
BEGIN
    DECLARE nombre_usuario VARCHAR(35);
    -- Nota: No hay id_usuario directo, usamos COALESCE para manejar casos nulos
    INSERT INTO Bitacora_Catalogo (ip, id_catalogo_recompensa, accion, fecha_accion, detalle)
    VALUES (
        NULL,
        OLD.id_catalogo_recompensa,
        'DELETE',
        NOW(),
        CONCAT('Recompensa eliminada por ', COALESCE(nombre_usuario, 'Desconocido'), ': ', OLD.nombre)
    );
END //

DELIMITER ;