from django.urls import path
from .import views

urlpatterns =[
    # Producción de Huevos
    path('produccion/', views.lista_produccion, name='lista_produccion'),
    path('produccion/nuevo/', views.crear_produccion, name='crear_produccion'),
    path('produccion/editar/<int:pk>/', views.editar_produccion, name='editar_produccion'),
    path('produccion/eliminar/<int:pk>/', views.eliminar_produccion, name='eliminar_produccion'), 

    # Productos vía API
    path('catalogo/', views.lista_productos_api, name='lista_productos'),
    path('nuevo/', views.crear_producto_api, name='crear_producto'),
    path('eliminar/<str:pk>/', views.eliminar_producto_api, name='eliminar_producto'),



    path('pdf/', views.pdf_produccion, name='pdf_produccion'), 
]