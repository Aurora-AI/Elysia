from chromadb import HttpClient
from aurora_platform.core.config import settings

chroma_client = HttpClient(
    host=settings.CHROMA_HOST,
    port=settings.CHROMA_PORT
)

def heartbeat():
    try:
        chroma_client.heartbeat()
        return True
    except Exception:
        return False
