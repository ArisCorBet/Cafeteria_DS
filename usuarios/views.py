from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroForm

@login_required
def configuracion_perfil(request):
	# Ahora usamos el template de usuarios
	return render(request, "usuarios/perfil.html", {
		"user": request.user
	})


def registro(request):
	if request.method == 'POST':
		form = RegistroForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Cuenta creada exitosamente. ¡Ahora puedes iniciar sesión!")
			return redirect('login')
	else:
		form = RegistroForm()
	return render(request, 'registration/registro.html', {'form': form})
