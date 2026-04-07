from django import forms
from .models import StockHuevo, StockAgricola

class HuevoForm(forms.ModelForm):
    class Meta:
        model = StockHuevo
        fields = ['produccion', 'cantidad_disponible', 'fecha_vencimiento']
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'produccion': forms.Select(attrs={'class': 'form-control'}),
            'cantidad_disponible': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AgricolaForm(forms.ModelForm):
    class Meta:
        model = StockAgricola
        # Opción A: Usar '__all__' para que no se te escape ninguno
        fields = '__all__' 
        
        # O Opción B: Listarlos explícitamente si 'fecha_vencimiento' es requerida
        # fields = ['producto', 'cantidad_disponible', 'fecha_cosecha', 'fecha_vencimiento']
        
        widgets = {
            'fecha_cosecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad_disponible': forms.NumberInput(attrs={'class': 'form-control'}),
        }