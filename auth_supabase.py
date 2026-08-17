#!/usr/bin/env python3
"""
Authentification par comptes individuels (Supabase).

Table attendue dans Supabase : `cv_users`
    id            : uuid (PK, default gen_random_uuid())
    username      : text (unique)
    password_hash : text
    is_active     : boolean (default true)
    role          : text   (default 'user')  -> 'admin' ou 'user'
    created_at    : timestamptz (default now())

Variables d'environnement (Render) :
    SUPABASE_URL              : https://xxxx.supabase.co
    SUPABASE_KEY              : clé service_role (côté serveur)
    BOOTSTRAP_ADMIN_USER      : (optionnel) identifiant du 1er admin
    BOOTSTRAP_ADMIN_PASSWORD  : (optionnel) mot de passe du 1er admin

Les mots de passe ne sont JAMAIS stockés en clair (hachage PBKDF2-SHA256).
"""

import os
import hashlib
import hmac
import secrets

try:
    import httpx
except Exception:  # pragma: no cover
    httpx = None

TABLE = "cv_users"
_PBKDF2_ITERS = 200_000


# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
def _cfg():
    return os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY")


def is_configured() -> bool:
    """True si Supabase est configuré (sinon on retombe sur le mot de passe legacy)."""
    url, key = _cfg()
    return bool(url and key and httpx is not None)


def _base():
    url, _ = _cfg()
    return f"{url.rstrip('/')}/rest/v1/{TABLE}"


def _headers(extra=None):
    _, key = _cfg()
    h = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    if extra:
        h.update(extra)
    return h


# ----------------------------------------------------------------------
# Hachage des mots de passe (PBKDF2-SHA256, stdlib — pas de dépendance)
# ----------------------------------------------------------------------
def hash_password(password: str, salt: str = None) -> str:
    salt = salt or secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), _PBKDF2_ITERS)
    return f"pbkdf2_sha256${_PBKDF2_ITERS}${salt}${dk.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        algo, iters, salt, hexdigest = stored.split("$")
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), int(iters))
        return hmac.compare_digest(dk.hex(), hexdigest)
    except Exception:
        return False


# ----------------------------------------------------------------------
# Opérations sur les utilisateurs (Supabase REST)
# ----------------------------------------------------------------------
def get_user(username: str):
    r = httpx.get(_base(), params={"username": f"eq.{username}", "select": "*"},
                  headers=_headers(), timeout=15)
    r.raise_for_status()
    rows = r.json()
    return rows[0] if rows else None


def list_users():
    r = httpx.get(_base(),
                  params={"select": "id,username,is_active,role,created_at", "order": "username.asc"},
                  headers=_headers(), timeout=15)
    r.raise_for_status()
    return r.json()


def create_user(username: str, password: str, role: str = "user"):
    body = {
        "username": username.strip(),
        "password_hash": hash_password(password),
        "is_active": True,
        "role": role if role in ("admin", "user") else "user",
    }
    r = httpx.post(_base(), json=body, headers=_headers({"Prefer": "return=representation"}), timeout=15)
    r.raise_for_status()
    return r.json()


def set_active(user_id, active: bool):
    r = httpx.patch(_base(), params={"id": f"eq.{user_id}"}, json={"is_active": bool(active)},
                    headers=_headers(), timeout=15)
    r.raise_for_status()


def set_password(user_id, password: str):
    r = httpx.patch(_base(), params={"id": f"eq.{user_id}"},
                    json={"password_hash": hash_password(password)}, headers=_headers(), timeout=15)
    r.raise_for_status()


def set_role(user_id, role: str):
    role = role if role in ("admin", "user") else "user"
    r = httpx.patch(_base(), params={"id": f"eq.{user_id}"}, json={"role": role},
                    headers=_headers(), timeout=15)
    r.raise_for_status()


def authenticate(username: str, password: str):
    """Retourne le dict utilisateur si identifiants OK ET compte actif, sinon None."""
    try:
        u = get_user((username or "").strip())
    except Exception:
        return None
    if not u or not u.get("is_active"):
        return None
    if verify_password(password, u.get("password_hash", "")):
        return u
    return None


def is_user_active(username: str) -> bool:
    """Revérifie qu'un compte est toujours actif (pour couper une session en cours)."""
    try:
        u = get_user((username or "").strip())
        return bool(u and u.get("is_active"))
    except Exception:
        # En cas d'erreur réseau transitoire, on ne coupe pas la session par précaution
        return True


def ensure_bootstrap_admin():
    """Crée un admin initial depuis les variables d'env si la table est vide (1re mise en route)."""
    au = os.getenv("BOOTSTRAP_ADMIN_USER")
    ap = os.getenv("BOOTSTRAP_ADMIN_PASSWORD")
    if not (au and ap):
        return
    try:
        r = httpx.get(_base(), params={"select": "id", "limit": "1"}, headers=_headers(), timeout=15)
        if r.status_code == 200 and len(r.json()) == 0:
            create_user(au, ap, role="admin")
    except Exception:
        pass
