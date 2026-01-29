from django.db import models
from cafeterias.models import Mesa, EstadoMesa
from django.contrib.auth.models import User

# Create your models here.
class Reserva(models.Model):
    codigo = models.CharField(max_length=20)
    fecha_creacion = models.DateField(auto_now_add=True, null=True)
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    plazo_limite = models.DateField()
    num_personas = models.PositiveIntegerField()

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservas'
    )

    def __str__(self):
        return self.codigo


class MesaReserva(models.Model):
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(
        max_length=15,
        choices=EstadoMesa.choices,
        default=EstadoMesa.LIBRE
    )

    mesa = models.ForeignKey(
        Mesa,
        on_delete=models.CASCADE,
        related_name='mesa_reservas'
    )

    reserva = models.OneToOneField(
        Reserva,
        on_delete=models.CASCADE
    )


