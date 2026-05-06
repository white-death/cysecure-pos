from urllib.parse import quote_plus
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    KEYCLOAK_URL: str
    KEYCLOAK_REALM: str
    KEYCLOAK_ADMIN_USERNAME: str
    KEYCLOAK_ADMIN_PASSWORD: str
    KEYCLOAK_ADMIN_CLIENT_ID: str

    class Config:
        env_file = "../.env"


settings = Settings()

encoded_password = quote_plus(settings.POSTGRES_PASSWORD)

DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:"
    f"{encoded_password}@"
    f"{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/"
    f"{settings.POSTGRES_DB}"
)
