# -*- coding: utf-8 -*-
"""Script temporal para ejecutar el SQL de crear tabla participantes_sala"""

import pymysql
from bd import obtener_conexion

def ejecutar_sql():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        print("🔧 Eliminando tabla participantes_sala si existe...")
        cursor.execute("DROP TABLE IF EXISTS `participantes_sala`")
        
        print("🔨 Creando tabla participantes_sala...")
        sql_create = """
        CREATE TABLE `participantes_sala` (
          `id_participante` INT NOT NULL AUTO_INCREMENT,
          `id_sala` INT NOT NULL,
          `id_usuario` INT DEFAULT NULL,
          `nombre_participante` VARCHAR(100) NOT NULL,
          `fecha_union` DATETIME DEFAULT CURRENT_TIMESTAMP,
          `estado` VARCHAR(20) DEFAULT 'esperando',
          PRIMARY KEY (`id_participante`),
          CONSTRAINT `FK_participantes_sala_id_sala` FOREIGN KEY (`id_sala`) REFERENCES `salas_juego` (`id_sala`) ON DELETE CASCADE,
          CONSTRAINT `FK_participantes_sala_id_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE SET NULL,
          CONSTRAINT `CK_participantes_sala_estado` CHECK (`estado` IN ('esperando', 'jugando', 'finalizado', 'desconectado'))
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """
        cursor.execute(sql_create)
        
        print("📊 Creando índices...")
        cursor.execute("CREATE INDEX `idx_participantes_sala_id_sala` ON `participantes_sala` (`id_sala`)")
        cursor.execute("CREATE INDEX `idx_participantes_sala_estado` ON `participantes_sala` (`estado`)")
        
        conexion.commit()
        
        print("\n✅ ¡Tabla participantes_sala creada exitosamente!")
        
        # Verificar
        cursor.execute("SHOW TABLES LIKE 'participantes_sala'")
        result = cursor.fetchone()
        if result:
            print("✅ Tabla verificada en la base de datos")
            cursor.execute("DESCRIBE participantes_sala")
            print("\n📋 Estructura de la tabla:")
            for row in cursor.fetchall():
                print(f"  - {row[0]}: {row[1]}")
        
        cursor.close()
        conexion.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ejecutar_sql()
