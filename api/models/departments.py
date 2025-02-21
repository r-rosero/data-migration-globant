from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from api.models.base import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True, comment="Id of the department")
    deparment = Column(String, nullable=False, comment="Name of the department")