# 🎮 Brain RUSH - Sistema de Juegos Educativos

## 📋 Descripción del Proyecto

Brain RUSH es una plataforma web educativa desarrollada con Flask que permite a docentes crear cuestionarios interactivos y gestionar juegos de conocimiento en tiempo real con sus estudiantes. El sistema incluye un completo conjunto de características para gamificación educativa, gestión de usuarios, ranking en vivo y exportación de resultados.

---

## 🚀 Características Principales

### 👥 Sistema de Usuarios
- **Roles**: Docentes y Estudiantes con permisos diferenciados
- **Autenticación**: JWT tokens para API + sesiones Flask
- **Registro**: Con verificación de email obligatoria
- **Perfil**: Gestión de datos personales y contraseñas

### 📝 Gestión de Cuestionarios
- Creación de cuestionarios con múltiples preguntas
- Tipos de preguntas: Opción múltiple (A/B/C/D)
- Importación masiva desde Excel con plantilla predefinida
- Configuración de tiempo límite por pregunta (5-300 segundos)
- Asignación de recompensas automáticas (trofeos, medallas, insignias)

### 🎯 Sistema de Juego en Tiempo Real
- **Salas de Juego**: Generación de PIN único de 6 dígitos
- **Grupos**: Organización de estudiantes en equipos
- **Juego en Vivo**: Preguntas sincronizadas con timer visual
- **Puntuación Dinámica**: Puntaje basado en velocidad de respuesta
  - Máximo: 1000 puntos (< 0.5 seg)
  - Decremento: 100 puntos cada 0.5 segundos
  - Mínimo: 10 puntos
- **Ranking en Tiempo Real**: Actualización automática de posiciones
- **Estadísticas**: Respuestas correctas/incorrectas, tiempo total, precisión

### 🏆 Sistema de Gamificación
- **XP y Niveles**: Experiencia acumulada y progresión automática
- **Insignias**: 12 insignias desbloqueables con requisitos específicos
- **Tienda de Insignias**: Compra con puntos acumulados
- **Recompensas Automáticas**: Top 3 reciben recompensas al finalizar juego
- **Historial**: Seguimiento de logros y progreso

### 📊 Exportación de Resultados
- **Excel (XLSX)**: Formato profesional con encabezados formateados
- **OneDrive OAuth2**: Subida automática a carpeta BrainRush
- **Email**: Envío automático con archivo adjunto (fallback)
- **Formatos**: Ranking completo con estadísticas detalladas

### 🔔 Notificaciones
- **Email Transaccional**: Confirmación de registro, restablecimiento de contraseña
- **Configuración Gmail**: Integración con contraseñas de aplicación
- **Templates HTML**: Emails con diseño profesional

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask 3.0.0**: Framework web principal
- **PyMySQL**: Conexión a base de datos MySQL
- **PyJWT**: Autenticación con tokens JWT
- **Flask-Mail**: Envío de correos electrónicos
- **python-dotenv**: Gestión de variables de entorno
- **bcrypt**: Hash seguro de contraseñas

### Frontend
- **HTML5 + CSS3**: Interfaz responsiva
- **JavaScript (ES6+)**: Interactividad y AJAX
- **SweetAlert2**: Alertas y modales elegantes
- **Font Awesome**: Iconografía

### Base de Datos
- **MySQL 5.7+**: 24 tablas con relaciones complejas
- **Triggers**: Actualización automática de XP y niveles
- **Stored Procedures**: Lógica de negocio optimizada
- **Índices**: Optimización de consultas

### Integraciones Externas
- **Microsoft Graph API**: Subida de archivos a OneDrive
- **Azure AD OAuth2**: Autenticación con cuentas Microsoft
- **MSAL Python**: Librería de autenticación Microsoft
- **openpyxl**: Generación de archivos Excel

---

## 📁 Estructura del Proyecto

```
brain_rush/
├── main.py                      # Aplicación Flask principal
├── config.py                    # Configuraciones del sistema
├── bd.py                        # Conexión a base de datos
├── api_crud.py                  # Operaciones CRUD para API
├── utils_auth.py                # Utilidades de autenticación
├── extensions.py                # Extensiones Flask (Mail)
├── onedrive_auth.py             # Autenticación OneDrive
├── requirements.txt             # Dependencias Python
├── .env                         # Variables de entorno (NO subir a Git)
├── database_schema_complete.sql # Esquema completo de BD
│
├── controladores/               # Lógica de negocio
│   ├── controlador_usuario.py
│   ├── controlador_cuestionarios.py
│   ├── controlador_preguntas.py
│   ├── controlador_opciones.py
│   ├── controlador_salas.py
│   ├── controlador_juego.py
│   ├── controlador_participaciones.py
│   ├── controlador_ranking.py
│   ├── controlador_xp.py
│   ├── controlador_insignias.py
│   └── controlador_recompensas.py
│
├── Templates/                   # Plantillas HTML
│   ├── login.html
│   ├── registro.html
│   ├── DashboardDocente.html
│   ├── DashboardEstudiante.html
│   ├── CrearCuestionario.html
│   ├── EditarCuestionario.html
│   ├── MisCuestionarios.html
│   ├── MonitoreoJuego.html
│   ├── JuegoEstudiante.html
│   ├── ResultadosJuego.html
│   └── (más archivos...)
│
└── static/                      # Archivos estáticos
    ├── css/
    ├── js/
    └── images/
```

---

## 🗄️ Base de Datos

### Tablas Principales (24 en total)

#### Usuarios y Autenticación
- `usuarios`: Docentes y estudiantes
- `activacion_cuentas`: Tokens de verificación de email
- `tokens_recuperacion`: Tokens para restablecer contraseña

#### Cuestionarios y Preguntas
- `cuestionarios`: Información de cuestionarios
- `preguntas`: Preguntas con tipo y tiempo límite
- `opciones_respuesta`: Opciones A/B/C/D para cada pregunta
- `cuestionario_preguntas`: Relación con orden de preguntas

#### Sistema de Juego
- `salas_juego`: Salas con PIN único y estado
- `participantes_sala`: Estudiantes en cada sala
- `grupos_sala`: Organización en equipos
- `estado_juego_sala`: Estado actual del juego
- `respuestas_participantes`: Respuestas con tiempo y puntaje
- `ranking_sala`: Posiciones finales

#### Gamificación
- `xp_estudiantes`: Experiencia y nivel de cada estudiante
- `insignias`: 12 tipos de insignias disponibles
- `insignias_estudiante`: Insignias desbloqueadas por cada estudiante
- `progreso_insignias`: Progreso hacia requisitos de insignias
- `tienda_insignias`: Insignias comprables con puntos
- `compras_insignias`: Historial de compras
- `recompensas`: Premios configurados por cuestionario
- `recompensas_usuarios`: Recompensas obtenidas

---

## ⚙️ Instalación y Configuración

### 1. Requisitos Previos

- Python 3.8+
- MySQL 5.7+ o MariaDB 10.3+
- Cuenta de Gmail (para envío de emails)
- Cuenta de Microsoft Azure (opcional, para OneDrive)

### 2. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/brain_rush.git
cd brain_rush
```

### 3. Crear Entorno Virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar Base de Datos

```bash
# Crear base de datos
mysql -u root -p

CREATE DATABASE brain_rush CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;

# Importar esquema
mysql -u root -p brain_rush < database_schema_complete.sql
```

### 6. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Base de Datos
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=brain_rush

# JWT
JWT_SECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria-aqui

# Email (Gmail)
MAIL_USERNAME=tu_correo@gmail.com
MAIL_PASSWORD=contraseña-de-aplicacion-gmail

# OneDrive (Opcional)
AZURE_CLIENT_ID=tu-application-id
AZURE_CLIENT_SECRET=tu-client-secret
AZURE_TENANT_ID=common
ONEDRIVE_REDIRECT_URI=http://localhost:5000/callback/onedrive
```

### 7. Configurar Gmail (para envío de emails)

1. Ve a https://myaccount.google.com/security
2. Activa "Verificación en 2 pasos"
3. Ve a https://myaccount.google.com/apppasswords
4. Genera contraseña de aplicación:
   - App: "Correo"
   - Dispositivo: "Otro" → "Brain RUSH"
5. Copia la contraseña de 16 caracteres
6. Pégala en `MAIL_PASSWORD` del archivo `.env`

### 8. Configurar OneDrive (Opcional)

#### Registrar Aplicación en Azure

1. Ve a https://portal.azure.com
2. Busca "Azure Active Directory" o "Microsoft Entra ID"
3. Ve a "App registrations" → "+ New registration"
4. Configura:
   - **Name**: BrainRush OneDrive Integration
   - **Supported account types**: Accounts in any organizational directory and personal Microsoft accounts
   - **Redirect URI**: Web → `http://localhost:5000/callback/onedrive`
5. Copia el **Application (client) ID**
6. Ve a "Certificates & secrets" → "+ New client secret"
7. Copia el **Value** (secret) inmediatamente
8. Ve a "API permissions":
   - "+ Add a permission" → Microsoft Graph
   - Delegated permissions:
     - `Files.ReadWrite`
     - `User.Read`
   - "Grant admin consent"

#### Configurar URLs en Azure

1. Ve a "Authentication"
2. Agrega ambas URLs de redirección:
   - `http://localhost:5000/callback/onedrive` (local)
   - `https://tu-dominio.com/callback/onedrive` (producción)
3. Marca:
   - ✅ Access tokens
   - ✅ ID tokens
4. Guarda cambios

### 9. Ejecutar la Aplicación

```bash
python main.py
```

La aplicación estará disponible en: http://localhost:5000

---

## 📖 Guías de Uso

### Para Docentes

#### Crear un Cuestionario

1. Login como docente
2. Dashboard → "Crear Cuestionario"
3. Completa información:
   - Título
   - Descripción
   - Nivel de dificultad
   - Categoría
4. Agrega preguntas:
   - **Manualmente**: Click "Nueva Pregunta"
   - **Desde Excel**: 
     - Click "Descargar Plantilla Excel"
     - Completa preguntas en Excel
     - Click "Importar desde Excel"
     - Selecciona archivo completado
5. Configura recompensas (opcional):
   - Trofeo (1er lugar)
   - Medalla (2do lugar)
   - Insignia (3er lugar)
6. Guarda cuestionario

#### Crear Sala de Juego

1. "Mis Cuestionarios" → Selecciona cuestionario
2. Click "Crear Sala de Juego"
3. Se genera PIN de 6 dígitos
4. Comparte PIN con estudiantes
5. Espera a que se unan
6. (Opcional) Organiza en grupos
7. Click "Iniciar Juego"

#### Monitorear Juego en Vivo

1. Vista en tiempo real de:
   - Pregunta actual mostrada
   - Cuántos estudiantes han respondido
   - Tiempo transcurrido
2. Click "Siguiente Pregunta" cuando estés listo
3. Repite hasta finalizar todas las preguntas
4. Sistema calcula ranking automáticamente
5. Asigna recompensas a top 3 automáticamente

#### Exportar Resultados

**Opción 1: OneDrive (Automático)**
1. "Ver Resultados" → Click "☁️ Subir a OneDrive"
2. Primera vez: Autoriza acceso con cuenta Microsoft
3. Archivo se sube automáticamente a OneDrive/BrainRush/
4. Click "Abrir OneDrive" para ver el archivo

**Opción 2: Email**
1. "Ver Resultados" → Click "📧 Enviar por Correo"
2. Recibes Excel adjunto en tu email
3. Guarda donde prefieras

### Para Estudiantes

#### Unirse a un Juego

1. Login como estudiante
2. Dashboard → "Unirse a Juego"
3. Ingresa PIN proporcionado por docente
4. Ingresa tu nombre (o usa el de tu cuenta)
5. Click "Unirse"
6. Espera a que docente inicie el juego

#### Jugar

1. Lee la pregunta mostrada
2. Observa el timer (cuenta regresiva)
3. Click en la opción que creas correcta
4. Feedback inmediato:
   - ✅ Correcta: Puntaje obtenido
   - ❌ Incorrecta: Respuesta correcta mostrada
5. Espera siguiente pregunta
6. Al finalizar, ve tu posición en el ranking

#### Gestionar Perfil y Logros

1. Dashboard → "Mi Perfil"
2. Ve tu XP, nivel actual y progreso
3. "Mis Insignias" → Insignias desbloqueadas y disponibles
4. "Tienda" → Compra insignias con puntos acumulados
5. "Historial" → Juegos pasados y estadísticas

---

## 🎮 Sistema de Puntuación

### Puntaje por Respuesta

El puntaje se calcula según la velocidad de respuesta:

| Tiempo de Respuesta | Puntaje Otorgado |
|---------------------|------------------|
| 0.0 - 0.5 seg       | 1000 puntos      |
| 0.5 - 1.0 seg       | 900 puntos       |
| 1.0 - 1.5 seg       | 800 puntos       |
| 1.5 - 2.0 seg       | 700 puntos       |
| ...                 | ...              |
| 4.5 - 5.0 seg       | 100 puntos       |
| > 5.0 seg           | 10 puntos (mín)  |

**Fórmula**: `Puntaje = 1000 - (intervalos_de_0.5_seg × 100)`

### Ranking

**Criterios de ordenamiento**:
1. **Puntaje Total** (mayor a menor)
2. En caso de empate → **Tiempo Total** (menor a mayor)

**Ejemplo**:
```
Pos | Nombre      | Puntaje | Correctas | Tiempo  | Precisión
----|-------------|---------|-----------|---------|----------
1   | Juan        | 8500    | 10        | 12.5s   | 100%
2   | María       | 8500    | 10        | 15.2s   | 100%  ← Empate por tiempo
3   | Pedro       | 7800    | 9         | 10.3s   | 90%
```

### Sistema XP

- **Por respuesta correcta**: +10 XP
- **Por finalizar juego**: +50 XP
- **Nivel automático**: Se calcula con triggers SQL
  - Nivel 1: 0-99 XP
  - Nivel 2: 100-299 XP
  - Nivel 3: 300-599 XP
  - ... (escalado exponencial)

### Insignias

**12 insignias disponibles**:
1. **Primera Victoria**: Ganar primer juego
2. **Racha Ganadora**: Ganar 3 juegos consecutivos
3. **Perfeccionista**: 100% de aciertos en un juego
4. **Velocista**: Responder todas en < 2 segundos promedio
5. **Constante**: Participar en 10 juegos
6. **Experto**: Alcanzar nivel 10
7. **Maestro**: Alcanzar nivel 25
8. **Leyenda**: Alcanzar nivel 50
9. **Coleccionista**: Desbloquear 5 insignias
10. **Millonario**: Acumular 10,000 puntos totales
11. **Competitivo**: Quedar top 3 en 5 juegos
12. **Dedicado**: 50 respuestas correctas acumuladas

**Insignias comprables en tienda**:
- Costo: 500-2000 puntos según rareza
- Desbloqueables: Aparecen al cumplir requisitos automáticamente

---

## 📊 API Endpoints

### Autenticación

```
POST /api/login          - Login (retorna JWT token)
POST /api/register       - Registro de usuario
POST /api/logout         - Cerrar sesión
GET  /verificar-email    - Verificar email con token
```

### Cuestionarios

```
GET    /api/cuestionarios                    - Listar cuestionarios
POST   /api/cuestionarios                    - Crear cuestionario
GET    /api/cuestionarios/<id>               - Obtener cuestionario
PUT    /api/cuestionarios/<id>               - Actualizar cuestionario
DELETE /api/cuestionarios/<id>               - Eliminar cuestionario
POST   /cuestionario/<id>/importar-preguntas - Importar preguntas desde Excel
GET    /cuestionario/<id>/descargar-plantilla - Descargar plantilla Excel
```

### Juego en Tiempo Real

```
POST /sala/<sala_id>/iniciar                     - Iniciar juego
GET  /api/sala/<sala_id>/pregunta-actual         - Obtener pregunta actual
POST /api/sala/<sala_id>/responder               - Enviar respuesta
POST /api/sala/<sala_id>/siguiente-pregunta      - Avanzar pregunta (docente)
GET  /api/sala/<sala_id>/ranking                 - Obtener ranking
GET  /api/sala/<sala_id>/estadisticas-pregunta   - Estadísticas en vivo
```

### Exportación

```
POST /api/exportar-resultados/<sala_id>/onedrive - Exportar a OneDrive
POST /api/exportar-resultados/<sala_id>/email    - Enviar por email
GET  /auth/onedrive                              - Iniciar auth OneDrive
GET  /callback/onedrive                          - Callback OAuth2
```

---

## 🔒 Seguridad

### Autenticación
- **Contraseñas**: Hash con bcrypt (cost factor 12)
- **JWT Tokens**: Firmados con clave secreta
- **Sesiones**: Cookies con `httponly`, `secure` (HTTPS), `samesite=Lax`
- **CSRF**: Protección en formularios (csrf_token)

### Validaciones
- **Email**: Formato válido + verificación obligatoria
- **Contraseñas**: Mínimo 6 caracteres
- **SQL Injection**: Consultas parametrizadas (PyMySQL)
- **XSS**: Escapado automático de templates (Jinja2)

### Permisos
- **Docente**: CRUD de cuestionarios, crear salas, ver resultados
- **Estudiante**: Unirse a salas, jugar, ver perfil
- **Validaciones**: Verificación de propiedad en cada endpoint

### Variables de Entorno
- `.env` en `.gitignore` (no subir a Git)
- Credenciales fuera del código fuente
- Tokens y secrets rotativos

---

## 🚀 Despliegue en PythonAnywhere

### 1. Subir Archivos

```bash
# Usar Web Interface o Git
git clone https://github.com/tu-usuario/brain_rush.git
```

### 2. Configurar Entorno Virtual

```bash
cd ~/brain_rush
mkvirtualenv --python=/usr/bin/python3.10 brain-rush-env
pip install -r requirements.txt
```

### 3. Configurar Base de Datos

En PythonAnywhere → Databases:
- Crear base de datos MySQL
- Importar `database_schema_complete.sql`
- Anotar host, usuario, contraseña

### 4. Crear `.env`

```bash
nano .env
```

Pega configuración (cambia URL de redirección):
```env
DB_HOST=tu-usuario.mysql.pythonanywhere-services.com
DB_USER=tu-usuario
DB_PASSWORD=tu-password
DB_NAME=tu-usuario$brain_rush

JWT_SECRET_KEY=clave-secreta-aleatoria

MAIL_USERNAME=tu_correo@gmail.com
MAIL_PASSWORD=contraseña-aplicacion-gmail

AZURE_CLIENT_ID=tu-client-id
AZURE_CLIENT_SECRET=tu-client-secret
AZURE_TENANT_ID=common
ONEDRIVE_REDIRECT_URI=https://tu-usuario.pythonanywhere.com/callback/onedrive
```

### 5. Configurar Web App

En PythonAnywhere → Web:
- Source code: `/home/tu-usuario/brain_rush`
- Working directory: `/home/tu-usuario/brain_rush`
- Virtualenv: `/home/tu-usuario/.virtualenvs/brain-rush-env`
- WSGI file: Edita y apunta a `main.py`

```python
import sys
path = '/home/tu-usuario/brain_rush'
if path not in sys.path:
    sys.path.append(path)

from main import app as application
```

### 6. Reload y Probar

Click en "Reload" (botón verde)

Abre: `https://tu-usuario.pythonanywhere.com`

---

## 🧪 Pruebas

### Ejecutar Pruebas Locales

```bash
# Instalar pytest
pip install pytest

# Ejecutar tests (cuando se implementen)
pytest tests/
```

### Casos de Prueba Importantes

1. **Registro y Login**:
   - Registro con email válido
   - Verificación de email
   - Login con credenciales correctas/incorrectas
   - Recuperación de contraseña

2. **Cuestionarios**:
   - Crear cuestionario con preguntas
   - Importar preguntas desde Excel
   - Editar/eliminar cuestionarios
   - Validaciones de permisos

3. **Juego**:
   - Crear sala con PIN
   - Unirse con PIN
   - Responder preguntas
   - Calcular puntaje correcto
   - Generar ranking

4. **Exportación**:
   - Exportar a OneDrive (con autorización)
   - Enviar por email
   - Formato Excel correcto

---

## 🐛 Solución de Problemas Comunes

### Error: "No se pudo conectar a la base de datos"

**Causa**: Credenciales incorrectas en `.env`

**Solución**:
1. Verifica `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
2. Prueba conexión:
   ```bash
   mysql -h DB_HOST -u DB_USER -p DB_NAME
   ```

### Error: "Las librerías de Microsoft no están instaladas"

**Causa**: Falta instalar `msal` y `requests`

**Solución**:
```bash
pip install msal requests
```

### Error: "redirect_uri_mismatch" (OneDrive)

**Causa**: URL de redirección no configurada en Azure

**Solución**:
1. Azure Portal → Tu aplicación → Authentication
2. Agrega URL: `http://localhost:5000/callback/onedrive`
3. Para producción: `https://tu-dominio.com/callback/onedrive`

### Error: "SMTPAuthenticationError" (Gmail)

**Causa**: Contraseña de aplicación incorrecta

**Solución**:
1. Ve a https://myaccount.google.com/apppasswords
2. Genera nueva contraseña de aplicación
3. Actualiza `MAIL_PASSWORD` en `.env`

### Archivos no se suben a OneDrive

**Verificar**:
1. ¿Autorizaste OneDrive? → Click "Subir a OneDrive" y autoriza
2. ¿Expiraron tokens? → Volverá a pedir autorización automáticamente
3. ¿Hay error de conexión? → Usa fallback de email

### Emails no llegan

**Verificar**:
1. Revisa carpeta SPAM
2. Verifica `MAIL_USERNAME` y `MAIL_PASSWORD` en `.env`
3. Verifica email en base de datos sea válido
4. Revisa logs de Flask para errores SMTP

---

## 📝 Mantenimiento

### Renovar Client Secret de Azure

Los secrets expiran cada 24 meses:

1. Azure Portal → Certificates & secrets
2. "+ New client secret"
3. Copia nuevo valor
4. Actualiza `AZURE_CLIENT_SECRET` en `.env`
5. Reload aplicación

### Backup de Base de Datos

```bash
# Exportar
mysqldump -u root -p brain_rush > backup_brain_rush_$(date +%Y%m%d).sql

# Restaurar
mysql -u root -p brain_rush < backup_brain_rush_20251027.sql
```

### Logs y Debugging

```python
# En main.py, activar modo debug (solo desarrollo):
app.run(debug=True, host='0.0.0.0', port=5000)
```

**En producción**, revisar logs en:
- PythonAnywhere: `/var/log/`
- Local: Consola del terminal

---

## 🤝 Contribuciones

Este proyecto es parte de un trabajo académico. Para contribuir:

1. Fork del repositorio
2. Crea rama para feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m "Descripción"`
4. Push a rama: `git push origin feature/nueva-funcionalidad`
5. Abre Pull Request

---

## 📄 Licencia

Proyecto educativo - Universidad Señor de Sipán (USAT)

---

## 📞 Soporte y Contacto

Para dudas o problemas:
- **Email**: alonzopezoi@gmail.com
- **Institución**: Universidad Señor de Sipán
- **Proyecto**: Brain RUSH - Sistema de Juegos Educativos

---

## 📚 Documentación Adicional

### Importación de Preguntas desde Excel

**Formato de Plantilla**:
- Columna A: Pregunta (obligatoria)
- Columnas B-E: Opciones A, B, C, D (A y B obligatorias)
- Columna F: Respuesta Correcta (A/B/C/D)
- Columna G: Tiempo en segundos (5-300)

**Validaciones**:
- Mínimo 2 opciones por pregunta
- Respuesta correcta debe existir
- Tiempo entre 5 y 300 segundos

### Sistema de Recompensas Automáticas

Al finalizar un juego, el sistema asigna automáticamente:
- **1er Lugar**: Trofeo configurado para el cuestionario
- **2do Lugar**: Medalla configurada
- **3er Lugar**: Insignia configurada

Las recompensas deben configurarse ANTES de crear la sala de juego.

### Renovación Automática de Tokens OneDrive

El sistema maneja automáticamente:
1. **Access Token** (válido ~1 hora) → Se renueva automáticamente
2. **Refresh Token** (válido 90 días - 2 años) → Se renueva al usarse

Solo necesitas autorizar UNA VEZ. El sistema se encarga del resto.

---

## 🎯 Roadmap y Mejoras Futuras

- [ ] Modo offline para juegos sin internet
- [ ] Integración con Google Classroom
- [ ] Reportes avanzados con gráficos
- [ ] App móvil (React Native)
- [ ] Preguntas con imágenes
- [ ] Preguntas de respuesta abierta
- [ ] Chat en vivo durante juego
- [ ] Torneos y ligas escolares
- [ ] Integración con Moodle/Blackboard

---

**Última actualización**: Noviembre 2024  
**Versión**: 3.0  
**Estado**: ✅ Funcional en producción

---

¡Gracias por usar Brain RUSH! 🎮📚
