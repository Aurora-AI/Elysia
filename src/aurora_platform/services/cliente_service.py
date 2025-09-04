
from fastapi import HTTPException, status
from firebase_admin import firestore

from ..schemas.cliente_schema import Cliente, ClienteCreate


def create_cliente(cliente_data: ClienteCreate) -> Cliente:
    try:
        db = firestore.client()
        clientes_ref = db.collection("clientes")
        doc_ref = clientes_ref.document()
        cliente_dict = cliente_data.model_dump()
        doc_ref.set(cliente_dict)
        return Cliente(id=doc_ref.id, **cliente_dict)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro inesperado ao criar o cliente: {e}",
        )


def get_all_clientes() -> list[Cliente]:
    try:
        db = firestore.client()
        clientes_ref = db.collection("clientes")
        docs = clientes_ref.stream()
        clientes = [Cliente(id=doc.id, **doc.to_dict()) for doc in docs]
        return clientes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro inesperado ao listar os clientes: {e}",
        )
