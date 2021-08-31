from sqlalchemy.orm import Session

from . import models
from .schemas import UserCreate, MovieBase


class UserService:
    def __init__(self, database_session: Session):
        self.session = database_session

    def get_user(self, user_id: str):
        return self.session.query(models.User).filter(models.User.id == user_id).first()

    def get_user_by_email(self, email: str):
        return self.session.query(models.User).filter(models.User.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.session.query(models.User).offset(skip).limit(limit).all()

    def create_user(self, user: UserCreate):
        db_user = models.User(**user.dict())
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user


class MovieService:
    def __init__(self, database_session: Session):
        self.session = database_session

    def get_movie(self, movie_id: str):
        return self.session.query(models.Movie).filter(models.Movie.id == movie_id).first()

    def delete(self, imdb_id: str):
        return self.session.query(models.Movie).filter(models.Movie.imdb_id == imdb_id).delete()

    def get_movie_by_imdb_id(self, imdb_id: str):
        return self.session.query(models.Movie).filter(models.Movie.imdb_id == imdb_id).first()

    def get_movies(self, skip: int = 0, limit: int = 100):
        return self.session.query(models.Movie).offset(skip).limit(limit).all()

    def create_movie(self, movie: MovieBase):
        db_movie = models.Movie(**movie.dict())
        self.session.add(db_movie)
        self.session.commit()
        self.session.refresh(db_movie)
        return db_movie
