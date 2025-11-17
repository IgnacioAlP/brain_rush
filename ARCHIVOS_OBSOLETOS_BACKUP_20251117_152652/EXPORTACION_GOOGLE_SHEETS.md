# 📈 Configuración de Exportación a Google Sheets

## 🎯 Descripción General

Brain RUSH permite exportar los resultados de los juegos directamente a Google Sheets, creando una hoja de cálculo en tu Google Drive con todos los datos del ranking.

## ⚙️ Configuración Necesaria

### 1. Crear Proyecto en Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Nombre sugerido: "Brain RUSH Exports"

### 2. Habilitar APIs Necesarias

En tu proyecto de Google Cloud:

1. Ve a **APIs & Services > Library**
2. Busca y habilita las siguientes APIs:
   - **Google Sheets API**
   - **Google Drive API**

### 3. Crear Credenciales OAuth 2.0

1. Ve a **APIs & Services > Credentials**
2. Clic en **+ CREATE CREDENTIALS** → **OAuth client ID**
3. Si es la primera vez, configura la **OAuth consent screen**:
   - User Type: **External**
   - App name: **Brain RUSH**
   - User support email: tu email
   - Developer contact: tu email
   - Scopes: Agregar los siguientes:
     - `https://www.googleapis.com/auth/spreadsheets`
     - `https://www.googleapis.com/auth/drive.file`

4. Después de configurar el consent screen, crea las credenciales:
   - Application type: **Web application**
   - Name: **Brain RUSH Web Client**
   - Authorized redirect URIs:
     - `http://localhost:8081/oauth2callback` (para desarrollo)
     - `https://tu-dominio.com/oauth2callback` (para producción)

5. Descarga el archivo JSON de credenciales

### 4. Configurar Variables de Entorno

Agrega las siguientes variables a tu archivo `.env`:

```env
# Google Sheets Configuration
GOOGLE_CLIENT_ID=tu_client_id_aqui.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu_client_secret_aqui
GOOGLE_REDIRECT_URI=http://localhost:8081/oauth2callback
```

### 5. Instalar Librerías Necesarias

```bash
pip install google-auth google-auth-oauthlib google-api-python-client
```

## 🔧 Implementación Completa (Para Desarrolladores)

### Archivo: `google_sheets_service.py`

```python
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from datetime import datetime

class GoogleSheetsService:
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file'
    ]
    
    def __init__(self):
        self.client_config = {
            "web": {
                "client_id": os.getenv('GOOGLE_CLIENT_ID'),
                "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
                "redirect_uris": [os.getenv('GOOGLE_REDIRECT_URI')],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        }
    
    def get_authorization_url(self, state=None):
        """Genera URL de autorización de Google"""
        flow = Flow.from_client_config(
            self.client_config,
            scopes=self.SCOPES,
            state=state
        )
        flow.redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        return authorization_url, state
    
    def get_credentials_from_code(self, code):
        """Obtiene credenciales a partir del código de autorización"""
        flow = Flow.from_client_config(
            self.client_config,
            scopes=self.SCOPES
        )
        flow.redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')
        flow.fetch_token(code=code)
        
        return flow.credentials
    
    def create_spreadsheet(self, credentials, titulo, ranking, total_preguntas):
        """Crea una hoja de cálculo con los resultados"""
        try:
            service = build('sheets', 'v4', credentials=credentials)
            
            # Crear spreadsheet
            spreadsheet = {
                'properties': {
                    'title': f'Brain RUSH - {titulo} - {datetime.now().strftime("%Y-%m-%d %H:%M")}'
                },
                'sheets': [{
                    'properties': {
                        'title': 'Resultados',
                        'gridProperties': {
                            'frozenRowCount': 1
                        }
                    }
                }]
            }
            
            spreadsheet = service.spreadsheets().create(
                body=spreadsheet,
                fields='spreadsheetId,spreadsheetUrl'
            ).execute()
            
            spreadsheet_id = spreadsheet.get('spreadsheetId')
            
            # Preparar datos
            headers = [['Posición', 'Nombre', 'Resp. Correctas', 'Total Preguntas', 'Precisión', 'Puntuación', 'Tiempo (s)']]
            
            rows = []
            for player in ranking:
                precision = round((player['respuestas_correctas'] / total_preguntas) * 100) if total_preguntas > 0 else 0
                rows.append([
                    player['posicion'],
                    player['nombre_participante'],
                    player['respuestas_correctas'],
                    total_preguntas,
                    f"{precision}%",
                    player['puntaje_total'],
                    round(player['tiempo_total_respuestas'], 2)
                ])
            
            # Insertar datos
            body = {
                'values': headers + rows
            }
            
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range='Resultados!A1',
                valueInputOption='RAW',
                body=body
            ).execute()
            
            # Formatear encabezados
            requests = [{
                'repeatCell': {
                    'range': {
                        'sheetId': 0,
                        'startRowIndex': 0,
                        'endRowIndex': 1
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': {
                                'red': 0.4,
                                'green': 0.49,
                                'blue': 0.91
                            },
                            'textFormat': {
                                'foregroundColor': {
                                    'red': 1.0,
                                    'green': 1.0,
                                    'blue': 1.0
                                },
                                'bold': True
                            }
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            }]
            
            service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={'requests': requests}
            ).execute()
            
            return spreadsheet.get('spreadsheetUrl')
            
        except HttpError as error:
            print(f'Error creating spreadsheet: {error}')
            raise
```

### Actualizar `main.py`

```python
from google_sheets_service import GoogleSheetsService

# Instancia global
google_sheets_service = GoogleSheetsService()

@app.route('/oauth2callback')
def oauth2callback():
    """Callback de OAuth2 para Google"""
    code = request.args.get('code')
    state = request.args.get('state')
    
    if not code:
        flash('Error en la autorización de Google', 'error')
        return redirect(url_for('dashboard_docente'))
    
    try:
        credentials = google_sheets_service.get_credentials_from_code(code)
        
        # Guardar credenciales en sesión (o en base de datos para persistencia)
        session['google_credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        flash('✅ Cuenta de Google conectada correctamente', 'success')
        
        # Redirigir a la página de resultados si hay sala_id en state
        if state:
            return redirect(url_for('ver_resultados_juego', sala_id=state))
        
        return redirect(url_for('dashboard_docente'))
        
    except Exception as e:
        print(f"Error en OAuth callback: {e}")
        flash('❌ Error al conectar con Google', 'error')
        return redirect(url_for('dashboard_docente'))

@app.route('/api/exportar-resultados/<int:sala_id>/google-sheets', methods=['POST'])
def exportar_resultados_google_sheets(sala_id):
    """Exportar resultados a Google Sheets"""
    try:
        data = request.get_json()
        ranking = data.get('ranking', [])
        total_preguntas = data.get('totalPreguntas', 0)
        cuestionario_titulo = data.get('cuestionarioTitulo', 'Cuestionario')
        
        # Verificar si hay credenciales guardadas
        google_creds = session.get('google_credentials')
        
        if not google_creds:
            # Generar URL de autorización
            auth_url, state = google_sheets_service.get_authorization_url(state=str(sala_id))
            return jsonify({
                'success': False,
                'auth_required': True,
                'auth_url': auth_url
            })
        
        # Reconstruir credenciales
        from google.oauth2.credentials import Credentials
        credentials = Credentials(
            token=google_creds['token'],
            refresh_token=google_creds.get('refresh_token'),
            token_uri=google_creds['token_uri'],
            client_id=google_creds['client_id'],
            client_secret=google_creds['client_secret'],
            scopes=google_creds['scopes']
        )
        
        # Crear spreadsheet
        sheet_url = google_sheets_service.create_spreadsheet(
            credentials, 
            cuestionario_titulo, 
            ranking, 
            total_preguntas
        )
        
        return jsonify({
            'success': True,
            'sheet_url': sheet_url
        })
        
    except Exception as e:
        print(f"ERROR exportar_google_sheets: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500
```

## 📝 Uso

1. **Primera vez**: Al hacer clic en "Subir a Google Sheets", se abrirá una ventana para autorizar la aplicación
2. **Autorización**: Inicia sesión con tu cuenta de Google y acepta los permisos
3. **Exportación**: Después de autorizar, vuelve a hacer clic en "Subir a Google Sheets"
4. **Resultado**: Se creará una nueva hoja de cálculo en tu Google Drive y se abrirá automáticamente

## 🔒 Seguridad

- Las credenciales se guardan de forma segura en la sesión del usuario
- Solo se solicitan permisos para crear archivos nuevos (no acceso completo al Drive)
- La aplicación solo puede acceder a archivos que ella misma creó

## 🐛 Solución de Problemas

### Error: "Redirect URI mismatch"
- Verifica que la URI en Google Cloud Console coincida exactamente con la de tu `.env`
- Para desarrollo local: `http://localhost:8081/oauth2callback`

### Error: "Invalid client"
- Verifica que `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET` estén correctamente configurados
- Descarga nuevamente las credenciales de Google Cloud Console

### Error: "Access denied"
- El usuario rechazó los permisos
- Vuelve a intentar la exportación para obtener una nueva URL de autorización

## 📚 Referencias

- [Google Sheets API Documentation](https://developers.google.com/sheets/api)
- [Google Drive API Documentation](https://developers.google.com/drive/api)
- [OAuth 2.0 for Web Applications](https://developers.google.com/identity/protocols/oauth2/web-server)
