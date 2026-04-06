from django.shortcuts import render
from productos.models import Producto

def home_view(request):
    """ Página de aterrizaje para clientes """
    return render(request, 'home.html')

def catalogo_productos(request):
    """ Vista del catálogo con el carrito que armamos antes """
    productos_db = Producto.objects.all()
    return render(request, 'productos/catalogo.html', {'productos': productos_db})