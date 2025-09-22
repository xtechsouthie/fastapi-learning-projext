from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

SECRET_KEY = "helloworld" #i am lazy to put this in .gitignore
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#def verify_access_token(token: str, credentials_exception):
