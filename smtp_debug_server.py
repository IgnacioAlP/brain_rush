"""
Servidor SMTP de debugging para desarrollo local
Este servidor recibe correos y los muestra en la consola sin enviarlos realmente.

USO:
1. Abre una terminal y ejecuta: python smtp_debug_server.py
2. Deja esta terminal abierta mientras desarrollas
3. En otra terminal, ejecuta: python main.py
4. Los correos aparecerán en la terminal del servidor SMTP

IMPORTANTE: Este servidor es SOLO para desarrollo.
NO usar en producción.
"""

import asyncore
from smtpd import SMTPServer
from datetime import datetime

class DebuggingSMTPServer(SMTPServer):
    """Servidor SMTP que imprime los correos en la consola"""
    
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        """Procesar mensaje recibido"""
        print("\n" + "="*80)
        print(f"📧 CORREO RECIBIDO - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        print(f"De: {mailfrom}")
        print(f"Para: {', '.join(rcpttos)}")
        print(f"Peer: {peer}")
        print("-"*80)
        print("Contenido del mensaje:")
        print("-"*80)
        
        # Decodificar el mensaje
        try:
            message = data.decode('utf-8')
        except:
            message = data.decode('latin-1')
        
        print(message)
        print("="*80 + "\n")
        
        # No retornar nada significa que el mensaje fue procesado exitosamente
        return

if __name__ == '__main__':
    print("="*80)
    print("🚀 Servidor SMTP de Debugging para Brain RUSH")
    print("="*80)
    print(f"Escuchando en: localhost:1025")
    print("Presiona Ctrl+C para detener el servidor")
    print("-"*80)
    print("Los correos enviados desde la aplicación aparecerán aquí")
    print("="*80 + "\n")
    
    try:
        server = DebuggingSMTPServer(('localhost', 1025), None)
        asyncore.loop()
    except KeyboardInterrupt:
        print("\n\n" + "="*80)
        print("❌ Servidor SMTP detenido")
        print("="*80)
