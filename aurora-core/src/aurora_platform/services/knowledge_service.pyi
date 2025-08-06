<<<<<<< HEAD
# Interface para KnowledgeService usando Qdrant como backend vetorial
=======
from typing import List

from chromadb.api import ClientAPI
from chromadb.api.models.Collection import Collection

class KnowledgeBaseService:
    client: ClientAPI
    host: str
    port: int

    def __init__(self, host: str = "chromadb", port: int = 8000) -> None: ...

    def _connect_with_retry(self) -> ClientAPI: ...

    async def verify_connection_health(self) -> None: ...

    def get_or_create_collection(self, name: str) -> Collection: ...

    def query(self, collection_name: str, query_texts: List[str], n_results: int = 5) -> dict: ...
>>>>>>> origin/main
