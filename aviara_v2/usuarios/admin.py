from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, TipoDocumento

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin): 
    list_display = ('username', 'nombre_completo', 'documento', 'rol', 'is_staff') 
    list_filter = ('rol', 'is_staff') 
    search_fields = ('username', 'nombre_completo', 'documento')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información de Granja', {'fields': ('nombre_completo', 'documento', 'tipo_documento', 'rol')}),
    )

admin.site.register(TipoDocumento)
