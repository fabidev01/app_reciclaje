from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.db import connection

class Command(BaseCommand):
    help = 'Hashea las contraseñas en la tabla usuario con contraseñas conocidas'

    def handle(self, *args, **options):
        # Diccionario de correos y contraseñas originales (ajústalas según tus datos)
        password_map = {
            'luis.morales@email.com': '123',
            'ana.quispe@email.com': '123',
            'pedro.vargas@email.com': '123',
            'maria.rojas@email.com': '123',
            'carlos.mamani@email.com': '123',
            'andy@gmail.com': '123',
        }

        with connection.cursor() as cursor:
            cursor.execute("SELECT id_usuario, correo FROM usuario")
            users = cursor.fetchall()
            for user in users:
                id_usuario, correo = user
                password = password_map.get(correo, '123')  # Usa '123' como predeterminado
                hashed_password = make_password(password)
                cursor.execute(
                    "UPDATE usuario SET contraseña = %s WHERE id_usuario = %s",
                    [hashed_password, id_usuario]
                )
        connection.commit()
        self.stdout.write(self.style.SUCCESS('Contraseñas hasheadas con éxito'))