from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from productos.models import VariacionProducto


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


# 🔥 NUEVO: actualizar cantidad
def actualizar_cantidad(request):
    if request.method == 'POST':
        producto_id = request.POST.get('id')
        accion = request.POST.get('accion')

        carrito = request.session.get('carrito', {})

        if producto_id in carrito:
            if accion == 'sumar':
                carrito[producto_id]['cantidad'] += 1
            elif accion == 'restar':
                carrito[producto_id]['cantidad'] -= 1

                if carrito[producto_id]['cantidad'] <= 0:
                    del carrito[producto_id]

        request.session['carrito'] = carrito
        request.session.modified = True

        return JsonResponse({'ok': True})


def vaciar_carrito(request):
    request.session['carrito'] = {}
    request.session.modified = True
    return redirect('ver_carrito')

def finalizar_compra(request):
    request.session['carrito'] = {}
    request.session.modified = True

    return render(request, 'compra_exitosa.html')