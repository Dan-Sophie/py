from django.urls import path
from . import views

# Si tienes esta línea, bórrala un momento para probar: app_name = 'ventas'

urlpatterns = [
    path('lista/', views.lista_pedidos, name='lista_pedidos'),
    path('nuevo/', views.crear_pedido, name='crear_pedido'),
    path('editar/<int:pk>/', views.editar_pedido, name='editar_pedido'),
    path('eliminar/<int:pk>/', views.eliminar_pedido, name='confirmar_eliminar'),
    path('mis-pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('detalle/<int:pk>/', views.detalle_pedido, name='detalle_pedido'),
]