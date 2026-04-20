from django.shortcuts import render, redirect, get_object_or_404
from .models import Pedido
from .forms import PedidoForm
from django.contrib.auth.decorators import login_required
from .models import Pedido, ItemPedido

@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user).order_by('-fecha_pedido')
    return render(request, 'lista_pedidos.html', {'pedidos': pedidos})

@login_required
def detalle_pedido(request, pk):
    pedido =get_object_or_404(Pedido, pk=pk, cliente=request.user)
    items = pedido.items.all()
    return render(request, 'detalle_pedido.html', {
        'pedido': pedido,
        'items': items
    })


def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            # CORRECCIÓN: Cambiado 'lista' por 'lista_pedidos'
            return redirect('lista_pedidos')
    else:
        form = PedidoForm()
    return render(request, 'pedidos/crear_pedido.html', {'form': form, 'titulo': 'Nuevo Pedido'})

def editar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            # CORRECCIÓN: Cambiado 'lista' por 'lista_pedidos' para que no salte al inventario
            return redirect('lista_pedidos')
    else:
        form = PedidoForm(instance=pedido)
    return render(request, 'pedidos/crear_pedido.html', {'form': form, 'titulo': 'Editar Pedido'})

def eliminar_pedido(request, pk): 
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        pedido.delete()
        return redirect('lista_pedidos')
    return render(request, 'pedidos/confirmar_eliminar.html', {'pedido': pedido})

