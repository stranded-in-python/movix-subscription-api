from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = Field("Subscription API")
    app_port: int = Field(3000)


settings = Settings()
