from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'fecha_pedido', 'estado', 'total']
        widgets = {
            'cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_pedido': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'cliente': 'Nombre del Cliente',
            'fecha_pedido': 'Fecha del Pedido',
            'estado': 'Estado',
            'total': 'Total ($)',
        }