import os
from typing import (
    List,
    Type,
)

from be.configuration import (
    DB_NAME,
    DB_PASSWORD,
    DB_URL,
    DB_USER_NAME,
)

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    CONFIG_NAME = "base"
    USE_MOCK_EQUIVALENCY = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_ROOT = "tokengallery"
    VERTEX_TABLE_NAME = lambda graph_id: f"graph_{graph_id}_vertex"
    EDGE_TABLE_NAME = lambda graph_id: f"graph_{graph_id}_edge"


class DevelopmentConfig(BaseConfig):
    CONFIG_NAME = "development"
    SECRET_KEY = os.getenv(
        "DEV_SECRET_KEY", "You can't see California without Marlon Widgeto's eyes"
    )
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER_NAME}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}'

class TestingConfig(BaseConfig):
    CONFIG_NAME = "test"
    SECRET_KEY = os.getenv("TEST_SECRET_KEY", "Thanos did nothing wrong")
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER_NAME}:{DB_PASSWORD}@{DB_URL}/tg_test'


EXPORT_CONFIGS: List[Type[BaseConfig]] = [
    DevelopmentConfig,
    TestingConfig
]
config_by_name = {cfg.CONFIG_NAME: cfg for cfg in EXPORT_CONFIGS}
