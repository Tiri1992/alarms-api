from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Time
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

# Declarative Base
from app.database.db import Base


class AlarmModel(Base):

    __tablename__ = "alarms"

    id = Column(Integer, primary_key=True, nullable=False)
    day_of_week = Column(Integer, nullable=False)
    time = Column(Time(timezone=True), nullable=False)
    is_on = Column(Boolean, nullable=False, server_default='TRUE')
    message = Column(String(150), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('NOW()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", name="alarms_user_id_fkey", ondelete="CASCADE"), nullable=False)

    user = relationship("UserModel", back_populates="alarm")
