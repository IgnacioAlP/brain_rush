import os

class Config:
    """Configuración base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-temporal-desarrollo'
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    SECRET_KEY = 'clave-temporal-desarrollo'

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