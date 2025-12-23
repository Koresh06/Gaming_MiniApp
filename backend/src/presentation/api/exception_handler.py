from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

from src.domain.exceptions.base import ApplicationException


def register_exception_handlers(app: FastAPI):
    """
    Регистрирует обработчики ошибок приложения.
    """

    @app.exception_handler(ApplicationException)
    async def internal_exception_handler(request: Request, exc: ApplicationException):
        return JSONResponse(
            status_code=exc.getstatus_code(),
            content={
                "status": "error",
                "status_code": exc.getstatus_code(),
                "error_code": exc.geterror_code(),
                "message": exc.getmessage(),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        return JSONResponse(
            status_code=422,
            content={
                "status": "error",
                "status_code": 422,
                "error_code": "VALIDATION_ERROR",
                "message": "Ошибка валидации входящих данных",
                "errors": exc.errors(),
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "status_code": exc.status_code,
                "error_code": exc.detail,
                "message": exc.detail,
            },
        )

    @app.exception_handler(IntegrityError)
    async def db_exception_handler(request: Request, exc: IntegrityError):
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "status_code": 500,
                "error_code": "DATABASE_ERROR",
                "message": "Ошибка уровня базы данных",
            },
        )
