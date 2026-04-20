from django.shortcuts import render, redirect, get_object_or_404
from .models import StockHuevo, StockAgricola
from .forms import HuevoForm, AgricolaForm  # Importante crear este archivo forms.py
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa 

# 1. LA VISTA PRINCIPAL
def lista_inventario(request):
    return render(request, 'inventario/lista_inventario.html', {
        'huevos': StockHuevo.objects.all(),
        'agricola': StockAgricola.objects.all(),
    })

# 2. LÓGICA PARA AGRÍCOLA (Crear/Editar con Forms)
def gestionar_agricola(request, pk=None):
    # Si hay pk, editamos; si no, creamos uno nuevo
    obj = get_object_or_404(StockAgricola, pk=pk) if pk else None
    
    if request.method == 'POST':
        # Pasamos instance=obj para que Django sepa si debe actualizar o insertar
        form = AgricolaForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('inventario_list')
    else:
        form = AgricolaForm(instance=obj)
        
    return render(request, 'inventario/form_inventario.html', {
        'form': form, 
        'tipo': 'Agrícola',
        'item': obj # Mantenemos 'item' por si tu template lo usa para el título
    })

# 3. LÓGICA PARA HUEVOS (Crear/Editar con Forms)
def gestionar_huevos(request, pk=None):
    obj = get_object_or_404(StockHuevo, pk=pk) if pk else None
    
    if request.method == 'POST':
        form = HuevoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('inventario_list')
    else:
        form = HuevoForm(instance=obj)
        
    return render(request, 'inventario/form_inventario.html', {
        'form': form, 
        'tipo': 'Huevos',
        'item': obj
    })

# 4. ELIMINACIÓN GENÉRICA
def eliminar_item(request, pk, tipo):
    if tipo == 'huevos':
        item = get_object_or_404(StockHuevo, pk=pk)
    else:
        item = get_object_or_404(StockAgricola, pk=pk)
    item.delete()
    return redirect('inventario_list')

# 5. EXPORTACIÓN PDF
def exportar_inventario_pdf(request):
    template_path = 'inventario/reporte_pdf.html'
    
    # --- FILTROS MULTICRITERIO ---
    # Capturamos parámetros de la URL (si vienen del formulario)
    categoria_filtro = request.GET.get('categoria')
    solo_bajo_stock = request.GET.get('bajo_stock')

    # Inicializamos los querysets
    huevos = StockHuevo.objects.all()
    agricola = StockAgricola.objects.all()

    # Aplicamos filtros si el usuario los seleccionó
    if categoria_filtro:
        # Filtramos huevos o agrícola según la categoría
        huevos = huevos.filter(variacion__producto__categoria__nombre__icontains=categoria_filtro)
        agricola = agricola.filter(producto__categoria__nombre__icontains=categoria_filtro)

    if solo_bajo_stock == 'true':
        # Filtro multicriterio: solo productos con stock menor a 10 (por ejemplo)
        huevos = huevos.filter(cantidad__lt=10)
        agricola = agricola.filter(cantidad__lt=10)

    # --- GENERACIÓN DEL PDF ---
    context = {
        'huevos': huevos,
        'agricola': agricola,
        'empresa': 'Aviara v2 - Reporte Inteligente de Inventario',
        'filtros': {
            'categoria': categoria_filtro if categoria_filtro else "Todas",
            'estado': "Crítico (Bajo Stock)" if solo_bajo_stock == 'true' else "Completo"
        }
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_inventario_filtrado.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Error al generar el reporte <pre>' + html + '</pre>')
    return response