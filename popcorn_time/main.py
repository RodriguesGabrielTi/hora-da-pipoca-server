from typing import List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from popcorn_time.domain.schemas import Token, UserBase
from popcorn_time.domain.auth import Auth
from popcorn_time.domain.service import MovieService
from popcorn_time.domain import models, schemas
from popcorn_time.domain.database import engine, SessionLocal
from popcorn_time.domain.service import UserService

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.middleware("http")
async def app_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# user
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate,  db: Session = Depends(get_db)):
    user_service = UserService(db)
    db_user = user_service.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return user_service.create_user(user=user)


@app.get("/users/", response_model=List[schemas.User], response_model_exclude={"email"})
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: Session = Depends(oauth2_scheme)):
    user_service = UserService(db)
    users = user_service.get_users(skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: str, db: Session = Depends(get_db), token: Session = Depends(oauth2_scheme)):
    user_service = UserService(db)
    db_user = user_service.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.patch("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: str, user: UserBase, db: Session = Depends(get_db), token: Session = Depends(oauth2_scheme)):
    user_service = UserService(db)
    db_user = user_service.update_user(user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users-me", response_model=schemas.User)
async def read_users_me(db: Session = Depends(get_db), token: Session = Depends(oauth2_scheme)):
    user_service = UserService(db)
    auth = Auth(user_service)
    return auth.get_current_active_user(token)


# login
@app.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db),):
    user_service = UserService(db)
    auth = Auth(user_service)
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# books
# user
@app.get("/movies", response_model=List[schemas.Movie])
def read_movies(
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        type: Optional[str] = None,
        year: Optional[str] = None,
        db: Session = Depends(get_db),
        token: Session = Depends(oauth2_scheme)
):
    """
    Liste todos os livros
    :param skip: pagina
    :param limit: intens por pagina
    :param search: busca pelo titulo
    :param type: tipo, pode ser movie ou serie
    :param year: ano de publicação, 2011 exp
    :return:
    """
    movie_service = MovieService(db)
    filters = []
    if type:
        filters.append({'column': 'type', 'value': type})
    if year:
        filters.append({'column': 'year', 'value': year})

    users = movie_service.get_movies(search=search, filters=filters, skip=skip, limit=limit)
    return users


@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def read_movie(movie_id: str, db: Session = Depends(get_db), token: Session = Depends(oauth2_scheme)):
    movie_service = MovieService(db)
    db_user = movie_service.get_movie(movie_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_user


@app.post("/movies/{movie_id}/add-to-favorites")
def favorite_movie(movie_id: str, db: Session = Depends(get_db), token: Session = Depends(oauth2_scheme)):
    user_service = UserService(db)
    movie_service = MovieService(db)
    auth = Auth(user_service)
    user = auth.get_current_active_user(token)
    movie = movie_service.get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=400, detail="Movie not found")

    movie_service.add_to_favorite(movie, user)
    return {'added to favorites'}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
