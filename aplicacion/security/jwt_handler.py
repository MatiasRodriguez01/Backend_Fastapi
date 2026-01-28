from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 # minutes

def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = {
        "sub": username,
        "exp": expire
    }
    token = jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }