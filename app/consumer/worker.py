import asyncio
import os
from aio_pika import connect_robust, IncomingMessage
import json
from aiormq import AMQPException

from app.api.services.truck_data_service import create_data
from app.core.database import get_db
from app.payload.truck_data import TruckDataRequest


async def wait_for_rabbitmq(url, retries=10, delay=5):
    for attempt in range(retries):
        try:
            connection = await connect_robust(url)
            await connection.close()
            print("RabbitMQ is ready.")
            return
        except (AMQPException, OSError):
            print(f"RabbitMQ not ready yet. Retrying in {delay} seconds... ({attempt+1}/{retries})")
            await asyncio.sleep(delay)

    raise RuntimeError("RabbitMQ is not ready")


async def process_message(message: IncomingMessage):
    async with message.process():
        try:
            data = json.loads(message.body.decode())
            print(f"Received message: {data}")

            await save_to_db(data)
        except Exception as e:
            print(f"Error processing message: {e}")
            raise

async def save_to_db(message_data):
    try:
        async for db_session in get_db():
            request_data = TruckDataRequest(**message_data)
            saved_data = await create_data(db_session, request_data)
            print(f"Data successfully saved to database: {saved_data}")
    except Exception as e:
        print(f"Error saving data to database: {e}")
        raise

async def main():
    rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    await wait_for_rabbitmq(rabbitmq_url)

    connection = await connect_robust(rabbitmq_url)

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("truck_data_queue", durable=True)

        await queue.consume(process_message)

        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Worker script failed with error: {e}")
