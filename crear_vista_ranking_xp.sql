-- ================================================================================
-- CREAR VISTA RANKING_XP PARA BRAIN RUSH
-- ================================================================================
USE brain_rush;

-- Eliminar la vista si existe
DROP VIEW IF EXISTS ranking_xp;

-- Crear vista de ranking de XP
CREATE VIEW ranking_xp AS
SELECT 
    u.id_usuario,
    CONCAT(u.nombre, ' ', u.apellidos) as nombre_completo,
    u.email,
    e.nivel_actual,
    e.xp_actual,
    e.xp_total_acumulado,
    (SELECT COUNT(DISTINCT id_insignia) 
     FROM insignias_usuarios 
     WHERE id_usuario = u.id_usuario) as total_insignias,
    ROW_NUMBER() OVER (ORDER BY e.nivel_actual DESC, e.xp_actual DESC) as posicion_ranking
FROM usuarios u
JOIN experiencia_usuarios e ON u.id_usuario = e.id_usuario
WHERE u.tipo_usuario = 'estudiante'
ORDER BY e.nivel_actual DESC, e.xp_actual DESC;

-- Verificación
SELECT '✅ Vista ranking_xp creada exitosamente' as resultado;

-- Probar la vista
SELECT * FROM ranking_xp LIMIT 10;
