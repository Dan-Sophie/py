from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from .forms import RegistroForm
from usuarios.models import Usuario
from django.http import JsonResponse
from productos.models import Producto
from django.db import IntegrityError
from datetime import datetime


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                # Usamos commit=False para encriptar la contraseña antes de guardar
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()
                
                messages.success(request, "Cuenta creada exitosamente.")
                return redirect('login')
            except IntegrityError:
                form.add_error('documento', 'Este número de documento ya está registrado.')
        
        # IMPORTANTE: Si el formulario NO es válido, el código saltará 
        # automáticamente al render de abajo, enviando el 'form' con los errores.
                
    else:
        form = RegistroForm()
    
    # Este return DEBE estar fuera de todos los IF para que siempre devuelva algo
    return render(request, 'registro.html', {'form': form})    
def salir(request):
    """Cierra sesión y redirige al login"""
    django_logout(request)
    return redirect('login')

# --- DASHBOARD Y HOME ---

@login_required
def dashboard(request):
    """
    Esta vista actúa como un repartidor:
    - Si es ADMIN: Entra al panel de control (dashboard.html)
    - Si es USUARIO: Entra a la página estética (home.html)
    """
    
    # Definimos los datos comunes (como las categorías)
    contexto = {
        'categorias': [
            {'id': 'huevos', 'icon': 'egg', 'color': 'warning'},
            {'id': 'pollos', 'icon': 'drumstick-bite', 'color': 'danger'},
            {'id': 'lacteos', 'icon': 'cheese', 'color': 'info'},
        ],
    }

    if request.user.is_staff:
        # --- DESTINO PARA EL ADMINISTRADOR ---
        return render(request, 'dashboard.html', contexto)
    else:
        # --- DESTINO PARA EL USUARIO COMÚN ---
        # Aquí es donde el cliente verá el banner de los huevos
        return render(request, 'home.html', contexto)


def productos_api(request):
    productos = Producto.objects.all().values('id', 'nombre', 'precio') # Ajusta según tus campos
    return JsonResponse(list(productos), safe=False)