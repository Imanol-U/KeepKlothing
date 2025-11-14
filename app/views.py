from django.shortcuts import render,get_object_or_404
from django.db.models import Sum, Avg
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from .models import Producto, ProductoCompra, Categoria

# Create your views here.

def home(request):

    fecha_hace_30_dias = timezone.now() - timedelta(days=30)

    top_productos_tendencia = ProductoCompra.objects.filter(
            compra__fecha__gte=fecha_hace_30_dias
        ).values(
            'producto__id_producto',
            'producto__nombre',
            'producto__imagen_url',
            'producto__precio' 
        ).annotate(
            total_vendido=Sum('cantidad')
        ).order_by('-total_vendido')[:3]
    
    productos_mas_vendidos_total = ProductoCompra.objects.values(
            'producto__id_producto',
            'producto__nombre',
            'producto__imagen_url',
            'producto__precio'
        ).annotate(
            total_vendido=Sum('cantidad')
        ).order_by('-total_vendido')[:3]
    
    context = {
            'productos_tendencia': top_productos_tendencia,
            'mas_vendidos' : productos_mas_vendidos_total,
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
def producto_detalle(request, id_producto):
    producto = get_object_or_404(Producto, pk=id_producto)

    # Si quieres mostrar reseñas y media de estrellas:
    resenias = producto.resenias.select_related("usuario").all()
    rating_medio = resenias.aggregate(Avg("estrellas"))["estrellas__avg"]

    context = {
        "producto": producto,
        "resenias": resenias,
        "rating_medio": rating_medio,
    }
    return render(request, "productDetails.html", context)
