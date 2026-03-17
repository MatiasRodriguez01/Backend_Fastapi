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
class Settings():
    """
    Clase de configuración para seguridad y autenticación.
    - SECRET_KEY: clave secreta usada para firmar los JWT.
    - ALGORITHM: algoritmo de firma (ejemplo: HS256).
    - ACCESS_TOKEN_DURATION: duración del token en minutos.
    - ENV: entorno de ejecución (development, production).
    """

    SECRET_KEY: str = os.getenv("SECRET_KEY","super-secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")  # por defecto 'HS256'
    ACCESS_TOKEN_DURATION: int = os.getenv("ACCESS_TOKEN_DURATION", 5)  # por defecto 5 minutos
    ENV: str = os.getenv("ENVIRONMENT", "development")  # por defecto 'development'
    USERNAME: str = os.getenv("USERNAME", "matias_01")
    PASSWORD: str = os.getenv("PASSWORD", "wEdtGgtzVf3vZhiT")
    DATABASE: str = os.getenv("DATABASE", "users")
    ROLE: str = os.getenv("ROLE", "admin")
    MONGODB_URL: str = os.getenv("MONGODB_URL", f"mongodb://matias_01:wEdtGgtzVf3vZhiT@ac-cfgjuuh-shard-00-01.m62gvbp.mongodb.net,ac-cfgjuuh-shard-00-00.m62gvbp.mongodb.net,ac-cfgjuuh-shard-00-02.m62gvbp.mongodb.net/?replicaSet=atlas-ydrdwl-shard-0&tls=true&authSource=admin")
    """
    MONGODB_URL: str = os.getenv("MONGODB_URL", f"mongodb://{USERNAME}:{PASSWORD}@ac-cfgjuuh-shard-00-01.m62gvbp.mongodb.net,ac-cfgjuuh-shard-00-00.m62gvbp.mongodb.net,ac-cfgjuuh-shard-00-02.m62gvbp.mongodb.net/?replicaSet=atlas-ydrdwl-shard-0&tls=true&authSource={ROLE}")
    def MONGO_URI(self) -> str:
        return (
            f"mongodb://{self.USERNAME}:{self.PASSWORD}"
            f"@ac-cfgjuuh-shard-00-01.m62gvbp.mongodb.net,"
            f"ac-cfgjuuh-shard-00-00.m62gvbp.mongodb.net,"
            f"ac-cfgjuuh-shard-00-02.m62gvbp.mongodb.net/"
            f"{self.DATABASE}?replicaSet=atlas-ydrdwl-shard-0&tls=true&authSource={self.ROLE}"
        )
    """

