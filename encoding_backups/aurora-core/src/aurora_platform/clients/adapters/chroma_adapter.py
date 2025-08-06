<<<<<<< HEAD
from chromadb import HttpClient

from aurora_platform.core.config import settings
=======
from aurora_platform.core.config import settings
from chromadb import HttpClient
>>>>>>> origin/main

chroma_client = HttpClient(host=settings.CHROMA_HOST, port=settings.CHROMA_PORT)


def heartbeat():
    try:
        chroma_client.heartbeat()
        return True
    except Exception:
        return False
