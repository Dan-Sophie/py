from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ProduccionForm 
from .models import ProduccionHuevos

# --- CRUD DE PRODUCCIÓN (Control Interno Aviara v2) ---

# 1. VER LISTA DE RECOLECCIÓN
def lista_produccion(request):
    registros = ProduccionHuevos.objects.all().order_by('-fecha_recoleccion')
    # BUSCA EN: templates/produccion/produccion_lista.html
    return render(request, 'produccion/produccion_lista.html', {'producciones': registros})


# 2. REGISTRAR NUEVA RECOLECCIÓN
def crear_produccion(request):
    if request.method == 'POST':
        form = ProduccionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Registro guardado con éxito!")
            return redirect('produccion_lista')
    else:
        form = ProduccionForm()
    
    # BUSCA EN: templates/produccion/crear.html
    return render(request, 'produccion/crear_produccion.html', {
        'form': form, 
        'titulo': 'Registrar Producción'
    })


# 3. MODIFICAR REGISTRO EXISTENTE
def editar_produccion(request, pk):
    produccion = get_object_or_404(ProduccionHuevos, pk=pk)
    if request.method == 'POST':
        form = ProduccionForm(request.POST, instance=produccion)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro actualizado correctamente.")
            return redirect('produccion_lista')
    else:
        form = ProduccionForm(instance=produccion)
    
    # REUTILIZA: templates/produccion/crear.html
    return render(request, 'produccion/crear_produccion.html', {
        'form': form, 
        'titulo': 'Editar Registro de Producción'
    })


# 4. ELIMINAR REGISTRO
def eliminar_produccion(request, pk):
    registro = get_object_or_404(ProduccionHuevos, pk=pk)
    if request.method == 'POST':
        registro.delete()
        messages.warning(request, "El registro ha sido eliminado del sistema.")
        return redirect('produccion_lista')
    
    # BUSCA EN: templates/produccion/eliminar_produccion.html
    return render(request, 'produccion/eliminar_produccion.html', {'registro': registro})