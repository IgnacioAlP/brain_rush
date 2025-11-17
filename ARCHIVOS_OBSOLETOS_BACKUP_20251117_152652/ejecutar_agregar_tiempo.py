"""
Script para ejecutar la migración de agregar el campo tiempo_por_pregunta a salas_juego
"""
import pymysql
from bd import obtener_conexion

def ejecutar_migracion():
    """Ejecuta el script SQL para agregar el campo tiempo_por_pregunta"""
    try:
        print("🔄 Conectando a la base de datos...")
        
        # Conectar a la base de datos usando la función del proyecto
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        print("✅ Conexión establecida")
        
        # Primero verificar si la columna ya existe
        print("🔍 Verificando si la columna ya existe...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'brain_rush' 
            AND TABLE_NAME = 'salas_juego' 
            AND COLUMN_NAME = 'tiempo_por_pregunta'
        """)
        existe = cursor.fetchone()[0] > 0
        
        if existe:
            print("⚠️  La columna 'tiempo_por_pregunta' ya existe en la tabla")
            print("   No es necesario ejecutar la migración")
        else:
            print("📝 Ejecutando migración...")
            
            # Agregar la columna
            cursor.execute("""
                ALTER TABLE salas_juego 
                ADD COLUMN tiempo_por_pregunta INT DEFAULT 30 AFTER estado
            """)
            conexion.commit()
            print("✅ Columna agregada exitosamente")
        
        print("\n📋 Verificando estructura de tabla...")
        
        # Verificar que la columna existe
        cursor.execute("DESCRIBE salas_juego")
        columnas = cursor.fetchall()
        
        print("\n🔍 Estructura actual de salas_juego:")
        print(f"{'Campo':<25} {'Tipo':<20} {'Null':<8} {'Key':<8} {'Default':<15}")
        print("-" * 80)
        
        tiempo_encontrado = False
        for columna in columnas:
            print(f"{columna[0]:<25} {columna[1]:<20} {columna[2]:<8} {columna[3]:<8} {str(columna[4]):<15}")
            if columna[0] == 'tiempo_por_pregunta':
                tiempo_encontrado = True
        
        if tiempo_encontrado:
            print("\n✅ ¡Campo 'tiempo_por_pregunta' agregado correctamente!")
        else:
            print("\n⚠️  Advertencia: El campo 'tiempo_por_pregunta' no se encontró")
        
        # Cerrar conexión
        cursor.close()
        conexion.close()
        
        print("\n🎉 Proceso completado con éxito")
        return True
        
    except pymysql.err.OperationalError as e:
        print(f"❌ Error de conexión a la base de datos: {e}")
        print("   Verifica que MySQL esté corriendo y la configuración sea correcta")
        return False
        
    except pymysql.err.ProgrammingError as e:
        print(f"❌ Error de SQL: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*80)
    print("  MIGRACIÓN: Agregar campo tiempo_por_pregunta a salas_juego")
    print("="*80)
    print()
    
    confirmacion = input("¿Deseas continuar con la migración? (s/n): ").lower()
    
    if confirmacion == 's':
        print()
        exito = ejecutar_migracion()
        
        if exito:
            print("\n" + "="*80)
            print("  ✅ MIGRACIÓN COMPLETADA")
            print("="*80)
        else:
            print("\n" + "="*80)
            print("  ❌ MIGRACIÓN FALLIDA")
            print("="*80)
    else:
        print("\n❌ Migración cancelada por el usuario")
