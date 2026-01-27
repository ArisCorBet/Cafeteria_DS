from django.db import models
from infraestructura.models import Bloque
# Create your models here.
class EstadoMesa(models.TextChoices):
    LIBRE = 'LIBRE', 'Libre'
    OCUPADO = 'OCUPADO', 'Ocupado'
    MANTENIMIENTO = 'MANTENIMIENTO', 'Mantenimiento'

    
class Cafeteria(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    hora_apertura = models.TimeField()
    hora_cierre = models.TimeField()
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=150)

    bloque = models.OneToOneField(
        Bloque,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nombre
    

class Menu(models.Model):
    archivo = models.FileField(upload_to='menus/')
    cafeteria = models.OneToOneField(
        Cafeteria,
        on_delete=models.CASCADE,
        related_name='menu'
    )

    def __str__(self):
        return f"Menú - {self.cafeteria.nombre}"

class Mesa(models.Model):
    codigo = models.CharField(max_length=20)
    capacidad = models.PositiveIntegerField()
    cafeteria = models.ForeignKey(
        Cafeteria,
        on_delete=models.CASCADE,
        related_name='mesas'
    )

    def __str__(self):
        return f"Mesa {self.codigo}"
