from datetime import date
from typing import Optional

from pydantic import BaseModel


# token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_email: Optional[str] = None


# user
class UserBase(BaseModel):
    nick_name: str
    full_name: str
    email: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    is_active: bool
    created_date: date

    class Config:
        orm_mode = True


# movie
class MovieBase(BaseModel):
    imdb_id: str
    title: str
    year: str
    rated: str
    released: str
    runtime_minutes: int
    genre: str
    director: str
    writer: str
    actors: str
    plot: str
    language: str
    country: str
    awards: str
    poster: str
    rating_rotten_tomatoes: str = None
    meta_score: str = None
    imdb_rating: float
    imdb_votes: int
    type: str


class Movie(MovieBase):
    id: str

    class Config:
        orm_mode = True


# favorite
class FavoriteBase(BaseModel):
    user_id: str
    movie_id: str


class Favorite(FavoriteBase):
    id: str

    class Config:
        orm_mode: True
