from productos.models import VariacionProducto

class Carrito:
    def __init__(self,request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            carrito = self.session["carrito"] = {}
        self.carrito = carrito
    
    def agregar(self, variacion):
        variacion_id = str(variacion.id)

        if variacion_id not in self.carrito.keys():
            self.carrito[variacion_id] = {
                "variacion_id": variacion.id,
                "nombre": f"{variacion.producto.nombre} ({variacion.presentacion})",
                "precio": int(variacion.precio),
                "cantidad": 1,
                "total": int(variacion.precio),
                "imagen": variacion.producto.imagen.url if variacion.producto.imagen else ""
            }
        else:
            self.carrito[variacion_id]["cantidad"] += 1
            self.carrito[variacion_id]["total"] = (
                self.carrito[variacion_id]["precio"] * self.carrito[variacion_id]["cantidad"]
            )

        self.guardar_carrito()
    
    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified=True

    def eliminar(self, variacion):
        variacion_id = str(variacion.id)
        if variacion_id in self.carrito:
            del self.carrito[variacion_id]
            self.guardar_carrito()
    
    def restar(self, variacion):
        variacion_id = str(variacion.id)
        if variacion_id in self.carrito:
            self.carrito[variacion_id]["cantidad"] -=1
            if self.carrito[variacion_id]["cantidad"] < 1:
                self.eliminar(variacion)
            else:
                self.carrito[variacion_id]["total"] = str (
                    int(self.carrito[variacion_id]["precio"]) * self.carrito[variacion_id]["cantidad"]
                )
            self.guardar_carrito()
    
    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True
