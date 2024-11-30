from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.endpoints import truck_data_api
from app.core.database import engine
from app.models.truck_data import Base



@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        raise

    yield

app = FastAPI(
    title="Truck Data API",
    description="",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(truck_data_api.router, prefix="/api/v1", tags=["Data"])