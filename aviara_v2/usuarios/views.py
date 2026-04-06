from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

# Modelos
from inventario.models import StockHuevo, StockAgricola
from productos.models import Producto
from .forms import RegistroForm 
from django.contrib.auth.models import User
from .forms import UserEditForm
from django.views.decorators.cache import never_cache

# 1. Función de prueba para verificar si es admin
def es_admin(user):
    return user.is_staff

# 2. Dashboard Unificado y Protegido
 # Importa esto

@login_required
@user_passes_test(es_admin, login_url='home')
@never_cache  # <--- ESTO ES LA CLAVE
def admin_dashboard(request):
    total_huevos = StockHuevo.objects.aggregate(Sum('cantidad_disponible'))['cantidad_disponible__sum'] or 0
    total_productos = StockAgricola.objects.all().count()
    
    # Alertas de inventario bajo
    fecha_limite = timezone.now().date() + timedelta(days=3)
    alertas_huevos = StockHuevo.objects.filter(fecha_vencimiento__lte=fecha_limite)
    alertas_agricola = StockAgricola.objects.filter(cantidad_disponible__lt=5)

    context = {
        'total_huevos': total_huevos,
        'total_productos': total_productos,
        'alertas_huevos': alertas_huevos,
        'alertas_agricola': alertas_agricola,
        'suministros': StockAgricola.objects.all()[:5],
    }
    return render(request, 'dashboard.html', context)


# 3. Vista de redirección inteligente (Úsala en tus URLs)
@login_required
def redireccion_segun_rol(request):
    if request.user.is_staff:
        return redirect('dashboard')
    else:
        return redirect('home')
    
# 4. Registro de usuarios
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, f"¡Bienvenido a Aviara, {user.username}!")
                return redirect('home')
            except ValidationError as e:
                messages.error(request, str(e).strip("[]'"))
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})

# Vista para ver la lista de todos los usuarios
@user_passes_test(es_admin)
def lista_usuarios(request):
    usuarios = User.objects.all().order_by('-date_joined')
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

# Vista para editar un usuario existente
@user_passes_test(es_admin)
def editar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f"Usuario {usuario.username} actualizado.")
            return redirect('lista_usuarios')
    else:
        form = UserEditForm(instance=usuario)
    return render(request, 'usuarios/usuario_form.html', {'form': form, 'usuario_editado': usuario})

# Vista para eliminar (o desactivar) un usuario
@user_passes_test(es_admin)
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        messages.warning(request, "Usuario eliminado correctamente.")
        return redirect('lista_usuarios')
    return render(request, 'usuarios/usuario_confirm_delete.html', {'usuario': usuario})