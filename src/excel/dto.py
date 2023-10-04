from dataclasses import dataclass
from typing import Optional, List


@dataclass(frozen=True)
class NewSheetDTO:
    name: str
    id: Optional[int] = None


@dataclass(frozen=True)
class SheetNameDTO:
    name: str


@dataclass(frozen=True)
class CellDTO:
    name: str
    value: str
    result: str
    sheet: SheetNameDTO
    id: Optional[int] = None


@dataclass(frozen=True)
class SheetDTO:
    name: str
    cells: List[CellDTO]
    id: Optional[int] = None


@dataclass()
class NewCellDTO:
    name: str
    value: str
    sheet: NewSheetDTO
