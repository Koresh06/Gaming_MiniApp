from dishka.integrations.fastapi import inject, FromDishka
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.core.mediator.mediator import Mediator
from src.application.use_cases.user.get_by_tg_id import GetUserByTgIdRequest
from src.infrastructure.security.jwt import JWTService


bearer_scheme = HTTPBearer()


@inject
async def get_current_user(
    jwt_service: FromDishka[JWTService],
    mediator: FromDishka[Mediator],
    creat: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        payload = jwt_service.decode_token(creat.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    tg_id = payload.get("sub")
    if not tg_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await mediator.handle(GetUserByTgIdRequest(tg_id=int(tg_id)))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
