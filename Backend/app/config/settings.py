import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def get_database_url():
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        name = os.getenv("DB_NAME", "vlab_db")
        user = os.getenv("DB_USER", "postgres")
        password = os.getenv("DB_PASSWORD", "postgres")
        return f"postgresql://{user}:{password}@{host}:{port}/{name}"

    SQLALCHEMY_DATABASE_URI = get_database_url.__func__()


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_by_env = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
