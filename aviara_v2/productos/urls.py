# productos/urls.py
from django.urls import path
from . import views
# productos/urls.py
urlpatterns = [
    # Cambiamos 'catalogo_usuario' por 'lista_productos'
    path('', views.catalogo_publico, name='lista_productos'), 
    path('procesar-pedido/', views.procesar_pedido, name='procesar_pedido'),
]