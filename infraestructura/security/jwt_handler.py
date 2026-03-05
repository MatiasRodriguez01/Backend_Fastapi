from datetime import datetime, timedelta, timezone
from jose import jwt
from infraestructura.security.settings import Settings

def create_access_token(username: str):
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=Settings.ACCESS_TOKEN_DURATION)
    
    access_token = {
        "sub": username,
        "exp": expire
    }
    token = jwt.encode(access_token, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }