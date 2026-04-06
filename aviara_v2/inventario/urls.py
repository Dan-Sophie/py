from django.urls import path
from .import views

urlpatterns =[
    # Lectura: Lista completa de suministros y huevos
    path('lista/', views.lista_inventario, name='inventario_list'),

    # Creación: Formulario para nuevo suministro agrícola
    path('nuevo/', views.crear_suministro, name='crear_suministro'),

    # Actualización: Editar un suministro específico usando su ID (pk)
    path('editar/<int:pk>/', views.editar_suministro, name='editar_suministro'),

    # Borrado: Eliminar un suministro específico
    path('eliminar/<int:pk>/', views.eliminar_suministro, name='eliminar_suministro'),
]