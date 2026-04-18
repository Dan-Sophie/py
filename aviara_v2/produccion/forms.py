from django import forms
from .models import ProduccionHuevos, ProductoAgricola

# --- Formulario para Producción de Huevos ---
class ProduccionForm(forms.ModelForm):
    class Meta:
        model = ProduccionHuevos
        fields = ['lote', 'fecha_recoleccion', 'cantidad_total', 'clasificacion']
        widgets = {
            'lote': forms.Select(attrs={'class': 'form-control'}),
            'fecha_recoleccion': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'cantidad_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'clasificacion': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'lote': 'Lote de Aves',
            'fecha_recoleccion': 'Fecha de Recolección',
            'cantidad_total': 'Cantidad de Huevos',
            'clasificacion': 'Clasificación',
        }

# --- Formulario para Productos Agrícolas ---
class ProductoForm(forms.ModelForm):
    class Meta:
        model = ProductoAgricola
        fields = ['nombre', 'unidad_medida', 'fecha_siembra', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Papa Sabanera'}),
            'unidad_medida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Bulto, Kg, Canasta'}),
            'fecha_siembra': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'unidad_medida': 'Unidad de Medida',
            'fecha_siembra': 'Fecha de Siembra',
            'imagen': 'Imagen del Producto'
        }