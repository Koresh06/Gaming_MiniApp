from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationException(Exception):
    status_code = 500
    error_code = "INTERNAL_SERVER_ERROR"
    message = "Internal server error"

    def __init__(
        self,
        message: str | None = None,
        error_code: str | None = None,
        status_code: int | None = None,
    ):
        self.message = message or self.message
        self.error_code = error_code or self.error_code
        self.status_code = status_code or self.status_code

    def get_message(self):
        return self.message
