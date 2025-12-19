from fastapi import Depends, HTTPException, status

from src.core.config import settings
from src.domain.entities.user import User
from src.presentation.api.v1.depandancies.auth import get_current_user


def require_admin(
    user: User = Depends(get_current_user),
) -> User:
    if user.tg_id not in settings.bot.admin_ids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return user
