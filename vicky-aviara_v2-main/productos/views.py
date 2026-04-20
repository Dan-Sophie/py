import requests
from django.shortcuts import render, redirect
from .models import Producto

# Nueva API: Trae categorías de comida (Pollo, Carne, Vegetales, etc.)
FOOD_API_URL = "https://www.themealdb.com/api/json/v1/1/categories.php"

# CLIENTE: Se queda igual (Base de datos local)
def lista_productos_api(request):
    productos_locales = Producto.objects.all()
    return render(request, 'productos/lista_productos.html', {'productos': productos_locales})

# ADMIN: Ahora con comida real
def admin_productos_api(request):
    try:
        response = requests.get(FOOD_API_URL, timeout=5)
        data = response.json()
        # La API de comida guarda la lista en 'categories'
        productos_externos = data.get('categories', [])
    except:
        productos_externos = []
        
    return render(request, 'productos/lista_productos_api.html', {
        'productos': productos_externos,
        'es_comida': True
    })

# Esta función DEBE existir para que no te dé el AttributeError en las URLs
def crear_producto_api(request):
    return render(request, 'productos/lista_productos_api.html')

def catalogo_local(request):
    productos_locales = Producto.objects.all()
    # Cambiamos el nombre del template aquí:
    return render(request, 'productos/tienda_virtual.html', {
        'productos': productos_locales
    })

def tienda_virtual_view(request):
    # Traemos los productos con sus variaciones para evitar muchas consultas a la BD
    productos_locales = Producto.objects.all().prefetch_related('variaciones')
    return render(request, 'productos/tienda_virtual.html', {
        'productos': productos_locales
    })