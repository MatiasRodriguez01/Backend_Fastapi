# Dependencias necesarias:
# - dotenv.load_dotenv (para cargar variables desde archivo .env)
# - os (para leer variables de entorno del sistema)

from dotenv import load_dotenv
import os

# settings.py
# Archivo de configuración de seguridad.
# Define las variables globales utilizadas para la autenticación y generación de tokens JWT.
# Carga valores desde variables de entorno usando dotenv.
# Contiene la clave secreta, el algoritmo de firma y el tiempo de expiración de los tokens.

load_dotenv()
class Settings:
    """
    Clase de configuración para seguridad y autenticación.
    - SECRET_KEY: clave secreta usada para firmar los JWT.
    - ALGORITHM: algoritmo de firma (ejemplo: HS256).
    - ACCESS_TOKEN_DURATION: duración del token en minutos.
    - ENV: entorno de ejecución (development, production).
    """

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_DURATION: int = int(os.getenv("ACCESS_TOKEN_DURATION"))
    ENV: str = os.getenv("ENVIRONMENT", "development")  # por defecto 'development'


