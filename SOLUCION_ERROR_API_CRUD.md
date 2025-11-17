# 🔧 Solución al Error 400 en APIs CRUD con JWT

## ❌ Problema Identificado

El error **400 Bad Request** al crear usuarios ocurre por:
1. Faltan campos requeridos en el JSON
2. La contraseña no está siendo hasheada correctamente
3. El formato del JSON no es válido

## ✅ Solución Implementada

### 1. **API mejorada con validaciones**

La API ahora:
- ✅ Valida que todos los campos requeridos estén presentes
- ✅ Hashea automáticamente la contraseña si no está hasheada
- ✅ Devuelve errores más descriptivos (400, 409, 500)
- ✅ Registra logs para debugging

### 2. **Cómo probar en Postman**

#### **Opción A: JSON Simple (Recomendado)**

```json
{
  "nombre": "José",
  "apellidos": "Pérez",
  "email": "76ab239@usat.pe",
  "contraseña_hash": "Peso123",
  "tipo_usuario": "estudiante",
  "estado": "activo"
}
```

#### **Opción B: Con contraseña ya hasheada**

```json
{
  "nombre": "José",
  "apellidos": "Pérez",
  "email": "76ab239@usat.pe",
  "contraseña_hash": "de03bd53e93242b639cdb4a5f9396297901760cf9e6f6e93a09f0c397Dc5972665e87",
  "tipo_usuario": "estudiante",
  "estado": "activo"
}
```

### 3. **Configuración correcta en Postman**

#### **Headers (Pestaña Headers)**
```
Key: Authorization
Value: JWT eyJhbGc... (TU_TOKEN_AQUÍ)

Key: Content-Type
Value: application/json
```

#### **Body (Pestaña Body > raw > JSON)**
Pega el JSON de arriba (Opción A o B)

### 4. **Verificar que el servidor esté corriendo**

```bash
python main.py
```

Debe mostrar:
```
 * Running on http://127.0.0.1:5000
```

### 5. **Probar con el script de prueba**

```bash
python test_api_crud.py
```

Este script:
1. ✅ Obtiene el token JWT
2. ✅ Lista todos los usuarios
3. ✅ Crea un nuevo usuario

## 🔍 Debugging

### Ver logs del servidor

En la consola donde corre `python main.py` verás:
```
✅ Usuario autenticado: 1
📊 Usuarios encontrados: 5
```

### Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| 400 Bad Request | JSON mal formado o campos faltantes | Verificar JSON y campos requeridos |
| 401 Unauthorized | Token JWT inválido o expirado | Obtener nuevo token con POST /api/auth |
| 409 Conflict | Email ya registrado | Cambiar el email en el JSON |
| 500 Internal Server Error | Error en base de datos | Verificar logs del servidor |

## 📋 Checklist de verificación

- [ ] Servidor corriendo en http://127.0.0.1:5000
- [ ] Token JWT obtenido con POST /api/auth
- [ ] Header `Authorization: JWT <token>` configurado
- [ ] Header `Content-Type: application/json` configurado
- [ ] JSON con todos los campos requeridos: nombre, apellidos, email, contraseña_hash
- [ ] Email único (no duplicado)

## 🎯 Próximos pasos

1. **Ejecuta el servidor**: `python main.py`
2. **Obtén un token**: POST /api/auth con credenciales válidas
3. **Prueba GET /api/usuarios**: Debe devolver la lista de usuarios
4. **Prueba POST /api/usuarios**: Debe crear un nuevo usuario
5. **Verifica logs**: La consola debe mostrar "✅ Usuario autenticado"

## 🆘 Si aún tienes errores

1. Copia el **JSON exacto** que estás enviando
2. Copia la **respuesta completa** de Postman
3. Copia los **logs del servidor** (consola donde corre main.py)
4. Comparte las capturas para diagnóstico más específico
