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