from django.db import models
from reservas.models import Reserva
from django.contrib.auth.models import User

# Create your models here.

class Resena(models.Model):
    calificacion = models.PositiveSmallIntegerField()
    comentario = models.TextField()
    fecha_resena = models.DateField(auto_now_add=True)

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='resenas'
    )

    reserva = models.OneToOneField(
        Reserva,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
