"""Database Task schemas"""

from db.sqlalchemy_database import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


class SQLAlchemyTask(Base):
    """Relational Tasks database schema"""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
