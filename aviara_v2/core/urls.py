"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from usuarios import views as usuarios_views
from ventas import views as ventas_views
from inventario import views as inventario_views
from django.conf import settings
from django.conf.urls.static import static
from produccion import views as produccion_views
from produccion import views as produccion_views
from pedidos import views as pedidos_views
 
urlpatterns = [
    # 1. Administración nativa y Autenticación
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    # 2. Módulo de Usuarios (Dashboard, Registro y Redirección)
    path('panel/', usuarios_views.admin_dashboard, name='dashboard'),
    path('registro/', usuarios_views.registro_view, name='registro'),
    # CORRECCIÓN: Usamos usuarios_views para encontrar la función
    path('check-auth/', usuarios_views.redireccion_segun_rol, name='redireccion_rol'),

    # 3. Página Principal (Home)
    path('', ventas_views.home_view, name='home'),
    path('produccion/', produccion_views.lista_produccion, name='lista_produccion'),


    # 4. Reportes y PDF
    path('exportar-pdf/', inventario_views.exportar_inventario_pdf, name='exportar_pdf'),
    path('produccion/pdf/', produccion_views.pdf_produccion, name='pdf_produccion'),

    # 5. Inclusión de módulos (Apps)
    path('inventario/', include('inventario.urls')),
    path('ventas/', include('ventas.urls')),
    path('catalogo/', include('productos.urls')), 
    path('carrito/', include('carrito.urls')),
    path('produccion/', include('produccion.urls')),
    path('pedidos/', include('pedidos.urls')),

]

# Configuración para servir archivos multimedia (Imágenes de productos)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
