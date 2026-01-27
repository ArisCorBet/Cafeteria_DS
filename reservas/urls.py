from django.contrib import admin
from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path(
        '',
        views.realizar_reserva,
        name='realizar_reserva'
    ),

    path(
        'cafeteria/<int:cafeteria_id>/calendario/',
        views.calendario_general,
        name='calendario_general'
    ),

    path(
        'cafeteria/<int:cafeteria_id>/calendario/<str:fecha>/',
        views.calendario_dia,
        name='calendario_dia'
    ),

    path(
        'cafeteria/<int:cafeteria_id>/mesas/',
        views.seleccionar_mesa,
        name='seleccionar_mesa'
    ),

    path(
        'confirmar/<int:mesa_id>/',
        views.confirmar_reserva,
        name='confirmar_reserva'
    ),

    path(
        'eventos/mesa/<int:mesa_id>/',
        views.eventos_mesa,
        name='eventos_mesa'
    ),
]
