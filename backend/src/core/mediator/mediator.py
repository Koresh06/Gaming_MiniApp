from typing import Any, Type, Dict

from src.core.dependencies import container
from src.application.use_cases.base import UseCaseRequest, UseCase


class Mediator:
    def __init__(self) -> None:
        self._handlers: Dict[Type[UseCaseRequest], Type[UseCase[Any, Any]]] = {}

    def register(self, request_type: Type[UseCaseRequest], handler: Type[UseCase]):
        """Регистрирует UseCase по типу запроса."""
        self._handlers[request_type] = handler

    async def handle(self, request: UseCaseRequest) -> Any:
        handler_type = self._handlers.get(type(request))

        if handler_type is None:
            raise ValueError(f"No handler registered for {type(request)}")

        async with container() as req_container:
            handler: UseCase = await req_container.get(handler_type)
            return await handler(request)
