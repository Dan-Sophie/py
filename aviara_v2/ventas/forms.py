from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        # Usamos exactamente los nombres de tu modelo
        fields = ['cliente', 'estado', 'direccion', 'completado']
        
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Calle 10 #20-30'}),
            'completado': forms.CheckboxInput(attrs={'class': 'form-check-input ml-2'}),
        }