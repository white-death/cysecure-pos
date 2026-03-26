import requests
from cachetools import TTLCache
from fastapi import HTTPException
from app.core.config import settings

jwks_cache = TTLCache(maxsize=10, ttl=600)

JWKS_URL = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"


def get_jwks():
    if "jwks" in jwks_cache:
        return jwks_cache["jwks"]

    try:
        res = requests.get(JWKS_URL, timeout=5)
        res.raise_for_status()
        jwks_cache["jwks"] = res.json()
        return jwks_cache["jwks"]
    except:
        raise HTTPException(500, "JWKS fetch failed")


def get_key(kid):
    jwks = get_jwks()

    for key in jwks["keys"]:
        if key["kid"] == kid:
            return key

    jwks_cache.clear()
    jwks = get_jwks()

    for key in jwks["keys"]:
        if key["kid"] == kid:
            return key

    raise HTTPException(401, "Key not found")
