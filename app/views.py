from django.shortcuts import render
from django.db.models import Sum
from django.http import HttpResponse
from .models import Producto, ProductoCompra

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