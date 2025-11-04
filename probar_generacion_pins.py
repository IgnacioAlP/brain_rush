# -*- coding: utf-8 -*-
"""
Script para probar la generación de PINs para modo automático vs normal
"""

import random
import string

def generar_pin_normal():
    """Genera un PIN de 6 dígitos para salas normales"""
    return str(random.randint(100000, 999999))

def generar_pin_automatico():
    """Genera un PIN de 8 caracteres alfanuméricos para modo automático"""
    codigo_aleatorio = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f'AUTO{codigo_aleatorio}'

def es_sala_automatica(pin_sala):
    """Verifica si un PIN corresponde a una sala en modo automático"""
    if not pin_sala:
        return False
    return pin_sala.startswith('AUTO') and len(pin_sala) == 8

print("🔑 PRUEBA DE GENERACIÓN DE PINS")
print("=" * 60)

print("\n📌 PINS NORMALES (Salas creadas por docentes):")
print("-" * 60)
for i in range(5):
    pin = generar_pin_normal()
    es_auto = es_sala_automatica(pin)
    print(f"   {i+1}. {pin:12} → {'❌ Automático' if es_auto else '✓ Normal'} (6 dígitos)")

print("\n🤖 PINS AUTOMÁTICOS (Salas desde dashboard estudiante):")
print("-" * 60)
for i in range(5):
    pin = generar_pin_automatico()
    es_auto = es_sala_automatica(pin)
    print(f"   {i+1}. {pin:12} → {'✓ Automático' if es_auto else '❌ Normal'} (AUTO + 4 caracteres)")

print("\n" + "=" * 60)
print("✅ DIFERENCIACIÓN:")
print("   • Salas NORMALES: 6 dígitos numéricos (ej: 123456)")
print("   • Salas AUTOMÁTICAS: AUTO + 4 caracteres (ej: AUTOA1B2)")
print("   • Fácil identificación del tipo de sala por el formato del PIN")
