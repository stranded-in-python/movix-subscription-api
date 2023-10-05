from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = Field("Subscription API")
    app_port: int = Field(3000)

    # Настройки PSQL
    pghost: str = "localhost"
    pgport: str = "5432"
    pgdb: str = "yamp_movies_db"
    pguser: str = "yamp_dummy"
    pgpassword: str = "qweasd123"
    database_adapter: str = "postgresql"
    database_sqlalchemy_adapter: str = "postgresql+asyncpg"
    # Параметры аутентификации
    google_oauth_client_id: SecretStr = SecretStr("SECRET")
    google_oauth_client_secret: SecretStr = SecretStr("SECRET")
    state_secret: SecretStr = SecretStr("SECRET")
    reset_password_token_secret: SecretStr = SecretStr('reset_password')
    verification_password_token_secret: SecretStr = SecretStr('verify_password')
    access_token_secret: SecretStr = SecretStr('access_token')
    refresh_token_secret: SecretStr = SecretStr('refresh_token')


def get_database_url_async() -> str:
    return (
        f"{settings.database_sqlalchemy_adapter}://{settings.pguser}:"
        f"{settings.pgpassword}@{settings.pghost}:{settings.pgport}/{settings.pgdb}"
    )


settings = Settings()  # type: ignore
