-- 1 Rol
DELIMITER //
CREATE PROCEDURE insertar_rol(
    IN p_nombre VARCHAR(35),
    IN p_descripcion TEXT
)
BEGIN
    INSERT INTO Rol (nombre, descripcion)
    VALUES (p_nombre, p_descripcion);
END //

CREATE PROCEDURE actualizar_rol(
    IN p_id_rol INT,
    IN p_nombre VARCHAR(35),
    IN p_descripcion TEXT
)
BEGIN
    UPDATE Rol
    SET nombre = p_nombre,
        descripcion = p_descripcion
    WHERE id_rol = p_id_rol;
END //

CREATE PROCEDURE eliminar_rol(
    IN p_id_rol INT
)
BEGIN
    DELETE FROM Rol WHERE id_rol = p_id_rol;
END //

-- 2 Permiso
CREATE PROCEDURE insertar_permiso(
    IN p_nombre VARCHAR(35)
)
BEGIN
    INSERT INTO Permiso (nombre)
    VALUES (p_nombre);
END //

CREATE PROCEDURE actualizar_permiso(
    IN p_id_permiso INT,
    IN p_nombre VARCHAR(35)
)
BEGIN
    UPDATE Permiso
    SET nombre = p_nombre
    WHERE id_permiso = p_id_permiso;
END //

CREATE PROCEDURE eliminar_permiso(
    IN p_id_permiso INT
)
BEGIN
    DELETE FROM Permiso WHERE id_permiso = p_id_permiso;
END //

-- 3 Rol Permiso
CREATE PROCEDURE insertar_rol_permiso(
    IN p_id_rol INT,
    IN p_id_permiso INT
)
BEGIN
    INSERT INTO Rol_Permiso (id_rol, id_permiso)
    VALUES (p_id_rol, p_id_permiso);
END //

CREATE PROCEDURE actualizar_rol_permiso(
    IN p_id_rol INT,
    IN p_id_permiso INT,
    IN p_nuevo_id_rol INT,
    IN p_nuevo_id_permiso INT
)
BEGIN
    UPDATE Rol_Permiso
    SET id_rol = p_nuevo_id_rol,
        id_permiso = p_nuevo_id_permiso
    WHERE id_rol = p_id_rol AND id_permiso = p_id_permiso;
END //

CREATE PROCEDURE eliminar_rol_permiso(
    IN p_id_rol INT,
    IN p_id_permiso INT
)
BEGIN
    DELETE FROM Rol_Permiso WHERE id_rol = p_id_rol AND id_permiso = p_id_permiso;
END //

-- 4 Usuario
CREATE PROCEDURE insertar_usuario(
    IN p_nombre VARCHAR(35),
    IN p_correo VARCHAR(50),
    IN p_telefono VARCHAR(10),
    IN p_balance_puntos INT,
    IN p_fecha_registro DATE,
    IN p_contraseña VARCHAR(200),
    IN p_ip VARCHAR(45),
    IN p_id_rol INT
)
BEGIN
    INSERT INTO Usuario (nombre, correo, telefono, balance_puntos, fecha_registro, contraseña, ip, id_rol)
    VALUES (p_nombre, p_correo, p_telefono, p_balance_puntos, p_fecha_registro, p_contraseña, p_ip, p_id_rol);
END //

CREATE PROCEDURE actualizar_usuario(
    IN p_id_usuario INT,
    IN p_nombre VARCHAR(35),
    IN p_correo VARCHAR(50),
    IN p_telefono VARCHAR(10),
    IN p_balance_puntos INT,
    IN p_contraseña VARCHAR(200),
    IN p_ip VARCHAR(45),
    IN p_id_rol INT
)
BEGIN
    UPDATE Usuario
    SET nombre = p_nombre,
        correo = p_correo,
        telefono = p_telefono,
        balance_puntos = p_balance_puntos,
        contraseña = p_contraseña,
        ip = p_ip,
        id_rol = p_id_rol
    WHERE id_usuario = p_id_usuario;
END //

CREATE PROCEDURE eliminar_usuario(
    IN p_id_usuario INT
)
BEGIN
    DELETE FROM Usuario WHERE id_usuario = p_id_usuario;
END //

-- 5 Material Reciclable

CREATE PROCEDURE insertar_material_reciclable(
    IN p_nombre VARCHAR(35),
    IN p_puntos_por_unidad INT,
    IN p_co2_por_unidad FLOAT,
    IN p_unidad_medida VARCHAR(10)
)
BEGIN
    INSERT INTO Material_Reciclable (nombre, puntos_por_unidad, co2_por_unidad, unidad_medida)
    VALUES (p_nombre, p_puntos_por_unidad, p_co2_por_unidad, p_unidad_medida);
END //

CREATE PROCEDURE actualizar_material_reciclable(
    IN p_id_material_reciclable INT,
    IN p_nombre VARCHAR(35),
    IN p_puntos_por_unidad INT,
    IN p_co2_por_unidad FLOAT,
    IN p_unidad_medida VARCHAR(10)
)
BEGIN
    UPDATE Material_Reciclable
    SET nombre = p_nombre,
        puntos_por_unidad = p_puntos_por_unidad,
        co2_por_unidad = p_co2_por_unidad,
        unidad_medida = p_unidad_medida
    WHERE id_material_reciclable = p_id_material_reciclable;
END //

CREATE PROCEDURE eliminar_material_reciclable(
    IN p_id_material_reciclable INT
)
BEGIN
    DELETE FROM Material_Reciclable WHERE id_material_reciclable = p_id_material_reciclable;
END //

-- 6 Punto Reciclaje

CREATE PROCEDURE insertar_punto_reciclaje(
    IN p_nombre VARCHAR(35),
    IN p_capacidad_maxima INT,
    IN p_hora_apertura TIME,
    IN p_hora_cierre TIME,
    IN p_latitud DECIMAL(10,8),
    IN p_longitud DECIMAL(11,8),
    IN p_estado_punto VARCHAR(15)
)
BEGIN
    INSERT INTO Punto_Reciclaje (nombre, capacidad_maxima, hora_apertura, hora_cierre, latitud, longitud, estado_punto)
    VALUES (p_nombre, p_capacidad_maxima, p_hora_apertura, p_hora_cierre, p_latitud, p_longitud, p_estado_punto);
END //

CREATE PROCEDURE actualizar_punto_reciclaje(
    IN p_id_punto_reciclaje INT,
    IN p_nombre VARCHAR(35),
    IN p_capacidad_maxima INT,
    IN p_hora_apertura TIME,
    IN p_hora_cierre TIME,
    IN p_latitud DECIMAL(10,8),
    IN p_longitud DECIMAL(11,8),
    IN p_estado_punto VARCHAR(15)
)
BEGIN
    UPDATE Punto_Reciclaje
    SET nombre = p_nombre,
        capacidad_maxima = p_capacidad_maxima,
        hora_apertura = p_hora_apertura,
        hora_cierre = p_hora_cierre,
        latitud = p_latitud,
        longitud = p_longitud,
        estado_punto = p_estado_punto
    WHERE id_punto_reciclaje = p_id_punto_reciclaje;
END //

CREATE PROCEDURE eliminar_punto_reciclaje(
    IN p_id_punto_reciclaje INT
)
BEGIN
    DELETE FROM Punto_Reciclaje WHERE id_punto_reciclaje = p_id_punto_reciclaje;
END //

-- 7 Material Punto Reciclaje

CREATE PROCEDURE insertar_material_punto_reciclaje(
    IN p_id_material_reciclable INT,
    IN p_id_punto_reciclaje INT,
    IN p_condiciones_especificas TEXT
)
BEGIN
    INSERT INTO Material_Punto_Reciclaje (id_material_reciclable, id_punto_reciclaje, condiciones_especificas)
    VALUES (p_id_material_reciclable, p_id_punto_reciclaje, p_condiciones_especificas);
END //

CREATE PROCEDURE actualizar_material_punto_reciclaje(
    IN p_id_material_reciclable INT,
    IN p_id_punto_reciclaje INT,
    IN p_condiciones_especificas TEXT
)
BEGIN
    UPDATE Material_Punto_Reciclaje
    SET condiciones_especificas = p_condiciones_especificas
    WHERE id_material_reciclable = p_id_material_reciclable AND id_punto_reciclaje = p_id_punto_reciclaje;
END //

CREATE PROCEDURE eliminar_material_punto_reciclaje(
    IN p_id_material_reciclable INT,
    IN p_id_punto_reciclaje INT
)
BEGIN
    DELETE FROM Material_Punto_Reciclaje WHERE id_material_reciclable = p_id_material_reciclable AND id_punto_reciclaje = p_id_punto_reciclaje;
END // 

-- 8 Registro Reciclaje
DELIMITER //
CREATE PROCEDURE insertar_registro_reciclaje(
    IN p_id_usuario INT,
    IN p_id_punto_reciclaje INT,
    IN p_id_material_reciclable INT,
    IN p_cantidad_kg FLOAT,
    IN p_fecha_registro DATE,
    IN p_nombre_subtipo VARCHAR(35)
)
BEGIN
    INSERT INTO Registro_Reciclaje (id_usuario, id_punto_reciclaje, id_material_reciclable, cantidad_kg, fecha_registro, nombre_subtipo)
    VALUES (p_id_usuario, p_id_punto_reciclaje, p_id_material_reciclable, p_cantidad_kg, p_fecha_registro, p_nombre_subtipo);
END //
CREATE PROCEDURE actualizar_registro_reciclaje(
    IN p_id_registro_reciclaje INT,
    IN p_id_usuario INT,
    IN p_id_punto_reciclaje INT,
    IN p_id_material_reciclable INT,
    IN p_cantidad_kg FLOAT,
    IN p_fecha_registro DATE,
    IN p_nombre_subtipo VARCHAR(35)
)
BEGIN
    UPDATE Registro_Reciclaje
    SET id_usuario = p_id_usuario,
        id_punto_reciclaje = p_id_punto_reciclaje,
        id_material_reciclable = p_id_material_reciclable,
        cantidad_kg = p_cantidad_kg,
        fecha_registro = p_fecha_registro,
        nombre_subtipo = p_nombre_subtipo
    WHERE id_registro_reciclaje = p_id_registro_reciclaje;
END //

CREATE PROCEDURE eliminar_registro_reciclaje(
    IN p_id_registro_reciclaje INT
)
BEGIN
    DELETE FROM Registro_Reciclaje WHERE id_registro_reciclaje = p_id_registro_reciclaje;
END //

-- 9 Catalogo Recompensa

CREATE PROCEDURE insertar_catalogo_recompensa(
    IN p_nombre VARCHAR(35),
    IN p_puntos_coste INT,
    IN p_disponible BOOLEAN,
    IN p_stock INT,
    IN p_descuento FLOAT,
    IN p_categoria VARCHAR(35),
	IN p_ruta_imagen VARCHAR(255)
)
BEGIN
    INSERT INTO Catalogo_Recompensa (nombre, puntos_coste, disponible, stock, descuento, categoria, ruta_imagen)
    VALUES (p_nombre, p_puntos_coste, p_disponible, p_stock, p_descuento, p_categoria, p_ruta_imagen);
END //

CREATE PROCEDURE actualizar_catalogo_recompensa(
    IN p_id_catalogo_recompensa INT,
    IN p_nombre VARCHAR(35),
    IN p_puntos_coste INT,
    IN p_disponible BOOLEAN,
    IN p_stock INT,
    IN p_descuento FLOAT,
    IN p_categoria VARCHAR(35),
	IN p_ruta_imagen VARCHAR(255)
)
BEGIN
    UPDATE Catalogo_Recompensa
    SET nombre = p_nombre,
        puntos_coste = p_puntos_coste,
        disponible = p_disponible,
        stock = p_stock,
        descuento = p_descuento,
        categoria = p_categoria,
        ruta_imagen = p_ruta_imagen
    WHERE id_catalogo_recompensa = p_id_catalogo_recompensa;
END //

CREATE PROCEDURE eliminar_catalogo_recompensa(
    IN p_id_catalogo_recompensa INT
)
BEGIN
    DELETE FROM Catalogo_Recompensa WHERE id_catalogo_recompensa = p_id_catalogo_recompensa;
END //

-- 10 Donacion

CREATE PROCEDURE insertar_donacion(
    IN p_nombre VARCHAR(35),
    IN p_entidad_donacion VARCHAR(35),
    IN p_monto_donacion FLOAT,
    IN p_ruta_imagen VARCHAR(255)
)
BEGIN
    INSERT INTO Donacion (nombre, entidad_donacion, monto_donacion, ruta_imagen)
    VALUES (p_nombre, p_entidad_donacion, p_monto_donacion, p_ruta_imagen);
END //

CREATE PROCEDURE actualizar_donacion(
    IN p_id_donacion INT,
    IN p_nombre VARCHAR(35),
    IN p_entidad_donacion VARCHAR(35),
    IN p_monto_donacion FLOAT,
    IN p_ruta_imagen VARCHAR(255)
)
BEGIN
    UPDATE Donacion
    SET nombre = p_nombre,
        entidad_donacion = p_entidad_donacion,
        monto_donacion = p_monto_donacion,
        ruta_imagen = p_ruta_imagen
    WHERE id_donacion = p_id_donacion;
END //
CREATE PROCEDURE eliminar_donacion(
    IN p_id_donacion INT
)
BEGIN
    DELETE FROM Donacion WHERE id_donacion = p_id_donacion;
END //

-- 11 Canje Recompensa

CREATE PROCEDURE insertar_canje_recompensa(
    IN p_id_usuario INT,
    IN p_id_catalogo_recompensa INT,
    IN p_estado VARCHAR(35),
    IN p_fecha_canje DATE,
    IN p_puntos_descontados INT
)
BEGIN
    INSERT INTO Canje_Recompensa (id_usuario, id_catalogo_recompensa, estado, fecha_canje, puntos_descontados)
    VALUES (p_id_usuario, p_id_catalogo_recompensa, p_estado, p_fecha_canje, p_puntos_descontados);
END //

CREATE PROCEDURE actualizar_canje_recompensa(
    IN p_id_canje_recompensa INT,
    IN p_id_usuario INT,
    IN p_id_catalogo_recompensa INT,
    IN p_estado VARCHAR(35),
    IN p_fecha_canje DATE,
    IN p_puntos_descontados INT
)
BEGIN
    UPDATE Canje_Recompensa
    SET id_usuario = p_id_usuario,
        id_catalogo_recompensa = p_id_catalogo_recompensa,
        estado = p_estado,
        fecha_canje = p_fecha_canje,
        puntos_descontados = p_puntos_descontados
    WHERE id_canje_recompensa = p_id_canje_recompensa;
END //
CREATE PROCEDURE eliminar_canje_recompensa(
    IN p_id_canje_recompensa INT
)
BEGIN
    DELETE FROM Canje_Recompensa WHERE id_canje_recompensa = p_id_canje_recompensa;
END //


-- 12 Canje Donacion

CREATE PROCEDURE insertar_canje_donacion(
    IN p_id_usuario INT,
    IN p_id_donacion INT,
    IN p_estado VARCHAR(35),
    IN p_fecha_canje DATE,
    IN p_puntos_descontados INT
)
BEGIN
    INSERT INTO Canje_Donacion (id_usuario, id_donacion, estado, fecha_canje, puntos_descontados)
    VALUES (p_id_usuario, p_id_donacion, p_estado, p_fecha_canje, p_puntos_descontados);
END //
CREATE PROCEDURE actualizar_canje_donacion(
    IN p_id_canje_donacion INT,
    IN p_id_usuario INT,
    IN p_id_donacion INT,
    IN p_estado VARCHAR(35),
    IN p_fecha_canje DATE,
    IN p_puntos_descontados INT
)
BEGIN
    UPDATE Canje_Donacion
    SET id_usuario = p_id_usuario,
        id_donacion = p_id_donacion,
        estado = p_estado,
        fecha_canje = p_fecha_canje,
        puntos_descontados = p_puntos_descontados
    WHERE id_canje_donacion = p_id_canje_donacion;
END //

CREATE PROCEDURE eliminar_canje_donacion(
    IN p_id_canje_donacion INT
)
BEGIN
    DELETE FROM Canje_Donacion WHERE id_canje_donacion = p_id_canje_donacion;
END //

DELIMITER ;
