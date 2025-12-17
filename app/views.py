from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Sum, Avg
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
from .models import Producto, ProductoCompra, Categoria, Usuario, Marca, Resenia, Compra
from .models import Producto, ProductoCompra, Categoria, Usuario, Marca, Resenia
from .forms import ReviewForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


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
        ).order_by('-total_vendido')[:4]
        
    productos_mas_vendidos_total = ProductoCompra.objects.values(
            'producto__id_producto',
            'producto__nombre',
            'producto__imagen_url',
            'producto__precio'
        ).annotate(
            total_vendido=Sum('cantidad')
        ).order_by('-total_vendido')[:4]
    
    context = {
            'productos_tendencia': top_productos_tendencia,
            'mas_vendidos' : productos_mas_vendidos_total,
        }

    return render(request, "home.html", context)

def filters(request, nombre_categoria):
    categoria = get_object_or_404(Categoria, nombre = nombre_categoria)
    lista_productos = categoria.productos.all()  # Aqui uso el related name "productos" de la relacion Categoria-Producto
    context = {
        'categoria': categoria,
        'productos': lista_productos
    }
    return render(request, 'productFilter.html', context)

def producto_detalle(request, id_producto):
    producto = get_object_or_404(Producto, pk=id_producto)

    #Detectar AJAX correctamente
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' 

    default_user = Usuario.objects.get(pk= 2)
    review_exists = Resenia.objects.filter(usuario=default_user, producto=producto).exists()

    if request.method == 'POST':
        # --- Manejo de caso donde la reseña ya existe ---
        if review_exists:
            if is_ajax:
                return JsonResponse({'success': False, 'message': 'Solo puedes dejar una reseña por producto.'}, status=400)
            else:
                return redirect('producto_detalle', id_producto=producto.pk)
        
        # --- Manejo de la nueva reseña ---
        else:
            form = ReviewForm(request.POST)
            if form.is_valid():
                
                # LA LÓGICA DEL GUARDADO DEBE IR AQUÍ (antes del if is_ajax)
                resenia = form.save(commit=False)
                resenia.producto = producto
                resenia.usuario = default_user 
                resenia.save()
                
                if is_ajax:
                    # Respuesta AJAX (201 Created)
                    return JsonResponse({
                        'success': True,
                        'comentario': resenia.comentario, 
                        'usuario_nombre': default_user.nombre,
                        'fecha_resenia' : resenia.fecha_resenia.strftime('%d/%m/%Y %H:%M'),
                        'estrellas' : resenia.estrellas
                        #importante poner los mismos nombres aquí que luego en los datos del form de ajax
                    }, status=201)
                else:
                    # Respuesta Sincrónica (Redirección, que queremos evitar con AJAX)
                    return redirect('producto_detalle', id_producto=producto.pk)
            
            # Manejo de formulario inválido
            else:
                if is_ajax:
                    return JsonResponse({'success': False, 'errors': form.errors}, status=400)
                # Si no es AJAX, el código caerá al render.

    # ... (resto del código GET) ...
    
    resenias = producto.resenias.select_related("usuario").all()
    rating_medio = resenias.aggregate(Avg("estrellas"))["estrellas__avg"]

    context = {
        "producto": producto,
        "resenias": resenias,
        "rating_medio": rating_medio,
        "form": form if 'form' in locals() else ReviewForm(), # Usa la instancia del formulario
        "allowReview" : not review_exists
    }
    return render(request, "productDetails.html", context)

def eliminar_resenia(request, id_resenia):  #Vista para eliminar una reseña concreta
    resenia = get_object_or_404(Resenia, pk=id_resenia)  #Busca la reseña por su id y si no existe, devuelve error 404
    usuario_defecto = Usuario.objects.get(pk=2) 

    if resenia.usuario != usuario_defecto:
        messages.error(request, "No puedes borrar esta reseña")
        return redirect("producto_detalle", id_producto=resenia.producto.id_producto)

    if request.method == "POST":   # Solo queremos borrar si llega una petición POST 
        id_producto = resenia.producto.id_producto  #Guarda el id del producto asocioado a la reseña y luego te sirve para volver a la ficha de ese producto
        resenia.delete()  #Elimina la reseña de la base de datos
        messages.success(request, "Reseña eliminada correctamente.")
        return redirect("producto_detalle", id_producto=id_producto) #Redirige a la ficha del producto asociado a la reseña borrada y así se recarga la página sin esa reseña.

    
    return redirect("producto_detalle", id_producto=resenia.producto.id_producto)


def marca_info(request, nombre):
    marca = get_object_or_404(Marca,nombre = nombre)
    productos = marca.productos.all()

    context = {"marca": marca,
               "productos" : productos}

    return render(request, "marcaInfo.html", context)

def carrito(request):
    return render(request, "cart.html")

@csrf_exempt
def tramitar_pedido(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)
    
    data = json.loads(request.body)
    cart = data.get('cart', [])
    
    if not cart:
        return JsonResponse({'success': False, 'message': 'El carrito está vacío'})

    usuario = Usuario.objects.get(pk=2) 

    with transaction.atomic():
        total_compra = 0
        item_details = []
        
        for item in cart:
            try:
                producto = Producto.objects.select_for_update().get(pk=item['id'])
            except Producto.DoesNotExist:
                return JsonResponse({'success': False, 'message': f"Producto ID {item['id']} no encontrado"})
            
            cantidad = int(item['quantity'])
            
            producto.stock -= cantidad
            producto.save()
            subtotal = producto.precio * cantidad
            total_compra += subtotal
            
            item_details.append({
                'producto': producto,
                'cantidad': cantidad,
                'precio_unitario': producto.precio
            })

        #Creamos compra en la base de datos
        compra = Compra.objects.create(
            usuario=usuario,
            total=total_compra,
            estado='pendiente',
            metodo_pago='tarjeta'
        )

        #Creamos detalles de compra en la base de datos
        for detail in item_details:
            ProductoCompra.objects.create(
                compra=compra,
                producto=detail['producto'],
                cantidad=detail['cantidad'],
                precio_unitario=detail['precio_unitario']
            )
    return JsonResponse({'success': True, 'message': '¡Compra realizada con éxito!'})

@login_required
def profile(request):
    # Aquí en el futuro cargarás los pedidos reales de la base de datos
    # orders = Order.objects.filter(user=request.user)
    return render(request, 'profile.html')

def olvidar_contrasena(request):
    ctx = {}

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        p1 = request.POST.get("password1", "")
        p2 = request.POST.get("password2", "")

        if not username or not p1 or not p2:
            ctx["error"] = "Rellena todos los campos."
            return render(request, "olvidarContrasena.html", ctx)

        if p1 != p2:
            ctx["error"] = "Las contraseñas no coinciden."
            return render(request, "olvidarContrasena.html", ctx)

        if len(p1) < 6:
            ctx["error"] = "La contraseña debe tener al menos 6 caracteres."
            return render(request, "olvidarContrasena.html", ctx)

        # 1) Intentar actualizar tu tabla USUARIO por email
        usuario = Usuario.objects.filter(email__iexact=username).first()
        if usuario:
            usuario.password_hash = make_password(p1)
            usuario.save(update_fields=["password_hash"])
            ctx["success"] = "Contraseña actualizada (tabla USUARIO). Ya puedes iniciar sesión."
            return render(request, "olvidarContrasena.html", ctx)

        # 2) (Opcional) si no existe en USUARIO, intentar en auth_user por username o email
        django_user = User.objects.filter(username=username).first() or User.objects.filter(email__iexact=username).first()
        if django_user:
            django_user.set_password(p1)
            django_user.save(update_fields=["password"])
            ctx["success"] = "Contraseña actualizada correctamente."
            return render(request, "olvidarContrasena.html", ctx)

        ctx["error"] = "No encuentro ese usuario (ni en USUARIO ni en Django)."

    return render(request, "olvidarContrasena.html", ctx)