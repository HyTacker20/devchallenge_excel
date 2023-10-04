from django.contrib import admin

from excel.models import Sheet, Cell


class CellInline(admin.TabularInline):
    model = Cell
    extra = 1


@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    inlines = [CellInline]


@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value', 'result', 'sheet')
    list_filter = ('sheet',)
