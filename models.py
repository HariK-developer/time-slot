import uuid
from sqlalchemy import (
    ForeignKey,
    func,
    text,
    Column,
    String,
    TIMESTAMP,
    UUID,
)
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=func.now(),
    )


class TimeSlot(Base):
    __tablename__ = "time_slots"
    id = Column(UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    date = Column(String, nullable=False)
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    time_zone = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=func.now(),
    )
