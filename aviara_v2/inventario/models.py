from django.db import models
from django.conf import settings
from produccion.models import validar_fecha_no_pasada
from django.core.validators import MinValueValidator
# Usamos strings para las relaciones para evitar errores de importación circular
# 'produccion.ProduccionHuevos' y 'produccion.ProductoAgricola'

class StockHuevo(models.Model):
    produccion = models.OneToOneField('produccion.ProduccionHuevos', on_delete=models.CASCADE)
    cantidad_disponible = models.PositiveIntegerField()
    fecha_vencimiento = models.DateField(validators=[validar_fecha_no_pasada])

    def __str__(self):
        return f"Stock {self.produccion}"

class StockAgricola(models.Model):
    producto = models.ForeignKey('produccion.ProductoAgricola', on_delete=models.CASCADE)
    cantidad_disponible = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0, message="El stock no puede ser negativo.")])
    fecha_cosecha = models.DateField()
    fecha_vencimiento = models.DateField()

    def __str__(self):
        return f"Stock {self.producto.nombre}"

class HistorialMovimiento(models.Model):
    TIPOS = (('entrada', 'Entrada'), ('salida', 'Salida/Venta'), ('ajuste', 'Ajuste'))
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_movimiento = models.CharField(max_length=10, choices=TIPOS)
    producto_nombre = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(blank=True)