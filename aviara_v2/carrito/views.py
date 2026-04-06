from django.shortcuts import redirect, render, get_object_or_404
from productos.models import VariacionProducto
from .carrito import Carrito
from django.contrib.auth.decorators import login_required
from ventas.models import Pedido, ItemPedido 
from django.contrib import messages


# ===== PEDIDO =====
@login_required(login_url='login')
def procesar_pedido(request):
    carrito = Carrito(request)

    if not request.session.get("carrito"):
        messages.warning(request, "Tu carrito está vacío.")
        return redirect("catalogo")

    pedido = Pedido.objects.create(user=request.user)

    for key, value in request.session.get("carrito", {}).items():
        variacion = get_object_or_404(VariacionProducto, id=key)

        ItemPedido.objects.create(
            pedido=pedido,
            user=request.user,
            variacion=variacion,
            cantidad=value["cantidad"],
            precio_unitario=value["precio"]
        )

    carrito.limpiar()

    messages.success(request, "¡Tu pedido en Aviara ha sido recibido con éxito!")
    return redirect("catalogo")


# ===== AGREGAR =====
@login_required(login_url='login')
def agregar_producto(request, variacion_id):
    carrito = Carrito(request)
    variacion = get_object_or_404(VariacionProducto, id=variacion_id)
    carrito.agregar(variacion=variacion)
    if not request.user.is_authenticated:
        return redirect('login')



# ===== ELIMINAR =====
@login_required(login_url='login')
def eliminar_producto(request, variacion_id):
    carrito = Carrito(request)
    variacion = get_object_or_404(VariacionProducto, id=variacion_id)

    carrito.eliminar(variacion=variacion)

    return redirect("carrito:ver_carrito")


# ===== RESTAR =====
@login_required(login_url='login')
def restar_producto(request, variacion_id):
    carrito = Carrito(request)
    variacion = get_object_or_404(VariacionProducto, id=variacion_id)

    carrito.restar(variacion=variacion)

    return redirect("carrito:ver_carrito")


# ===== LIMPIAR =====
@login_required(login_url='login')
def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()

    return redirect("carrito:ver_carrito")


# ===== VER =====
@login_required(login_url='login')
def ver_carrito(request):
    carrito = request.session.get("carrito", {})

    if not carrito:
        messages.info(request, "Tu carrito está vacío.")

    return render(request, 'carrito/ver_carrito.html')