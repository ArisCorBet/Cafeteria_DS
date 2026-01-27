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
from reservas.views import home_cliente, redireccion_post_login

urlpatterns = [
    path('', home_cliente, name='home_cliente'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('post-login/', redireccion_post_login, name='post_login'),
    path('admin/', admin.site.urls),
    path('reservas/', include('reservas.urls')),
]
