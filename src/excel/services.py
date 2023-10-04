from core.interface import RepositoryInterface
from excel.dto import NewCellDTO, SheetDTO, CellDTO, NewSheetDTO


class SheetService:
    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    def get_instance(self, sheet_name: str) -> SheetDTO:
        return self.repository.get_instance(sheet_name)

    def is_exist(self, sheet_name) -> bool:
        return self.repository.is_exist(sheet_name)

    def create_instance(self, dto: NewSheetDTO):
        return self.repository.create_instance(dto)

    def update_instance(self, *args, **kwargs):
        pass


class CellService:
    def __init__(self, repository: RepositoryInterface, sheet_service: SheetService):
        self.repository = repository
        self.sheet_service = sheet_service

    def get_instance(self, cell_id, sheet_id) -> CellDTO:
        return self.repository.get_instance(cell_id, sheet_id)

    def is_exist(self, dto) -> bool:
        return self.repository.is_exist(dto)

    def create_instance(self, dto: NewCellDTO):
        if not self.sheet_service.is_exist(dto.sheet.name):
            sheet_dto = NewSheetDTO(name=dto.sheet.name)
            dto.sheet = self.sheet_service.create_instance(sheet_dto)
        else:
            dto.sheet = self.sheet_service.get_instance(dto.sheet.name)
        print(dto.sheet)

        if self.is_exist(dto):
            return self.update_instance(dto)
        cell = self.repository.create_instance(dto)
        print(cell)
        return cell

    def update_instance(self, dto: NewCellDTO):
        return self.repository.update_instance(dto)
