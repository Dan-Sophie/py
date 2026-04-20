from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.db import transaction


def validar_fecha_no_pasada(value):
    if value < timezone.now().date():
        raise ValidationError("La fecha no puede ser anterior a la de hoy.")

class LoteAves(models.Model):
    # Definimos las razas más comunes para que aparezcan en una lista
    class RazaAves(models.TextChoices):
        ROSS = 'ROSS', 'Ross 308 (Carne)'
        COBB = 'COBB', 'Cobb 500 (Carne)'
        ISA_BROWN = 'ISA', 'Isa Brown (Ponedora)'
        HY_LINE = 'HYL', 'Hy-Line (Ponedora)'
        OTRA = 'OTRA', 'Otra Raza'

    codigo_lote = models.CharField(max_length=20, help_text="Ej: LOTE-2026-001")
    fecha_ingreso = models.DateField(default=timezone.now)
    cantidad_inicial = models.PositiveIntegerField(verbose_name="Pollos recibidos")
    
    # Ahora 'raza' es una lista desplegable
    raza = models.CharField(
        max_length=50, 
        choices=RazaAves.choices, 
        default=RazaAves.ROSS
    )
    
    mortalidad_acumulada = models.PositiveIntegerField(
        default=0, 
        help_text="Total de aves muertas a la fecha"
    )
    estado = models.BooleanField(default=True, verbose_name="Lote Activo")
    imagen = models.ImageField(upload_to='lotes/', null=True, blank=True)

    @property
    def aves_vivas(self):
        """Calcula automáticamente cuántas aves quedan"""
        return self.cantidad_inicial - self.mortalidad_acumulada

    def __str__(self):
        return f"{self.codigo_lote} - {self.get_raza_display()}"


class ProduccionHuevos(models.Model):
    class Clasificacion(models.TextChoices):
        TRIPLE_A = 'AAA', 'Triple A'
        DOBLE_A = 'AA', 'Doble A'
        A = 'A', 'A'
        B = 'B', 'B'

    # Relaciones
    lote = models.ForeignKey(
        'LoteAves', 
        on_delete=models.CASCADE, 
        related_name='recolecciones',
        verbose_name="Lote de Aves"
    )
    # Vinculamos a la Variación para que el catálogo se actualice de una
    variacion_objetivo = models.ForeignKey(
        'productos.VariacionProducto', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Producto/Presentación en Tienda",
        help_text="Seleccione qué producto del catálogo recibirá este stock"
    )

    # Datos de producción
    fecha_recoleccion = models.DateTimeField(default=timezone.now)
    cantidad_total = models.PositiveIntegerField(verbose_name="Cantidad (Unidades)")
    clasificacion = models.CharField(max_length=5, choices=Clasificacion.choices)

    class Meta:
        verbose_name = "Producción de Huevo"
        verbose_name_plural = "Producción de Huevos"

    def __str__(self):
        return f"{self.get_clasificacion_display()} - {self.lote.codigo_lote} ({self.fecha_recoleccion.date()})"

    def registrar_flujo_inventario(self):
        """Lógica para conectar Producción con el Inventario y la Tienda"""
        from inventario.models import StockHuevo, HistorialMovimiento
        
        # 1. Calculamos vencimiento
        vencimiento = self.fecha_recoleccion.date() + timedelta(days=30)
        
        # 2. Creamos el registro de Stock técnico
        StockHuevo.objects.create(
            produccion=self,
            cantidad_disponible=self.cantidad_total,
            fecha_vencimiento=vencimiento
        )
        
        # 3. ACTUALIZAMOS EL STOCK DE LA TIENDA (Lo que la profe quiere ver)
        if self.variacion_objetivo:
            # Asumiendo que tu modelo VariacionProducto tiene un campo 'stock'
            # Si no lo tiene, este paso asegura que al menos exista la relación
            self.variacion_objetivo.stock = (self.variacion_objetivo.stock or 0) + self.cantidad_total
            self.variacion_objetivo.save()

        # 4. Historial para auditoría
        HistorialMovimiento.objects.create(
            tipo_movimiento='entrada',
            producto_nombre=f"Huevo {self.get_clasificacion_display()} - Lote {self.lote.codigo_lote}",
            cantidad=self.cantidad_total,
            observacion=f"Producción vinculada a: {self.variacion_objetivo}" if self.variacion_objetivo else "Entrada sin producto asignado"
        )

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None
        # Usamos transaction para asegurar que si algo falla, no se guarde nada a medias
        with transaction.atomic():
            super().save(*args, **kwargs)
            if es_nuevo:
                self.registrar_flujo_inventario()

class ProductoAgricola(models.Model):
    nombre = models.CharField(max_length=100)
    unidad_medida = models.CharField(max_length=20)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    fecha_siembra = models.DateField(validators=[validar_fecha_no_pasada])

    def __str__(self):
        return self.nombre

