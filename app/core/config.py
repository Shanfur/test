from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Simple API"
    app_version: str = "0.1.0"
    debug: bool = False

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
