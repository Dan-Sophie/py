from django.urls import path
from . import views

urlpatterns = [
    path('lista/', views.lista_usuarios, name='lista_usuarios'),
    path('editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
]