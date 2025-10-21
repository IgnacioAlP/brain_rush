from flask_mail import Mail

# Creamos la instancia de Mail aquí, pero sin asociarla a la app todavía.
# Se inicializará en main.py usando mail.init_app(app).
mail = Mail()