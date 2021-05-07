from sqlalchemy import text, create_engine

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)

