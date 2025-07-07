import json

import aio_pika

from app.config.settings import settings_config
from app.models import OutboxEventModel


async def send_to_rabbitmq(event: OutboxEventModel, queue_name: str = "events"):
    connection = await aio_pika.connect_robust(settings_config.RABBIT_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, durable=True)

        message = aio_pika.Message(
            body=event.payload.encode("utf-8"),
            headers={"event_type": event.event_type}
        )

        await channel.default_exchange.publish(
            message,
            routing_key=queue.name
        )
