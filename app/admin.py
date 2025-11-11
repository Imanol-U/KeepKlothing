from django.contrib import admin
from .models import Categoria, Producto, Compra, ProductoCompra, Usuario


# Register your models here.
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Usuario)
admin.site.register(Compra)
admin.site.register(ProductoCompra)
