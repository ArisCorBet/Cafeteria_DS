from django.contrib import admin
from .models import Cafeteria, Mesa, Menu

# Register your models here.
admin.site.register(Cafeteria)
admin.site.register(Mesa)
admin.site.register(Menu)