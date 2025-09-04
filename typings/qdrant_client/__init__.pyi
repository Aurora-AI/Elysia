from collections.abc import Iterable, Mapping, Sequence
from typing import Any

class Distance:
    COSINE: Any
    EUCLID: Any
    DOT: Any


class PointStruct:
    def __init__(self, id: int | str | None = ...,
                 vector: Sequence[float] | None = ..., payload: Mapping[str, Any] | None = ...) -> None: ...


class Filter:
    ...


class ScoredPoint:
    id: int | str
    score: float
    payload: Mapping[str, Any] | None


class CollectionInfo:
    name: str


class CollectionList:
    collections: list[CollectionInfo]


class ModelsNamespace:
    Distance: type[Distance]
    ScoredPoint: type[ScoredPoint]
    Filter: type[Filter]
    PointStruct: type[PointStruct]
    VectorParams: type[VectorParams]
    OptimizersConfigDiff: type[OptimizersConfigDiff]


models: ModelsNamespace


class QdrantClient:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def close(self) -> None: ...

    def get_collections(self) -> CollectionList: ...
    def collection_exists(self, name: str) -> bool: ...

    def recreate_collection(self, collection_name: str,
                            *args: Any, **kwargs: Any) -> Any: ...
    def create_collection(self, collection_name: str, *
                          args: Any, **kwargs: Any) -> Any: ...

    def has_collection(self, collection_name: str) -> bool: ...
    def delete_collection(self, collection_name: str) -> Any: ...

    def upsert(self, collection_name: str, points: Iterable[PointStruct] |
               Iterable[Mapping[str, Any]] | Any, *args: Any, **kwargs: Any) -> Any: ...

    def search(self, collection_name: str, query_vector: Sequence[float] | Mapping[str, Any], limit: int = ..., size: int = ..., distance: Distance | None = ...,
               query_filter: Filter | None = ..., with_payload: bool | Sequence[str] | Mapping[str, Any] | None = ..., *args: Any, **kwargs: Any) -> list[ScoredPoint]: ...

    def scroll(self, *args: Any, **kwargs: Any) -> Any: ...
    def count(self, *args: Any, **kwargs: Any) -> Any: ...


class VectorParams:
    def __init__(self, size: int = ..., distance: Distance |
                 None = ...) -> None: ...


class OptimizersConfigDiff:
    def __init__(self, indexing_threshold: int | None = ...,
                 memmap_threshold: int | None = ...) -> None: ...


class FieldCondition:
    def __init__(self, key: str = ..., match: MatchValue |
                 None = ...) -> None: ...


class MatchValue:
    def __init__(self, value: Any = ...) -> None: ...


__all__ = ["QdrantClient", "models", "Distance",
           "ScoredPoint", "Filter", "PointStruct"]
