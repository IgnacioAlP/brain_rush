# -*- coding: utf-8 -*-
"""
Script de prueba para verificar envío de correo
"""
import sys
import os

# Agregar el directorio al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_envio_correo():
    """Probar envío de correo"""
    print("\n" + "="*60)
    print("📧 PRUEBA DE ENVÍO DE CORREO - BRAIN RUSH")
    print("="*60)
    
    # Importar después de configurar el path
    from flask import Flask
    from config import config
    from extensions import mail
    from dotenv import load_dotenv
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Crear app de Flask
    app = Flask(__name__)
    env = os.getenv('FLASK_ENV', 'development')
    app_config = config.get(env, config['default'])
    app.config.from_object(app_config)
    
    # Inicializar mail
    mail.init_app(app)
    
    print(f"\n📋 Configuración actual de correo:")
    print(f"   MAIL_ENABLED: {app.config.get('MAIL_ENABLED')}")
    print(f"   MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
    print(f"   MAIL_PORT: {app.config.get('MAIL_PORT')}")
    print(f"   MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
    print(f"   MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
    
    # Verificar que esté habilitado
    if not app.config.get('MAIL_ENABLED'):
        print("\n⚠️  ADVERTENCIA: MAIL_ENABLED está en False")
        print("   Cambia MAIL_ENABLED = True en config.py")
        return False
    
    # Verificar credenciales
    if not app.config.get('MAIL_USERNAME') or not app.config.get('MAIL_PASSWORD'):
        print("\n❌ ERROR: Faltan credenciales de correo en .env")
        print("   Asegúrate de tener:")
        print("   MAIL_USERNAME=tu-correo@gmail.com")
        print("   MAIL_PASSWORD=tu-contraseña-de-aplicacion")
        return False
    
    # Pedir correo de destino
    print("\n" + "-"*60)
    destinatario = input("✉️  Ingresa tu correo para recibir el correo de prueba: ").strip()
    
    if not destinatario or '@' not in destinatario:
        print("❌ Correo inválido")
        return False
    
    print(f"\n📤 Enviando correo de prueba a: {destinatario}")
    print("⏳ Espera un momento...")
    
    try:
        with app.app_context():
            from flask_mail import Message
            
            msg = Message(
                subject='🧠 Prueba de Correo - Brain Rush',
                sender=app.config.get('MAIL_USERNAME'),
                recipients=[destinatario],
                html="""
                <html>
                    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                        <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                            <h1 style="color: #4ECDC4; text-align: center;">🧠 Brain Rush</h1>
                            <h2 style="color: #333; border-bottom: 2px solid #4ECDC4; padding-bottom: 10px;">
                                ¡Correo de Prueba Exitoso! ✅
                            </h2>
                            <p style="color: #666; font-size: 16px; line-height: 1.6;">
                                Si estás viendo este correo, significa que la configuración de Gmail 
                                está <strong>correctamente configurada</strong> y funcionando.
                            </p>
                            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 5px; margin: 20px 0;">
                                <h3 style="margin-top: 0; color: white;">📊 Configuración Verificada:</h3>
                                <p style="margin: 5px 0;">✅ Servidor SMTP conectado</p>
                                <p style="margin: 5px 0;">✅ Autenticación exitosa</p>
                                <p style="margin: 5px 0;">✅ Puerto TLS funcionando</p>
                                <p style="margin: 5px 0;">✅ Envío de correos operativo</p>
                            </div>
                            <div style="background: #f9f9f9; padding: 15px; border-left: 4px solid #4ECDC4; margin: 20px 0;">
                                <p style="margin: 5px 0; color: #555;"><strong>Servidor:</strong> smtp.gmail.com</p>
                                <p style="margin: 5px 0; color: #555;"><strong>Puerto:</strong> 587</p>
                                <p style="margin: 5px 0; color: #555;"><strong>Seguridad:</strong> TLS</p>
                                <p style="margin: 5px 0; color: #555;"><strong>Estado:</strong> <span style="color: #4ECDC4; font-weight: bold;">Activo ✅</span></p>
                            </div>
                            <p style="color: #666; font-size: 14px; line-height: 1.6;">
                                Ahora puedes usar el sistema de registro y recuperación de contraseña 
                                sin problemas. Los correos de confirmación se enviarán automáticamente.
                            </p>
                            <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                                <p style="color: #999; font-size: 12px; margin: 0;">
                                    Este es un correo automático de prueba del sistema Brain Rush
                                </p>
                                <p style="color: #999; font-size: 12px; margin: 5px 0;">
                                    No respondas a este correo
                                </p>
                            </div>
                        </div>
                    </body>
                </html>
                """
            )
            
            mail.send(msg)
            
            print("\n" + "="*60)
            print("✅ ¡CORREO ENVIADO EXITOSAMENTE!")
            print("="*60)
            print(f"\n📬 Revisa la bandeja de entrada de: {destinatario}")
            print(f"📁 Si no lo ves, revisa la carpeta de SPAM/Correo no deseado")
            print("\n💡 Si recibiste el correo, la configuración está PERFECTA ✅")
            print()
            return True
            
    except Exception as e:
        print("\n" + "="*60)
        print("❌ ERROR AL ENVIAR CORREO")
        print("="*60)
        print(f"\n🔴 Error: {str(e)}")
        
        print("\n🔍 Posibles causas y soluciones:")
        print("\n1️⃣  Contraseña de aplicación incorrecta:")
        print("   → Ve a: https://myaccount.google.com/apppasswords")
        print("   → Genera una nueva contraseña de aplicación")
        print("   → Actualiza MAIL_PASSWORD en el archivo .env")
        
        print("\n2️⃣  Verificación en 2 pasos no activada:")
        print("   → Ve a: https://myaccount.google.com/signinoptions/two-step-verification")
        print("   → Activa la verificación en 2 pasos")
        print("   → Luego genera la contraseña de aplicación")
        
        print("\n3️⃣  Credenciales incorrectas en .env:")
        print("   → Abre: .env")
        print("   → Verifica MAIL_USERNAME (debe ser tu correo completo)")
        print("   → Verifica MAIL_PASSWORD (debe ser la contraseña de 16 caracteres)")
        
        print("\n4️⃣  Firewall o antivirus bloqueando:")
        print("   → Desactiva temporalmente el firewall/antivirus")
        print("   → Prueba de nuevo")
        
        print("\n📋 Detalles técnicos del error:")
        print("-" * 60)
        import traceback
        traceback.print_exc()
        print("-" * 60)
        
        return False

if __name__ == "__main__":
    try:
        resultado = test_envio_correo()
        sys.exit(0 if resultado else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
