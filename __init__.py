from flask import Flask

from routes.register_routes import *

# Importa las rutas desde otro archivo


def create_app():
    app = Flask(__name__)

    # Configuración (por ejemplo, claves, conexión a bases de datos, etc.)
    # app.config.from_object('config.json')  # Si tienes configuraciones adicionales en config.py
    def load_config(file_path):
        import json

        with open(file_path, "r") as file:
            return json.load(file)

    # Leer la configuración desde el archivo JSON
    config = load_config("config.json")
    app.config.update(config)

    # Registramos las rutas
    register_routes(app)

    return app
