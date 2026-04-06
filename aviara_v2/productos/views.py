# productos/views.py
from django.shortcuts import render
from .models import Producto
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # Opcional si usas el token correctamente

def catalogo_publico(request):
    # Traemos los productos con sus variaciones (precios) de una vez
    productos_db = Producto.objects.all().prefetch_related('variaciones')
    
    context = {
        'productos': productos_db,
    }
    # Asegúrate de que el archivo esté en esta ruta exacta:
    return render(request, 'productos/catalogo.html', context)


def procesar_pedido(request):
    if request.method == 'POST':
        try:
            # Cargamos los datos del cuerpo de la petición (JSON)
            carrito = json.loads(request.body)
            
            # --- AQUÍ ESTÁ LA MAGIA ---
            # Por ahora, imprimimos en la consola de VS Code / Terminal
            print("\n" + "="*30)
            print("🚀 ¡NUEVO PEDIDO RECIBIDO!")
            print("="*30)
            
            total_general = 0
            for id_v, info in carrito.items():
                subtotal = info['price'] * info['qty']
                total_general += subtotal
                print(f"📦 {info['name']} | Cant: {info['qty']} | Sub: ${subtotal}")
            
            print(f"\n TOTAL DEL PEDIDO: ${total_general}")
            print("="*30 + "\n")

            return JsonResponse({'status': 'success', 'message': 'Pedido recibido'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error'}, status=405)
