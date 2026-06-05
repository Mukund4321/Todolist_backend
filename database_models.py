from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

class Task(base):
    __tablename__ = "todolistfastapi"

    id = Column(Integer, primary_key=True)
    task = Column(String(200), nullable=False)
    status = Column(String(50), nullable=False)