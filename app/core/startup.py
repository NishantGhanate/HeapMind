# app/core/startup.py

async def startup_events():
    print("[Startup] Initializing vector DB, LLM, etc.")
    # e.g., chroma_client.init(), db.connect(), etc.

async def shutdown_events():
    print("[Shutdown] Cleaning up.")
    # e.g., db.disconnect(), chroma_client.close(), etc.
