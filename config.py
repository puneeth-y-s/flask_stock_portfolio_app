import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='112358132134123467894321876583426')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        default=f"sqlite:///{os.path.join(BASEDIR, 'instance', 'app.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI',
                                        default=f"sqlite:///{os.path.join(BASEDIR, 'instance', 'test.db')}")