from django.db import models

class Producto(models.Model):
    CATEGORIAS_CHOICES = [
        ('HUEVOS', 'Huevos y Derivados'),
        ('POLLO', 'Pollo y Carnes Blancas'),
        ('VEG', 'Vegetales y Frutas'),
        ('LACTEOS', 'Lácteos y Derivados'),
        ('TUBERCULOS', 'Tubérculos'),
        ('GRANOS', 'Granos y Harinas'),
    ]
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Producto")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    categoria = models.CharField(
        max_length=10,
        choices= CATEGORIAS_CHOICES,
        default= 'HUEVOS'
    )
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    es_organico = models.BooleanField(default=False, verbose_name="¿Es orgánico?")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name= "Producto"
        verbose_name_plural = "Productos"
    
    def __str__(self):
        return f"{self.nombre} [{self.get_categoria_display()}]"

class VariacionProducto(models.Model):
    UNIDADES_MEDIDA = [
        ('UN', 'Unidad'),
        ('LT', 'Litro'),
        ('KG', 'Kilogramo'),
        ('LB', 'Libra'),
        ('AT', 'Atado'),
        ('CB', 'Cubeta(30 unds)'),
        ('CN', 'Canasta'),
        ('PQ', 'Paquete'),
        ('ML', 'Mililitro'),
        ('G', 'Gramos')
    ]
    producto = models.ForeignKey(
        Producto,
        related_name='variaciones',
        on_delete=models.CASCADE
    )
    presentacion = models.CharField(
        max_length=50,
       help_text="Ej: Bloque 500g, Bolsa 1 Litro, Atado Pequeño"
    )
    unidad_medida = models.CharField(
        max_length=2,
        choices=UNIDADES_MEDIDA,
        default='UN'
    )
    precio = models.PositiveIntegerField(verbose_name="Precio de venta (COP)")
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name="Variación de Producto"
        verbose_name_plural = "Variaciones de Productos"
    def __str__(self):
        return f"{self.producto.nombre} - {self.presentacion} (${self.precio})"
