from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Lead(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    direccion_domicilio = models.CharField(max_length=200)
    direccion_evento = models.CharField(max_length=200)
    cedula = models.IntegerField()
    email = models.EmailField()
    description = models.TextField()
    fecha_ingreso = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey("Category", related_name="leads", null=True, blank=True, on_delete=models.SET_NULL)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agente = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Agent(models.Model):
    cedula = models.IntegerField()
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField(default=timezone.now)
    email = models.EmailField()

    def __str__(self):
        return self.user.username


class Category(models.Model):  # Nuevo, Contactado, Vendido
    name = models.CharField(max_length=30)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Articulo(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()
    stock = models.IntegerField()
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Proforma(models.Model):
    fecha_cotizacion = models.DateTimeField(default=timezone.now)
    fecha = models.DateField()
    agente = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    estado = models.BooleanField()
    observacion = models.CharField(max_length=200)
    pvp = models.FloatField()
    cantidad = models.IntegerField()
    tiempo = models.CharField(max_length=200, verbose_name='tiempo de alquiler')
    articulos = models.ManyToManyField(Articulo)
    pdf_file = models.FileField(upload_to='proformas/', blank=True, null=True)

    def __str__(self):
        return f"{self.lead.cedula} {self.lead.apellido}"

def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)
