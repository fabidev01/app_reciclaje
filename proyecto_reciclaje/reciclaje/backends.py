from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import Usuario

class UsuarioAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Usuario.objects.get(correo=username)
            if check_password(password, user.contraseña):
                return user
        except Usuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None