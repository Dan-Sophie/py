from django.urls import path
from . import views

urlpatterns = [
    # --- RUTA DE LA LISTA (Lectura) ---
    path('produccion/lista/', views.lista_produccion, name='produccion_lista'),

    # --- RUTAS DE ACCIÓN (Escritura / CRUD) ---
    path('produccion/crear/', views.crear_produccion, name='crear_produccion'),
    
    # Usamos <int:pk> para que Django sepa qué registro específico editar o borrar
    path('produccion/editar/<int:pk>/', views.editar_produccion, name='editar_produccion'),
    path('produccion/eliminar/<int:pk>/', views.eliminar_produccion, name='eliminar_produccion'),
]