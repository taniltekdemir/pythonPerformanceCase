from datetime import datetime

from sqlalchemy import select, desc, cast, String
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


async def get_data_by_date_range(db: AsyncSession, start_date: str, end_date: str):
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

    result = await db.execute(
        select(TruckData).where(TruckData.timestamp.between(start_date_obj, end_date_obj))
    )
    return result.scalars().all()

async def get_last_data_by_truckId(db: AsyncSession, truck_id: str):
    result = await db.execute(
        select(TruckData)
        .where(cast(TruckData.truck_id, String) == truck_id)
        .order_by(desc(TruckData.timestamp))
        .limit(1)
    )

    return result.scalar_one_or_none()
