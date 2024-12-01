from fastapi import APIRouter, HTTPException
from app.payload.truck_data import TruckDataResponse, TruckDataRequest
import pika
from app.core.config import settings
import json
from datetime import datetime

router = APIRouter()
@router.post("/truckdata", response_model=str)
async def create_new_data(data: TruckDataRequest):
    try:
        data_dict = data.dict()
        if "timestamp" in data_dict and isinstance(data_dict["timestamp"], datetime):
            data_dict["timestamp"] = data_dict["timestamp"].isoformat()

        await send_to_queue("truck_data_queue", data_dict, settings.RABBITMQ_URL)

        # connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
        # print("conenction success and send to queue...")
        # channel = connection.channel()
        # channel.queue_declare(queue="truck_data_queue", durable=True)
        # channel.basic_publish(
        #     exchange="",
        #     routing_key="truck_data_queue",
        #     body=json.dumps(data_dict),
        #     properties=pika.BasicProperties(delivery_mode=2, content_type="application/json"),
        # )
        # print("conenction success and send to queue...END!!")
        # connection.close()
        return "Data was successfully posted"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred on queue: {str(e)}")

async def send_to_queue(queue_name: str, data: dict, rabbitmq_url: str):
    try:
        connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
        print("conenction success and send to queue...")
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json.dumps(data),
            properties=pika.BasicProperties(delivery_mode=2, content_type="application/json"),
        )
        print("conenction success and send to queue...END!!")
        connection.close()
    except Exception as e:
        raise RuntimeError(f"An error occurred while sending data to the queue: {str(e)}")


@router.get("/")
async def test():
    return {"message": "Welcome to the Truck Data API!"}

