from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from xhtml2pdf import pisa

from .models import StockHuevo, StockAgricola
from .forms import SuministroForm

# --- SEGURIDAD ---
def es_admin(user):
    return user.is_staff

# --- VISTAS DEL CRUD ---

@login_required
def lista_inventario(request):
    """ 
    Si decides usar esta vista independiente, 
    asegúrate de que el template exista en 'inventario/lista.html'
    """
    suministros = StockAgricola.objects.all()
    huevos = StockHuevo.objects.all()
    return render(request, 'inventario/lista.html', {
        'suministros': suministros,
        'huevos': huevos
    })

@login_required
def crear_suministro(request):
    if request.method == 'POST':
        form = SuministroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Suministro creado con éxito.")
            # Redirigimos al dashboard para ver el cambio de inmediato
            return redirect('admin_dashboard')
    else:
        form = SuministroForm()
    return render(request, 'inventario/suministro_form.html', {
        'form': form, 
        'titulo': 'Nuevo Suministro'
    })

@login_required
def editar_suministro(request, pk):
    suministro = get_object_or_404(StockAgricola, pk=pk)
    if request.method == 'POST':
        form = SuministroForm(request.POST, instance=suministro)
        if form.is_valid():
            form.save()
            # Corregido: Usamos .producto en lugar de .nombre
            messages.success(request, f"Suministro {suministro.producto} actualizado.")
            return redirect('admin_dashboard')
    else:
        form = SuministroForm(instance=suministro)
    return render(request, 'inventario/suministro_form.html', {
        'form': form, 
        'titulo': 'Editar Suministro'
    })

@login_required
def eliminar_suministro(request, pk):
    suministro = get_object_or_404(StockAgricola, pk=pk)
    
    if request.method == 'POST':
        suministro.delete()
        messages.warning(request, "Suministro eliminado correctamente.")
        # Redirige al dashboard principal
        return redirect('admin_dashboard') 
    
    return render(request, 'inventario/suministro_confirm_delete.html', {
        'item': suministro 
    })

@login_required
def exportar_inventario_pdf(request):
    huevos = StockHuevo.objects.all()
    agricola = StockAgricola.objects.all()
    # Verifica que este template exista en tu carpeta de ventas
    template_path = 'ventas/reporte_inventario.html' 
    
    context = {
        'huevos': huevos, 
        'agricola': agricola, 
        'fecha': timezone.now()
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_inventario.pdf"'
    
    try:
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('Error al generar PDF', status=500)
        return response
    except Exception as e:
        return HttpResponse(f'Error: {e}', status=500)