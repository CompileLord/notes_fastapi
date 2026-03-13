from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_NAME

engine = create_engine(DB_NAME, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    session = SessionLocal()
    return session
