from core.interface import RepositoryInterface
from excel.dto import CellDTO, NewCellDTO, SheetDTO
from excel.models import Cell, Sheet
from auto_dataclass.dj_model_to_dataclass import ToDTOConverter
from annoying.functions import get_object_or_None


class SheetRepository(RepositoryInterface):
    def __init__(self, converter: ToDTOConverter):
        self.converter = converter

    def get_instance(self, sheet_name):
        sheet = Sheet.objects.filter(name__iexact=sheet_name).prefetch_related("cells").first()
        return self.converter.to_dto(sheet, SheetDTO) if sheet else None

    def is_exist(self, sheet_name) -> bool:
        return Sheet.objects.filter(name__iexact=sheet_name).exists()

    def create_instance(self, dto: NewCellDTO):
        sheet = Sheet.objects.create(name=dto.name)
        return self.converter.to_dto(sheet, SheetDTO)

    def update_instance(self, dto: CellDTO):
        pass


class CellRepository(RepositoryInterface):
    def __init__(self, converter: ToDTOConverter):
        self.converter = converter

    def get_instance(self, cell_id, sheet_id):
        cell = Cell.objects.filter(sheet__name__iexact=sheet_id, name__iexact=cell_id).first()
        if cell:
            cell.calculate_result()
        return self.converter.to_dto(cell, CellDTO) if cell else None

    def is_exist(self, dto: NewCellDTO) -> bool:
        return Cell.objects.filter(name=dto.name, sheet__name__iexact=dto.sheet.name).exists()

    def create_instance(self, dto: NewCellDTO):
        cell = Cell.objects.create(
            name=dto.name,
            value=dto.value,
            sheet_id=dto.sheet.id
        )
        return self.converter.to_dto(cell, CellDTO)

    def update_instance(self, dto: CellDTO):
        cell = Cell.objects.filter(name__iexact=dto.name, sheet__name__iexact=dto.sheet.name).first()
        if cell:
            cell.value = dto.value
            cell.save()
            return self.converter.to_dto(cell, CellDTO)
        return None
