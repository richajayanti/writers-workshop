from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from typing import Generator

DATABASE_URL = "sqlite:///./throughline.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# A session is one unit of work. In a web app, a session is a short-lived workspace for an HTTP request.
# It tracks the objects I've loaded/added and notices which ones changed.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Generator function (from 312)
def get_db() -> Generator:
    db = SessionLocal()
    # FastAPI runs the code up to yield, hands the session my endpoint, and after endpoint finishes, runs the finally.
    try:
        yield db
    finally:
        db.close()





