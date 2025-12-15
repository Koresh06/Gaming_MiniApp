from pydantic_settings import BaseSettings


class TgBotSettings(BaseSettings):
    token: str = "your_bot_token"
    admin_ids: list[int] = [123456789]
    base_url: str = "https://your.domain.com"
    webhook_route: str = "/tg-webhook"
    web_server_host: str = "0.0.0.0"
    web_server_port: int = 8000
    secret_token: str = "my_super_secret" 

    @property
    def webhook_url(self) -> str:
        return f"{self.base_url}{self.webhook_route}"
