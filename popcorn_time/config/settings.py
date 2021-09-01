import os

# Database
DATABASE_URL = os.getenv('REAL_DATABASE_URL', f'postgresql://user_pop:1234@localhost/popcorn_time')

# OMDB Api
OMDB_API = os.getenv('OMDB_API', 'http://www.omdbapi.com/')
OMDB_API_2 = os.getenv('API_KEY', 'a953d81e')
OMDB_KEY = os.getenv('API_KEY', 'a953d81e')

# Auth
SECRET_KEY = "781e5920c29873d717c4218c36b35c4e092d3a5f9df5835a84502bb41a8d8c8a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 90

