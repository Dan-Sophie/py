from django.contrib import admin
from .models import LoteAves, ProduccionHuevos, ProductoAgricola

@admin.register(LoteAves)
class LoteAvesAdmin(admin.ModelAdmin):
    list_display = ('codigo_lote', 'raza', 'estado')

@admin.register(ProduccionHuevos)
class ProduccionHuevosAdmin(admin.ModelAdmin):
    list_display = ('fecha_recoleccion', 'lote', 'clasificacion', 'cantidad_total')

@admin.register(ProductoAgricola)
class ProductoAgricolaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'unidad_medida')
