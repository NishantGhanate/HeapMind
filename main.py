"""
Code excution starts from here
"""
from contextlib import asynccontextmanager

from app.config.logger import get_dict_logger


logger = get_dict_logger("heap_mind")


from fastapi import FastAPI

from app.api.v1 import ingest, search_api
from app.core.startup import shutdown_events, startup_events


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Logger initialized.")
    await startup_events()
    yield
    await shutdown_events()

app = FastAPI(lifespan=lifespan)

app.include_router(ingest.router, prefix="/api/v1/ingest")
app.include_router(search_api.router, prefix="/api/v1/search")
# app.include_router(quiz.router, prefix="/api/v1/quiz")
# app.include_router(flashcards.router, prefix="/api/v1/flashcards")
