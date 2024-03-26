from sqlalchemy import create_engine

from config.conf import Conf


class DB:
    DB_NAME = Conf.db.DB_NAME
    DB_USER = Conf.db.DB_USER
    DB_PASSWORD = Conf.db.DB_PASSWORD
    DB_HOST = Conf.db.DB_HOST
    DB_PORT = Conf.db.DB_PORT
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
