from __future__ import annotations
from typing import Dict, Any, Iterable, Tuple
from .config import EMAIL_RE, NAME_HINT_RE, KEYWORDS_BY_CATEGORY, ALLOWED_SUFFIXES, DISALLOW_PERSONAL

PERSONAL_PROVIDERS = ("gmail.com", "hotmail.com", "outlook.com", "yahoo.com", "icloud.com")


def is_official(email: str) -> bool:
    dom = email.split("@")[-1].lower()
    if dom.endswith(tuple(s.lstrip(".") for s in ALLOWED_SUFFIXES)):
        return True
    if dom in PERSONAL_PROVIDERS:
        return False
    # outros domínios privados -> não-oficial
    return False


def should_keep(email: str, allow_non_official: bool) -> bool:
    return is_official(email) or allow_non_official


def guess_category_role(text_blob: str) -> Tuple[str|None, str|None]:
    low = text_blob.lower()
    for cat, keys in KEYWORDS_BY_CATEGORY.items():
        if any(k in low for k in keys):
            # role_hint simplista: primeira palavra-chave que bate
            return cat, next((k for k in keys if k in low), None)
    return None, None


def near_name(text_blob: str) -> str|None:
    m = NAME_HINT_RE.search(text_blob)
    return m.group("nome").strip() if m else None


def extract_from_text(url: str, title: str|None, text: str, *, allow_non_official: bool=False) -> Iterable[Dict[str, Any]]:
    hits = []
    for m in EMAIL_RE.finditer(text or ""):
        email = m.group("email")
        if not should_keep(email, allow_non_official):
            continue
        name = near_name(text[max(0, m.start()-400): m.end()+400])  # janela em torno do e-mail
        category, role_hint = guess_category_role(text[max(0, m.start()-1000): m.end()+1000])
        org_hint = title or ""
        official = is_official(email)
        confidence = "high" if official else "low"
        hits.append({
            "email": email,
            "name": name,
            "category": category,
            "role_hint": role_hint,
            "official": official,
            "confidence": confidence,
            "page_url": url,
            "page_title": title,
        })
    return hits
