from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from api.models.base import Base

class HiredEmployee(Base):
    __tablename__ = "hired_employees"

    id = Column(Integer, primary_key=True, index=True, comment="Id of the employee")
    name = Column(String, nullable=False, comment="Name and surname of the employee")
    datetime = Column(String, nullable=False, comment="Hire datetime in ISO format")
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False, comment="Id of the department which the employee was hired for")
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, comment="Id of the job which the employee was hired for")

class HireEmployeeBatch:
    def __init__(self, hired_employees):
        self.hired_employees = hired_employees