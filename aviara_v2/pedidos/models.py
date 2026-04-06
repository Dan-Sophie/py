from django.db import models
from django.utils import timezone

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.CharField(max_length=100)
    fecha_pedido = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente}"