-- 1. Puntos de reciclaje disponibles
SELECT 
    pr.id_punto_reciclaje,
    pr.nombre AS punto_reciclaje,
    pr.hora_apertura,
    pr.hora_cierre,
    pr.latitud,
    pr.longitud,
    pr.estado_punto,
    GROUP_CONCAT(mr.nombre) AS materiales_aceptados
FROM Punto_Reciclaje pr
LEFT JOIN Material_Punto_Reciclaje mpr ON pr.id_punto_reciclaje = mpr.id_punto_reciclaje
LEFT JOIN Material_Reciclable mr ON mpr.id_material_reciclable = mr.id_material_reciclable
WHERE pr.estado_punto = 'Disponible'
GROUP BY pr.id_punto_reciclaje
ORDER BY pr.nombre;

-- 2. Materiales reciclables y sus puntos
SELECT 
    mr.id_material_reciclable,
    mr.nombre AS material,
    mr.puntos_por_unidad,
    mr.co2_por_unidad,
    mr.unidad_medida,
    GROUP_CONCAT(pr.nombre) AS puntos_reciclaje
FROM Material_Reciclable mr
LEFT JOIN Material_Punto_Reciclaje mpr ON mr.id_material_reciclable = mpr.id_material_reciclable
LEFT JOIN Punto_Reciclaje pr ON mpr.id_punto_reciclaje = pr.id_punto_reciclaje
GROUP BY mr.id_material_reciclable
ORDER BY mr.nombre;

-- 3. Recompensas disponibles para canje
SELECT 
    cr.id_catalogo_recompensa,
    cr.nombre AS recompensa,
    cr.puntos_coste,
    cr.disponible,
    cr.stock,
    cr.descuento,
    cr.categoria
FROM Catalogo_Recompensa cr
WHERE cr.disponible = TRUE
ORDER BY cr.puntos_coste;

-- 4. Historial de reciclaje de un usuario
SELECT 
    u.nombre AS usuario,
    mr.nombre AS material,
    rr.cantidad_kg,
    rr.puntos_obtenidos,
    rr.co2_reducido,
    DATE_FORMAT(rr.fecha_registro, '%d/%m/%Y') AS fecha_registro,
    rr.nombre_subtipo
FROM Registro_Reciclaje rr
JOIN Usuario u ON rr.id_usuario = u.id_usuario
JOIN Material_Reciclable mr ON rr.id_material_reciclable = mr.id_material_reciclable
WHERE u.id_usuario = 1
ORDER BY rr.fecha_registro DESC;

-- 5. Historial de accesos de un usuario
SELECT 
    u.nombre AS usuario,
    u.correo,
    ba.tipo_acceso,
    DATE_FORMAT(ba.fecha_acceso, '%d/%m/%Y') AS fecha_acceso,
    ba.resultado,
    ba.detalle
FROM Bitacora_Acceso ba
JOIN Usuario u ON ba.id_usuario = u.id_usuario
WHERE u.id_usuario = 1
ORDER BY ba.fecha_acceso DESC;

-- 6. Historial de acciones en el catálogo de recompensas
SELECT 
    bc.id_bitacora_catalogo,
    cr.nombre AS recompensa,
    bc.accion,
    DATE_FORMAT(bc.fecha_accion, '%d/%m/%Y') AS fecha_accion,
    bc.ip
FROM Bitacora_Catalogo bc
JOIN Catalogo_Recompensa cr ON bc.id_catalogo_recompensa = cr.id_catalogo_recompensa
ORDER BY bc.fecha_accion DESC;

-- 7. Impacto ambiental total por fecha
SELECT  
    DATE_FORMAT(iad.fecha_dia, '%d/%m/%Y') AS fecha,  
    SUM(iad.cantidad_reciclada_por_tipo) AS cantidad_reciclada,  
    SUM(iad.co2_reducido_por_tipo) AS co2_reducido  
FROM Impacto_Ambiental_Diario iad  
GROUP BY iad.fecha_dia  
ORDER BY iad.fecha_dia DESC;  

-- 8. Historial de canjes de un usuario
SELECT 
    u.nombre AS usuario,
    cr.nombre AS recompensa,
    rc.puntos_descontados,
    rc.estado,
    DATE_FORMAT(rc.fecha_canje, '%d/%m/%Y') AS fecha_canje
FROM Canje_Recompensa rc
JOIN Usuario u ON rc.id_usuario = u.id_usuario
JOIN Catalogo_Recompensa cr ON rc.id_catalogo_recompensa = cr.id_catalogo_recompensa
WHERE u.id_usuario = 1
ORDER BY rc.fecha_canje DESC;

-- 9. Ranking de usuarios por puntos acumulados
SELECT 
    u.id_usuario,
    u.nombre AS usuario,
    u.correo,
    u.balance_puntos
FROM Usuario u
ORDER BY u.balance_puntos DESC;

-- 10. Donaciones realizadas por los usuarios
SELECT 
    u.nombre AS usuario,
    d.entidad_donacion,
    d.monto_donacion,
    cd.estado,
    cd.puntos_descontados,
    DATE_FORMAT(cd.fecha_canje, '%d/%m/%Y') AS fecha_canje
FROM Canje_Donacion cd
JOIN Usuario u ON cd.id_usuario = u.id_usuario
JOIN Donacion d ON cd.id_donacion = d.id_donacion
ORDER BY cd.fecha_canje DESC;