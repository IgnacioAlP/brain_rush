# -*- coding: utf-8 -*-
"""
Script para probar la visualización de todas las insignias
"""

from controladores import controlador_xp
from bd import obtener_conexion

def probar_insignias():
    print("🎖️ PRUEBA DE VISUALIZACIÓN DE INSIGNIAS")
    print("=" * 60)
    
    # Obtener un usuario
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT id_usuario, nombre, apellidos
                FROM usuarios
                WHERE tipo_usuario = 'estudiante'
                LIMIT 1
            ''')
            
            usuario = cursor.fetchone()
            if not usuario:
                print("❌ No hay usuarios")
                return
            
            id_usuario, nombre, apellidos = usuario
            print(f"\n👤 Usuario: {nombre} {apellidos} (ID: {id_usuario})")
            
    finally:
        conexion.close()
    
    # Obtener todas las insignias
    print("\n📋 Obteniendo todas las insignias...")
    insignias = controlador_xp.obtener_todas_insignias_usuario(id_usuario)
    
    print(f"\n✅ Total de insignias: {len(insignias)}")
    
    desbloqueadas = [i for i in insignias if i['desbloqueada']]
    bloqueadas = [i for i in insignias if not i['desbloqueada']]
    
    print(f"   🔓 Desbloqueadas: {len(desbloqueadas)}")
    print(f"   🔒 Bloqueadas: {len(bloqueadas)}")
    
    print("\n" + "=" * 60)
    print("🔓 INSIGNIAS DESBLOQUEADAS:")
    print("-" * 60)
    
    if desbloqueadas:
        for ins in desbloqueadas[:5]:  # Mostrar solo las primeras 5
            print(f"\n   {ins['icono']} {ins['nombre']} ({ins['rareza']})")
            print(f"      {ins['descripcion']}")
            if ins['fecha_obtencion']:
                print(f"      Obtenida: {ins['fecha_obtencion']}")
    else:
        print("   No tienes insignias desbloqueadas aún")
    
    print("\n" + "=" * 60)
    print("🔒 INSIGNIAS BLOQUEADAS (Primeras 5):")
    print("-" * 60)
    
    if bloqueadas:
        for ins in bloqueadas[:5]:
            print(f"\n   🔒 {ins['nombre']} ({ins['rareza']})")
            print(f"      {ins['descripcion']}")
            print(f"      Progreso: {ins['progreso']}%")
    else:
        print("   ¡Has desbloqueado todas las insignias!")
    
    print("\n" + "=" * 60)
    print("\n💡 RESUMEN POR RAREZA:")
    
    for rareza in ['legendario', 'epico', 'raro', 'comun']:
        ins_rareza = [i for i in insignias if i['rareza'] == rareza]
        desb_rareza = [i for i in ins_rareza if i['desbloqueada']]
        print(f"   {rareza.upper()}: {len(desb_rareza)}/{len(ins_rareza)}")

if __name__ == "__main__":
    probar_insignias()
