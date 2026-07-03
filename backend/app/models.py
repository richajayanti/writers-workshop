from app.database import Base
from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, UTC


class Investigation(Base):
    __tablename__ = "investigations"
    
    id: Mapped[int] = mapped_column(primary_key=True)   
    title: Mapped[str] = mapped_column(String(255))
    brain_dump: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(255), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    
    
    