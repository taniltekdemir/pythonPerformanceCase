import asyncio
import json
from app.core.config import settings
import pika
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.services.truck_data_service import create_data
from app.core.database import get_db


def get_data_from_queue(ch, method, properties, body):

    data = json.loads(body)
    db: AsyncSession = Depends(get_db)
    try:
        asyncio.run(create_data(db, data))
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing data: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)

def consume():

    connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
    channel = connection.channel()

    channel.queue_declare(queue="data_queue", durable=True)
    channel.basic_consume(queue="data_queue", on_message_callback=get_data_from_queue)
    channel.start_consuming()