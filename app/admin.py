from django.contrib import admin
from .models import Categoria, Producto, Compra, ProductoCompra, Usuario, Marca


# Register your models here.
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Usuario)
admin.site.register(Compra)
admin.site.register(ProductoCompra)
admin.site.register(Marca)
