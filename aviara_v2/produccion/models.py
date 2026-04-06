from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


def validar_fecha_no_pasada(value):
    if value < timezone.now().date():
        raise ValidationError("La fecha no puede ser anterior a la de hoy.")

class LoteAves(models.Model):
    codigo_lote = models.CharField(max_length=20, unique=True)
    fecha_ingreso = models.DateField()
    cantidad_inicial = models.PositiveIntegerField()
    raza = models.CharField(max_length=50)
    mortalidad_acumulada = models.PositiveIntegerField(default=0)
    estado = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='lotes/', null=True, blank=True)

    def __str__(self):
        return self.codigo_lote

class ProduccionHuevos(models.Model):
    CLASIFICACION = (('AAA', 'Triple A'), ('AA', 'Doble A'), ('A', 'A'), ('B', 'B'))
    lote = models.ForeignKey(LoteAves, on_delete=models.CASCADE, related_name='recolecciones')
    fecha_recoleccion = models.DateTimeField(default=timezone.now)
    cantidad_total = models.PositiveIntegerField()
    clasificacion = models.CharField(max_length=5, choices=CLASIFICACION)

    def __str__(self):
        return f"{self.clasificacion} - {self.lote.codigo_lote}"

    def save(self, *args, **kwargs):
        nuevo_registro = self.pk is None
        super().save(*args, **kwargs)
        if nuevo_registro:
            from inventario.models import StockHuevo, HistorialMovimiento
            vencimiento = self.fecha_recoleccion.date() + timedelta(days=30)
            StockHuevo.objects.create(
                produccion=self,
                cantidad_disponible=self.cantidad_total,
                fecha_vencimiento=vencimiento
            )
            HistorialMovimiento.objects.create(
                tipo_movimiento='entrada',
                producto_nombre=f"Huevo {self.clasificacion} (Lote {self.lote.codigo_lote})",
                cantidad=self.cantidad_total,
                observacion="Entrada automática por registro de producción."
            )

class ProductoAgricola(models.Model):
    nombre = models.CharField(max_length=100)
    unidad_medida = models.CharField(max_length=20)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    fecha_siembra = models.DateField(validators=[validar_fecha_no_pasada])

    def __str__(self):
        return self.nombre

