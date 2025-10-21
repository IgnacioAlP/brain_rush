# -*- coding: utf-8 -*-
"""Script para aplicar migración de grupos en la BD"""
from bd import obtener_conexion

SQL = '''
ALTER TABLE salas_juego
  ADD COLUMN IF NOT EXISTS grupos_habilitados TINYINT(1) DEFAULT 0,
  ADD COLUMN IF NOT EXISTS num_grupos INT DEFAULT 0;

ALTER TABLE participantes_sala
  ADD COLUMN IF NOT EXISTS id_grupo INT NULL;

CREATE TABLE IF NOT EXISTS grupos_sala (
  id_grupo INT NOT NULL AUTO_INCREMENT,
  id_sala INT NOT NULL,
  nombre_grupo VARCHAR(100) NOT NULL,
  capacidad INT DEFAULT NULL,
  PRIMARY KEY (id_grupo),
  CONSTRAINT FK_grupos_sala_id_sala FOREIGN KEY (id_sala) REFERENCES salas_juego (id_sala) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE INDEX IF NOT EXISTS idx_grupos_sala_id_sala ON grupos_sala (id_sala);
'''


def aplicar_migracion():
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            # MySQL doesn't support ADD COLUMN IF NOT EXISTS before 8.0.13 in some versions; we'll check columns
            # Agregar columnas a salas_juego si no existen
            cursor.execute("SHOW COLUMNS FROM salas_juego LIKE 'grupos_habilitados'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE salas_juego ADD COLUMN grupos_habilitados TINYINT(1) DEFAULT 0")
            cursor.execute("SHOW COLUMNS FROM salas_juego LIKE 'num_grupos'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE salas_juego ADD COLUMN num_grupos INT DEFAULT 0")

            # Agregar columna id_grupo a participantes_sala
            cursor.execute("SHOW COLUMNS FROM participantes_sala LIKE 'id_grupo'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE participantes_sala ADD COLUMN id_grupo INT NULL")

            # Crear tabla grupos_sala si no existe
            cursor.execute("SHOW TABLES LIKE 'grupos_sala'")
            if not cursor.fetchone():
                cursor.execute('''
                CREATE TABLE grupos_sala (
                  id_grupo INT NOT NULL AUTO_INCREMENT,
                  id_sala INT NOT NULL,
                  nombre_grupo VARCHAR(100) NOT NULL,
                  capacidad INT DEFAULT NULL,
                  PRIMARY KEY (id_grupo),
                  CONSTRAINT FK_grupos_sala_id_sala FOREIGN KEY (id_sala) REFERENCES salas_juego (id_sala) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
                ''')
                cursor.execute("CREATE INDEX idx_grupos_sala_id_sala ON grupos_sala (id_sala)")

            conn.commit()
            print('✅ Migración aplicada correctamente')
    except Exception as e:
        print('❌ Error aplicando migración:', e)
    finally:
        conn.close()

if __name__ == '__main__':
    aplicar_migracion()
