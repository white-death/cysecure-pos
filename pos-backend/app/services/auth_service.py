import requests

from fastapi import HTTPException

from app.core.config import settings


def login_user(username: str, password: str):

    token_url = (
        f"{settings.KEYCLOAK_URL}"
        f"/realms/{settings.KEYCLOAK_REALM}"
        f"/protocol/openid-connect/token"
    )

    payload = {
        "client_id": settings.KEYCLOAK_ADMIN_CLIENT_ID,
        "grant_type": "password",
        "username": username,
        "password": password,
    }

    response = requests.post(
        token_url,
        data=payload,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    if response.status_code != 200:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return response.json()
