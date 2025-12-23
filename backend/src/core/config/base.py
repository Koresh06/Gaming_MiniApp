from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "APP_NAME"
    debug: bool = True
    secret_key: str = "secret_key"
    algorithm: str = "HS256"
    expare_minutes: int = 60
    origins: list = ["*"]
    use_fake_stars: bool = True