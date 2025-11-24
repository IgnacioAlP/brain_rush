from controladores import controlador_xp

print('\n' + '='*60)
print('  PRUEBA: obtener_progreso_insignias')
print('='*60 + '\n')

try:
    insignias = controlador_xp.obtener_progreso_insignias(4)
    print(f'✅ Función ejecutada correctamente')
    print(f'📊 Insignias bloqueadas encontradas: {len(insignias)}\n')
    
    if insignias:
        print('Primeras 5 insignias bloqueadas:')
        for i in insignias[:5]:
            print(f'  • {i["icono"]} {i["nombre"]}')
            print(f'    Progreso: {i["porcentaje"]}% ({i["valor_actual"]}/{i["requisito_valor"]} {i["requisito_tipo"]})')
    else:
        print('No hay insignias bloqueadas (todas desbloqueadas o sin datos)')
    
    print('\n' + '='*60 + '\n')
except Exception as e:
    print(f'❌ ERROR: {e}')
    import traceback
    traceback.print_exc()
