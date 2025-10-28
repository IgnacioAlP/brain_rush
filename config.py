import os

class Config:
    """Configuración base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-temporal-desarrollo'
    DEBUG = False
    TESTING = False
    
    # Configuración de correo (Flask-Mail)
    # NOTA: Correo desactivado temporalmente - usuarios se crean directamente como 'activo'
    MAIL_ENABLED = False  # Cambiar a True cuando se configure un servidor SMTP
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'false').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@brainrush.com'
    
    # Configuración de OneDrive Azure AD
    AZURE_CLIENT_ID = os.environ.get('AZURE_CLIENT_ID')
    AZURE_CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET')
    AZURE_TENANT_ID = os.environ.get('AZURE_TENANT_ID')
    ONEDRIVE_REDIRECT_URI = os.environ.get('ONEDRIVE_REDIRECT_URI') or 'http://localhost:5000/callback/onedrive'
    ONEDRIVE_SCOPES = ['Files.ReadWrite', 'User.Read']

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    SECRET_KEY = 'clave-temporal-desarrollo'
    
    # Configuración de correo Gmail para desarrollo
    # Los correos se envían a direcciones reales vía Gmail SMTP
    MAIL_ENABLED = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')
    
    # Para usar servidor SMTP local (solo consola), descomentar estas líneas y comentar las de arriba:
    # MAIL_SERVER = 'localhost'
    # MAIL_PORT = 1025
    # MAIL_USE_TLS = False
    # MAIL_USERNAME = None
    # MAIL_PASSWORD = None
    # MAIL_DEFAULT_SENDER = 'noreply@brainrush.local'

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cambiar-esta-clave-en-produccion'

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'clave-temporal-testing'

# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}