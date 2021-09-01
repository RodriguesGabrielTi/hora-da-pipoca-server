import traceback
from json import JSONDecodeError

from config import settings
from domain.database import SessionLocal
from domain.schemas import MovieBase
from popcorn_time.domain.service import MovieService
import requests

WORLDS_TO_SEARCH = ['action', 'azul', 'barbie', 'mundo', 'pink', 'morte', 'terror', 'amor', 'homem','mulher','amanda','jesus','brasil','arma','love','house','car','travel','school','high','down','EUA']


def run():
    movies_imdb_ids = get_movies_imdb_ids()
    movies = get_movies(movies_imdb_ids)
    db = SessionLocal()
    movie_service = MovieService(db)
    count_success = 0
    for movie in movies:
        try:
            if movie_service.get_movie_by_imdb_id(movie.get('imdbID')):
                continue

            movie_base = MovieBase(
                imdb_id=movie.get('imdbID'),
                title=movie.get('Title'),
                year=movie.get('Year'),
                rated=movie.get('Rated'),
                released=movie.get('Released'),
                runtime_minutes=format_to_minute(movie.get('Runtime')),
                genre=movie.get('Genre'),
                director=movie.get('Director'),
                writer=movie.get('Writer'),
                actors=movie.get('Actors'),
                plot=movie.get('Plot'),
                language=movie.get('Language'),
                country=movie.get('Country'),
                awards=movie.get('Awards'),
                poster=movie.get('Poster'),
                rating_rotten_tomatoes=get_rotten_tomatoes(movie.get('Ratings')),
                meta_score=int(movie.get('Metascore')) if not movie.get('Metascore') == 'N/A' else None,
                imdb_rating=float(movie.get('imdbRating') if movie.get('imdbRating') != 'N/A' else 0),
                imdb_votes=int(movie.get('imdbVotes').replace(',', '')),
                type=movie.get('Type')
            )

            movie_service.create_movie(movie_base)
            count_success += 1
            print(count_success)
        except Exception as error:
            db.rollback()
            print(f'error:\n  short: {str(error)}\n  full: {str(traceback.format_exc())}')
    db.close()


def get_rotten_tomatoes(ratings: dict):
    for rating in ratings:
        if rating.get('Source') == 'Rotten Tomatoes':
            return rating.get('Value')


def get_movies(imdb_ids: []):
    movies = []
    for id in imdb_ids:
        response = requests.get(settings.OMDB_API, params={'apikey': settings.OMDB_API_2, 'i': id})
        if response.status_code == 200:
            print(response.json())
            movies.append(response.json())
    return movies


def format_to_minute(string_to_format: str):
    try:
        minute = int(string_to_format.replace(' min', ''))
    except ValueError:
        minute = 0
    return minute


def get_movies_imdb_ids():
    movies_imdb_ids = []
    query = {'apikey': settings.OMDB_KEY, 'type': 'series'}
    for word in WORLDS_TO_SEARCH:
        query.update({'s': word})
        for page in [1, 2, 3, 4]:
            query.update({'page': str(page)})
            response = requests.get(settings.OMDB_API, params=query)
            try:
                response_json = response.json().get('Search')
            except JSONDecodeError:
                continue
            if response.status_code == 200 and response_json is not None:
                for movie in response.json().get('Search'):
                    print(movie)
                    movies_imdb_ids.append(movie.get('imdbID'))
    return list(dict.fromkeys(movies_imdb_ids))


if __name__ == '__main__':
    run()