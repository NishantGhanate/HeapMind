import asyncio
from datetime import datetime

import backoff
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession  # ✅ ensure correct import

from app.config.settings import settings_config
from app.core.rabbitmq import send_to_rabbitmq
from app.db.session import AsyncSessionLocal
from app.models import OutboxEventModel


@backoff.on_exception(backoff.expo, Exception, max_tries=5, jitter=None)
async def safe_send(event: OutboxEventModel):
    await send_to_rabbitmq(event)


async def outbox_dispatcher(session_factory):
    while True:
        async with session_factory() as session:  # session: AsyncSession
            result = await session.exec(
                select(OutboxEventModel).where(OutboxEventModel.processed == False).limit(10)
            )
            events = result.all()

            for event in events:
                try:
                    await safe_send(event)
                    event.processed = True
                    event.processed_at = datetime.now(tz=settings_config.tzinfo)
                except Exception as e:
                    print(f"[DISPATCH ERROR] Failed to dispatch event {event.id}: {e}")

            await session.commit()

        await asyncio.sleep(5)  # polling interval


async def start_dispatcher():
    asyncio.create_task(outbox_dispatcher(AsyncSessionLocal))
