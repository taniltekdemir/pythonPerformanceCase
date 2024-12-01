from sqlalchemy.ext.asyncio import AsyncSession
from app.models.truck_data import TruckData
from app.payload.truck_data import TruckDataRequest


async def create_data(db: AsyncSession, data: TruckDataRequest):
    print(f"create_data:: Inserting data into the database: {TruckDataRequest}")
    db_data = TruckData(**data.dict())
    db.add(db_data)
    await db.commit()
    await db.refresh(db_data)
    return db_data
