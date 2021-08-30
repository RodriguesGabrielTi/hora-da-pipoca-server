from pydantic import BaseSettings


class Settings(BaseSettings):
    # default conf goes here
    app_name: str = "PopCorn Time Api"
    admin_email: str = "rodriguesgabrielti@gmail.com"
    items_per_user: int = 50

    class Config:
        env_file = ".env"
