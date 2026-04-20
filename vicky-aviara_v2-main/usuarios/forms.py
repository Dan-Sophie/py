from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model  # <--- IMPORTANTE: Esto faltaba

# Esta línea obtiene automáticamente tu modelo 'usuarios.Usuario'
# No necesitas importar 'Usuario' ni 'User' manualmente arriba
User = get_user_model()

class RegistroForm(UserCreationForm):
    # Añadimos el campo de documento manualmente
    documento = forms.CharField(label="Número de Documento", required=True)
    first_name = forms.CharField(label="Nombre", required=True)
    last_name = forms.CharField(label="Apellidos", required=True)
    email = forms.EmailField(label="Dirección de correo electrónico", required=True)

    class Meta:
        model = User
        # IMPORTANTE: El nombre aquí debe ser igual al que pusiste en models.py
        fields = ['username', 'email', 'first_name', 'last_name', 'documento']