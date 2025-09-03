from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os

from src.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()