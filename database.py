import logging
import classes
import pg8000

from dotenv import dotenv_values

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

USER, KEY_VAL, HOST, DB = (env for env in dotenv_values('.env').values())

# ENGINE = create_engine(f"postgresql+pg8000://{USER}:{KEY_VAL}@{HOST}/{DB}", client_encoding='utf8')

ENGINE = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
DB_BASE = classes.db_class
DB_BASE.metadata.create_all(ENGINE)


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


@session_context_mgr
def add_object(session, objects):
    for obj in objects:
        session.add(obj)
    return


@session_context_mgr
def select_object_all(session, query_obj, filter_kwargs):
    statement = select(query_obj).filter_by(**filter_kwargs)
    result = session.execute(statement).first()
    return result


@session_context_mgr
def delete_object(session, objects):
    for obj in objects:
        session.delete(obj)
    return
