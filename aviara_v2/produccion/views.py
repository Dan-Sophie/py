import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ProduccionHuevos
from . import views 
from .forms import ProduccionForm, ProductoForm
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

# URL de tu API local (la del profesor)
API_URL_LOCAL = "http://127.0.0.1:8000/api/productos/" 

# --- LECTURA (API EXTERNA) ---
def lista_productos_api(request):
    url = "https://world.openfoodfacts.org/category/eggs.json"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        raw_products = data.get('products', [])
        
        productos_limpios = []
        for p in raw_products[:12]:
            productos_limpios.append({
                'id': p.get('_id'),
                'nombre': p.get('product_name', 'Producto sin nombre'),
                'marca': p.get('brands', 'Genérico'),
                'imagen': p.get('image_url', ''),
                'cantidad': p.get('quantity', 'N/A'),
            })
    except Exception as e:
        productos_limpios = []
    
    return render(request, 'produccion/lista_productos.html', {'productos': productos_limpios})

# --- CREACIÓN (API LOCAL) ---
def crear_producto_api(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            datos = {
                "nombre": form.cleaned_data['nombre'],
                "unidad_medida": form.cleaned_data['unidad_medida'],
                "fecha_siembra": str(form.cleaned_data['fecha_siembra']),
            }
            archivos = {'imagen': request.FILES['imagen']} if 'imagen' in request.FILES else None
            
            try:
                response = requests.post(API_URL_LOCAL, data=datos, files=archivos)
                if response.status_code == 201:
                    messages.success(request, "Producto creado en la API con éxito.")
                    return redirect('admin_dashboard') # Volver al panel
                else:
                    form.add_error(None, f"Error API: {response.status_code}")
            except:
                form.add_error(None, "No se pudo conectar con el servidor de la API.")
    else:
        form = ProductoForm()
    
    return render(request, 'produccion/producto_form.html', {'form': form, 'titulo': 'Nuevo Producto (vía API)'})

# --- ELIMINACIÓN (API LOCAL) ---
def eliminar_producto_api(request, pk):
    if request.method == 'POST':
        try:
            # Enviamos la petición DELETE a la URL de la API con el ID
            response = requests.delete(f"{API_URL_LOCAL}{pk}/")
            if response.status_code in [200, 204]:
                messages.warning(request, "Producto eliminado de la API.")
            else:
                messages.error(request, "La API no permitió eliminar el producto.")
        except:
            messages.error(request, "Error de conexión con la API.")
        
        return redirect('admin_dashboard')
    
    # Si es GET, podrías mostrar un mini template de confirmación
    return render(request, 'produccion/producto_confirm_delete.html', {'pk': pk})

def lista_produccion(request):
    producciones = ProduccionHuevos.objects.all()
    return render(request, 'produccion/lista.html', {'producciones': producciones})


def crear_produccion(request):
    if request.method == 'POST':
        form = ProduccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_produccion')
    else:
        form = ProduccionForm()
    return render(request, 'produccion/crear.html', {'form': form, 'titulo': 'Nueva Producción'})

def editar_produccion(request, pk):
    produccion = get_object_or_404(ProduccionHuevos, pk=pk)
    if request.method == 'POST':
        form = ProduccionForm(request.POST, instance=produccion)
        if form.is_valid():
            form.save()
            return redirect('lista_produccion')
    else:
        form = ProduccionForm(instance=produccion)
    return render(request, 'produccion/crear.html', {'form': form, 'titulo': 'Editar Producción'})


def eliminar_produccion(request, pk):
    produccion = get_object_or_404(ProduccionHuevos, pk=pk)
    if request.method == 'POST':
        produccion.delete()
        return redirect('lista_produccion')
    return render(request, 'produccion/confirmar_eliminar.html', {
        'produccion': produccion
    })




def pdf_produccion(request):
    producciones = ProduccionHuevos.objects.all()
    template = get_template('produccion/pdf_produccion.html')
    html = template.render({'producciones': producciones})
    
    # Creamos un "buffer" en memoria para guardar el PDF
    result = BytesIO()
    
    # Convertimos el HTML en PDF
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    # Si no hubo errores, enviamos el PDF al navegador
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    
    return HttpResponse('Error al generar el PDF', status=400)

