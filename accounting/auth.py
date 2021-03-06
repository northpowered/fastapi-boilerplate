from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from jose import JWTError, jwt
from datetime import timedelta, datetime
from .models import User
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def create_access_token(data: dict, expires_delta: timedelta | None = None)->str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str)->dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as ex:
        print(ex)#unauthorized
    else:
        return payload

async def get_user_by_token(token: str = Depends(oauth2_scheme))->User:
    payload = decode_access_token(token)
    return await User.get_by_username(payload.get('sub'))