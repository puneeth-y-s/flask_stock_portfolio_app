from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

engine = None
SessionLocal = None

def init_db(uri: str):
    global engine, SessionLocal
    engine = create_engine(uri, future=True, echo=False)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

@contextmanager
def get_db_session():
    if SessionLocal is None:
        raise Exception("Database not initialized. Call init_db(uri) first.")
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()