from jose import jwt
from fastapi import HTTPException
from app.core.jwks import get_key


def verify_token(token: str):
    try:
        header = jwt.get_unverified_header(token)
        key = get_key(header["kid"])

        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            options={"verify_aud": False}
        )

        return payload

    except Exception:
        raise HTTPException(401, "Invalid token")
