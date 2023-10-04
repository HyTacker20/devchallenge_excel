from rest_framework import views, status
from rest_framework.response import Response

from core.container import CellContainer, SheetContainer
from excel.dto import NewCellDTO, NewSheetDTO
from excel.expections import UnknownCellException
from excel.serializers import CellGETSerializer, CellPOSTSerializer


class CellDetailAPIView(views.APIView):
    cell_service = CellContainer.service()

    def get(self, request, sheet_id, cell_id):
        cell_dto = self.cell_service.get_instance(cell_id, sheet_id)
        if not cell_dto:
            return Response(status=status.HTTP_404_NOT_FOUND)

        instance_serializer = CellGETSerializer(cell_dto)
        return Response(instance_serializer.data)

    def post(self, request, sheet_id, cell_id):
        new_instance_serializer = CellPOSTSerializer(data=request.data)
        if not new_instance_serializer.is_valid():
            return Response(new_instance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_instance_dto = NewCellDTO(
            name=cell_id,
            value=new_instance_serializer.validated_data["value"],
            sheet=NewSheetDTO(name=sheet_id)
        )
        try:
            instance_dto = self.cell_service.create_instance(new_instance_dto)
        except (UnknownCellException, SyntaxError, TypeError) as e:
            data = {
                "value": request.data['value'],
                "result": 'ERROR'
            }
            return Response(data, status=status.HTTP_412_PRECONDITION_FAILED)

        instance_serializer = CellGETSerializer(instance_dto)

        return Response(instance_serializer.data, status=status.HTTP_201_CREATED)


class SheetDetailAPIView(views.APIView):
    sheet_service = SheetContainer.service()

    def get(self, request, sheet_id):
        sheet_dto = self.sheet_service.get_instance(sheet_id)
        if not sheet_dto:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {}
        for cell in sheet_dto.cells:
            data[cell.name] = {
                "value": cell.value,
                "result": cell.result
            }

        return Response(data)
