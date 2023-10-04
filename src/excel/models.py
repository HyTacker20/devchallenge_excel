from django.db import models
import re

from excel.expections import UnknownCellException

OPERATORS = '+-/*()'


class Sheet(models.Model):
    name = models.CharField(db_index=True, unique=True)

    def __str__(self):
        return f'Sheet #{self.id} | {self.name}' if self.name is not None else f"Sheet #{self.id}"


class Cell(models.Model):
    name = models.CharField(db_index=True)
    value = models.CharField(blank=True, null=True)
    result = models.CharField(blank=True)

    sheet = models.ForeignKey(Sheet, related_name='cells', on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "sheet")

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.result = self.calculate_result()
        super().save(force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return f"Cell #{self.id}: name={self.name}, value={self.value}, sheet={self.sheet}"

    def calculate_result(self) -> str:
        if not self._is_func():
            return self.value

        elements = self._parse_operation()

        for n in range(len(elements)):
            if elements[n] not in OPERATORS and '.' not in elements[n] and not elements[n].isnumeric():
                elements[n] = self._get_cell_result(elements[n])

        result = ''.join(elements)

        if not any(ext.isalpha() for ext in elements):
            try:
                result = str(eval(result))
            except UnknownCellException:
                result = 'ERROR'

        self.result = result
        return result

    def _is_func(self) -> bool:
        return '=' == self.value[0]

    def _parse_operation(self):
        expression = re.findall(r'[a-zA-Z_]\w*|\d+\.\d+|\d+|[+\-*/()]|[-\w]+', self.value)
        print(expression)
        return expression

    def _get_cell_result(self, cell_name):
        print(cell_name)
        cell = Cell.objects.filter(name__iexact=cell_name, sheet=self.sheet).first()
        print(self.sheet)
        print(Cell.objects.all())
        if not cell:
            raise UnknownCellException(f"Passed undefined cell {cell}")
        return cell.calculate_result()
