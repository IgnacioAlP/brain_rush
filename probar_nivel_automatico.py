from controladores import controlador_xp
import bd

# Obtener estado actual
conn = bd.obtener_conexion()
cursor = conn.cursor()
cursor.execute('SELECT xp_actual, nivel_actual, xp_total_acumulado FROM experiencia_usuarios WHERE id_usuario = 4')
antes = cursor.fetchone()

print(f'\n{"="*60}')
print(f'  PRUEBA: SUBIDA DE NIVEL AUTOMÁTICA')
print(f'{"="*60}\n')

print(f'📊 ESTADO INICIAL:')
print(f'   Nivel: {antes[1]}')
print(f'   XP actual: {antes[0]}')
print(f'   XP total acumulado: {antes[2]}')

# Calcular XP necesario para subir de nivel
xp_necesario = controlador_xp.calcular_xp_para_nivel(antes[1] + 1)
print(f'\n🎯 XP necesario para nivel {antes[1]+1}: {xp_necesario}')

# Otorgar XP suficiente para subir de nivel
print(f'\n⚡ Otorgando {xp_necesario} XP...\n')
resultado = controlador_xp.otorgar_xp(4, xp_necesario, 'prueba_nivel')

# Mostrar resultados
print(f'{"="*60}')
print(f'  RESULTADOS')
print(f'{"="*60}\n')

print(f'✅ ¿Subió de nivel? {resultado["subio_nivel"]}')
print(f'📈 Nivel anterior: {resultado["nivel_anterior"]} → Nivel nuevo: {resultado["nivel_nuevo"]}')
print(f'⭐ Niveles ganados: {resultado["niveles_ganados"]}')
print(f'💰 XP ganado en esta acción: {resultado["xp_ganado"]}')
print(f'📊 XP actual (para siguiente nivel): {resultado["xp_actual"]}')
print(f'🎯 XP necesario para siguiente nivel: {resultado["xp_para_siguiente_nivel"]}')
print(f'🏆 XP total acumulado: {resultado["xp_total"]}')

if resultado.get('insignias_nuevas'):
    print(f'\n🏅 INSIGNIAS DESBLOQUEADAS: {len(resultado["insignias_nuevas"])}')
    for insignia in resultado['insignias_nuevas']:
        print(f'   • {insignia["icono"]} {insignia["nombre"]} (+{insignia["xp_bonus"]} XP bonus)')
else:
    print(f'\n🏅 No se desbloquearon nuevas insignias')

print(f'\n{"="*60}\n')
