import logging
import classes
import pg8000

from dotenv import dotenv_values

from sqlalchemy import text, create_engine
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

USER, KEY_VAL, HOST, DB = (env for env in dotenv_values('.env').values())

#ENGINE = create_engine(f"postgresql+pg8000://{USER}:{KEY_VAL}@{HOST}/{DB}", client_encoding='utf8')

ENGINE = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
DB_BASE = classes.db_class


def session_context_mgr(method):
    session = Session(ENGINE)

    def session_wrapper(*args, **kwargs):
        with session as sess:
            result = method(sess, *args, **kwargs)
            if result is not None:
                return result
            else:
                sess.commit()
                return

    return session_wrapper


DB_BASE.metadata.create_all(ENGINE)


@session_context_mgr
def add_instance(session, instances):
    for instance in instances:
        session.add(instance)
    return


@session_context_mgr
def delete_obj(session, objects):
    for obj in objects:
        session.delete(obj)
    return


DB_BASE.metadata.create_all(ENGINE)
user = classes.User('BoogtehWoog', 'BoogtehWoog@gmail.com', 'Boogest', 185, 180)


add_instance((user,))
