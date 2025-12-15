class BaseInternalException(Exception):
    _status_code = 500
    _error_code = "INTERNAL_SERVER_ERROR"
    _message = "Internal server error"

    def __init__(self, message: str | None = None, error_code: str | None = None, status_code: int | None = None):
        self.message = message or self._message
        self.error_code = error_code or self._error_code
        self.status_code = status_code or self._status_code

    def get_message(self):
        return self.message
    
    def get_error_code(self):
        return self.error_code

    def get_status_code(self):
        return self.status_code
    
