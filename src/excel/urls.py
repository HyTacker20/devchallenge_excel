from django.urls import path

from excel.views import CellDetailAPIView, SheetDetailAPIView

app_name = 'excel'
urlpatterns = [
    path("<str:sheet_id>/", SheetDetailAPIView.as_view(), name='sheet-detail'),
    path("<str:sheet_id>/<str:cell_id>/", CellDetailAPIView.as_view(), name='cell-detail'),
]
