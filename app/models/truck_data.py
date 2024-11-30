from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TruckData(Base):
    __tablename__ = "truck_data"

    id = Column(Integer, primary_key=True, index=True)
    truck_id = Column(String, index=True)
    location = Column(String)
    speed = Column(Float)
    timestamp = Column(DateTime, index=True)
