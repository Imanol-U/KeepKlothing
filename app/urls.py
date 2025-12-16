from django.urls import path
from . import views

urlpatterns = [
    # Aquí van las urls que vamos a asignar a las views de la app.
    path('', views.home, name="home"),
    path("filters/<str:nombre_categoria>", views.filters, name="filters"),
    path("productos/<int:id_producto>/", views.producto_detalle, name="producto_detalle"),
    path("marca/<str:nombre>", views.marca_info, name="marca"),
    path("carrito/", views.carrito, name="cart"),
    path("api/tramitar-pedido/", views.tramitar_pedido, name="tramitar_pedido"),
    path("resenias/<int:id_resenia>/eliminar/", views.eliminar_resenia, name="eliminar_resenia"),

]