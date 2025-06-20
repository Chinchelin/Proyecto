from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=50)
    numero_documento = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    eps = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    correo = models.EmailField(max_length=100, null=True, blank=True)
    antecedentes = models.TextField(null=True, blank=True)
    rol = models.CharField(max_length=30, choices=[
        ('Administrador', 'Administrador'),
        ('Recepcionista', 'Recepcionista'),
        ('Personal de Mantenimiento', 'Personal de Mantenimiento')
    ])
    contrasena = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=[
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo')
    ], default='Activo')

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=50)
    numero_documento = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    antecedentes = models.TextField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    correo = models.EmailField(max_length=100, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

class Habitacion(models.Model):
    numero_habitacion = models.CharField(max_length=10, unique=True)
    tipo_habitacion = models.CharField(max_length=50)
    numero_camas = models.IntegerField()
    capacidad = models.IntegerField()
    descripcion = models.TextField(null=True, blank=True)
    servicios = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=[
        ('Disponible', 'Disponible'),
        ('Ocupada', 'Ocupada'),
        ('Mantenimiento', 'Mantenimiento'),
        ('Limpieza', 'Limpieza')
    ], default='Disponible')
    precio_noche = models.DecimalField(max_digits=10, decimal_places=2)

class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    estado = models.CharField(max_length=20, choices=[
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Cancelada', 'Cancelada'),
        ('En curso', 'En curso'),
        ('Completada', 'Completada')
    ], default='Pendiente')
    abono_anticipado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(null=True, blank=True)

class DetalleReserva(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    precio_noche = models.DecimalField(max_digits=10, decimal_places=2)

class CheckIn(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(null=True, blank=True)

class CheckOut(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    pago_total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)
    observaciones = models.TextField(null=True, blank=True)

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

class Marca(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    cantidad = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(null=True, blank=True)

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, null=True, blank=True)
    nit = models.CharField(max_length=20)
    direccion = models.TextField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    correo = models.EmailField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=[
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo')
    ], default='Activo')

class Compra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(null=True, blank=True)

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    check_out = models.ForeignKey(CheckOut, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    nit = models.CharField(max_length=20, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.TextField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

class Tarea(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=[
        ('Pendiente', 'Pendiente'),
        ('En progreso', 'En progreso'),
        ('Completada', 'Completada')
    ], default='Pendiente')
    tipo_aseo = models.CharField(max_length=20, choices=[
        ('General', 'General'),
        ('Mantenimiento', 'Mantenimiento')
    ])
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateField(null=True, blank=True)

class AsignacionTarea(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_completada = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

class Capacitacion(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField()
    objetivo = models.TextField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)

class AsistenciaCapacitacion(models.Model):
    curso = models.ForeignKey(Capacitacion, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    asistio = models.BooleanField(default=False)
    calificacion = models.IntegerField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

class ReporteOcupacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    periodo = models.CharField(max_length=50)
    total_reservas = models.IntegerField()
    ocupacion_promedio = models.DecimalField(max_digits=5, decimal_places=2)
    ingresos_totales = models.DecimalField(max_digits=12, decimal_places=2)
    observaciones = models.TextField(null=True, blank=True)
