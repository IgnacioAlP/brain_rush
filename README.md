# 🎮 Brain Rush - Sistema de Gamificación Educativa

![Python](https://img.shields.io/badge/Python-43.8%25-blue)
![HTML](https://img.shields.io/badge/HTML-51%25-orange)
![CSS](https://img.shields.io/badge/CSS-3.2%25-blueviolet)
![JavaScript](https://img.shields.io/badge/JavaScript-2%25-yellow)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![License](https://img.shields.io/badge/License-Educational-red)

## 📋 Descripción

Brain Rush es una aplicación web educativa desarrollada con Flask y Python que permite a docentes crear y gestionar cuestionarios interactivos con mecánicas de juego en tiempo real. El sistema combina gamificación, seguimiento de progreso estudiantil y herramientas avanzadas de exportación de datos para crear una experiencia educativa atractiva e interactiva.

---

## 🚀 Características Principales

### 🔐 Sistema de Autenticación y Usuarios
- Autenticación segura con JWT tokens y sesiones Flask
- Registro de usuarios con verificación de email
- Recuperación de contraseña mediante email
- Roles diferenciados: Docentes y Estudiantes
- Gestión de perfil personal
- Hash seguro de contraseñas con bcrypt

### 📚 Gestión de Cuestionarios (Docentes)
- Creación y edición de cuestionarios interactivos
- Preguntas de opción múltiple (A/B/C/D)
- Importación masiva desde Excel con plantilla predefinida
- Configuración de tiempo límite por pregunta (5-300 segundos)
- Asignación de recompensas (trofeos, medallas, insignias)
- Categorización por nivel de dificultad

### 🎮 Sistema de Juego en Tiempo Real
- Generación automática de PIN único de 6 dígitos para salas
- Organización de estudiantes en grupos/equipos
- Sincronización en tiempo real de preguntas
- Contador visual de tiempo por pregunta
- Puntuación dinámica basada en velocidad de respuesta
- Ranking actualizado automáticamente
- Estadísticas detalladas: precisión, tiempo, respuestas correctas/incorrectas

### 📊 Dashboard para Docentes
- Vista de cuestionarios creados
- Monitoreo de juegos en vivo
- Estadísticas de participación estudiantil
- Exportación de resultados a Excel
- Integración con OneDrive para almacenamiento en la nube
- Envío de resultados por email

### 🏆 Sistema de Gamificación
- Sistema de XP y niveles automático
- 12 insignias desbloqueables con requisitos específicos
- Tienda de insignias con puntos acumulados
- Recompensas automáticas para Top 3 jugadores
- Historial de logros y progreso
- Ranking global de estudiantes

### 🔔 Sistema de Notificaciones
- Notificaciones por email transaccional
- Confirmación de registro
- Recuperación de contraseña
- Envío de resultados de juegos
- Sistema de notificaciones visuales en la aplicación
- Integración con Gmail SMTP

### 📈 Gestión de Datos Educativos
- Seguimiento de progreso estudiantil
- Estadísticas de rendimiento por cuestionario
- Análisis de respuestas y patrones
- Reportes exportables en múltiples formatos
- Almacenamiento seguro en base de datos MySQL

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.8+**: Lenguaje principal de desarrollo
- **Flask 3.0.0**: Framework web moderno y ligero
- **PyMySQL 1.1.0**: Conector para base de datos MySQL
- **Flask-Mail 0.9.1**: Gestión de correos electrónicos
- **python-dotenv 1.0.0**: Manejo de variables de entorno
- **Werkzeug 3.0.0**: Utilidades WSGI y seguridad
- **itsdangerous**: Generación de tokens seguros
- **bcrypt**: Hash de contraseñas

### Frontend
- **HTML5**: Estructura semántica
- **CSS3**: Estilos modernos y responsive
- **JavaScript (ES6+)**: Interactividad y comunicación asíncrona
- **Jinja2**: Motor de plantillas
- **Font Awesome**: Iconografía
- **SweetAlert2**: Alertas y notificaciones elegantes

### Base de Datos
- **MySQL 5.7+**: Sistema de gestión de base de datos relacional
- **24 Tablas**: Arquitectura normalizada
- **Triggers**: Actualización automática de XP y niveles
- **Stored Procedures**: Lógica de negocio optimizada
- **Índices**: Optimización de consultas

### Integraciones Externas
- **Microsoft Graph API**: Integración con OneDrive
- **Azure AD OAuth2**: Autenticación con cuentas Microsoft
- **MSAL Python 1.26.0**: Librería de autenticación Microsoft
- **openpyxl 3.1.2**: Generación y lectura de archivos Excel
- **ReportLab 4.0.7**: Generación de reportes PDF
- **Requests 2.31.0**: Cliente HTTP para APIs

### Herramientas de Desarrollo
- **Flask-WTF 1.2.1**: Formularios y validación
- **WTForms 3.1.1**: Construcción de formularios
- **Git**: Control de versiones
- **PythonAnywhere**: Plataforma de despliegue

---

## 📋 Requisitos Previos

Antes de instalar Brain Rush, asegúrate de tener:

- **Python 3.8 o superior** instalado en tu sistema
- **MySQL 5.7+** o **MariaDB 10.3+** como servidor de base de datos
- **Cuenta de Gmail** (para envío de correos electrónicos)
- **Cuenta de Microsoft Azure** (opcional, para integración con OneDrive)
- **Git** para clonar el repositorio
- **pip** para instalación de dependencias Python

---

## 💻 Instalación

Sigue estos pasos para configurar Brain Rush en tu entorno local:

### 1. Clonar el Repositorio

```bash
git clone https://github.com/IgnacioAlP/brain_rush.git
cd brain_rush
```

### 2. Crear Entorno Virtual

Es recomendable usar un entorno virtual para aislar las dependencias:

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual

# En Windows:
.venv\Scripts\activate

# En Linux/Mac:
source .venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con la siguiente estructura:

```bash
# Copiar archivo de ejemplo (si existe)
cp .env.example .env

# O crear manualmente con tu editor favorito
nano .env
```

Contenido del archivo `.env`:

```env
# Configuración de Base de Datos
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password_mysql
DB_NAME=brain_rush

# Clave secreta para JWT
JWT_SECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria-aqui

# Configuración de Email (Gmail)
MAIL_USERNAME=tu_correo@gmail.com
MAIL_PASSWORD=tu_contraseña_de_aplicacion_gmail

# Configuración de OneDrive (Opcional)
AZURE_CLIENT_ID=tu_application_id
AZURE_CLIENT_SECRET=tu_client_secret
AZURE_TENANT_ID=common
ONEDRIVE_REDIRECT_URI=http://localhost:5000/callback/onedrive
```

**Nota**: Nunca subas el archivo `.env` al repositorio. Ya está incluido en `.gitignore`.

### 5. Configurar Base de Datos

```bash
# Conectar a MySQL
mysql -u root -p

# Crear base de datos
CREATE DATABASE brain_rush CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;

# Importar esquema completo
mysql -u root -p brain_rush < database_schema_complete.sql
```

### 6. Ejecutar la Aplicación

```bash
python main.py
```

La aplicación estará disponible en: **http://localhost:5000**

---

## ⚙️ Configuración

### Configuración de Gmail para Envío de Correos

Para que Brain Rush pueda enviar correos de verificación y notificaciones:

1. Ve a [Seguridad de tu cuenta Google](https://myaccount.google.com/security)
2. Activa la **"Verificación en 2 pasos"**
3. Ve a [Contraseñas de aplicación](https://myaccount.google.com/apppasswords)
4. Genera una nueva contraseña de aplicación:
   - **App**: Correo
   - **Dispositivo**: Otro (escribe "Brain Rush")
5. Copia la contraseña de 16 caracteres generada
6. Pégala en la variable `MAIL_PASSWORD` del archivo `.env`

### Configuración de OneDrive (Opcional)

Para habilitar la exportación automática a OneDrive:

#### Paso 1: Registrar Aplicación en Azure

1. Ve al [Portal de Azure](https://portal.azure.com)
2. Busca **"Azure Active Directory"** o **"Microsoft Entra ID"**
3. Ve a **"App registrations"** → Click en **"+ New registration"**
4. Configura la aplicación:
   - **Name**: Brain Rush OneDrive Integration
   - **Supported account types**: Accounts in any organizational directory and personal Microsoft accounts
   - **Redirect URI**: Web → `http://localhost:5000/callback/onedrive`
5. Click **"Register"**

#### Paso 2: Obtener Credenciales

1. En la página de tu aplicación, copia el **Application (client) ID**
2. Ve a **"Certificates & secrets"** → **"+ New client secret"**
3. Crea un nuevo secreto y copia el **Value** inmediatamente (solo se muestra una vez)
4. Guarda ambos valores en tu archivo `.env`:
   - `AZURE_CLIENT_ID`: Application ID
   - `AZURE_CLIENT_SECRET`: Client Secret Value

#### Paso 3: Configurar Permisos

1. Ve a **"API permissions"**
2. Click **"+ Add a permission"** → Selecciona **"Microsoft Graph"**
3. Selecciona **"Delegated permissions"**
4. Agrega los siguientes permisos:
   - `Files.ReadWrite`
   - `User.Read`
5. Click **"Grant admin consent"** (si eres administrador)

### Configuración de la Base de Datos

El archivo `database_schema_complete.sql` incluye:

- 24 tablas relacionadas
- Triggers para actualización automática de XP
- Stored procedures para lógica de negocio
- Datos de ejemplo para insignias y configuraciones iniciales

Si necesitas resetear la base de datos:

```bash
# Eliminar y recrear
mysql -u root -p -e "DROP DATABASE IF EXISTS brain_rush; CREATE DATABASE brain_rush CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Reimportar esquema
mysql -u root -p brain_rush < database_schema_complete.sql
```

---

## 🚀 Uso

### Para Docentes

#### Crear un Cuestionario

1. **Inicia sesión** como docente
2. Ve al **Dashboard Docente**
3. Click en **"Crear Cuestionario"**
4. Completa la información:
   - Título del cuestionario
   - Descripción
   - Nivel de dificultad
   - Categoría
5. Agrega preguntas:
   - **Manualmente**: Click "Nueva Pregunta" y completa el formulario
   - **Desde Excel**: 
     - Download la plantilla Excel
     - Completa las preguntas en el formato indicado
     - Importa el archivo completado
6. (Opcional) Configura recompensas para Top 3
7. **Guarda** el cuestionario

#### Crear una Sala de Juego

1. Ve a **"Mis Cuestionarios"**
2. Selecciona un cuestionario
3. Click en **"Crear Sala de Juego"**
4. Se genera automáticamente un **PIN de 6 dígitos**
5. Comparte el PIN con tus estudiantes
6. Espera a que se unan los estudiantes
7. (Opcional) Organiza estudiantes en grupos
8. Click **"Iniciar Juego"** cuando estés listo

#### Exportar Resultados

**Opción 1: OneDrive**
1. Ve a **"Resultados"** de una sala finalizada
2. Click en **"☁️ Subir a OneDrive"**
3. Autoriza el acceso (solo primera vez)
4. El archivo se sube automáticamente a `OneDrive/BrainRush/`

**Opción 2: Email**
1. Ve a **"Resultados"** de una sala finalizada
2. Click en **"📧 Enviar por Correo"**
3. Recibirás el archivo Excel en tu email

### Para Estudiantes

#### Unirse a un Juego

1. **Inicia sesión** como estudiante
2. Ve al **Dashboard Estudiante**
3. Click en **"Unirse a Juego"**
4. Ingresa el **PIN** proporcionado por tu docente
5. Confirma tu nombre de usuario
6. Espera a que el docente inicie el juego

#### Jugar y Ganar Puntos

1. Lee cada pregunta cuidadosamente
2. Observa el **timer** (cuenta regresiva)
3. Selecciona la respuesta correcta lo más rápido posible
4. Mayor velocidad = Mayor puntaje (hasta 1000 puntos)
5. Al finalizar, revisa tu posición en el **ranking**
6. Gana **XP** e **insignias** por tu desempeño

### Rutas Principales de la Aplicación

- `/` - Página de inicio
- `/login` - Iniciar sesión
- `/registrarse` - Crear cuenta nueva
- `/dashboard-docente` - Panel de control para docentes
- `/dashboard-estudiante` - Panel de control para estudiantes
- `/crear-cuestionario` - Formulario de creación de cuestionarios
- `/mis-cuestionarios` - Lista de cuestionarios creados
- `/unirse-juego` - Unirse a sala con PIN

---

## 📁 Estructura del Proyecto

```
brain_rush/
│
├── main.py                      # 🎯 Punto de entrada de la aplicación Flask
├── config.py                    # ⚙️ Configuraciones por entorno (dev, prod)
├── bd.py                        # 💾 Gestión de conexión a base de datos
├── api_crud.py                  # 🔌 API REST para operaciones CRUD
├── utils_auth.py                # 🔐 Utilidades de autenticación (JWT, decoradores)
├── extensions.py                # 🔧 Extensiones Flask (Flask-Mail)
├── requirements.txt             # 📦 Dependencias Python del proyecto
├── .env                         # 🔒 Variables de entorno (NO INCLUIR EN GIT)
├── .env.pythonanywhere          # 🌐 Configuración para PythonAnywhere
├── .gitignore                   # 🚫 Archivos excluidos de Git
├── database_schema_complete.sql # 🗃️ Esquema completo de base de datos
│
├── controladores/               # 🎮 Lógica de negocio (Controladores MVC)
│   ├── __init__.py
│   ├── controlador_usuario.py          # Gestión de usuarios
│   ├── controlador_cuestionarios.py    # CRUD de cuestionarios
│   ├── controlador_preguntas.py        # Gestión de preguntas
│   ├── controlador_opciones.py         # Opciones de respuesta
│   ├── controlador_salas.py            # Salas de juego
│   ├── controlador_juego.py            # Lógica del juego en tiempo real
│   ├── controlador_participaciones.py  # Participantes en salas
│   ├── controlador_ranking.py          # Cálculo de rankings
│   ├── controlador_xp.py               # Sistema de experiencia
│   ├── controlador_respuestas.py       # Respuestas de participantes
│   └── controlador_recompensas.py      # Sistema de recompensas
│
├── Templates/                   # 🎨 Plantillas HTML (Jinja2)
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
│   └── ... (más plantillas)
│
└── static/                      # 📦 Archivos estáticos
    ├── css/                     # Hojas de estilo
    │   ├── brain_rush_v3.css
    │   ├── notifications.css
    │   ├── registro.css
    │   └── ... (más CSS)
    ├── js/                      # JavaScript del cliente
    │   ├── brain-rush-notifications.js
    │   ├── notifications.js
    │   └── ... (más JS)
    └── img/                     # Imágenes y recursos gráficos
```

### Descripción de Componentes Clave

- **`main.py`**: Archivo principal que contiene todas las rutas Flask, configuración de la aplicación y lógica de presentación.
- **`controladores/`**: Capa de lógica de negocio que abstrae las operaciones con la base de datos.
- **`Templates/`**: Plantillas HTML renderizadas por Jinja2 con datos dinámicos.
- **`static/`**: Recursos estáticos (CSS, JavaScript, imágenes) servidos directamente.
- **`bd.py`**: Funciones para obtener conexiones a MySQL y verificar la BD.
- **`api_crud.py`**: Endpoints de API REST para consumo externo o AJAX.

---

## 📚 Documentación Adicional

Para información más detallada sobre aspectos específicos del proyecto, consulta:

- **[CONFIGURACION_ONEDRIVE_PRODUCCION.md](./CONFIGURACION_ONEDRIVE_PRODUCCION.md)**: Guía completa para configurar la integración con OneDrive en producción
- **[ESTRUCTURA_CODIGO.md](./ESTRUCTURA_CODIGO.md)**: Documentación detallada de la arquitectura y organización del código
- **[EXPORTACION_DASHBOARD_DOCENTE.md](./EXPORTACION_DASHBOARD_DOCENTE.md)**: Guía de uso del sistema de exportación de datos para docentes
- **[NOTIFICACIONES_GUIA.md](./NOTIFICACIONES_GUIA.md)**: Documentación del sistema de notificaciones y alertas

---

## 🌐 Despliegue en Producción

### Despliegue en PythonAnywhere

Brain Rush está configurado para ser desplegado en PythonAnywhere, una plataforma de hosting Python gratuita y fácil de usar.

#### Pasos para Desplegar

1. **Crear cuenta en PythonAnywhere**: [www.pythonanywhere.com](https://www.pythonanywhere.com)

2. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/IgnacioAlP/brain_rush.git
   cd brain_rush
   ```

3. **Crear entorno virtual**:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 brain-rush-env
   pip install -r requirements.txt
   ```

4. **Configurar base de datos**:
   - Crear base de datos MySQL en el panel de PythonAnywhere
   - Importar `database_schema_complete.sql`
   - Actualizar credenciales en `.env.pythonanywhere`

5. **Configurar Web App**:
   - Source code: `/home/tu-usuario/brain_rush`
   - Working directory: `/home/tu-usuario/brain_rush`
   - Virtualenv: `/home/tu-usuario/.virtualenvs/brain-rush-env`

6. **Configurar WSGI**:
   Edita el archivo WSGI para apuntar a `main.py`:
   ```python
   import sys
   path = '/home/tu-usuario/brain_rush'
   if path not in sys.path:
       sys.path.append(path)
   
   from main import app as application
   ```

7. **Reload** la aplicación y accede a tu URL de PythonAnywhere.

#### Variables de Entorno en Producción

Utiliza el archivo `.env.pythonanywhere` como referencia para configurar las variables de entorno en producción:

- Actualiza `DB_HOST` con el host de PythonAnywhere
- Cambia `ONEDRIVE_REDIRECT_URI` a tu dominio de producción
- Asegúrate de usar contraseñas seguras y únicas

---

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Si deseas contribuir al proyecto:

1. **Fork** el repositorio
2. Crea una **rama** para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. **Commit** tus cambios: `git commit -m "Agregar nueva funcionalidad"`
4. **Push** a la rama: `git push origin feature/nueva-funcionalidad`
5. Abre un **Pull Request** describiendo tus cambios

### Guías de Contribución

- Sigue las convenciones de código Python (PEP 8)
- Documenta funciones y clases con docstrings
- Prueba tu código antes de hacer commit
- Mantén commits pequeños y descriptivos
- Actualiza la documentación si es necesario

---

## 📄 Licencia

Este proyecto es un trabajo académico desarrollado para la **Universidad Señor de Sipán (USAT)**.

**Licencia**: Uso Educativo

El código está disponible con fines educativos y de aprendizaje. Para uso comercial o redistribución, por favor contacta al autor.

---

## 👨‍💻 Autor

**Ignacio Alonzo Pérez**

- 📧 Email: [alonzopezoi@gmail.com](mailto:alonzopezoi@gmail.com)
- 🏫 Institución: Universidad Señor de Sipán (USAT)
- 💼 GitHub: [@IgnacioAlP](https://github.com/IgnacioAlP)

---

## 🙏 Agradecimientos

Gracias a todos los que han contribuido y apoyado el desarrollo de Brain Rush:

- Universidad Señor de Sipán por el apoyo académico
- Docentes y estudiantes que han probado la plataforma
- Comunidad de Flask y Python por la excelente documentación

---

## 📞 Soporte

¿Tienes preguntas o problemas? Contáctanos:

- **Issues**: [GitHub Issues](https://github.com/IgnacioAlP/brain_rush/issues)
- **Email**: alonzopezoi@gmail.com

---

## 🔄 Versión

**Versión actual**: 3.0  
**Última actualización**: Febrero 2025  
**Estado**: ✅ En producción

---

<div align="center">

**¡Gracias por usar Brain Rush! 🎮📚**

*Haciendo el aprendizaje más divertido, un quiz a la vez.*

</div>
