from fastapi.responses import JSONResponse

from src.domain.exceptions.base import ApplicationException


class BaseHttpException(ApplicationException):

    @classmethod
    def get_response(cls) -> JSONResponse:
        return JSONResponse(
            status_code=cls.status_code,
            content={
                "status": "error",
                "error_code": cls.error_code,
                "message": cls.message,
            },
        )
