from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.utils import timezone

def inicio(request):
    return render(request, 'reciclaje/inicio.html')

def dashboard(request):
    return render(request, 'reciclaje/dashboard.html')

def historial(request):
    return render(request, 'reciclaje/historial.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        messages.success(request, 'Inicio de sesión exitoso.')  # Placeholder
        return redirect('dashboard')
    return render(request, 'reciclaje/login.html')

def registro_reciclaje(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        tipo = request.POST.get('tipo')
        cantidad = request.POST.get('cantidad')
        try:
            with connection.cursor() as cursor:
                cursor.callproc('insertar_registro_reciclaje', [
                    1,
                    1,  
                    1 if tipo == 'plastico' else 2 if tipo == 'papel' else 3 if tipo == 'vidrio' else 4 if tipo == 'metal' else 5,
                    float(cantidad),
                    fecha,
                    tipo
                ])
            messages.success(request, 'Reciclaje registrado con éxito.')
        except Exception as e:
            messages.error(request, f'Error al registrar reciclaje: {str(e)}')
        return redirect('registro_reciclaje')
    return render(request, 'reciclaje/registro-reciclaje.html')

def registro_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        # Validar que las contraseñas coincidan
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('registro_usuario')

        # Verificar si el email ya existe
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM usuario WHERE correo = %s", [email])
            count = cursor.fetchone()[0]
            if count > 0:
                messages.error(request, 'El correo electrónico ya está registrado.')
                return redirect('registro_usuario')

        # Obtener la fecha actual
        fecha_registro = timezone.now().date()

        try:
            with connection.cursor() as cursor:
                cursor.callproc('insertar_usuario', [
                    nombre,
                    email,
                    telefono,
                    0,
                    fecha_registro,
                    password,
                    request.META.get('REMOTE_ADDR', '0.0.0.0'),
                    1
                ])
                connection.commit()
            messages.success(request, 'Usuario registrado con éxito.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error al registrar usuario: {str(e)}')
            return redirect('registro_usuario')

    return render(request, 'reciclaje/registro-usuario.html')