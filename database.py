import logging
import classes
import pg8000

from dotenv import dotenv_values

from sqlalchemy import text, create_engine

logger = logging.getLogger(__name__)

USER, KEY_VAL, HOST, DB = (env for env in dotenv_values('.env').values())

#ENGINE = create_engine(f"postgresql+pg8000://{USER}:{KEY_VAL}@{HOST}/{DB}", client_encoding='utf8')


class DatabaseManager:
    """Define"""

    def __init__(self, engine, db_base):
        """Define"""
        self.engine = engine
        self.db_base = db_base

    def __str__(self):
        return f'{self.engine}, {self.db_base}'

    def __repr__(self):
        return f'{__class__.__name__}({self.engine}, {self.db_base})'

    def initialize_tables(self):
        self.db_base.metadata.create_all(self.engine)
