from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "APP_NAME"
    secret_key: str = "secret_key"
    algorithm: str = "HS256"
    expare_minutes: int = 60
    debug: bool = True
    use_fake_stars: bool = True