from django.contrib import admin
from .models import Producto, VariacionProducto

class VariacionProductoInline(admin.TabularInline):
    model = VariacionProducto
    extra = 1
    fields = ['presentacion', 'unidad_medida', 'precio', 'stock']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'es_organico', 'fecha_creacion')
    list_filter = ('categoria', 'es_organico')
    search_fields = ('nombre',)
    inlines = [VariacionProductoInline]
