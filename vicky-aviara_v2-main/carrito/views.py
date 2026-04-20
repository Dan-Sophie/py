from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from productos.models import VariacionProducto
from datetime import datetime
from ventas.models import Pedido, ItemPedido

def agregar_carrito(request):
    if request.method == 'POST':
        var_id = request.POST.get('id')
        cantidad = int(request.POST.get('cantidad', 1))

        variacion = get_object_or_404(VariacionProducto, id=var_id)

        carrito = request.session.get('carrito', {})

        if var_id in carrito:
            carrito[var_id]['cantidad'] += cantidad
        else:
            carrito[var_id] = {
                'nombre': f"{variacion.producto.nombre} - {variacion.presentacion}",
                'precio': float(variacion.precio),
                'cantidad': cantidad
            }

        request.session['carrito'] = carrito
        request.session.modified = True

        return JsonResponse({'ok': True})


def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())

    return render(request, 'carrito.html', {
        'carrito': carrito,
        'total': total
    })


def eliminar_producto(request, producto_id):
    carrito = request.session.get('carrito', {})

    if producto_id in carrito:
        del carrito[producto_id]

    request.session['carrito'] = carrito
    request.session.modified = True

    return redirect('ver_carrito')


def actualizar_cantidad(request):
    if request.method == 'POST':
        producto_id = request.POST.get('id')
        accion = request.POST.get('accion')
        carrito = request.session.get('carrito', {})

        nuevo_subtotal = 0
        total_carrito = 0

        if producto_id in carrito:
            if accion == 'sumar':
                carrito[producto_id]['cantidad'] += 1
            elif accion == 'restar':
                carrito[producto_id]['cantidad'] -= 1
                if carrito[producto_id]['cantidad'] <= 0:
                    # Si llega a cero, podrías manejarlo para borrar el item
                    del carrito[producto_id]
            
            # Recalculamos el subtotal del producto si aún existe
            if producto_id in carrito:
                nuevo_subtotal = carrito[producto_id]['cantidad'] * carrito[producto_id]['precio']

        # Calculamos el total general de nuevo
        total_carrito = sum(item['precio'] * item['cantidad'] for item in carrito.values())

        request.session['carrito'] = carrito
        request.session.modified = True

        return JsonResponse({
            'ok': True,
            'nuevo_subtotal': nuevo_subtotal,
            'total_carrito': total_carrito,
            'cantidad': carrito[producto_id]['cantidad']
        })


def vaciar_carrito(request):
    request.session['carrito'] = {}
    request.session.modified = True
    return redirect('ver_carrito')

def finalizar_compra(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('ver_carrito')
    
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    
    if request.method == 'POST':
        # 1. Creamos el objeto Pedido principal
        nuevo_pedido = Pedido.objects.create(
            cliente=request.user,
            estado='pagado', # O 'pendiente' según tu flujo
            completado=True
        )

        # 2. Pasamos cada item del carrito a la base de datos (ItemPedido)
        for var_id, datos in carrito.items():
            variacion = VariacionProducto.objects.get(id=var_id)
            ItemPedido.objects.create(
                pedido=nuevo_pedido,
                variacion=variacion,
                cantidad=datos['cantidad'],
                precio_en_momento_venta=datos['precio']
            )
            
            # NOTA: Aquí podrías crear también el 'DetallePedido' si 
            # necesitas que se ejecute tu lógica de descuento de stock.

        # 3. Vaciamos el carrito
        request.session['carrito'] = {}
        request.session.modified = True
        
        return render(request, 'factura_exitosa.html', {
            'pedido': nuevo_pedido,
            'total': total
        })

    return render(request, 'confirmar_pedido.html', {'carrito': carrito, 'total': total})