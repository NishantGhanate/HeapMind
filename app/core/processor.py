# app/core/processor.py

async def process_uploaded_file(payload: dict):
    file_id = payload.get("file_id")
    path = payload.get("path")

    # Parse, embed, quiz generation etc
    print(f"[✔] Processing file: {file_id} at {path}")
