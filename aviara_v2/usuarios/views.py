from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from .forms import RegistroForm
from usuarios.models import Usuario
from django.http import JsonResponse
from productos.models import Producto
from .forms import RegistroForm


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta creada. Por favor, inicia sesión.")
            return redirect('login') 
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})

def salir(request):
    """Cierra sesión y redirige al login"""
    django_logout(request)
    return redirect('login')

# --- DASHBOARD Y HOME ---

@login_required
def dashboard(request):
    # 1. SI ES ADMINISTRADOR (Cualquiera de los 3 que mencionaste)
    if request.user.is_staff or request.user.is_superuser:
        # Al terminar el login, el admin se va al Panel de Control
        return render(request, 'dashboard.html')

    # 2. SI ES CLIENTE
    # Al terminar el login, el cliente se va a la Página Principal (Home)
    if hasattr(request.user, 'rol') and request.user.rol == 'cliente':
        # Definimos lo que verá el cliente en su home
        categorias_home = [
            {'id': 'huevos', 'icon': 'egg', 'color': 'warning'},
            {'id': 'pollos', 'icon': 'drumstick-bite', 'color': 'danger'},
            {'id': 'lacteos', 'icon': 'cheese', 'color': 'info'},
        ]
        return render(request, 'usuarios/home.html', {
            'categorias': categorias_home
        })

    # 3. SI NO TIENE ROL (Por si acaso)
    return render(request, 'home.html')
    




