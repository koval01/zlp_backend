from typing import Any

from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.types import DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects import mysql

from database.controller import Base


class Player(Base):
    """Player model"""

    __tablename__ = "luckperms_players"

    uuid = Column(String(36), nullable=False)
    username = Column(String(16), nullable=False)
    primary_group = Column(String(36), nullable=False)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)


class UserPermissions(Base):
    """User permissions model"""

    __tablename__ = "luckperms_user_permissions"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), nullable=False)
    permission = Column(String(200), nullable=False)
    value = Column(mysql.TINYINT(1), nullable=False)
    server = Column(String(36), nullable=False)
    world = Column(String(64), nullable=False)
    expiry = Column(BigInteger, nullable=False)
    contexts = Column(String(200), nullable=False)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)


class MonitoringStatistic:
    """Monitoring statistics model"""

    __tablename__ = "monitoring_statistic"

    username = Column(String(48), nullable=False)
    monitoring = Column(String(48), nullable=False)
    timestep = Column(DateTime(timezone=True), nullable=False, onupdate=func.now())
    votes = Column(Integer, nullable=False)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
