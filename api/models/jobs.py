from sqlalchemy import Column, Integer, String
from api.models.base import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True, comment="Id of the job")
    job = Column(String, nullable=False, comment="Name of the job")

class JobBatch:
    def __init__(self, jobs):
        self.jobs = jobs