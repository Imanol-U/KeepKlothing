from django.shortcuts import render
from django.db.models import Sum
from django.http import HttpResponse
from .models import Producto, ProductoCompra, Categoria

# Create your views here.

def home(request):
    
    productos_vendidos = ProductoCompra.objects.values('producto__id_producto', 'producto__nombre', 'producto__precio') \
            .annotate(total_vendido=Sum('cantidad')) \
            .order_by('-total_vendido')
            
    top_n = productos_vendidos[:2]

    context = {
            'top_productos': top_n
        }

    return render(request, "home.html", context)

def filters(request, nombre_categoria):
    categoria = Categoria.objects.get(nombre = nombre_categoria)
    lista_productos = categoria.productos.all()  # Aqui uso el related name "productos" de la relacion Categoria-Producto
    context = {
        'categoria': categoria,
        'productos': lista_productos
    }
    return render(request, 'productFilter.html', context)

