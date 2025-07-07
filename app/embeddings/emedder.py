from typing import List

from sentence_transformers import SentenceTransformer


class Embedder:
    _model = SentenceTransformer("all-MiniLM-L6-v2")

    @classmethod
    def embed_texts(cls, texts: List[str]) -> List[List[float]]:
        return cls._model.encode(texts, show_progress_bar=True, convert_to_numpy=True).tolist()
