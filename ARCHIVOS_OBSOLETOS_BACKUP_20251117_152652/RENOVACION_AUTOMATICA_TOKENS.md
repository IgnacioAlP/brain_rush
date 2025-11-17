# 🔄 Renovación Automática de Tokens OneDrive

## ✅ Estado Actual

**¡El sistema de renovación automática YA ESTÁ FUNCIONANDO!**

Tus tokens actuales:
- ✅ `ONEDRIVE_ACCESS_TOKEN`: Configurado
- ✅ `ONEDRIVE_REFRESH_TOKEN`: Configurado  
- ✅ `ONEDRIVE_TOKEN_EXPIRES`: 2025-10-28T23:19:51

## 🔄 Cómo Funciona la Renovación Automática

### 1️⃣ **Primera Vez (Ya lo hiciste)**
- Visitaste: `http://localhost:5000/auth/onedrive-sistema`
- Autorizaste con tu cuenta de OneDrive
- Se guardaron 3 valores en `.env`:
  * `ONEDRIVE_ACCESS_TOKEN` - Token temporal (~1 hora)
  * `ONEDRIVE_REFRESH_TOKEN` - Token permanente (dura meses/años)
  * `ONEDRIVE_TOKEN_EXPIRES` - Fecha de expiración del access_token

### 2️⃣ **Uso Normal (Automático)**

Cada vez que alguien exporta a OneDrive, el sistema:

1. **Verifica** si el token está vigente:
   ```python
   if datetime.now() < token_expires:
       # ✅ Token válido, usarlo directamente
       return access_token
   ```

2. **Si expiró**, usa el `refresh_token` para obtener uno nuevo:
   ```python
   # 🔄 Token expirado, refrescando automáticamente...
   result = msal_app.acquire_token_by_refresh_token(
       refresh_token,
       scopes=['Files.ReadWrite.All']
   )
   
   # Guardar nuevos tokens en .env
   actualizar_env_tokens(new_access_token, new_refresh_token, new_expires)
   ```

3. **Actualiza** automáticamente el `.env` con los nuevos tokens

4. **Continúa** con la exportación sin interrupciones

### 3️⃣ **Ciclo de Vida del Token**

```
┌─────────────────────────────────────────────────────────────────┐
│  PRIMERA AUTORIZACIÓN (Una sola vez)                            │
│   │
│                                                                  │
│  ├─ access_token  (válido ~1 hora)                             │
│  ├─ refresh_token (válido meses/años)                          │
│  └─ token_expires (2025-10-28 23:19:51)                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  RENOVACIÓN AUTOMÁTICA (Cada ~1 hora)                           │
│  Se ejecuta automáticamente al exportar                          │
│                                                                  │
│  ✅ Verifica: ¿access_token expiró?                             │
│  🔄 Refresca: Usa refresh_token → nuevo access_token            │
│  💾 Guarda: Actualiza .env con nuevos tokens                    │
│  ✅ Continúa: Exporta archivo sin problemas                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    ♻️  REPITE INFINITAMENTE
                    (sin necesidad de re-autorizar)
```

## 🎯 Lo Que Esto Significa Para Ti

### ✅ **SÍ necesitas hacer (SOLO UNA VEZ):**
1. Visitar `http://localhost:5000/auth/onedrive-sistema`
2. Autorizar con tu cuenta de OneDrive
3. Listo! Los tokens se guardan en `.env`

### ❌ **NO necesitas hacer:**
1. ❌ Volver a autorizar cada hora
2. ❌ Ingresar a ningún link periódicamente
3. ❌ Actualizar tokens manualmente
4. ❌ Preocuparte por la expiración

### 🔄 **El sistema hace automáticamente:**
1. ✅ Detectar cuando el token expira
2. ✅ Usar el refresh_token para obtener uno nuevo
3. ✅ Actualizar el `.env` con los nuevos tokens
4. ✅ Continuar con la exportación sin interrupciones

## 📊 Duración de los Tokens

| Token | Duración | Renovación |
|-------|----------|------------|
| `access_token` | ~1 hora | ✅ Automática cada hora |
| `refresh_token` | 90 días - 2 años* | ✅ Se renueva al usarse |
| `token_expires` | Se actualiza cada renovación | ✅ Automático |

*El refresh_token se renueva automáticamente cada vez que se usa, por lo que en la práctica **nunca expira** mientras el sistema se use regularmente.

## 🔐 Cuándo Necesitas Re-Autorizar

Solo en estos casos MUY raros:

1. **❌ Cambiaste la contraseña** de la cuenta de OneDrive
2. **❌ Revocaste permisos** manualmente en Microsoft
3. **❌ El refresh_token expiró** por no usar el sistema durante 90+ días
4. **❌ Borraste los tokens** del `.env`

En cualquiera de estos casos, simplemente vuelve a visitar:
```
http://localhost:5000/auth/onedrive-sistema
```

## 📝 Logs del Sistema

Cuando exportas, verás en la consola:

### ✅ Token Válido (No necesita renovación):
```
📤 Subiendo resultados a OneDrive...
✅ Usando token de OneDrive del .env (válido)
📤 Subiendo archivo a OneDrive: BrainRush_Resultados_...xlsx
✅ Archivo subido exitosamente
```

### 🔄 Token Expirado (Renovación Automática):
```
📤 Subiendo resultados a OneDrive...
🔄 Token expirado, refrescando...
✅ Token refrescado exitosamente
✅ Tokens actualizados en .env
📤 Subiendo archivo a OneDrive: BrainRush_Resultados_...xlsx
✅ Archivo subido exitosamente
```

## 🛡️ Seguridad

- ✅ Los tokens están en `.env` (no en el código)
- ✅ `.env` está en `.gitignore` (no se sube a GitHub)
- ✅ El `refresh_token` está cifrado por Microsoft
- ✅ Solo tu aplicación puede usarlo (CLIENT_SECRET requerido)

## 🚀 Conclusión

**¡Ya está todo configurado!** 

El sistema renovará los tokens automáticamente cada ~1 hora sin que tengas que hacer nada. Solo tuviste que autorizar UNA VEZ y el sistema se encarga del resto para siempre (o hasta que cambies la contraseña de OneDrive).

---

**Última actualización:** 28 de octubre, 2025  
**Estado:** ✅ Sistema de renovación automática ACTIVO
