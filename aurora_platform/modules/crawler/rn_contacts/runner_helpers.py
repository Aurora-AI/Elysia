# minimal ascii-only helpers for runner
from typing import Any, Dict, Optional, Iterable
import json, hashlib, re, importlib.util, math

def load_mission_file(path: str) -> Dict[str, Any]:
    b = open(path, 'rb').read()
    if b.startswith(b'\xef\xbb\xbf'):
        b = b[3:]
    s = b.decode('utf-8', 'replace')
    try:
        import yaml  # type: ignore
        m = yaml.safe_load(s)
        if m is None:
            raise ValueError('empty')
        return m
    except Exception:
        return json.loads(s)

def _detect_playwright_available() -> bool:
    return importlib.util.find_spec('playwright') is not None

def _slug_host(u: str) -> str:
    m = re.search(r'https?://([^/]+)/?', u)
    host = (m.group(1) if m else u).lower()
    return re.sub(r'[^a-z0-9]+', '_', host).strip('_')

def _derive_mission_id(mission: Optional[Dict[str, Any]], meta: Optional[Dict[str, Any]] = None) -> str:
    if mission and mission.get('mission_id'):
        return str(mission['mission_id'])
    seeds = (mission or {}).get('seeds') or (meta or {}).get('seeds') or []
    if isinstance(seeds, Iterable) and seeds:
        return _slug_host(str(list(seeds)[0]))
    h = hashlib.sha1(json.dumps(mission or meta or {}, sort_keys=True).encode()).hexdigest()[:12]
    return 'mission_%s' % h

def _render_meta_for_manifest(meta: Dict[str, Any], mission: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    mode, budget, timeout = 'auto', 0.10, 10
    if mission and isinstance(mission.get('constraints'), dict):
        rj = mission['constraints'].get('render_js') or {}
        mode = rj.get('mode', mode)
        budget = float(rj.get('budget', budget))
        timeout = int(rj.get('timeout_sec', timeout))
    base_pages = 0
    if mission and isinstance(mission.get('constraints'), dict):
        base_pages = int(mission['constraints'].get('max_pages') or 0)
    if not base_pages and isinstance(meta.get('visited'), int):
        base_pages = int(meta.get('visited'))
    cap = max(1, math.ceil((budget or 0.01) * max(50, base_pages or 100)))
    used = int(meta.get('render_used') or 0)
    return {
        'available': bool(_detect_playwright_available()),
        'mode': mode,
        'budget': float(budget),
        'timeout_sec': int(timeout),
        'used': used,
        'cap': int(cap),
    }
