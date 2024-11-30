from pydantic import BaseModel
from datetime import datetime

class TruckDataRequest(BaseModel):
    truck_id: str
    timestamp: datetime
    location: str
    speed: float

class TruckDataResponse(BaseModel):
    id: int
    truck_id: str
    timestamp: datetime
    location: str
    speed: float

    class Config:
        from_attributes = True