import asyncio
from datetime import datetime
import json
import logging

import backoff
from sqlmodel import select

from app.config.settings import settings_config
from app.core.rabbitmq import send_to_rabbitmq
from app.core.tasks import process_document
from app.db.session import AsyncSessionLocal
from app.models import OutboxEventModel


logger = logging.getLogger("heap_mind")

@backoff.on_exception(backoff.expo, Exception, max_tries=5, jitter=None)
async def safe_send(event: OutboxEventModel):
    await send_to_rabbitmq(event)


async def outbox_dispatcher(session_factory):
    """
    Outbox is an design pattern to enure broker/task processor fault tolerance
    """
    logger.info("outbox_dispatcher is online")
    while True:
        async with session_factory() as session:
            result = await session.exec(
                select(OutboxEventModel).where(OutboxEventModel.processed == False).limit(10)
            )
            events = result.all()


            for event in events:
                try:
                    # based on eevent creata map to route
                    # event_type="document_ingested"
                    payload = json.loads(event.payload)
                    process_document.delay(
                        event.id, payload, event.event_type
                    )
                    event.processed = True
                    event.processed_at = datetime.now(tz=settings_config.tzinfo)
                except Exception as e:
                    logger.error(f"[DISPATCH ERROR] Failed to dispatch event {event.id}: {e}")

            await session.commit()

        await asyncio.sleep(5)  # polling interval


async def start_dispatcher():
    asyncio.create_task(outbox_dispatcher(AsyncSessionLocal))
