""""
Event based functions
"""
from app.core.dispatcher import start_dispatcher
from app.db.session import init_db


async def startup_events():
    # e.g., chroma_client.init(), db.connect(), etc.
    print("[Startup] Initializing vector DB, LLM, etc.")
    await init_db()
    await start_dispatcher()

async def shutdown_events():
    print("[Shutdown] Cleaning up.")
    # e.g., db.disconnect(), chroma_client.close(), etc.
