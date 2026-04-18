from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver_carrito, name='ver_carrito'),
    path('agregar/', views.agregar_carrito, name='agregar_carrito'),
    path('eliminar/<str:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('actualizar/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('finalizar/', views.finalizar_compra, name='finalizar_compra'),
]