# -*- coding: utf-8 -*-
"""
Script para recalcular correctamente los niveles de todos los usuarios
basándose en su XP total acumulado
"""

from bd import obtener_conexion
import math

def calcular_xp_para_nivel(nivel):
    """
    Calcula cuánto XP se necesita para alcanzar un nivel específico
    Fórmula exponencial: 100 * nivel^1.5
    """
    return int(100 * math.pow(nivel, 1.5))

def calcular_nivel_correcto_por_xp(xp_total):
    """
    Calcula el nivel correcto y XP actual basándose en el XP total acumulado
    
    Returns:
        tuple: (nivel_correcto, xp_actual_en_nivel)
    """
    if xp_total == 0:
        return 1, 0
    
    nivel = 1
    xp_gastado = 0
    
    while True:
        xp_necesario = calcular_xp_para_nivel(nivel + 1)
        if xp_gastado + xp_necesario > xp_total:
            # Ya no alcanza para el siguiente nivel
            xp_actual = xp_total - xp_gastado
            return nivel, xp_actual
        
        xp_gastado += xp_necesario
        nivel += 1

def recalcular_todos_los_niveles():
    """
    Recalcula los niveles de todos los usuarios basándose en su XP total
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            print("🔄 Iniciando recalculación de niveles...")
            print("=" * 60)
            
            # Obtener todos los usuarios con XP
            cursor.execute('''
                SELECT e.id_usuario, u.nombre, u.apellidos, 
                       e.xp_actual, e.nivel_actual, e.xp_total_acumulado
                FROM experiencia_usuarios e
                JOIN usuarios u ON e.id_usuario = u.id_usuario
                WHERE u.tipo_usuario = 'estudiante'
                ORDER BY e.xp_total_acumulado DESC
            ''')
            
            usuarios = cursor.fetchall()
            
            if not usuarios:
                print("⚠️ No se encontraron usuarios con experiencia")
                return
            
            print(f"📊 Usuarios encontrados: {len(usuarios)}\n")
            
            usuarios_actualizados = 0
            
            for usuario in usuarios:
                id_usuario, nombre, apellidos, xp_actual, nivel_actual, xp_total = usuario
                
                # Calcular el nivel correcto
                nivel_correcto, xp_actual_correcto = calcular_nivel_correcto_por_xp(xp_total)
                
                print(f"👤 {nombre} {apellidos}")
                print(f"   ID: {id_usuario}")
                print(f"   XP Total Acumulado: {xp_total}")
                print(f"   Nivel Actual (BD): {nivel_actual}")
                print(f"   XP Actual (BD): {xp_actual}")
                print(f"   → Nivel Correcto: {nivel_correcto}")
                print(f"   → XP Actual Correcto: {xp_actual_correcto}")
                
                if nivel_actual != nivel_correcto or xp_actual != xp_actual_correcto:
                    print(f"   ⚠️ DESAJUSTE DETECTADO - Corrigiendo...")
                    
                    # Actualizar en la base de datos
                    cursor.execute('''
                        UPDATE experiencia_usuarios
                        SET nivel_actual = %s,
                            xp_actual = %s
                        WHERE id_usuario = %s
                    ''', (nivel_correcto, xp_actual_correcto, id_usuario))
                    
                    usuarios_actualizados += 1
                    print(f"   ✅ Nivel actualizado de {nivel_actual} a {nivel_correcto}")
                else:
                    print(f"   ✓ Nivel correcto")
                
                print()
            
            conexion.commit()
            
            print("=" * 60)
            print(f"✅ Recalculación completada")
            print(f"📈 Usuarios actualizados: {usuarios_actualizados}")
            print(f"📊 Total procesados: {len(usuarios)}")
            
    except Exception as e:
        print(f"\n❌ Error durante la recalculación: {e}")
        import traceback
        traceback.print_exc()
        conexion.rollback()
    finally:
        conexion.close()

def mostrar_tabla_niveles():
    """
    Muestra una tabla con los niveles y XP necesario para cada uno
    """
    print("\n📊 TABLA DE NIVELES Y XP")
    print("=" * 60)
    print(f"{'Nivel':<8} {'XP Necesario':<15} {'XP Acumulado Total':<20}")
    print("-" * 60)
    
    xp_acumulado = 0
    for nivel in range(1, 21):
        xp_necesario = calcular_xp_para_nivel(nivel)
        print(f"{nivel:<8} {xp_necesario:<15} {xp_acumulado:<20}")
        xp_acumulado += xp_necesario
    
    print("=" * 60)

if __name__ == "__main__":
    print("🎮 SISTEMA DE RECALCULACIÓN DE NIVELES - Brain RUSH")
    print("=" * 60)
    
    # Mostrar tabla de niveles primero
    mostrar_tabla_niveles()
    
    # Confirmar antes de proceder
    print("\n⚠️ Esta operación recalculará los niveles de TODOS los usuarios")
    respuesta = input("¿Deseas continuar? (s/n): ")
    
    if respuesta.lower() == 's':
        recalcular_todos_los_niveles()
    else:
        print("❌ Operación cancelada")
