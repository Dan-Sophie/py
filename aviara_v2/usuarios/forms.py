from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistroForm(UserCreationForm):
    # Aquí van tus campos personalizados si los tienes
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

# También deberías tener el que hicimos antes para editar
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']