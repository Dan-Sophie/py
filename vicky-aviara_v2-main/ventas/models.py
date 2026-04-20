from django.db import models
from django.conf import settings
from inventario.models import StockHuevo, StockAgricola, HistorialMovimiento
from productos.models import VariacionProducto

class Pedido(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado'),
    )
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Cliente")
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='pendiente')
    direccion = models.CharField(max_length=255, default="Bogota")
    completado = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    def get_total_pedido(self):
        try:
            # 1. Obtenemos todos los items relacionados
            items = self.items.all()
            
            # 2. Sumamos asegurándonos de que los valores existan (por si hay nulos)
            total = sum((item.precio_en_momento_venta or 0) * (item.cantidad or 0) for item in items)
            
            return total
        except Exception as e:
            # Si algo falla, devuelve 0 en lugar de romper la página
            return 0
        

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.username}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    variacion = models.ForeignKey(VariacionProducto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_en_momento_venta = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cantidad} x {self.variacion.producto.nombre}"

class DetallePedido(models.Model):
    TIPO_PRODUCTO = (('huevo', 'Huevo'), ('agricola', 'Agrícola'))
    
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    tipo_producto = models.CharField(max_length=10, choices=TIPO_PRODUCTO)
    producto_id = models.PositiveIntegerField(help_text="ID del StockHuevo o StockAgricola")
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        nuevo = self.pk is None
        if nuevo:
            # Lógica para descontar Stock de Huevos
            if self.tipo_producto == 'huevo':
                item_stock = StockHuevo.objects.get(id=self.producto_id)
                if item_stock.cantidad_disponible < self.cantidad:
                    raise ValueError(f"No hay suficiente stock. Disponible: {item_stock.cantidad_disponible}")
                
                item_stock.cantidad_disponible -= int(self.cantidad)
                item_stock.save()
                
                nombre_prod = f"Salida: {item_stock.produccion.clasificacion}"

            # Lógica para descontar Stock Agrícola
            else:
                item_stock = StockAgricola.objects.get(id=self.producto_id)
                if item_stock.cantidad_disponible < self.cantidad:
                    raise ValueError(f"No hay suficiente stock. Disponible: {item_stock.cantidad_disponible}")
                
                item_stock.cantidad_disponible -= self.cantidad
                item_stock.save()
                
                nombre_prod = f"Salida: {item_stock.producto.nombre}"

            # Crear el rastro en el Historial de Movimientos
            HistorialMovimiento.objects.create(
                tipo_movimiento='salida',
                producto_nombre=nombre_prod,
                cantidad=self.cantidad,
                observacion=f"Venta en Pedido #{self.pedido.id}"
            )

        super().save(*args, **kwargs)