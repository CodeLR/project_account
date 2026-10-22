
from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column
from database import Base
import datetime


class User(Base):
    __tablename__ = "Silvestr"
    id:Mapped[int]=mapped_column(primary_key=True)
    password_hash:Mapped[str]=mapped_column(String(255),nullable=False)
    name:Mapped[str]=mapped_column(String(30),nullable=False)
    role:Mapped[str]=mapped_column(String(10),nullable=False)
    email:Mapped[str]=mapped_column(String(40),unique=True,nullable=False)
    created_at:Mapped[datetime.datetime]=mapped_column(nullable=False,default=datetime.datetime.now)

