from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, status, Body

from src.core.mediator import get_mediator
from src.application.use_cases.user.get_by_tg_id import GetUserByTgIdRequest
from src.application.use_cases.user.get_by_uuid import GetUserByUUIDRequest
from src.presentation.api.v1.schemas.requests.user import CreateUserSchema
from src.presentation.api.v1.schemas.responses.user import UserResponseSchema


router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.post(
    "/",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создание нового пользователя",
)
async def create_user(
    data: Annotated[
        CreateUserSchema,
        Body(..., description="Данные для создания нового пользователя"),
    ],
) -> UserResponseSchema:
    """
    Создаёт нового пользователя на основе Telegram ID и профиля.

    **Request body:**
    - `tg_id`: Telegram ID пользователя  
    - `username`: username пользователя  
    - `first_name`: имя  
    - `last_name`: фамилия  
    - `language_code`: язык Telegram  

    **Response:**
    - Полная информация о созданном пользователе.
    """
    mediator = get_mediator()

    user = await mediator.handle(data.to_request())
    return UserResponseSchema.from_dto(user)


@router.get(
    "/{uuid}",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получение пользователя по UUID",
)
async def get_user_by_uuid(uuid: UUID) -> UserResponseSchema:
    """
    Возвращает данные пользователя по его уникальному UUID.

    **Path parameters:**
    - `uuid`: уникальный идентификатор пользователя  

    **Response:**
    - Полная информация о пользователе.
    """
    mediator = get_mediator()

    request = GetUserByUUIDRequest(
        user_uuid=uuid,
    )

    user = await mediator.handle(request)
    return UserResponseSchema.from_dto(user)


@router.get(
    "/tg/{tg_id}",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получение пользователя по Telegram ID",
)
async def get_user_by_tg_id(tg_id: int) -> UserResponseSchema:
    """
    Возвращает данные пользователя по Telegram ID.

    **Path parameters:**
    - `tg_id`: Telegram ID пользователя  

    **Response:**
    - Полная информация о пользователе.
    """
    mediator = get_mediator()

    request = GetUserByTgIdRequest(
        tg_id=tg_id,
    )
    user = await mediator.handle(request)
    return UserResponseSchema.from_dto(user)
