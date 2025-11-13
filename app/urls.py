from django.urls import path
from . import views

urlpatterns = [
    # Aquí van las urls que vamos a asignar a las views de la app.
    path('', views.home, name="home"),
    path('filters/<str:nombre_categoria>', views.filters, name="filters")
]