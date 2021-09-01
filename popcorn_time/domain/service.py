from passlib.context import CryptContext
from sqlalchemy import text
from sqlalchemy.orm import Session

from . import models
from .schemas import UserCreate, MovieBase, User, Movie


class UserService:
    def __init__(self, db):
        self.session = db
        self.__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_user(self, user_id: str):
        return self.session.query(models.User).filter(models.User.id == user_id).first()

    def update_user(self, user_id: str, data):
        update_data = data.dict(exclude_unset=True)
        self.session.query(models.User).filter(models.User.id == user_id).update(update_data)
        return self.get_user(user_id)

    def get_user_by_email(self, email: str):
        return self.session.query(models.User).filter(models.User.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.session.query(models.User).offset(skip).limit(limit).all()

    def create_user(self, user: UserCreate):
        user.password = self.get_password_hash(user.password)
        db_user = models.User(**user.dict())
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def get_password_hash(self, password):
        return self.__pwd_context.hash(password)


class MovieService:
    def __init__(self, database_session: Session):
        self.session = database_session

    def get_movie(self, movie_id: str):
        return self.session.query(models.Movie).filter(models.Movie.id == movie_id).first()

    def delete(self, imdb_id: str):
        return self.session.query(models.Movie).filter(models.Movie.imdb_id == imdb_id).delete()

    def get_movie_by_imdb_id(self, imdb_id: str):
        return self.session.query(models.Movie).filter(models.Movie.imdb_id == imdb_id).first()

    def get_movies(
            self,
            skip: int = 0,
            limit: int = 100,
            search: str = None,
            filters: [] = None,
    ):
        query = self.session.query(models.Movie)
        if search:
            query = query.filter(text("movie.title LIKE '%{}%'".format(search)))
        for filter in filters:
            query = query.filter(text("movie.{} = '{}'".format(filter['column'], filter['value'])))

        return query.order_by(text('-imdb_rating')).offset(skip).limit(limit).all()

    def create_movie(self, movie: MovieBase):
        db_movie = models.Movie(**movie.dict())
        self.session.add(db_movie)
        self.session.commit()
        self.session.refresh(db_movie)
        return db_movie

    def add_to_favorite(self, movie: Movie, user: User):
        db_favorite = models.Favorite(**{'movie_id': movie.id, 'user_id': user.id})
        self.session.add(db_favorite)
        self.session.commit()
        self.session.refresh(db_favorite)
        return db_favorite
