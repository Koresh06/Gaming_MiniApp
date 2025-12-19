from src.core.dependencies.base import BaseAppProvider
from src.core.dependencies.repositories import RepositoriesProvider
from src.core.dependencies.services import ServicesProvider
from src.core.dependencies.use_cases import UseCasesProvider
from src.core.dependencies.mediator import MediatorProvider


def make_base_providers():
    return (
        BaseAppProvider(),
        RepositoriesProvider(),
        ServicesProvider(),
        UseCasesProvider(),
        MediatorProvider(),
    )