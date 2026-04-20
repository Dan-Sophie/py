from django.contrib import admin
from .models import StockHuevo, StockAgricola, HistorialMovimiento

@admin.register(StockHuevo)
class StockHuevoAdmin(admin.ModelAdmin):
    list_display = ('produccion', 'cantidad_disponible', 'fecha_vencimiento')
    ordering = ('fecha_vencimiento',)

@admin.register(StockAgricola)
class StockAgricolaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad_disponible', 'fecha_vencimiento')
    list_filter = ('producto',)

@admin.register(HistorialMovimiento)
class HistorialMovimientoAdmin(admin.ModelAdmin):
    list_display = ('fecha_hora', 'usuario', 'tipo_movimiento', 'producto_nombre', 'cantidad')
    list_filter = ('tipo_movimiento', 'fecha_hora',)
    readonly_fields = ('fecha_hora', 'usuario', 'tipo_movimiento', 'producto_nombre', 'cantidad', 'observacion')
