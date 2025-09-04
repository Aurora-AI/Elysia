import asyncio
import importlib
import logging
from pathlib import Path
from typing import Any

import yaml
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# --- logging simples (stdout) ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("aurora.router")

app = FastAPI(title="AuroraRouter Capabilities API")


class InvokeRequest(BaseModel):
    capability_id: str
    payload: dict[str, Any] = Field(default_factory=dict)
    # legacy compatibility: alguns clientes usam `input` em vez de `payload`
    input: dict[str, Any] | None = None
    timeout_ms: int | None = Field(default=5000)


def _registry_path() -> Path:
    return Path(__file__).parent / "capabilities_registry.yaml"


def load_registry() -> dict[str, Any]:
    p = _registry_path()
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def find_capability(cap_id: str) -> dict[str, Any] | None:
    reg = load_registry()
    for c in (reg or {}).get("capabilities", []):
        if c.get("id") == cap_id:
            return c
    return None


def _validate_required(payload: dict[str, Any], required: list[str]) -> None:
    missing = [k for k in required if k not in payload]
    if missing:
        raise HTTPException(status_code=400, detail=f"Campos obrigatórios ausentes: {missing}")


async def _dispatch_internal_python(module: str, func: str, payload: dict[str, Any]) -> Any:
    try:
        mod = importlib.import_module(module)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao importar módulo '{module}': {e}")
    fn = getattr(mod, func, None)
    if fn is None:
        raise HTTPException(status_code=500, detail=f"Função '{func}' não encontrada em '{module}'")
    if asyncio.iscoroutinefunction(fn):
        return await fn(**payload)
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: fn(**payload))


@app.get("/capabilities")
def list_capabilities():
    reg = load_registry()
    return reg


@app.post("/invoke")
async def invoke(req: InvokeRequest):
    # suporte ao campo legado `input`
    if req.input and not req.payload:
        req.payload = req.input

    cap = find_capability(req.capability_id)
    if not cap:
        raise HTTPException(
            status_code=404,
            detail={"error": "capability_not_found", "capability_id": req.capability_id},
        )

    input_schema = cap.get("input_schema") or {}
    required = input_schema.get("required") or []
    _validate_required(req.payload, required)

    transport = cap.get("transport")
    timeout_sec = (req.timeout_ms or 5000) / 1000.0

    log.info(
        "Invocando capability id=%s transport=%s timeout=%.3fs",
        req.capability_id,
        transport,
        timeout_sec,
    )

    if transport == "internal_python":
        entry = cap.get("entrypoint") or {}
        module = entry.get("module")
        function = entry.get("function")
        if not module or not function:
            raise HTTPException(status_code=500, detail="entrypoint.module/function ausentes no registry")
        try:
            result = await asyncio.wait_for(
                _dispatch_internal_python(module, function, req.payload),
                timeout=timeout_sec,
            )
        except TimeoutError:
            raise HTTPException(status_code=504, detail="Invoke timeout")
    else:
        raise HTTPException(
            status_code=400,
            detail={"error": "unsupported_transport", "transport": transport},
        )

    return {"capability_id": req.capability_id, "result": result}


@app.get("/healthz")
def healthz():
    return {"ok": True}
