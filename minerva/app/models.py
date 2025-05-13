from django.db import models
from django.contrib.auth.models import User

# === Roles ===
class Rol(models.TextChoices):
    ADMIN = 'AD', 'Administrador'
    PRENSA = 'PR', 'Encargado de Prensa'
    CLASIFICACION = 'CL', 'Encargado de Clasificación'
    REDACCION = 'RE', 'Encargado de Redacción'
    MAPAS = 'MA', 'Encargado de Mapas'
    ESTADISTICA = 'ES', 'Encargado de Estadística'
    EDICION = 'ED', 'Encargado de Edición'
    PUBLICACION = 'PU', 'Encargado de Publicación'

# === Perfil extendido del Usuario ===
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=2, choices=Rol.choices)

    def __str__(self):
        return f"{self.user.username} ({self.get_rol_display()})"

# === Entidades Geográficas ===
class Zona(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Barrio(models.Model):
    nombre = models.CharField(max_length=100)
    zonas = models.ManyToManyField(Zona, related_name='barrios')

    def __str__(self):
        return self.nombre

# === Individuos y Bandas ===
class Individuo(models.Model):
    nombre = models.CharField(max_length=100)
    apodo = models.CharField(max_length=100, blank=True)
    dni = models.CharField(max_length=20, unique=True)
    edad = models.PositiveIntegerField(null=True, blank=True)
    domicilio = models.CharField(max_length=200, blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.apodo})"

class Pariente(models.Model):
    individuo = models.ForeignKey(Individuo, on_delete=models.CASCADE, related_name='parientes')
    pariente = models.ForeignKey(Individuo, on_delete=models.CASCADE, related_name='es_pariente_de')
    relacion = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.individuo} ↔ {self.relacion} ↔ {self.pariente}"

class Banda(models.Model):
    nombre = models.CharField(max_length=100)
    alias = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)
    individuos = models.ManyToManyField(Individuo, related_name='bandas')
    barrios = models.ManyToManyField(Barrio, related_name='bandas')

    def __str__(self):
        return self.nombre

# === Tipos de Fuente y Clasificación ===
class TipoFuente(models.TextChoices):
    DIARIO = 'DI', 'Diario Digital'
    RED_SOCIAL = 'RS', 'Red Social'
    TV = 'TV', 'Canal de TV'
    RADIO = 'RA', 'Canal de Radio'

class EstadoClasificacion(models.TextChoices):
    PENDIENTE = 'PE', 'Pendiente'
    APROBADO = 'AP', 'Aprobado'
    DESCARTADO = 'DE', 'Descartado'

# === Ítems de Interés ===
class ItemInteres(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

# === Link Relevante ===
class Link(models.Model):
    url = models.URLField(unique=True)
    descripcion = models.TextField(blank=True)
    tipo_fuente = models.CharField(max_length=2, choices=TipoFuente.choices)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    cargado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='links_cargados')
    estado_clasificacion = models.CharField(max_length=2, choices=EstadoClasificacion.choices, default=EstadoClasificacion.PENDIENTE)
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    clasificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='links_clasificados')
    items_interes = models.ManyToManyField(ItemInteres, blank=True)
    individuos_mencionados = models.ManyToManyField(Individuo, blank=True, related_name='links_mencionados')
    bandas_mencionadas = models.ManyToManyField(Banda, blank=True, related_name='links_mencionados')
    barrios_mencionados = models.ManyToManyField(Barrio, blank=True, related_name='links_mencionados')

    def __str__(self):
        return self.url

# === Artículo ===
class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    redactado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='articulos')
    fecha_redaccion = models.DateTimeField(auto_now_add=True)
    links_usados = models.ManyToManyField(Link, limit_choices_to={'estado_clasificacion': EstadoClasificacion.APROBADO})
    items_interes = models.ManyToManyField(ItemInteres, blank=True)

    def __str__(self):
        return self.titulo
