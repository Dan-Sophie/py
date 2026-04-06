from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo Electrónico")
    first_name = forms.CharField(max_length=30, label="Nombre")
    last_name = forms.CharField(max_length=30, label="Apellido")

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]