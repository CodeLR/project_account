from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE = os.getenv("DATABASE_URL")
if not DATABASE:
    raise ValueError("DATABASE_URL is not set")


engine=create_engine(DATABASE)

SessionLocal=sessionmaker(
    autoflush=False,
    bind=engine)



class Base(DeclarativeBase):
    pass

from models.refresh_session import RefreshSession
from models.user import User
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
    