from dependency_injector import containers, providers
from auto_dataclass.dj_model_to_dataclass import FromOrmToDataclass

from excel.repository import CellRepository, SheetRepository
from excel.services import CellService, SheetService


class ConvertorsContainer(containers.DeclarativeContainer):
    from_queryset_to_dto = providers.Factory(FromOrmToDataclass)


class RepositoryContainer(containers.DeclarativeContainer):
    cell_repository = providers.Factory(
        CellRepository, converter=ConvertorsContainer.from_queryset_to_dto
    )

    sheet_repository = providers.Factory(
        SheetRepository, converter=ConvertorsContainer.from_queryset_to_dto
    )


class ServiceContainer(containers.DeclarativeContainer):
    sheet_service = providers.Factory(
        SheetService, repository=RepositoryContainer.sheet_repository
    )

    cell_service = providers.Factory(
        CellService, repository=RepositoryContainer.cell_repository, sheet_service=sheet_service
    )


class CellContainer(containers.DeclarativeContainer):
    repository = RepositoryContainer.cell_repository
    service = ServiceContainer.cell_service


class SheetContainer(containers.DeclarativeContainer):
    repository = RepositoryContainer.sheet_repository
    service = ServiceContainer.sheet_service
