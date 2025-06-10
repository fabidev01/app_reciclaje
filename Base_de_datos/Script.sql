 
SET SQL_SAFE_UPDATES = 1;
DELETE FROM punto_reciclaje;
delete from material_punto_reciclaje;


CALL insertar_registro_reciclaje(1, 1, 2, 2.0, '2025-05-02', 'B');
select * from registro_reciclaje;
-- Verificar balance de puntos inicial
SELECT * FROM Usuario ;
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

