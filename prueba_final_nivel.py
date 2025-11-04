from controladores import controlador_xp

print('\n' + '='*60)
print('  PRUEBA FINAL: SUBIDA AUTOMÁTICA DE NIVEL')
print('='*60 + '\n')

# Otorgar 300 XP de una vez (suficiente para subir de nivel)
print('⚡ Otorgando 300 XP...\n')
resultado = controlador_xp.otorgar_xp(4, 300, 'prueba_final')

print('RESULTADOS:')
print(f'  • Nivel anterior: {resultado["nivel_anterior"]}')
print(f'  • Nivel nuevo: {resultado["nivel_nuevo"]}')
print(f'  • ¿Subió de nivel? {"✅ SÍ" if resultado["subio_nivel"] else "❌ NO"}')
print(f'  • Niveles ganados: {resultado["niveles_ganados"]}')
print(f'  • XP ganado: {resultado["xp_ganado"]}')
print(f'  • XP actual: {resultado["xp_actual"]}')
print(f'  • XP total acumulado: {resultado["xp_total"]}')
print(f'  • XP para nivel {resultado["nivel_nuevo"]+1}: {resultado["xp_para_siguiente_nivel"]}')

if resultado['insignias_nuevas']:
    print(f'\n🏅 INSIGNIAS DESBLOQUEADAS: {len(resultado["insignias_nuevas"])}')
    for i in resultado['insignias_nuevas']:
        print(f'  • {i["icono"]} {i["nombre"]} (+{i["xp_bonus"]} XP)')

print('\n' + '='*60 + '\n')
