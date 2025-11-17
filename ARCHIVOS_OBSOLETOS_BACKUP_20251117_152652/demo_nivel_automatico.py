from controladores import controlador_xp
import bd

conn = bd.obtener_conexion()
cursor = conn.cursor()

print(f'\n{"="*70}')
print(f'  DEMOSTRACIÓN: SUBIDA DE NIVEL AUTOMÁTICA')
print(f'{"="*70}\n')

# Simular 15 respuestas correctas
print('🎮 SIMULANDO 15 RESPUESTAS CORRECTAS...\n')

for i in range(1, 16):
    # Obtener estado actual
    cursor.execute('SELECT xp_actual, nivel_actual FROM experiencia_usuarios WHERE id_usuario = 4')
    antes = cursor.fetchone()
    
    if not antes:
        print(f'Respuesta {i}: Usuario no encontrado, creando...')
        cursor.execute('''
            INSERT INTO experiencia_usuarios (id_usuario, xp_actual, nivel_actual, xp_total_acumulado)
            VALUES (4, 0, 1, 0)
        ''')
        conn.commit()
        antes = (0, 1)
    
    nivel_antes = antes[1]
    xp_antes = antes[0]
    
    # Otorgar 10 XP por respuesta correcta (valor base)
    resultado = controlador_xp.otorgar_xp(4, 10, 'respuesta_correcta')
    
    # Mostrar si hubo cambio de nivel
    if resultado['subio_nivel']:
        print(f'✨ Respuesta {i:2d}: {xp_antes:4d} XP → {resultado["xp_actual"]:4d} XP | '
              f'⬆️  NIVEL {resultado["nivel_anterior"]} → NIVEL {resultado["nivel_nuevo"]} 🎉')
    else:
        print(f'   Respuesta {i:2d}: {xp_antes:4d} XP → {resultado["xp_actual"]:4d} XP | '
              f'   Nivel {resultado["nivel_nuevo"]} ({resultado["xp_para_siguiente_nivel"]-resultado["xp_actual"]} XP para nivel {resultado["nivel_nuevo"]+1})')

# Estado final
cursor.execute('SELECT xp_actual, nivel_actual, xp_total_acumulado FROM experiencia_usuarios WHERE id_usuario = 4')
final = cursor.fetchone()

print(f'\n{"="*70}')
print(f'  RESULTADO FINAL')
print(f'{"="*70}\n')
print(f'🏆 Nivel alcanzado: {final[1]}')
print(f'⭐ XP actual: {final[0]}')
print(f'💰 XP total acumulado: {final[2]}')
print(f'🎯 XP necesario para nivel {final[1]+1}: {controlador_xp.calcular_xp_para_nivel(final[1]+1)}')
print(f'\n{"="*70}\n')
