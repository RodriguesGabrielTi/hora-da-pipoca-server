import os

# Database
DATABASE_USER = os.getenv('DATABASE_USER', 'user_pop')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '1234')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'popcorn_time')
DATABASE_URL = os.getenv('REAL_DATABASE_URL', f'postgresql://user_pop:1234@localhost/popcorn_time')
