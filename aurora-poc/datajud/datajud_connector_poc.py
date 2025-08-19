#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Conector mínimo (POC) para a API Pública do DataJud (CNJ).

- Autentica via header: Authorization: APIKey <chave_publica_vigente>
- Consulta por numeroProcesso OU DSL (arquivo JSON) no endpoint do tribunal desejado
- Suporta paginação com size + sort(@timestamp) + search_after
- Salva JSON bruto em /artifacts, se solicitado
- Mensagens de diagnóstico claras (salvamento OK com bytes; erros exibem corpo)

Opções novas:
--verbose    -> loga URL, alguns headers e payload antes da chamada
--no-stdout  -> quando usar --save, suprime impressão do JSON no stdout (mantém mensagem de OK/ERRO)

Retornos:
- Exit code 0: sucesso
- Exit code 2: erro de argumentos
- Exit code 3: erro de rede/HTTP
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, Optional, List, Tuple

import requests

DEFAULT_BASE = "https://api-publica.datajud.cnj.jus.br"
# Fallback para rodar "out-of-the-box" hoje (19/08/2025). Atualize via .env quando o CNJ rotacionar.
FALLBACK_API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

def load_env_key(env_path: str = ".env") -> Optional[str]:
    """Carrega DATAJUD_API_KEY de .env (formato simples KEY=VALUE)."""
    key = os.getenv("DATAJUD_API_KEY")
    if key:
        return key.strip()
    if os.path.isfile(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == "DATAJUD_API_KEY":
                    return v.strip().strip('"').strip("'")
    return None

def make_headers(api_key: Optional[str]) -> Dict[str, str]:
    token = api_key or FALLBACK_API_KEY
    return {
        "Authorization": f"APIKey {token}",
        "Content-Type": "application/json",
    }

def tribunal_url(tribunal_alias: str, base: str = DEFAULT_BASE) -> str:
    """
    Monta a URL do endpoint /_search do tribunal informado.
    Exemplos:
      - api_publica_trf1
      - api_publica_tjsp
      - api_publica_tjpr
      - api_publica_trt9
      - api_publica_tjdft
    """
    alias = tribunal_alias.strip().rstrip("/")
    return f"{base}/{alias}/_search"

def post_search(url: str, headers: Dict[str, str], payload: Dict[str, Any], timeout: int = 120) -> requests.Response:
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
        return resp
    except requests.RequestException as exc:
        print(f"[ERRO] Falha na requisição: {exc}", file=sys.stderr)
        sys.exit(3)

def ensure_ok(resp: requests.Response) -> None:
    if resp.status_code >= 400:
        # tenta JSON, senão texto
        try:
            body = resp.json()
            body_txt = json.dumps(body, ensure_ascii=False, indent=2)
        except Exception:
            body_txt = resp.text
        msg = f"[ERRO] HTTP {resp.status_code} {resp.reason}\n{body_txt}"
        print(msg, file=sys.stderr)
        sys.exit(3)

def pretty(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2)

def build_payload(
    numero_processo: Optional[str],
    dsl_file: Optional[str],
    size: int,
    sort_timestamp_asc: bool,
    search_after: Optional[List[Any]]
) -> Dict[str, Any]:
    if numero_processo and dsl_file:
        print("[ERRO] Use --numero OU --dsl-file, não ambos.", file=sys.stderr)
        sys.exit(2)

    if dsl_file:
        try:
            with open(dsl_file, "r", encoding="utf-8") as f:
                payload = json.load(f)
        except Exception as e:
            print(f"[ERRO] Falha ao ler DSL file: {e}", file=sys.stderr)
            sys.exit(2)
    else:
        if not numero_processo:
            print("[ERRO] Informe --numero ou --dsl-file.", file=sys.stderr)
            sys.exit(2)
        payload = {"query": {"match": {"numeroProcesso": numero_processo}}}

    if size:
        payload["size"] = size

    if sort_timestamp_asc:
        payload["sort"] = [{"@timestamp": {"order": "asc"}}]

    if search_after is not None:
        payload["search_after"] = search_after

    return payload

def paginate(
    url: str,
    headers: Dict[str, str],
    base_payload: Dict[str, Any],
    max_pages: int,
    verbose: bool = False,
) -> Tuple[List[Dict[str, Any]], Optional[List[Any]]]:
    """
    Pagina resultados usando sort @timestamp + search_after.
    Retorna lista de hits e o último ponteiro 'search_after'.
    """
    all_hits: List[Dict[str, Any]] = []
    search_after_ptr: Optional[List[Any]] = base_payload.get("search_after")
    for page in range(max_pages):
        payload = dict(base_payload)
        if search_after_ptr is not None:
            payload["search_after"] = search_after_ptr

        if verbose:
            print(f"[VERBOSE] POST {url}")
            print(f"[VERBOSE] Headers: Authorization=APIKey ****, Content-Type={headers.get('Content-Type')}")
            print(f"[VERBOSE] Payload: {pretty(payload)}")

        resp = post_search(url, headers, payload)
        ensure_ok(resp)
        data = resp.json()

        hits = (data.get("hits") or {}).get("hits") or []
        all_hits.extend(hits)
        if not hits:
            break
        last_sort = hits[-1].get("sort")
        if not last_sort:
            break
        search_after_ptr = last_sort
    return all_hits, search_after_ptr

def main():
    parser = argparse.ArgumentParser(description="POC DataJud API Connector")
    parser.add_argument("--tribunal", default="api_publica_trf1", help="Alias do tribunal (ex: api_publica_trf1, api_publica_tjsp, api_publica_trt9, ...)")
    parser.add_argument("--numero", help="Número do processo (ex.: 0000993-58.2022.5.09.0014 ou 00009935820225090014)")
    parser.add_argument("--dsl-file", help="Arquivo JSON com a DSL de busca (alternativo a --numero)")
    parser.add_argument("--size", type=int, default=10, help="Qtd de registros por página (padrão 10; máx. 10000)")
    parser.add_argument("--sort-timestamp-asc", action="store_true", help="Ordena por @timestamp crescente (recomendado para paginação)")
    parser.add_argument("--pages", type=int, default=1, help="Qtde de páginas via search_after (1 = sem paginação)")
    parser.add_argument("--search-after", help="JSON array com ponteiro search_after da página anterior (opcional)")
    parser.add_argument("--save", help="Caminho do arquivo para salvar o JSON bruto")
    parser.add_argument("--no-stdout", action="store_true", help="Quando usado com --save, não imprime o JSON no stdout (imprime só mensagem de OK/ERRO)")
    parser.add_argument("--verbose", action="store_true", help="Mostra URL, headers mínimos e payload antes da chamada")
    args = parser.parse_args()

    # Carrega API Key do ambiente ou .env; fallback público vigente
    api_key = load_env_key()
    headers = make_headers(api_key)
    url = tribunal_url(args.tribunal)

    # Monta payload
    search_after_ptr = None
    if args.search_after:
        try:
            search_after_ptr = json.loads(args.search_after)
            if not isinstance(search_after_ptr, list):
                raise ValueError
        except Exception:
            print('[ERRO] --search-after deve ser um JSON array válido, ex.: "[1681366085550]"', file=sys.stderr)
            sys.exit(2)

    payload = build_payload(
        numero_processo=args.numero,
        dsl_file=args.dsl_file,
        size=args.size,
        sort_timestamp_asc=args.sort_timestamp_asc or args.pages > 1,
        search_after=search_after_ptr
    )

    # Log verbose
    if args.verbose:
        print(f"[VERBOSE] URL: {url}")
        print(f"[VERBOSE] Headers: Authorization=APIKey ****, Content-Type={headers.get('Content-Type')}")
        print(f"[VERBOSE] Payload: {pretty(payload)}")

    # Execução
    if args.pages <= 1:
        resp = post_search(url, headers, payload)
        ensure_ok(resp)
        data = resp.json()

        # Impressão/Salvamento
        out_text = pretty(data)
        if args.save:
            try:
                os.makedirs(os.path.dirname(args.save) or ".", exist_ok=True)
                with open(args.save, "w", encoding="utf-8") as f:
                    f.write(out_text)
                nbytes = os.path.getsize(args.save)
                print(f"[OK] JSON salvo em: {args.save} ({nbytes} bytes)")
            except Exception as e:
                print(f"[ERRO] Falha ao salvar em {args.save}: {e}", file=sys.stderr)
                sys.exit(3)

            if not args.no_stdout:
                # imprime JSON também, útil para pipe/tee
                print(out_text)
        else:
            print(out_text)
        sys.exit(0)

    # Paginação (>=2 páginas)
    hits, last_ptr = paginate(url, headers, payload, max_pages=args.pages, verbose=args.verbose)
    output = {
        "total_hits_returned": len(hits),
        "last_search_after": last_ptr,
        "hits": hits,
    }
    out_text = pretty(output)
    if args.save:
        try:
            os.makedirs(os.path.dirname(args.save) or ".", exist_ok=True)
            with open(args.save, "w", encoding="utf-8") as f:
                f.write(out_text)
            nbytes = os.path.getsize(args.save)
            print(f"[OK] JSON paginado salvo em: {args.save} ({nbytes} bytes)")
        except Exception as e:
            print(f"[ERRO] Falha ao salvar em {args.save}: {e}", file=sys.stderr)
            sys.exit(3)
        if not args.no_stdout:
            print(out_text)
    else:
        print(out_text)
    sys.exit(0)

if __name__ == "__main__":
    main()
