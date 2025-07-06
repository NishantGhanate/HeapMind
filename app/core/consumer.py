"""
app/worker/consumer.py
custom cosnumer for rabbit-mq alternative celery
"""

import asyncio
import json

import aio_pika

from app.config.settings import settings_config
from app.core.processor import process_uploaded_file


async def handle_event(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        try:
            payload = json.loads(message.body.decode())
            event_type = message.headers.get("event_type")

            print(f"[x] Received event: {event_type} | Payload: {payload}")

            if event_type == "document_ingested":
                await process_uploaded_file(payload)

        except Exception as e:
            print(f"[!] Failed to handle event: {e}")
            # optionally: message.reject() or message.nack(requeue=True)


async def consume(queue_name="events"):
    connection = await aio_pika.connect_robust(settings_config.RABBIT_URL)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue(queue_name, durable=True)

        print("[*] Waiting for messages. To exit press CTRL+C")
        await queue.consume(handle_event)

        await asyncio.Future()  # keep running
