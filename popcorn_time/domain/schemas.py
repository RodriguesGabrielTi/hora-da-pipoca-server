from datetime import date
from pydantic import BaseModel


# user
class UserBase(BaseModel):
    nick_name: str
    full_name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    is_active: bool
    created_date: date

    class Config:
        orm_mode = True
