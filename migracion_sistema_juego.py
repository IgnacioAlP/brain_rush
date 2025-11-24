# -*- coding: utf-8 -*-
"""Script para crear el sistema de juego en tiempo real"""

import pymysql
from bd import obtener_conexion

def ejecutar_migracion():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        print("🎮 Creando sistema de juego en tiempo real...")
        
        # 1. Tabla estado_juego_sala
        print("\n📊 Creando tabla estado_juego_sala...")
        cursor.execute("DROP TABLE IF EXISTS estado_juego_sala")
        cursor.execute("""
            CREATE TABLE estado_juego_sala (
              id_estado INT NOT NULL AUTO_INCREMENT,
              id_sala INT NOT NULL,
              pregunta_actual INT NOT NULL DEFAULT 0,
              tiempo_inicio_pregunta DATETIME NULL,
              estado_pregunta VARCHAR(20) DEFAULT 'esperando',
              PRIMARY KEY (id_estado),
              UNIQUE KEY UK_estado_sala (id_sala),
              CONSTRAINT FK_estado_juego_id_sala FOREIGN KEY (id_sala) 
                REFERENCES salas_juego (id_sala) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """)
        print("✅ Tabla estado_juego_sala creada")
        
        # 2. Tabla respuestas_participantes
        print("\n📝 Creando tabla respuestas_participantes...")
        cursor.execute("DROP TABLE IF EXISTS respuestas_participantes")
        cursor.execute("""
            CREATE TABLE respuestas_participantes (
              id_respuesta_participante INT NOT NULL AUTO_INCREMENT,
              id_participante INT NOT NULL,
              id_sala INT NOT NULL,
              id_pregunta INT NOT NULL,
              id_opcion_seleccionada INT NULL,
              tiempo_respuesta DECIMAL(10,3) NOT NULL,
              es_correcta TINYINT(1) DEFAULT 0,
              puntaje_obtenido INT DEFAULT 0,
              fecha_respuesta DATETIME DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (id_respuesta_participante),
              UNIQUE KEY UK_participante_pregunta (id_participante, id_sala, id_pregunta),
              CONSTRAINT FK_respuestas_part_participante FOREIGN KEY (id_participante) 
                REFERENCES participantes_sala (id_participante) ON DELETE CASCADE,
              CONSTRAINT FK_respuestas_part_sala FOREIGN KEY (id_sala) 
                REFERENCES salas_juego (id_sala) ON DELETE CASCADE,
              CONSTRAINT FK_respuestas_part_pregunta FOREIGN KEY (id_pregunta) 
                REFERENCES preguntas (id_pregunta) ON DELETE CASCADE,
              CONSTRAINT FK_respuestas_part_opcion FOREIGN KEY (id_opcion_seleccionada) 
                REFERENCES opciones_respuesta (id_opcion) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """)
        print("✅ Tabla respuestas_participantes creada")
        
        # Índices para respuestas_participantes
        print("📊 Creando índices para respuestas_participantes...")
        cursor.execute("CREATE INDEX idx_respuestas_part_sala ON respuestas_participantes (id_sala)")
        cursor.execute("CREATE INDEX idx_respuestas_part_pregunta ON respuestas_participantes (id_pregunta)")
        cursor.execute("CREATE INDEX idx_respuestas_part_tiempo ON respuestas_participantes (tiempo_respuesta)")
        print("✅ Índices creados")
        
        # 3. Tabla ranking_sala
        print("\n🏆 Creando tabla ranking_sala...")
        cursor.execute("DROP TABLE IF EXISTS ranking_sala")
        cursor.execute("""
            CREATE TABLE ranking_sala (
              id_ranking_sala INT NOT NULL AUTO_INCREMENT,
              id_participante INT NOT NULL,
              id_sala INT NOT NULL,
              puntaje_total INT DEFAULT 0,
              respuestas_correctas INT DEFAULT 0,
              tiempo_total_respuestas DECIMAL(10,3) DEFAULT 0,
              posicion INT DEFAULT NULL,
              PRIMARY KEY (id_ranking_sala),
              UNIQUE KEY UK_ranking_participante_sala (id_participante, id_sala),
              CONSTRAINT FK_ranking_sala_participante FOREIGN KEY (id_participante) 
                REFERENCES participantes_sala (id_participante) ON DELETE CASCADE,
              CONSTRAINT FK_ranking_sala_sala FOREIGN KEY (id_sala) 
                REFERENCES salas_juego (id_sala) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """)
        print("✅ Tabla ranking_sala creada")
        
        # Índice para ranking
        print("📊 Creando índice para ranking_sala...")
        cursor.execute("""
            CREATE INDEX idx_ranking_sala_puntaje 
            ON ranking_sala (id_sala, puntaje_total DESC, tiempo_total_respuestas ASC)
        """)
        print("✅ Índice creado")
        
        # 4. Agregar columnas a salas_juego
        print("\n🔧 Actualizando tabla salas_juego...")
        try:
            cursor.execute("ALTER TABLE salas_juego ADD COLUMN pregunta_actual INT DEFAULT 0")
            print("✅ Columna pregunta_actual agregada")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("⚠️  Columna pregunta_actual ya existe")
            else:
                raise
        
        try:
            cursor.execute("ALTER TABLE salas_juego ADD COLUMN total_preguntas INT DEFAULT 0")
            print("✅ Columna total_preguntas agregada")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("⚠️  Columna total_preguntas ya existe")
            else:
                raise
        
        try:
            cursor.execute("ALTER TABLE salas_juego ADD COLUMN tiempo_inicio_juego DATETIME NULL")
            print("✅ Columna tiempo_inicio_juego agregada")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("⚠️  Columna tiempo_inicio_juego ya existe")
            else:
                raise
        
        conexion.commit()
        
        print("\n" + "="*60)
        print("✅ ¡Sistema de juego creado exitosamente!")
        print("="*60)
        
        # Verificar tablas creadas
        print("\n📋 Tablas verificadas:")
        tablas_verificar = ['estado_juego_sala', 'respuestas_participantes', 'ranking_sala']
        for tabla in tablas_verificar:
            cursor.execute(f"SHOW TABLES LIKE '{tabla}'")
            result = cursor.fetchone()
            if result:
                print(f"  ✓ {tabla}")
            else:
                print(f"  ✗ {tabla} NO ENCONTRADA")
        
        cursor.close()
        conexion.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ejecutar_migracion()
