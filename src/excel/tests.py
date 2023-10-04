from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Sheet, Cell


class CellModelTest(TestCase):
    def setUp(self):
        self.sheet = Sheet.objects.create(name="Test Sheet")

    def test_string_data_type(self):
        cell = Cell.objects.create(name="A1", value="Hello, World!", sheet=self.sheet)
        self.assertEqual(cell.result, "Hello, World!")

    def test_integer_data_type(self):
        cell = Cell.objects.create(name="A2", value="42", sheet=self.sheet)
        self.assertEqual(cell.result, "42")

    def test_float_data_type(self):
        cell = Cell.objects.create(name="A3", value="3.14", sheet=self.sheet)
        self.assertEqual(cell.result, "3.14")


class CellModelMathTest(TestCase):
    def setUp(self):
        self.sheet = Sheet.objects.create(name="Test Sheet")

    def test_addition_operation(self):
        cell = Cell.objects.create(name="A1", value="=5 + 3", sheet=self.sheet)
        self.assertEqual(cell.result, "8")

    def test_subtraction_operation(self):
        cell = Cell.objects.create(name="A2", value="=10 - 4", sheet=self.sheet)
        self.assertEqual(cell.result, "6")

    def test_multiplication_operation(self):
        cell = Cell.objects.create(name="A3", value="=3 * 7", sheet=self.sheet)
        self.assertEqual(cell.result, "21")

    def test_division_operation(self):
        cell = Cell.objects.create(name="A4", value="=20 / 4", sheet=self.sheet)
        self.assertEqual(cell.result, "5.0")

    def test_complex_expression(self):
        cell = Cell.objects.create(name="A5", value="=10 + 5 * (3 - 1)", sheet=self.sheet)
        self.assertEqual(cell.result, "20")


class SheetModelTest(TestCase):
    def test_case_insensitive_sheet_id(self):
        sheet = Sheet.objects.create(name="TestSheet")
        cell = Cell.objects.create(name="A1", value="5", sheet=sheet)
        url = reverse('excel:sheet-detail', args=["testsheet"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_case_insensitive_cell_id(self):
        sheet = Sheet.objects.create(name="TestSheet")
        cell = Cell.objects.create(name="A1", value="5", sheet=sheet)
        url = reverse('excel:cell-detail', args=["testsheet", "a1"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SheetDetailAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.sheet = Sheet.objects.create(name='test-sheet')
        self.url = reverse('excel:sheet-detail', args=[self.sheet.name])

    def test_get_sheet_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_sheet_detail(self):
        url = reverse('excel:sheet-detail', args=['nonexistent-sheet'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CellDetailAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.sheet = Sheet.objects.create(name='test-sheet')
        self.cell = Cell.objects.create(name='var1', value='1', sheet=self.sheet)
        self.url = reverse('excel:cell-detail', args=[self.sheet.name, self.cell.name])

    def test_get_cell_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_cell_detail(self):
        url = reverse('excel:cell-detail', args=[self.sheet.name, 'nonexistent-cell'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_cell(self):
        data = {'value': '3'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
