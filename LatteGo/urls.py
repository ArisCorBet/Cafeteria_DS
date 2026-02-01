"""
URL configuration for LatteGo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from reservas.views import home_cliente, redireccion_post_login, mis_reservas
from usuarios.views import registro
from django.views.generic.base import RedirectView
from reservas.views import cancelar_reserva 
from usuarios.forms import TripleLoginForm
from django.contrib.auth import views as auth_views
from usuarios.views import configuracion_perfil

urlpatterns = [
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('home/', home_cliente, name='home_cliente'),
    path('mis-reservas/', mis_reservas, name='mis_reservas'),
    path('configuracion/', configuracion_perfil, name='configuracion'),
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=TripleLoginForm
    ), name='login'),
    path('accounts/registro/', registro, name='registro'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('post-login/', redireccion_post_login, name='post_login'),
    path('admin/', admin.site.urls),
    path('reservas/', include('reservas.urls')),
    path('cancelar-reserva/<int:reserva_id>/', cancelar_reserva, name='cancelar_reserva'),

]


