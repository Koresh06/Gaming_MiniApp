from dishka import make_async_container

from src.core.dependencies.base import BaseAppProvider
from src.core.dependencies.repositories import RepositoriesProvider
from src.core.dependencies.services import ServicesProvider
from src.core.dependencies.use_cases import UseCasesProvider


def make_base_providers():
    return (
        BaseAppProvider(),
        RepositoriesProvider(),
        ServicesProvider(),
        UseCasesProvider(),
    )


container = make_async_container(*make_base_providers())