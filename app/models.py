from sqlalchemy import Column, Integer, String
from .database import Base

class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    relation = Column(String)
    shagun_amount = Column(Integer, default=0)
    status = Column(String, default="Invited")
    