"""
Servidor SMTP de debugging para desarrollo local
Este servidor recibe correos y los muestra en la consola sin enviarlos realmente.

USO:
1. Abre una terminal y ejecuta: python smtp_debug_server.py
2. Deja esta terminal abierta mientras desarrollas
3. En otra terminal, ejecuta tu aplicación para enviar un correo
4. Los correos aparecerán en la terminal del servidor SMTP

IMPORTANTE: Este servidor es SOLO para desarrollo. NO usar en producción.
"""

# ⚠️ CAMBIO CLAVE: SMTPServer ahora se importa desde smtplib.smtp en Python 3.12+
from smtplib.smtp import SMTPServer 
from datetime import datetime
import asyncio

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

        # Decodificar el mensaje.
        # En esta versión, 'data' ya suele ser una instancia de email.message.Message, 
        # pero mantenemos la decodificación por si el cliente envía datos brutos.
        try:
            # Intentar decodificar como texto simple
            message = data.decode('utf-8')
        except AttributeError:
            # Si 'data' es un objeto Message, obtener el contenido
            try:
                message = data.as_string()
            except:
                message = str(data) # Último recurso
        except:
            message = data.decode('latin-1')

        print(message)
        print("="*80 + "\n")

        # Retornar una cadena vacía o None indica que el mensaje fue aceptado.
        return None 

# ---

async def run_server():
    """Ejecuta el servidor SMTP usando asyncio"""
    
    # Crea la fábrica de protocolos SMTPServer
    # Nota: SMTPServer en la nueva API se usa como una clase de fábrica
    server_factory = lambda: DebuggingSMTPServer(('localhost', 1025), None)
    
    # Inicia el servidor. start_server es la función de alto nivel para iniciar servidores TCP
    server = await asyncio.start_server(
        server_factory, 'localhost', 1025
    )

    addr = server.sockets[0].getsockname()
    print("="*80)
    print("🚀 Servidor SMTP de Debugging")
    print("="*80)
    print(f"Escuchando en: {addr[0]}:{addr[1]}")
    print("Presiona Ctrl+C para detener el servidor")
    print("-"*80)
    print("Los correos enviados desde la aplicación aparecerán aquí")
    print("="*80 + "\n")

    async with server:
        # Esto mantendrá el servidor ejecutándose hasta que se detenga (por Ctrl+C)
        await server.serve_forever()

if __name__ == '__main__':
    try:
        # Ejecuta la función asíncrona principal
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("\n\n" + "="*80)
        print("❌ Servidor SMTP detenido")
        print("="*80)