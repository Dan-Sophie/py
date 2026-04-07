from django.shortcuts import render, redirect, get_object_or_404
from .models import Pedido
from .forms import PedidoForm

def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedidos/lista_pedidos.html', {'pedidos': pedidos})

def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista')
    else:
        form = PedidoForm()
    return render(request, 'pedidos/crear_pedido.html', {'form': form, 'titulo': 'Nuevo Pedido'})

def editar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('lista')
    else:
        form = PedidoForm(instance=pedido)
    return render(request, 'pedidos/crear_pedido.html', {'form': form, 'titulo': 'Editar Pedido'})

def eliminar_pedido(request, pk): # El nombre 'pk' debe ser igual al de urls.py
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        pedido.delete()
        return redirect('lista_pedidos')
    return render(request, 'pedidos/confirmar_eliminar.html', {'pedido': pedido})