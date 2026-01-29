from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse
from cafeterias.models import Cafeteria, Mesa
from .models import Reserva, MesaReserva, EstadoMesa
from django.shortcuts import redirect
from datetime import timedelta, datetime, date
from calendar import monthrange

@login_required
def realizar_reserva(request):
    cafeterias = Cafeteria.objects.all() #Obtener todas las cafeterías
    # Obtener hora actual según la zona horaria configurada en settings.py
    hora_actual = timezone.localtime().time()
    cafeterias_estado = []
    for c in cafeterias:
        cafeterias_estado.append({
            'cafeteria': c,
            'abierta': c.esta_abierta(hora_actual)
        })
    return render(
        request,
        "reservas/realizar_reserva.html",
        {"cafeterias_estado": cafeterias_estado, "current_step": 1, "hora_actual": hora_actual}
    )


@login_required
def calendario_general(request, cafeteria_id):
    cafeteria = get_object_or_404(Cafeteria, id=cafeteria_id)

    mesas = Mesa.objects.filter(cafeteria=cafeteria)

    hoy = date.today()
    anio = hoy.year
    mes = hoy.month

    _, dias_mes = monthrange(anio, mes)
    fechas_mes = [date(anio, mes, dia) for dia in range(1, dias_mes + 1)]

    # Obtener todas las reservas ocupadas del mes en una sola consulta
    reservas_mes = MesaReserva.objects.filter(
        mesa__in=mesas,
        fecha__month=mes,
        fecha__year=anio,
        estado=EstadoMesa.OCUPADO
    ).select_related('mesa')

    # Agrupar reservas por fecha
    reservas_por_fecha = {}
    for r in reservas_mes:
        reservas_por_fecha.setdefault(r.fecha, []).append(r)

    eventos_calendar = []
    for fecha in fechas_mes:
        reservas_dia = reservas_por_fecha.get(fecha, [])
        if reservas_dia:
            # Procesar en memoria para saber si hay huecos
            # Crear un set de mesas ocupadas en ese día
            mesas_ocupadas = set(r.mesa_id for r in reservas_dia)
            if len(mesas_ocupadas) < mesas.count():
                # Hay al menos una mesa libre en algún bloque
                eventos_calendar.append({
                    "start": fecha.isoformat(),
                    "allDay": True,
                    "color": "#3b82f6"  
                })
            else:
                # Todas las mesas ocupadas en algún momento, pero puede haber huecos
                # Usar la función original para precisión
                tiene_huecos = dia_tiene_huecos(
                    fecha=fecha,
                    mesas=mesas,
                    hora_apertura=cafeteria.hora_apertura,
                    hora_cierre=cafeteria.hora_cierre
                )
                if tiene_huecos:
                    eventos_calendar.append({
                        "start": fecha.isoformat(),
                        "allDay": True,
                        "color": "#3b82f6"  # 🔵 Azul
                    })
                else:
                    eventos_calendar.append({
                        "start": fecha.isoformat(),
                        "allDay": True,
                        "color": "#e66e6e"  
                    })

    context = {
        "cafeteria": cafeteria,
        "eventos": eventos_calendar,
        "current_step": 2
    }

    return render(
        request,
        "reservas/calendario_general.html",
        context
    )

@login_required
def calendario_dia(request, cafeteria_id, fecha):
    cafeteria = get_object_or_404(Cafeteria, id=cafeteria_id)
    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()

    mesas = Mesa.objects.filter(cafeteria=cafeteria)

    reservas = MesaReserva.objects.filter(
        mesa__in=mesas,
        fecha=fecha_dt
    )

    eventos = []
    for r in reservas:
        if r.estado == EstadoMesa.OCUPADO:
            title = "Reservada"
        else:
            title = r.get_estado_display()
        eventos.append({
            "title": title,
            "start": f"{fecha}T{r.hora_inicio.strftime('%H:%M:%S')}",
            "end": f"{fecha}T{r.hora_fin.strftime('%H:%M:%S')}",
            "color": (
                "#dc6b6b"
                if r.estado == EstadoMesa.OCUPADO
                else "#e0d254"
            )
        })

    # Calcular slotMinTime y slotMaxTime basados en horario de cafetería
    slot_min_time = cafeteria.hora_apertura.strftime('%H:%M:%S')
    if cafeteria.hora_cierre <= cafeteria.hora_apertura:
        slot_max_time = '24:00:00'
    else:
        slot_max_time = cafeteria.hora_cierre.strftime('%H:%M:%S')

    return render(
        request,
        "reservas/calendario_dia.html",
        {
            "cafeteria": cafeteria,
            "fecha": fecha,
            "eventos": eventos,
            "hora_apertura": cafeteria.hora_apertura,
            "hora_cierre": cafeteria.hora_cierre,
            "slot_min_time": slot_min_time,
            "slot_max_time": slot_max_time,
            "current_step": 3
        }
    )


@login_required
def seleccionar_mesa(request, cafeteria_id):
    cafeteria = get_object_or_404(Cafeteria, id=cafeteria_id)

    # Parámetros enviados desde el calendario diario
    fecha_str = request.GET.get("fecha")
    hora_inicio_str = request.GET.get("hora_inicio")
    hora_fin_str = request.GET.get("hora_fin")

    # Convertir a objetos date y time
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date() if fecha_str else None
    hora_inicio = datetime.strptime(hora_inicio_str, "%H:%M").time() if hora_inicio_str else None
    hora_fin = datetime.strptime(hora_fin_str, "%H:%M").time() if hora_fin_str else None

    mesas = Mesa.objects.filter(cafeteria=cafeteria)

    # Si NO viene un rango horario válido → mostrar todas las mesas
    if not (fecha and hora_inicio and hora_fin):
        mesas_disponibles = mesas
    else:
        #Filtrar mesas ocupadas SOLO en ese rango horario
        mesas_ocupadas = MesaReserva.objects.filter(
            mesa__cafeteria=cafeteria,
            fecha=fecha,
            estado=EstadoMesa.OCUPADO,
            hora_inicio__lt=hora_fin,
            hora_fin__gt=hora_inicio
        ).values_list("mesa_id", flat=True)

        mesas_disponibles = mesas.exclude(id__in=mesas_ocupadas)

    return render(
        request,
        "reservas/seleccionar_mesa.html",
        {
            "cafeteria": cafeteria,
            "fecha": fecha_str,
            "hora_inicio": hora_inicio_str,
            "hora_fin": hora_fin_str,
            "mesas": mesas_disponibles,
            "current_step": 4
        }
    )



@login_required
def confirmar_reserva(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)

    if request.method == "POST":
        fecha_str = request.GET.get("fecha")
        hora_inicio_str = request.GET.get("hora_inicio")
        hora_fin_str = request.GET.get("hora_fin")

        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        hora_inicio = datetime.strptime(hora_inicio_str, "%H:%M").time()
        hora_fin = datetime.strptime(hora_fin_str, "%H:%M").time()

        from datetime import timedelta
        plazo_limite = fecha - timedelta(days=1)

        reserva = Reserva.objects.create(
            codigo=f"RES-{int(timezone.now().timestamp())}",
            fecha_reserva=timezone.now().date(),
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            plazo_limite=plazo_limite,
            num_personas=mesa.capacidad,
            usuario=request.user
        )

        MesaReserva.objects.create(
            mesa=mesa,
            reserva=reserva,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            estado=EstadoMesa.OCUPADO
        )

        return render(
            request,
            "reservas/reserva_confirmada.html",
            {
                "reserva": reserva,
                "fecha_seleccionada": fecha,
                "mesa": mesa,
                "current_step": 6
            }
        )
    else:
        fecha_str = request.GET.get("fecha")
        hora_inicio_str = request.GET.get("hora_inicio")
        hora_fin_str = request.GET.get("hora_fin")

        return render(
            request,
            "reservas/confirmar_reserva.html",
            {
                "mesa": mesa,
                "fecha": fecha_str,
                "hora_inicio": hora_inicio_str,
                "hora_fin": hora_fin_str,
                "current_step": 5
            }
        )

def eventos_mesa(request, mesa_id):
    fecha_str = request.GET.get("fecha")
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()

    reservas = MesaReserva.objects.filter(
        mesa_id=mesa_id,
        fecha=fecha
    )

    eventos = []
    for r in reservas:
        eventos.append({
            "title": r.estado.capitalize(),
            "start": f"{fecha}T{r.hora_inicio.strftime('%H:%M:%S')}",
            "end": f"{fecha}T{r.hora_fin.strftime('%H:%M:%S')}",
            "color": (
                "#e57373"
                if r.estado == EstadoMesa.OCUPADO
                else "#fff176"
            )
        })

    return JsonResponse(eventos, safe=False)

def home_cliente(request):
    return render(request, "reservas/home.html")

@login_required
def redireccion_post_login(request):
    user = request.user

    if user.is_staff or user.is_superuser:
        return redirect('/admin/')
    else:
        return redirect('home_cliente')
    

def dia_tiene_huecos(fecha, mesas, hora_apertura, hora_cierre):
    intervalo = timedelta(minutes=30)

    inicio_dia = datetime.combine(fecha, hora_apertura)

    # Caso: horario cruza medianoche
    if hora_cierre <= hora_apertura:
        fin_dia = datetime.combine(fecha + timedelta(days=1), hora_cierre)
    else:
        fin_dia = datetime.combine(fecha, hora_cierre)

    actual = inicio_dia

    while actual + intervalo <= fin_dia:
        bloque_inicio = actual.time()
        bloque_fin = (actual + intervalo).time()

        mesas_ocupadas = MesaReserva.objects.filter(
            mesa__in=mesas,
            fecha=fecha,
            estado=EstadoMesa.OCUPADO,
            hora_inicio__lt=bloque_fin,
            hora_fin__gt=bloque_inicio
        ).values_list("mesa_id", flat=True)

        #Si existe al menos una mesa libre → hay hueco
        if len(mesas_ocupadas) < mesas.count():
            return True

        actual += intervalo

    # Ningún bloque tuvo mesas libres
    return False