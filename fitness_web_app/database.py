import logging

from dotenv import dotenv_values
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from fitness_web_app import DBASE

logger = logging.getLogger(__name__)

# USER, KEY_VAL, HOST, DB = (env for env in dotenv_values('fitness_web_app/.env').values())
# ENGINE = create_engine(f"postgresql+pg8000://{USER}:{KEY_VAL}@{HOST}/{DB}", client_encoding='utf8')

ENGINE = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
DBASE.metadata.create_all(ENGINE)


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
def update_object(session, query_obj, filter_kwargs):
    obj = select_object(query_obj, filter_kwargs)
    session.delete(obj)


@session_context_mgr
def delete_object(session, query_obj, filter_kwargs):
    statement = select(query_obj).filter_by(**filter_kwargs)
    result = session.execute(statement).first()
    session.delete(result[0])


@session_context_mgr
def retrieve_object(session, query_obj, statement, filter_kwargs):
    result = session.execute(select(query_obj).filter_by(**filter_kwargs))
    return result


def select_object(session, query_obj, filter_kwargs):
    statement = select(query_obj).filter_by(**filter_kwargs)
    result = session.execute(statement)
    return result
