from django.urls import path
from . import views

app_name= "carrito"

urlpatterns = [
    path("agregar/<int:variacion_id>/", views.agregar_producto, name="agregar"),
    path("eliminar/<int:variacion_id>/", views.eliminar_producto, name="eliminar"),
    path("restar/<int:variacion_id>/", views.restar_producto, name="restar"),
    path("limpiar/<int:variacion_id>/", views.limpiar_carrito, name="limpiar"),
    path("mi-carrito/", views.ver_carrito, name="ver_carrito"),
    path("procesar/", views.procesar_pedido, name='procesar_pedido'),
]