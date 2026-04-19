from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, DecimalWidget
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats
from .models import Producto, VariacionProducto

# 1. El formato de punto y coma que ya sabemos que te funciona
class CSV_PuntoYComa(base_formats.CSV):
    def get_delimiter(self):
        return ';'

# 2. Recurso para Producto (La carga masiva que quieres hacer ahora)
class ProductoResource(resources.ModelResource):
    class Meta:
        model = Producto
        # Asegúrate de que estos nombres coincidan con tu CSV
        fields = ('nombre', 'descripcion', 'categoria', 'es_organico')
        import_id_fields = [] # No pedimos ID
        skip_unchanged = False # Queremos ver errores, no que se salte filas
        report_skipped = True

# 3. Recurso para Variaciones (El que hicimos antes)
class VariacionProductoResource(resources.ModelResource):
    producto = fields.Field(
        column_name='producto',
        attribute='producto',
        widget=ForeignKeyWidget(Producto, 'nombre')
    )
    precio = fields.Field(
        column_name='precio',
        attribute='precio',
        widget=DecimalWidget()
    )
    class Meta:
        model = VariacionProducto
        fields = ('producto', 'presentacion', 'unidad_medida', 'precio', 'stock')
        import_id_fields = []
        skip_unchanged = False

# --- CONFIGURACIÓN DEL ADMIN ---

@admin.register(Producto)
class ProductoAdmin(ImportExportModelAdmin):
    resource_class = ProductoResource
    formats = [CSV_PuntoYComa] # Aplicamos el punto y coma aquí
    list_display = ('nombre', 'categoria', 'es_organico', 'fecha_creacion')

@admin.register(VariacionProducto)
class VariacionProductoAdmin(ImportExportModelAdmin):
    resource_class = VariacionProductoResource
    formats = [CSV_PuntoYComa] # Y aquí también
    list_display = ('producto', 'presentacion', 'precio', 'stock')