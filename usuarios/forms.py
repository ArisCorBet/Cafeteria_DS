
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Formulario de login personalizado
class TripleLoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario", widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Tu usuario'
    }))
    email = forms.EmailField(label="Correo Institucional", required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'usuario@unl.edu.ec'
    }))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = self.data.get('email')  # Tomar el email directamente del POST, no del cleaned_data

        # 1. Validar dominio solo si se ingresó email
        if email:
            if not email.endswith('@unl.edu.ec'):
                raise ValidationError("Solo se permiten correos institucionales (@unl.edu.ec).")

            # 2. Validar que el correo sea del usuario
            if username:
                try:
                    user = User.objects.get(username=username)
                    if user.email != email:
                        raise ValidationError("El correo no coincide con el usuario registrado.")
                except User.DoesNotExist:
                    pass
        return cleaned_data
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")
    email = forms.EmailField(required=True, label="Correo Institucional")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@unl.edu.ec'):
            raise ValidationError("Solo se permiten correos con el dominio @unl.edu.ec")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
