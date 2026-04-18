from django import forms
from django.contrib.auth.forms import UserCreationForm
# IMPORTA TU MODELO PERSONALIZADO
from .models import Usuario 

class RegistroForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario  # <--- Esto es lo más importante
        fields = ['username', 'email', 'first_name', 'last_name']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']