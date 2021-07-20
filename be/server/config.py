import os
from typing import List, Type

from be.configuration import DB_USER_NAME, DB_PASSWORD, DB_URL, DB_NAME

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    CONFIG_NAME = "base"
    USE_MOCK_EQUIVALENCY = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    CONFIG_NAME = "development"
    API_ROOT = "tokengallery"
    SECRET_KEY = os.getenv(
        "DEV_SECRET_KEY", "You can't see California without Marlon Widgeto's eyes"
    )
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER_NAME}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}'


EXPORT_CONFIGS: List[Type[BaseConfig]] = [
    DevelopmentConfig
]
config_by_name = {cfg.CONFIG_NAME: cfg for cfg in EXPORT_CONFIGS}
