
"""
Api for search
"""
import traceback

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.embeddings.emedder import Embedder
from app.models.search_result_model import SearchResult
from app.vector_store.qdrant_db import qdrant_store


router = APIRouter()


@router.get("/search")
async def search(query: str, collection_name: str = 'documents'):
    """
    Peform search on Qdrant vector db

    """
    try :
        query_vector = Embedder.embed_texts(texts= query)
        hits = qdrant_store.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=1
        )
        for hit in hits:
            payload = hit.payload
            print("Matched Chunk:", payload["chunk"])
            print("File Name:", payload["file_name"])
            print("File Path:", payload["file_path"])
            print("Page Number:", payload.get("chunk_index"))
            print("Score:", hit.score)

        results = [
            SearchResult(
                chunk=hit.payload["chunk"],
                file_name=hit.payload["file_name"],
                file_path=hit.payload["file_path"],
                page_number=hit.payload.get("chunk_index", 0),
                score=hit.score
            ).model_dump()
            for hit in hits
        ]


    except Exception as e:
        traceback.print_exc()
        raise e

    return JSONResponse(
        status_code=200,
        content={
            "message": "Fetching sucessful",
            "data": results
        }
    )




