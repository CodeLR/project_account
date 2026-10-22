from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
DATABASE="postgresql://myuser:qwerty@127.0.0.1:5432/mydatabase"

engine=create_engine(DATABASE)

SessionLocal=sessionmaker(
    autoflush=False,
    bind=engine)



class Base(DeclarativeBase):
    pass


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
    