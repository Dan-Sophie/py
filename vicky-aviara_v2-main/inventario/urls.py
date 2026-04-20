from django.urls import path
from . import views

urlpatterns = [
    # Ruta principal del inventario
    path('lista/', views.lista_inventario, name='inventario_list'),
    path('lista-alias/', views.lista_inventario, name='lista'), # Para retrocompatibilidad
    
    # CRUD de Huevos
    path('huevos/crear/', views.gestionar_huevos, name='crear_huevos'),
    path('huevos/editar/<int:pk>/', views.gestionar_huevos, name='editar_huevos'),
    
    # CRUD de Agrícola
    path('agricola/crear/', views.gestionar_agricola, name='crear_agricola'),
    path('agricola/editar/<int:pk>/', views.gestionar_agricola, name='editar_agricola'),
    
    # Eliminar (Genérico)
    path('eliminar/<str:tipo>/<int:pk>/', views.eliminar_item, name='eliminar_item'),
    
    # Reportes
    path('exportar-pdf/', views.exportar_inventario_pdf, name='exportar_pdf'),
]