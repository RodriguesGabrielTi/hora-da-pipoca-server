import os

# Database
DATABASE_USER = os.getenv('DATABASE_USER', 'user_pop')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '1234')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'popcorn_time')
SQLALCHEMY_DATABASE_URL = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'