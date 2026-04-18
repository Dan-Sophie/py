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
    # 1. Definición de constantes fuera de la clase para limpieza
    class Clasificacion(models.TextChoices):
        TRIPLE_A = 'AAA', 'Triple A'
        DOBLE_A = 'AA', 'Doble A'
        A = 'A', 'A'
        B = 'B', 'B'

    # 2. Campos del modelo
    lote = models.ForeignKey(
        'LoteAves', 
        on_delete=models.CASCADE, 
        related_name='recolecciones',
        verbose_name="Lote de Origen"
    )
    fecha_recoleccion = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Recolección"
    )
    cantidad_total = models.PositiveIntegerField(verbose_name="Cantidad Recolectada")
    clasificacion = models.CharField(
        max_length=5, 
        choices=Clasificacion.choices,
        verbose_name="Clasificación del Huevo"
    )

    class Meta:
        verbose_name = "Producción de Huevo"
        verbose_name_plural = "Producciones de Huevos"
        ordering = ['-fecha_recoleccion']

    def __str__(self):
        return f"{self.get_clasificacion_display()} - Lote: {self.lote.codigo_lote}"

    # 3. Lógica de negocio (Refactorizada)
    def registrar_en_inventario(self):
        """Encapsula la lógica de inventario en un método separado"""
        from inventario.models import StockHuevo, HistorialMovimiento
        
        vencimiento = self.fecha_recoleccion.date() + timedelta(days=30)
        
        # Crear el stock
        StockHuevo.objects.create(
            produccion=self,
            cantidad_disponible=self.cantidad_total,
            fecha_vencimiento=vencimiento
        )
        
        # Registrar el historial
        HistorialMovimiento.objects.create(
            tipo_movimiento='entrada',
            producto_nombre=f"Huevo {self.get_clasificacion_display()} (Lote {self.lote.codigo_lote})",
            cantidad=self.cantidad_total,
            observacion="Entrada automática por registro de producción."
        )

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None
        super().save(*args, **kwargs)
        if es_nuevo:
            self.registrar_en_inventario()

class ProductoAgricola(models.Model):
    nombre = models.CharField(max_length=100)
    unidad_medida = models.CharField(max_length=20)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    fecha_siembra = models.DateField(validators=[validar_fecha_no_pasada])

    def __str__(self):
        return self.nombre

