from dotenv import load_dotenv
import os

# Carga por defecto el archivo .env en el directorio raiz del proyecto
# Por defecto, las variables de .env no sobreescriben las variables de entorno
# https://saurabh-kumar.com/python-dotenv/#getting-started
load_dotenv()

# Aunque hay varios métodos de gestionar la configuración en python
# https://stackoverflow.com/q/6198372/1647238
# se optó por usar propiedades de las clases
class SERVER_CONF:
    PORT = os.environ.get('PORT') or 4000
    IP = os.environ.get('IP') or ''