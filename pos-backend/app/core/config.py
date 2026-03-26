from pydantic_settings import BaseSettings
from urllib.parse import quote_plus


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    KEYCLOAK_URL: str
    KEYCLOAK_REALM: str

    KEYCLOAK_ADMIN_USERNAME: str
    KEYCLOAK_ADMIN_PASSWORD: str
    KEYCLOAK_ADMIN_CLIENT_ID: str

    class Config:
        env_file = ".env"


settings = Settings()

encoded_password = quote_plus(settings.DB_PASS)

DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:{encoded_password}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)
