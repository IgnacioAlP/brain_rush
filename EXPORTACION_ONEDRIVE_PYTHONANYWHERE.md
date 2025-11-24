# Exportación a OneDrive en PythonAnywhere

## Problema con OAuth2 en PythonAnywhere

PythonAnywhere tiene limitaciones con el flujo OAuth2 interactivo tradicional:
- Las redirecciones pueden ser complicadas
- El servidor puede tener restricciones de firewall
- La URL de callback debe ser HTTPS en producción

## Solución Alternativa: Usar OneDrive Personal con Token de Aplicación

En lugar de OAuth2 interactivo, usaremos **Microsoft Graph API con tokens de aplicación** o **carga directa con credenciales de usuario**.

### Opción 1: Usar Compartir por Correo (MÁS SIMPLE)

La forma más sencilla es enviar el archivo por correo electrónico al usuario en lugar de subirlo directamente a OneDrive.

#### Ventajas:
- ✅ No requiere configuración de Azure
- ✅ Compatible con PythonAnywhere
- ✅ El usuario puede guardar el archivo donde quiera (OneDrive, Google Drive, etc.)
- ✅ Ya tienes configurado el envío de emails

#### Implementación:

Modificar el endpoint para enviar el archivo por correo:

```python
@app.route('/api/exportar-resultados/<int:sala_id>/email', methods=['POST'])
def exportar_resultados_email(sala_id):
    """Enviar resultados por correo electrónico"""
    try:
        data = request.get_json()
        ranking = data.get('ranking', [])
        total_preguntas = data.get('totalPreguntas', 0)
        cuestionario_titulo = data.get('cuestionarioTitulo', 'Cuestionario')
        
        # Obtener email del usuario
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT email, nombre, apellidos FROM usuarios WHERE id_usuario = %s", 
                      (session['usuario_id'],))
        usuario = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        if not usuario:
            return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 404
        
        email_destino = usuario[0]
        
        # Crear archivo Excel en memoria (código existente)
        import io
        from openpyxl import Workbook
        from openpyxl.styles import Font, Alignment, PatternFill
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Resultados"
        
        # ... (código de creación del Excel igual que antes)
        
        # Guardar en memoria
        excel_buffer = io.BytesIO()
        wb.save(excel_buffer)
        excel_buffer.seek(0)
        
        # Nombre del archivo
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"BrainRush_Resultados_{cuestionario_titulo}_{timestamp}.xlsx"
        
        # Enviar por correo
        enviar_email_con_adjunto(
            destinatario=email_destino,
            asunto=f"Resultados de BrainRush - {cuestionario_titulo}",
            mensaje=f"""
            Hola {usuario[1]} {usuario[2]},
            
            Adjunto encontrarás los resultados de "{cuestionario_titulo}".
            
            Puedes guardar este archivo en tu OneDrive, Google Drive o donde prefieras.
            
            Saludos,
            Sistema BrainRush
            """,
            archivo_adjunto=excel_buffer.getvalue(),
            nombre_archivo=filename
        )
        
        return jsonify({
            'success': True,
            'message': f'Resultados enviados a {email_destino}',
            'filename': filename
        }), 200
        
    except Exception as e:
        print(f"ERROR exportar_email: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500
```

### Opción 2: Usar Microsoft Graph con Application Permissions (Más Complejo)

Esta opción permite subir archivos a una cuenta de OneDrive específica sin interacción del usuario.

#### Requisitos:
1. Cuenta de Microsoft 365 institucional (@usat.pe)
2. Una cuenta de "servicio" donde se almacenarán todos los archivos
3. Permisos de aplicación en Azure

#### Pasos de Configuración:

1. **Registrar App en Azure** (mismo que antes)

2. **Configurar Permisos de APLICACIÓN** (no delegados):
   - En Azure Portal → API Permissions
   - Agregar `Files.ReadWrite.All` como **Application Permission**
   - Requiere consentimiento de administrador

3. **Crear carpetas por usuario**:
   ```
   OneDrive Institucional/
   └── BrainRush/
       ├── ignacio.perez@usat.pe/
       │   ├── Resultados_Cuest1.xlsx
       │   └── Resultados_Cuest2.xlsx
       └── maria.lopez@usat.pe/
           └── Resultados_Cuest3.xlsx
   ```

#### Código de Implementación:

```python
@app.route('/api/exportar-resultados/<int:sala_id>/onedrive-app', methods=['POST'])
def exportar_resultados_onedrive_app(sala_id):
    """Exportar a OneDrive usando Application Permissions"""
    try:
        import msal
        import requests as requests_lib
        
        # Configuración
        CLIENT_ID = os.getenv('ONEDRIVE_CLIENT_ID')
        CLIENT_SECRET = os.getenv('ONEDRIVE_CLIENT_SECRET')
        TENANT_ID = os.getenv('ONEDRIVE_TENANT_ID')
        SERVICE_USER_ID = os.getenv('ONEDRIVE_SERVICE_USER_ID')  # ID del usuario de servicio
        
        # Obtener token de aplicación (no requiere interacción del usuario)
        authority = f"https://login.microsoftonline.com/{TENANT_ID}"
        app = msal.ConfidentialClientApplication(
            CLIENT_ID,
            authority=authority,
            client_credential=CLIENT_SECRET
        )
        
        # Adquirir token para la aplicación
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        
        if "access_token" not in result:
            return jsonify({
                'success': False,
                'error': 'No se pudo obtener token de aplicación'
            }), 500
        
        access_token = result['access_token']
        
        # Obtener datos del usuario actual
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT email FROM usuarios WHERE id_usuario = %s", (session['usuario_id'],))
        usuario = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        email_usuario = usuario[0]
        
        # Crear Excel (mismo código que antes)
        data = request.get_json()
        ranking = data.get('ranking', [])
        total_preguntas = data.get('totalPreguntas', 0)
        cuestionario_titulo = data.get('cuestionarioTitulo', 'Cuestionario')
        
        # ... código de creación del Excel ...
        
        excel_buffer = io.BytesIO()
        wb.save(excel_buffer)
        excel_buffer.seek(0)
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"BrainRush_Resultados_{cuestionario_titulo}_{timestamp}.xlsx"
        
        # Subir a OneDrive del usuario de servicio
        # Crear carpeta por usuario si no existe
        user_folder = email_usuario.replace('@', '_').replace('.', '_')
        upload_url = f"https://graph.microsoft.com/v1.0/users/{SERVICE_USER_ID}/drive/root:/BrainRush/{user_folder}/{filename}:/content"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
        
        response = requests_lib.put(upload_url, headers=headers, data=excel_buffer.getvalue())
        
        if response.status_code in [200, 201]:
            file_info = response.json()
            
            # Crear enlace para compartir
            share_url = f"https://graph.microsoft.com/v1.0/users/{SERVICE_USER_ID}/drive/items/{file_info['id']}/createLink"
            share_response = requests_lib.post(
                share_url,
                headers={'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'},
                json={'type': 'view', 'scope': 'anonymous'}
            )
            
            share_link = share_response.json().get('link', {}).get('webUrl', '')
            
            return jsonify({
                'success': True,
                'message': 'Archivo subido exitosamente',
                'file_name': filename,
                'share_link': share_link
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Error al subir: {response.status_code} - {response.text}'
            }), 500
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500
```

### Opción 3: Usar Dropbox (ALTERNATIVA RECOMENDADA)

Dropbox tiene una API más simple y funciona mejor en PythonAnywhere.

#### Ventajas:
- ✅ API más simple que OneDrive
- ✅ No requiere OAuth2 interactivo
- ✅ Funciona perfectamente en PythonAnywhere
- ✅ Token de acceso permanente

#### Instalación:
```bash
pip install dropbox
```

#### Configuración:

1. Ve a [Dropbox App Console](https://www.dropbox.com/developers/apps)
2. Crea una nueva app
3. Genera un Access Token
4. Agrega el token al `.env`:
   ```
   DROPBOX_ACCESS_TOKEN=tu-token-aqui
   ```

#### Código:

```python
@app.route('/api/exportar-resultados/<int:sala_id>/dropbox', methods=['POST'])
def exportar_resultados_dropbox(sala_id):
    """Exportar a Dropbox"""
    try:
        import dropbox
        
        ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN')
        
        if not ACCESS_TOKEN:
            return jsonify({
                'success': False,
                'error': 'Dropbox no configurado. Agrega DROPBOX_ACCESS_TOKEN al .env'
            }), 501
        
        # Crear cliente de Dropbox
        dbx = dropbox.Dropbox(ACCESS_TOKEN)
        
        # Crear Excel (mismo código)
        data = request.get_json()
        # ... código de Excel ...
        
        excel_buffer = io.BytesIO()
        wb.save(excel_buffer)
        excel_buffer.seek(0)
        
        filename = f"BrainRush_Resultados_{cuestionario_titulo}_{timestamp}.xlsx"
        dropbox_path = f"/BrainRush/{filename}"
        
        # Subir archivo
        dbx.files_upload(
            excel_buffer.getvalue(),
            dropbox_path,
            mode=dropbox.files.WriteMode.add,
            autorename=True
        )
        
        # Crear enlace compartido
        shared_link = dbx.sharing_create_shared_link_with_settings(dropbox_path)
        
        return jsonify({
            'success': True,
            'message': 'Archivo subido a Dropbox',
            'file_name': filename,
            'share_link': shared_link.url
        }), 200
        
    except Exception as e:
        print(f"ERROR dropbox: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
```

## Recomendación para PythonAnywhere

**OPCIÓN RECOMENDADA: Envío por Email** (Opción 1)

Razones:
1. ✅ Ya tienes email configurado
2. ✅ Sin dependencias externas complicadas
3. ✅ El usuario puede guardar donde quiera
4. ✅ Funciona 100% en PythonAnywhere
5. ✅ Sin configuración adicional de Azure/Dropbox

### Implementación Simplificada

Solo necesitas agregar la función para enviar email con adjunto:

```python
def enviar_email_con_adjunto(destinatario, asunto, mensaje, archivo_adjunto, nombre_archivo):
    """Envía un email con un archivo adjunto"""
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    import smtplib
    
    msg = MIMEMultipart()
    msg['From'] = os.getenv('SMTP_USERNAME')
    msg['To'] = destinatario
    msg['Subject'] = asunto
    
    msg.attach(MIMEText(mensaje, 'plain'))
    
    # Adjuntar archivo
    adjunto = MIMEApplication(archivo_adjunto)
    adjunto.add_header('Content-Disposition', 'attachment', filename=nombre_archivo)
    msg.attach(adjunto)
    
    # Enviar
    with smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as server:
        server.starttls()
        server.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD'))
        server.send_message(msg)
```

Y cambiar el botón en el frontend de "Subir a OneDrive" a "Enviar por Correo".

## Decisión Final

¿Qué opción prefieres?

1. **Email con Adjunto** - Más simple, ya funcional
2. **Dropbox** - Almacenamiento en la nube, API simple
3. **OneDrive con App Permissions** - Más complejo, requiere cuenta institucional

---

**Para PythonAnywhere, recomiendo fuertemente la Opción 1 (Email).**
