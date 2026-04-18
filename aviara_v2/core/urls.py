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
from django.contrib.auth import views as auth_views
from usuarios import views as usuarios_views
from inventario import views as inventario_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- Autenticación (Login, Logout, Registro) ---
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('salir/', usuarios_views.salir, name='logout'),
    path('registro/', usuarios_views.registro_view, name='registro'),

    # --- Recuperación de Contraseña (Recuperado) ---
    # 1. Formulario inicial para pedir el reset
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"), 
         name="reset_password"),

    # 2. Confirmación de envío de correo
    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), 
         name="password_reset_done"),

    # 3. El enlace que llega al correo (validación de token)
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), 
         name="password_reset_confirm"),

    # 4. Mensaje de éxito tras cambiar la clave
    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), 
         name="password_reset_complete"),

    # --- El Dashboard (Punto de entrada principal) ---
    # Aquí es donde ocurre la redirección de roles que hizo tu compañera
    path('', usuarios_views.dashboard, name='home'),
    path('panel/', usuarios_views.dashboard), 

    # --- Aplicaciones (Modularizadas) ---
    path('inventario/', include('inventario.urls')),
    path('productos/', include('productos.urls')),
    path('ventas/', include('ventas.urls')),
    path('produccion/', include('produccion.urls')),
    path('carrito/', include('carrito.urls')),
    

    # --- Reportes Globales ---
    path('exportar-pdf/', inventario_views.exportar_inventario_pdf, name='exportar_pdf'),

]

# Configuración para archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)