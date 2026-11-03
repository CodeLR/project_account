
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped,mapped_column
from database import Base
import datetime

class RefreshSession(Base):
    __tablename__ = "refresh_sessions"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id:Mapped[int]=mapped_column(Integer,ForeignKey("Silvestr.id"),nullable=False)
    token_hash:Mapped[str]=mapped_column(String(64),unique=True,nullable=False)
    expires_at:Mapped[datetime.datetime]=mapped_column(DateTime(timezone=True),nullable=False)
    revoked:Mapped[bool]=mapped_column(Boolean,default=False,nullable=False)

