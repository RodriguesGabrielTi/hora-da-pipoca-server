import os

# Database
DATABASE_URL = os.getenv('REAL_DATABASE_URL', f'postgresql://user_pop:1234@localhost/popcorn_time')

# OMDB Api
OMDB_API = os.getenv('OMDB_API', 'http://www.omdbapi.com/')
OMDB_API_2 = os.getenv('API_KEY', 'a953d81e')
OMDB_KEY = os.getenv('API_KEY', 'a953d81e')

