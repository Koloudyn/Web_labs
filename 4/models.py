from sqlalchemy import Column, Integer, String
from database import base

class Persons(base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    todo = Column(String)
