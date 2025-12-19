from typing import Annotated
from fastapi import APIRouter, Header, status, Body
from dishka.integrations.fastapi import inject, FromDishka

from src.core.mediator.mediator import Mediator
from src.presentation.api.v1.schemas.requests.stars import (
    StarsPaymentCallbackSchema,
    StarsPayoutCallbackSchema,
)


router = APIRouter(prefix="/stars", tags=["Звезды"])


# POST /stars/payment/callback
@router.post(
    "/payment/callback",
    status_code=status.HTTP_200_OK,
    summary="Callback Telegram Stars по оплате ставки",
)
@inject
async def payment_callback(
    data: Annotated[
        StarsPaymentCallbackSchema,
        Body(..., description="Данные callback от Stars"),
    ],
    mediator: FromDishka[Mediator],
    secret: str = Header(
        alias="X-Telegram-Bot-Api-Secret-Token",
        description="Секретный токен, подтверждающий, что запрос отправлен Telegram.",
    ),
):
    """
    Обрабатывает callback от Telegram Stars о результате оплаты ставки.

    **Описание процесса:**
    Telegram Stars отправляет callback после обработки платежа.
    Этот эндпоинт принимает данные об оплате и передаёт их в соответствующий UseCase.

    ### Требуемые заголовки:
    - **X-Telegram-Bot-Api-Secret-Token** — секрет, настроенный в боте.  
      Обязателен для прохождения проверки middleware.

    **Request body:**
    - `bet_uuid`: UUID ставки
    - `status`: статус оплаты (`paid` / `failed`)
    - `telegram_transaction_id`: ID транзакции Stars

    **Response:**
    - `{ "status": "ok" }` — после успешной обработки callback.
    """
    await mediator.handle(data.to_request())
    return {"status": "ok"}


# POST /stars/payout/callback
@router.post(
    "/payout/callback",
    status_code=status.HTTP_200_OK,
    summary="Callback Telegram Stars о выплате",
)
@inject
async def payout_callback(
    data: Annotated[
        StarsPayoutCallbackSchema,
        Body(..., description="Данные payout callback"),
    ],
    mediator: FromDishka[Mediator],
    secret: str = Header(
        alias="X-Telegram-Bot-Api-Secret-Token",
        description=(
            "Секретный токен Telegram. " 
            "Используется для проверки подлинности webhook."
        ),
    ),
):
    """
    Обрабатывает callback от Telegram Stars о статусе выплаты выигрыша.

    **Описание процесса:**
    Когда выплата игроку завершена или отклонена,
    Telegram Stars отправляет callback на этот endpoint.

    ### Требуемые заголовки:
    - **X-Telegram-Bot-Api-Secret-Token** — обязательный заголовок для валидации webhook.

    **Request body:**
    - `payout_uuid`: UUID выплаты
    - `status`: статус выплаты (`pending` / `success` / `failed`)
    - `telegram_transaction_id`: ID транзакции Stars

    **Response:**
    - `{ "status": "ok" }` — после успешной обработки callback.
    """
    await mediator.handle(data.to_request())
    return {"status": "ok"}
