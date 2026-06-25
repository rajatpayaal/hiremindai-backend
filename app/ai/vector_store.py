from qdrant_client import QdrantClient

from app.core.config import settings


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)

