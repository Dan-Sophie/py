from django import forms
from .models import StockAgricola

class SuministroForm(forms.ModelForm):
    class Meta:
        model = StockAgricola
        # Estos son los 4 campos exactos de tu modelo:
        fields = ['producto', 'cantidad_disponible', 'fecha_cosecha', 'fecha_vencimiento']
        
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad_disponible': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'fecha_cosecha': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'fecha_vencimiento': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
        }
        labels = {
            'producto': 'Producto Agrícola',
            'cantidad_disponible': 'Cantidad en Stock',
            'fecha_cosecha': 'Fecha de Cosecha',
            'fecha_vencimiento': 'Fecha de Vencimiento',
        }