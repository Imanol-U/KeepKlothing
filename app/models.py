from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from decimal import Decimal



class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150,unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        db_table = "MARCA"

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    password_hash = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "USUARIO"

    def __str__(self):
        return f"{self.nombre} <{self.email}>"

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=120, unique=True)

    class Meta:
        db_table = "CATEGORIA"
        verbose_name_plural = "categorías"

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="productos"
    )
    precio = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))]
    )
    marca = models.ForeignKey(Marca,on_delete= models.PROTECT, related_name="productos")
    stock = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    imagen_url = models.URLField(blank=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "PRODUCTO"

    def __str__(self):
        return self.nombre

class Compra(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("pagada", "Pagada"),
        ("enviado", "Enviado"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
    ]
    METODOS_PAGO = [
        ("tarjeta", "Tarjeta"),
        ("paypal", "PayPal"),
        ("transferencia", "Transferencia"),
        ("contra_reembolso", "Contra reembolso"),
    ]

    id_compra = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name="compras"
    )
    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))]
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO)
    productos = models.ManyToManyField(
        "Producto",
        through="ProductoCompra",
        related_name="compras"
    )

    class Meta:
        db_table = "COMPRA"

    def __str__(self):
        return f"Compra #{self.id_compra} - {self.usuario}"

class ProductoCompra(models.Model):
    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        related_name="lineas"
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name="lineas_compra"
    )
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))]
    )

    class Meta:
        db_table = "PRODUCTO_COMPRA"
        unique_together = (("compra", "producto"),)

    def __str__(self):
        return f"{self.producto} x {self.cantidad} (Compra #{self.compra_id})"

class Resenia(models.Model):
    id_resenia= models.AutoField(primary_key=True)
    usuario= models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        related_name="resenias")
    producto= models.ForeignKey(
        Producto,
        on_delete= models.CASCADE,
        related_name="resenias"
    )
    estrellas= models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    comentario= models.TextField(blank=True)
    fecha_resenia= models.DateTimeField(auto_now_add=True)

    class Meta: 
        db_table= "RESENIA"
        versobe_name_plural = "resenias"
        unique_together= (("usuario", "producto"))
    
    def __str__(self):
        return f"Resenia de {self.usuario.nombre} sobre {self.producto.nombre} ({self.puntuacion}/5)"
 