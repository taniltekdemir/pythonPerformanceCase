from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.services.truck_data_service import create_data
from app.payload.truck_data import TruckDataResponse, TruckDataRequest
from app.core.database import get_db

router = APIRouter()

@router.post("/truckdata", response_model=TruckDataResponse)
async def create_new_data(data: TruckDataRequest, db: AsyncSession = Depends(get_db)):
    try:
        # Veriyi oluşturma işlemi
        return await create_data(db, data)
    except ValueError as e:
        # Veri doğrulama ile ilgili hata
        raise HTTPException(status_code=400, detail=f"Invalid data: {str(e)}")
    except Exception as e:
        # Genel hata durumu
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@router.get("/")
async def test():
    return {"message": "Welcome to the Truck Data API!"}

