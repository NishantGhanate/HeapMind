import hashlib
from pathlib import Path
from typing import Dict, List, Union
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.http.models import (CollectionStatus, Distance, Payload, PointStruct,
                                       VectorParams)


# Connect to Qdrant instance
class QdrantVectorStore:
    """
    Efficient and reusable Qdrant interface for storing document chunks and embeddings.
    """

    _client: QdrantClient = None
    _collections_initialized: set = set()

    def __init__(self, host: str = "localhost", port: int = 6333, default_collection: str = "documents"):
        if not QdrantVectorStore._client:
            QdrantVectorStore._client = QdrantClient(host=host, port=port)
        self.default_collection = default_collection

    @property
    def client(self) -> QdrantClient:
        return QdrantVectorStore._client

    def ensure_collection(self, dimension: int, collection_name: str = None):
        collection_name = collection_name or self.default_collection
        if collection_name in QdrantVectorStore._collections_initialized:
            return  # Already ensured

        existing_names = [c.name for c in self.client.get_collections().collections]
        if collection_name not in existing_names:
            self.client.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=dimension,
                    distance=Distance.COSINE,
                ),
            )
        QdrantVectorStore._collections_initialized.add(collection_name)

    def store(
        self,
        embeddings: List[List[float]],
        chunks: List[str],
        metadata: Dict[str, Union[str, int]],
        collection_name: str = None,
    ):
        if not embeddings or not chunks or len(embeddings) != len(chunks):
            raise ValueError("Embeddings and chunks must be non-empty and match in length.")

        collection_name = collection_name or self.default_collection
        self.ensure_collection(dimension=len(embeddings[0]), collection_name=collection_name)

        points = [
            PointStruct(
                id=str(uuid4()),
                vector=vector,
                payload={
                    **metadata,
                    "chunk": chunk,
                    "chunk_index": i + 1,
                },
            )
            for i, (chunk, vector) in enumerate(zip(chunks, embeddings))
        ]

        self.client.upsert(collection_name=collection_name, points=points)


qdrant_store = QdrantVectorStore()
