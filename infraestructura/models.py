from django.db import models

# Create your models here.

class Direccion(models.Model):
    calle_principal = models.CharField(max_length=100)
    calle_secundaria = models.CharField(max_length=100)
    referencia = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.calle_principal} y {self.calle_secundaria}"


class Universidad(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.OneToOneField(
        Direccion,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nombre

class Facultad(models.Model):
    nombre = models.CharField(max_length=100)
    universidad = models.ForeignKey(
        Universidad,
        on_delete=models.CASCADE,
        related_name='facultades'
    )

    def __str__(self):
        return self.nombre
    

class Bloque(models.Model):
    numero_bloque = models.CharField(max_length=10)
    facultad = models.ForeignKey(
        Facultad,
        on_delete=models.CASCADE,
        related_name='bloques'
    )

    def __str__(self):
        return f"Bloque {self.numero_bloque}"

