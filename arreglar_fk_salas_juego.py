# -*- coding: utf-8 -*-
"""
Script para arreglar la foreign key de salas_juego que tiene RESTRICT
"""

from bd import obtener_conexion

def arreglar_fk_salas_juego():
    """Cambia la FK de salas_juego a CASCADE"""
    conexion = obtener_conexion()
    
    try:
        cursor = conexion.cursor()
        
        print("🔧 Arreglando foreign key de salas_juego...")
        
        # Eliminar la FK existente
        cursor.execute("""
            ALTER TABLE salas_juego
            DROP FOREIGN KEY salas_juego_ibfk_1
        """)
        print("✅ FK antigua eliminada")
        
        # Agregar la FK con CASCADE
        cursor.execute("""
            ALTER TABLE salas_juego
            ADD CONSTRAINT salas_juego_ibfk_1
            FOREIGN KEY (id_cuestionario) REFERENCES cuestionarios(id_cuestionario)
            ON DELETE CASCADE
        """)
        print("✅ FK con CASCADE agregada")
        
        conexion.commit()
        cursor.close()
        conexion.close()
        
        print("\n✅ Operación completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        if 'conexion' in locals():
            conexion.rollback()
            cursor.close()
            conexion.close()

if __name__ == "__main__":
    arreglar_fk_salas_juego()
