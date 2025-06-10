DELIMITER //
-- 1.para el impacto ambiental diario

CREATE TRIGGER after_registro_reciclaje_insert_impacto
AFTER INSERT ON Registro_Reciclaje
FOR EACH ROW
BEGIN
    DECLARE impacto_id INT;
    DECLARE nombre_material VARCHAR(35);
    DECLARE unidad VARCHAR(10);
    
    -- Obtenemos el nombre del material y la unidad de medida desde Material_Reciclable
    SELECT nombre, unidad_medida INTO nombre_material, unidad
    FROM Material_Reciclable
    WHERE id_material_reciclable = NEW.id_material_reciclable;
    
    -- Buscar si ya existe un registro para el día y tipo de basura
    SELECT id_impacto_ambiental_diario INTO impacto_id
    FROM Impacto_Ambiental_Diario 
    WHERE fecha_dia = NEW.fecha_registro
    AND tipo_basura = nombre_material;
    
    -- Si existe, actualizar los valores sumando por tipo de basura
    IF impacto_id IS NOT NULL THEN
        UPDATE Impacto_Ambiental_Diario
        SET cantidad_reciclada_por_tipo = cantidad_reciclada_por_tipo + NEW.cantidad_kg,
            co2_reducido_por_tipo = co2_reducido_por_tipo + NEW.co2_reducido
        WHERE id_impacto_ambiental_diario = impacto_id;
    -- Si no existe, crear una nueva fila con el tipo de basura
    ELSE
        INSERT INTO Impacto_Ambiental_Diario (fecha_dia, tipo_basura, unidad_medida, cantidad_reciclada_por_tipo, co2_reducido_por_tipo)
        VALUES (NEW.fecha_registro, nombre_material, unidad, NEW.cantidad_kg, NEW.co2_reducido);
    END IF;
END //

-- para actuazliar el balance de puntos del usuario al registrar un nuevo registro reciclaje

CREATE TRIGGER before_registro_reciclaje_insert
BEFORE INSERT ON Registro_Reciclaje
FOR EACH ROW
BEGIN
    DECLARE puntos INT;
    DECLARE co2 FLOAT;
    -- Obtener los puntos por unidad y CO2 por unidad del material reciclable
    SELECT puntos_por_unidad, co2_por_unidad
    INTO puntos, co2
    FROM Material_Reciclable
    WHERE id_material_reciclable = NEW.id_material_reciclable;
    
    -- Calcular los puntos y CO2 para el registro
    SET NEW.puntos_obtenidos = puntos * NEW.cantidad_kg;
    SET NEW.co2_reducido = co2 * NEW.cantidad_kg;
    
    -- Actualizar el balance de puntos del usuario (incrementar)
    UPDATE Usuario 
    SET balance_puntos = balance_puntos + (puntos * NEW.cantidad_kg)
    WHERE id_usuario = NEW.id_usuario;
END //
-- bitacora INSERT Registro_Reciclaje

CREATE TRIGGER after_registro_reciclaje_insert_bitacora
AFTER INSERT ON Registro_Reciclaje
FOR EACH ROW
BEGIN
    DECLARE nombre_usuario VARCHAR(35);
    -- Obtener el nombre del usuario desde NEW.id_usuario
    SELECT nombre INTO nombre_usuario
    FROM Usuario
    WHERE id_usuario = NEW.id_usuario;
    
    INSERT INTO Bitacora_Reciclaje (ip, id_registro_reciclaje, accion, fecha_accion, detalle)
    VALUES (
        NULL,  -- Dejamos ip como NULL ya que no lo necesitamos
        NEW.id_registro_reciclaje,
        'INSERT',
        CURDATE(),
        CONCAT('Registro creado por ', nombre_usuario, ': ', NEW.cantidad_kg, ' kg de ', NEW.nombre_subtipo)
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
        CURDATE(),
        CONCAT('Registro actualizado por ', nombre_usuario, ': cantidad_kg de ', OLD.cantidad_kg, ' a ', NEW.cantidad_kg)
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
        CURDATE(),
        CONCAT('Registro eliminado por ', nombre_usuario, ': ', OLD.cantidad_kg, ' kg de ', OLD.nombre_subtipo)
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
        CURDATE(),
        CONCAT('Canje creado por ', nombre_usuario, ': ', NEW.puntos_descontados, ' puntos (', NEW.estado, ')')
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
    WHERE id_usuario = @current_user_id;
    
    INSERT INTO Bitacora_Canje (ip, id_canje_recompensa, id_catalogo_recompensa, accion, fecha_accion, detalle)
    VALUES (
        @current_user_ip,
        OLD.id_canje_recompensa,
        OLD.id_catalogo_recompensa,
        'UPDATE',
        CURDATE(),
        CONCAT('Canje actualizado por ', nombre_usuario, ': estado de ', OLD.estado, ' a ', NEW.estado)
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
    WHERE id_usuario = @current_user_id;
    
    INSERT INTO Bitacora_Canje (ip, id_canje_recompensa, id_catalogo_recompensa, accion, fecha_accion, detalle)
    VALUES (
        @current_user_ip,
        OLD.id_canje_recompensa,
        OLD.id_catalogo_recompensa,
        'DELETE',
        CURDATE(),
        CONCAT('Canje eliminado por ', nombre_usuario, ': ', OLD.puntos_descontados, ' puntos (', OLD.estado, ')')
    );
END //

-- after_catalogo_recompensa_insert_bitacora (Auditoría INSERT en Bitacora_Catalogo)

CREATE TRIGGER after_catalogo_recompensa_insert_bitacora
AFTER INSERT ON Catalogo_Recompensa
FOR EACH ROW
BEGIN
    DECLARE nombre_usuario VARCHAR(35);
    SELECT nombre INTO nombre_usuario
    FROM Usuario
    WHERE id_usuario = @current_user_id;
    
    INSERT INTO Bitacora_Catalogo (ip, id_catalogo_recompensa, accion, fecha_accion, detalle)
    VALUES (
        @current_user_ip,
        NEW.id_catalogo_recompensa,
        'INSERT',
        CURDATE(),
        CONCAT('Recompensa creada por ', nombre_usuario, ': ', NEW.nombre)
    );
END //

-- after_catalogo_recompensa_update_bitacora (Auditoría UPDATE en Bitacora_Catalogo)

CREATE TRIGGER after_catalogo_recompensa_update_bitacora
AFTER UPDATE ON Catalogo_Recompensa
FOR EACH ROW
BEGIN
    DECLARE nombre_usuario VARCHAR(35);
    SELECT nombre INTO nombre_usuario
    FROM Usuario
    WHERE id_usuario = @current_user_id;
    
    INSERT INTO Bitacora_Catalogo (ip, id_catalogo_recompensa, accion, fecha_accion, detalle)
    VALUES (
        @current_user_ip,
        NEW.id_catalogo_recompensa,
        'UPDATE',
        CURDATE(),
        CONCAT('Recompensa actualizada por ', nombre_usuario, ': ', OLD.nombre, ' a ', NEW.nombre)
    );
END //

-- after_catalogo_recompensa_delete_bitacora (Auditoría DELETE en Bitacora_Catalogo)

CREATE TRIGGER after_catalogo_recompensa_delete_bitacora
AFTER DELETE ON Catalogo_Recompensa
FOR EACH ROW
BEGIN
    DECLARE nombre_usuario VARCHAR(35);
    SELECT nombre INTO nombre_usuario
    FROM Usuario
    WHERE id_usuario = @current_user_id;
    
    INSERT INTO Bitacora_Catalogo (ip, id_catalogo_recompensa, accion, fecha_accion, detalle)
    VALUES (
        @current_user_ip,
        OLD.id_catalogo_recompensa,
        'DELETE',
        CURDATE(),
        CONCAT('Recompensa eliminada por ', nombre_usuario, ': ', OLD.nombre)
    );
END //
DELIMITER ;

