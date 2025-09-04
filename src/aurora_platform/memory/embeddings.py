import os

import numpy as np
from sentence_transformers import SentenceTransformer

_MODEL = None
_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME",
                        "intfloat/multilingual-e5-small")
_NORMALIZE = os.getenv("EMBEDDING_NORMALIZE", "true").lower() in {
    "1", "true", "yes", "y"}


def _load_model() -> SentenceTransformer:
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer(_MODEL_NAME)
    return _MODEL  # type: ignore[return-value]


def embedding_dim() -> int:
    """
    Garante int, nunca Optional[int].
    """
    model = _load_model()
    dim = None
    try:
        dim = getattr(model, "get_sentence_embedding_dimension",
                      lambda: None)()
    except Exception:
        dim = None
    if isinstance(dim, int):
        return dim
    # fallback robusto
    v = model.encode(["dummy"], convert_to_numpy=True,
                     normalize_embeddings=False)
    return int(v.shape[-1])


def encode_texts(texts: list[str]) -> np.ndarray:
    model = _load_model()
    vecs = model.encode(texts, convert_to_numpy=True,
                        normalize_embeddings=False, show_progress_bar=False)
    if _NORMALIZE:
        norms = np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-12
        vecs = vecs / norms
    return vecs


def encode_one(text: str) -> np.ndarray:
    return encode_texts([text])[0]
