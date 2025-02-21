from sqlalchemy import Column, Integer, String
from api.models.base import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True, comment="Id of the department")
    department = Column(String, nullable=False, comment="Name of the department")

class DepartmentBatch:
    def __init__(self, departments):
        self.departments = departments