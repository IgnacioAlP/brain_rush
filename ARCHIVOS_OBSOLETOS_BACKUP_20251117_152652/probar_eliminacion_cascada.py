# -*- coding: utf-8 -*-
"""
Script para probar la eliminación en cascada de usuarios
"""

from bd import obtener_conexion
from controladores import controlador_usuario

def verificar_datos_usuario(usuario_id):
    """Verifica cuántos registros relacionados tiene un usuario"""
    conexion = obtener_conexion()
    
    try:
        cursor = conexion.cursor()
        
        # Obtener información del usuario
        cursor.execute("""
            SELECT id_usuario, nombre, apellidos, tipo_usuario 
            FROM usuarios 
            WHERE id_usuario = %s
        """, (usuario_id,))
        usuario = cursor.fetchone()
        
        if not usuario:
            print(f"❌ Usuario {usuario_id} no encontrado")
            cursor.close()
            conexion.close()
            return None
        
        id_u, nombre, apellidos, tipo = usuario
        print(f"\n👤 Usuario: {nombre} {apellidos} (ID: {id_u})")
        print(f"   Tipo: {tipo}")
        print(f"\n📊 Datos relacionados:")
        
        tablas_a_verificar = [
            ('experiencia_usuarios', 'id_usuario'),
            ('estadisticas_juego', 'id_usuario'),
            ('insignias_usuarios', 'id_usuario'),
            ('historial_xp', 'id_usuario'),
            ('participantes_sala', 'id_usuario'),
            ('respuestas_participantes', 'id_participante'),
            ('ranking_sala', 'id_participante'),
            ('participaciones', 'id_estudiante'),
            ('ranking', 'id_estudiante'),
            ('respuestas_estudiantes', 'id_estudiante'),
            ('recompensas_otorgadas', 'id_estudiante'),
            ('usuario_roles', 'id_usuario'),
        ]
        
        total_registros = 0
        
        for tabla, columna in tablas_a_verificar:
            try:
                if 'participante' in columna:
                    # Para tablas que usan id_participante, necesitamos hacer un JOIN
                    cursor.execute(f"""
                        SELECT COUNT(*) 
                        FROM {tabla} t
                        INNER JOIN participantes_sala ps ON t.id_participante = ps.id_participante
                        WHERE ps.id_usuario = %s
                    """, (usuario_id,))
                else:
                    cursor.execute(f"SELECT COUNT(*) FROM {tabla} WHERE {columna} = %s", (usuario_id,))
                
                count = cursor.fetchone()[0]
                if count > 0:
                    print(f"   • {tabla}: {count} registros")
                    total_registros += count
            except Exception as e:
                # Tabla no existe, ignorar
                pass
        
        if tipo == 'docente':
            # Verificar cuestionarios
            cursor.execute("SELECT COUNT(*) FROM cuestionarios WHERE id_docente = %s", (usuario_id,))
            count = cursor.fetchone()[0]
            if count > 0:
                print(f"   • cuestionarios: {count} registros")
                total_registros += count
            
            # Verificar salas
            cursor.execute("SELECT COUNT(*) FROM salas_juego WHERE id_docente = %s", (usuario_id,))
            count = cursor.fetchone()[0]
            if count > 0:
                print(f"   • salas_juego: {count} registros")
                total_registros += count
        
        print(f"\n📈 Total de registros relacionados: {total_registros}")
        
        cursor.close()
        conexion.close()
        
        return usuario
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if 'conexion' in locals():
            cursor.close()
            conexion.close()
        return None

def probar_eliminacion():
    """Prueba la eliminación en cascada"""
    print("=" * 60)
    print("🧪 PRUEBA DE ELIMINACIÓN EN CASCADA")
    print("=" * 60)
    
    # Listar usuarios disponibles
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id_usuario, nombre, apellidos, tipo_usuario 
        FROM usuarios 
        ORDER BY tipo_usuario, nombre
    """)
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    print("\n📋 Usuarios disponibles:\n")
    for u in usuarios:
        print(f"   {u[0]:3d}. {u[1]} {u[2]} ({u[3]})")
    
    print("\n" + "=" * 60)
    usuario_id = input("\n🔍 Ingresa el ID del usuario a verificar (o 0 para cancelar): ")
    
    try:
        usuario_id = int(usuario_id)
        if usuario_id == 0:
            print("\n❌ Operación cancelada")
            return
        
        # Verificar datos antes de eliminar
        usuario = verificar_datos_usuario(usuario_id)
        
        if not usuario:
            return
        
        print("\n" + "=" * 60)
        respuesta = input("\n⚠️ ¿Deseas ELIMINAR este usuario y todos sus datos? (s/n): ")
        
        if respuesta.lower() == 's':
            print("\n🗑️ Eliminando usuario...")
            exito, mensaje = controlador_usuario.eliminar_usuario_completo(usuario_id)
            
            if exito:
                print(f"\n✅ {mensaje}")
                
                # Verificar que los datos fueron eliminados
                print("\n🔍 Verificando eliminación...")
                verificar_datos_usuario(usuario_id)
            else:
                print(f"\n❌ {mensaje}")
        else:
            print("\n❌ Eliminación cancelada")
            
    except ValueError:
        print("\n❌ ID inválido")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    probar_eliminacion()
