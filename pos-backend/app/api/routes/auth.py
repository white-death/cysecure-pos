from fastapi import APIRouter

from app.schemas.auth import (
    LoginRequest,
    TokenResponse
)

from app.services.auth_service import login_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(data: LoginRequest):

    tokens = login_user(
        username=data.username,
        password=data.password
    )

    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": tokens["token_type"]
    }
