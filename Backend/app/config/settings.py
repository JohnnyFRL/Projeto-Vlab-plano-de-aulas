import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def get_database_url():
        host = "localhost"
        port = "5432"
        name = "vlab_db"
        user = "postgres"
        password = "13052001"
        return (
        f"postgresql+psycopg2://{user}:{password}"
        f"@{host}:{port}/{name}?client_encoding=utf8"
    )

    SQLALCHEMY_DATABASE_URI = get_database_url.__func__()


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_by_env = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
