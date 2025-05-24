# reciclaje/middleware.py
print("Middleware file loaded")
class UserIpMiddleware:
    def _init_(self, get_response):
        self.get_response = get_response  # Almacena la función get_response
        print("Middleware UserIpMiddleware inicializado")  # Depuración

    def _call_(self, request):
        print("Procesando solicitud en UserIpMiddleware")  # Depuración
        # Obtener el ID del usuario (0 si no está autenticado)
        user_id = request.user.id if request.user.is_authenticated else 0
        # Obtener la IP del cliente
        user_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')

        # Establecer las variables en la conexión a MySQL
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SET @current_user_id = %s", [user_id])
            cursor.execute("SET @current_user_ip = %s", [user_ip])

        # Procesar la solicitud y obtener la respuesta
        response = self.get_response(request)
        return response