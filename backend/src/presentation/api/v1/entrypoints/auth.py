from fastapi import APIRouter, Header, HTTPException, Depends

from src.core.config import settings
from src.core.mediator.mediator import Mediator
from src.presentation.api.v1.depandancies.mediator import get_mediator
from src.application.dtos.auth import AuthResultDTO
from src.application.use_cases.auth.auth import TelegramAuthRequest


router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/telegram")
async def telegram_auth(
    x_telegram_init_data: str = Header(...),
    mediator: Mediator = Depends(get_mediator),
):
    try:
        result: AuthResultDTO = await mediator.handle(
            TelegramAuthRequest(init_data=x_telegram_init_data)
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Telegram auth failed")

    return {
        "access_token": result.access_token,
        "token_type": "bearer",
        "expires_minutes": settings.app.expare_minutes,
    }
