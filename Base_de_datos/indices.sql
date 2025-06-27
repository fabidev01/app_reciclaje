-- 1. Registro_Reciclaje - id_usuario y fecha_registro
CREATE INDEX idx_registro_reciclaje_usuario_fecha ON Registro_Reciclaje (id_usuario, fecha_registro);

-- 2. Bitacora_Acceso - id_usuario y fecha_acceso
CREATE INDEX idx_bitacora_acceso_usuario_fecha ON Bitacora_Acceso (id_usuario, fecha_acceso);

-- 3. Canje_Recompensa - id_usuario y fecha_canje
CREATE INDEX idx_canje_recompensa_usuario_fecha ON Canje_Recompensa (id_usuario, fecha_canje);

-- 4. Catalogo_Recompensa - disponible y puntos_coste
CREATE INDEX idx_catalogo_recompensa_disponible ON Catalogo_Recompensa (disponible, puntos_coste);

-- 5. Usuario - balance_puntos
CREATE INDEX idx_usuario_balance_puntos ON Usuario (balance_puntos);

-- Índice para Registro_Reciclaje
CREATE INDEX idx_registro_reciclaje_usuario ON Registro_Reciclaje (id_usuario);
CREATE INDEX idx_registro_reciclaje_punto ON Registro_Reciclaje (id_punto_reciclaje);
CREATE INDEX idx_registro_reciclaje_material ON Registro_Reciclaje (id_material_reciclable);
CREATE INDEX idx_registro_reciclaje_fecha ON Registro_Reciclaje (fecha_registro);
CREATE INDEX idx_registro_reciclaje_cantidad ON Registro_Reciclaje (cantidad_kg);
CREATE INDEX idx_registro_reciclaje_puntos ON Registro_Reciclaje (puntos_obtenidos);
CREATE INDEX idx_registro_reciclaje_co2 ON Registro_Reciclaje (co2_reducido);

-- Índice para Usuario (para filtrado por nombre y correo)
CREATE INDEX idx_usuario_nombre ON Usuario (nombre);
CREATE INDEX idx_usuario_correo ON Usuario (correo);

-- Índice para Punto_Reciclaje (para filtrado por nombre)
CREATE INDEX idx_punto_reciclaje_nombre ON Punto_Reciclaje (nombre);

-- Índice para Material_Reciclable (para filtrado por nombre)
CREATE INDEX idx_material_reciclable_nombre ON Material_Reciclable (nombre);