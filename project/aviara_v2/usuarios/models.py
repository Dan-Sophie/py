from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self): return self.nombre

class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
        ('cliente', 'Cliente'),
    )
    nombre_completo = models.CharField(max_length=150)
    documento = models.CharField(max_length=30, unique=True)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT, null=True)
    rol = models.CharField(max_length=10, choices=ROLES, default='empleado')
    estado = models.CharField(max_length=10, default='activo')
    
    def save(self, *args, **kwargs):
        if self.is_staff and not self.pk:
            admin_count = Usuario.objects.filter(is_staff=True).count()
            if admin_count >=3:
                raise ValidationError("Límite de administradores alcanzado. Solo se permiten 3.")
        if self.pk:
            old_user = Usuario.objects.get(pk=self.pk)
            if self.is_staff and not old_user.is_staff:
                admin_count = Usuario.objects.filter(is_staff=True).count()
                if admin_count >= 3:
                    raise ValidationError("No se puede promover a administrador. Cupo lleno (máx 3).")
        super().save(*args, **kwargs)