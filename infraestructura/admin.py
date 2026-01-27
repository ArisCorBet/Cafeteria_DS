from django.contrib import admin
from .models import Direccion, Universidad, Facultad, Bloque

# Register your models here.

admin.site.register(Direccion)
admin.site.register(Universidad)
admin.site.register(Facultad)
admin.site.register(Bloque)

