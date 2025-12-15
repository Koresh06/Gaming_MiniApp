from fastapi.responses import JSONResponse

from src.domain.exceptions.base import BaseInternalException


class BaseHttpException(BaseInternalException):

    @classmethod
    def get_response(cls) -> JSONResponse:
        return JSONResponse(
            status_code=cls._status_code,
            content={
                "status": "error",
                "error_code": cls._error_code,
                "message": cls._message,
            },
    )