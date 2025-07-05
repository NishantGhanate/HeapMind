"""
Code excution starts from here
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1 import ingest
from app.core.startup import shutdown_events, startup_events


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_events()
    yield
    await shutdown_events()

app = FastAPI(lifespan=lifespan)

app.include_router(ingest.router, prefix="/api/v1/ingest")
# app.include_router(quiz.router, prefix="/api/v1/quiz")
# app.include_router(flashcards.router, prefix="/api/v1/flashcards")
