from datetime import datetime
import uuid

from sqlalchemy import Column, String, Integer, ARRAY, Float, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    nick_name = Column(String)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created_date = Column(Date, default=datetime.today())
    new_field = Column(String)


class Favorite(Base):
    __tablename__ = 'favorite'

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('user.id'))
    movie_id = Column(String(36), ForeignKey('movie.id'))



class Movie(Base):
    __tablename__ = "movie"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    imdb_id = Column(String, unique=True, index=True)
    title = Column(String)
    year = Column(String(4))
    rated = Column(String)
    released = Column(String)
    runtime_minutes = Column(Integer)
    genre = Column(String)
    director = Column(String)
    writer = Column(String)
    actors = Column(String)
    plot = Column(String)
    language = Column(String)
    country = Column(String)
    awards = Column(String)
    poster = Column(String)
    rating_rotten_tomatoes = Column(String)
    meta_score = Column(Integer)
    imdb_rating = Column(Float)
    imdb_votes = Column(Integer)
    type = Column(String)
