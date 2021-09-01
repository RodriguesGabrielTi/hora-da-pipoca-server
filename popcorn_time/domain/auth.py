from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette.status import HTTP_401_UNAUTHORIZED

from popcorn_time.config import settings
from popcorn_time.config.settings import SECRET_KEY, ALGORITHM
from popcorn_time.domain.schemas import TokenData
from popcorn_time.domain.service import UserService


class Auth:
    def __init__(self, user_service: UserService):
        self.__user_service = user_service
        self.__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def authenticate_user(self, user_email: str, password: str):
        user = self.__user_service.get_user_by_email(user_email)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user

    def verify_password(self, plain_password, hashed_password):
        return self.__pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.__pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def get_current_user(self, token):
        credentials_exception = HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_email: str = payload.get("sub")
            if user_email is None:
                raise credentials_exception
            token_data = TokenData(user_email=user_email)
        except JWTError:
            raise credentials_exception
        user = self.__user_service.get_user_by_email(token_data.user_email)
        if user is None:
            raise credentials_exception
        return user

    def get_current_active_user(self, token):
        user = self.get_current_user(token)
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

        return user

    def is_authentic(self, token):
        self.get_current_active_user(token)
