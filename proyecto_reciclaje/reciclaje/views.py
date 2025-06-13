from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.db import connection
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django import forms
from .models import Usuario
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

# Formulario personalizado para login
class LoginForm(forms.Form):
    email = forms.EmailField(label="Correo", max_length=254)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
class LoginView(FormView):
    template_name = 'usuario_regular/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('dashboard')  # Valor por defecto, se sobrescribirá

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id_usuario, contraseña, id_rol FROM Usuario WHERE correo = %s",
                    [email]
                )
                user = cursor.fetchone()
                if user and check_password(password, user[1]):
                    self.request.session['user_id'] = user[0]
                    id_rol = user[2]  # id_rol está en el índice 2
                    if id_rol == 1:  # Administrador
                        messages.success(self.request, 'Inicio de sesión exitoso como Administrador.')
                        return HttpResponseRedirect(reverse_lazy('admin_panel'))
                    else:  # Otros roles (Regular u otros)
                        messages.success(self.request, f'Inicio de sesión exitoso como usuario regular (Rol ID: {id_rol}).')
                        return HttpResponseRedirect(reverse_lazy('dashboard'))
                else:
                    messages.error(self.request, 'Correo o contraseña incorrectos.')
                    return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f'Error al iniciar sesión: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Correo o contraseña incorrectos.')
        response = self.render_to_response(self.get_context_data(form=form))
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

# Vista de inicio
def inicio(request):
    response = render(request, 'usuario_regular/inicio.html')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Vista de logout
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    response = redirect('inicio')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Vista de registro de usuario
def registro_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('registro_usuario')

        if Usuario.objects.filter(correo=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return redirect('registro_usuario')

        fecha_registro = timezone.now().date()
        try:
            user = Usuario(
                nombre=nombre,
                correo=email,
                telefono=telefono,
                balance_puntos=0,
                fecha_registro=fecha_registro,
                contraseña=make_password(password),
                ip=request.META.get('REMOTE_ADDR', '0.0.0.0'),
                id_rol=2
            )
            user.save()
            messages.success(request, 'Usuario registrado con éxito.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error al registrar usuario: {str(e)}')
            return redirect('registro_usuario')

    response = render(request, 'usuario_regular/registro-usuario.html')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Vista de donación
def donacion(request):
    if not request.session.get('user_id'):
        messages.error(request, 'Debes iniciar sesión para ver las donaciones.')
        return redirect('login')

    nombre_usuario = ""
    donaciones = []
    try:
        user_id = request.session['user_id']
        with connection.cursor() as cursor:
            cursor.execute("SELECT nombre FROM Usuario WHERE id_usuario = %s", [user_id])
            result = cursor.fetchone()
            if result:
                nombre_usuario = result[0]

            cursor.execute(
                """
                SELECT id_donacion, nombre, entidad_donacion, monto_donacion
                FROM Donacion
                """
            )
            donaciones = cursor.fetchall()

            if request.method == 'POST':
                id_donacion = request.POST.get('id_donacion')
                cantidad = int(request.POST.get('cantidad', 1))
                fecha_canje = timezone.now().date()

                cursor.execute(
                    "SELECT monto_donacion FROM Donacion WHERE id_donacion = %s",
                    [id_donacion]
                )
                result = cursor.fetchone()
                if not result:
                    raise Exception("ID de donación no válido.")
                monto_por_unidad = float(result[0])
                puntos_totales = monto_por_unidad * cantidad

                cursor.callproc('canjear_donacion', [
                    user_id,
                    int(id_donacion),
                    cantidad,
                    'Completado',
                    fecha_canje
                ])
                connection.commit()
                messages.success(request, f'Donación realizada con éxito. Puntos descontados: {puntos_totales} (equivalente a {puntos_totales} Bs.)')
                return redirect('donacion')
    except Exception as e:
        messages.error(request, f'Error al realizar la donación: {str(e)}')
        connection.rollback()

    response = render(request, 'usuario_regular/donacion.html', {
        'nombre_usuario': nombre_usuario,
        'donaciones': donaciones
    })
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Vista de catálogo
def catalogo(request):
    if not request.session.get('user_id'):
        messages.error(request, 'Debes iniciar sesión para ver el catálogo.')
        return redirect('login')

    nombre_usuario = ""
    catalogo = []
    try:
        user_id = request.session['user_id']
        with connection.cursor() as cursor:
            cursor.execute("SELECT nombre FROM Usuario WHERE id_usuario = %s", [user_id])
            result = cursor.fetchone()
            if result:
                nombre_usuario = result[0]

            cursor.execute(
                """
                SELECT id_catalogo_recompensa, nombre, puntos_coste, stock
                FROM Catalogo_Recompensa
                WHERE disponible = TRUE AND stock > 0
                """
            )
            catalogo = cursor.fetchall()

            if request.method == 'POST':
                id_catalogo = request.POST.get('id_catalogo')
                cantidad = int(request.POST.get('cantidad', 1))
                fecha_canje = timezone.now().date()

                cursor.execute(
                    "SELECT puntos_coste FROM Catalogo_Recompensa WHERE id_catalogo_recompensa = %s",
                    [id_catalogo]
                )
                puntos_por_unidad = float(cursor.fetchone()[0])
                puntos_totales = puntos_por_unidad * cantidad

                cursor.callproc('canjear_recompensa', [
                    user_id,
                    int(id_catalogo),
                    'Completado',
                    fecha_canje
                ])
                connection.commit()
                messages.success(request, f'Recompensa canjeada con éxito. Puntos descontados: {puntos_totales}.')
                return redirect('catalogo')
    except Exception as e:
        messages.error(request, f'Error al canjear recompensa: {str(e)}')
        connection.rollback()

    response = render(request, 'usuario_regular/catalogo.html', {
        'nombre_usuario': nombre_usuario,
        'catalogo': catalogo
    })
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Vista de dashboard
def dashboard(request):
    if not request.session.get('user_id'):
        messages.error(request, 'Debes iniciar sesión para ver el dashboard.')
        return redirect('login')

    total_reciclado = 0.0
    puntos_acumulados = 0
    co2_reducido = 0.0
    ultimas_actividades = []
    nombre_usuario = ""
    es_admin = False

    try:
        user_id = request.session['user_id']
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT nombre, balance_puntos FROM Usuario WHERE id_usuario = %s",
                [user_id]
            )
            result = cursor.fetchone()
            if result:
                nombre_usuario, puntos_acumulados = result

            cursor.callproc('reporte_actividad_reciclaje', [user_id])
            reporte = cursor.fetchall()
            for row in reporte:
                total_reciclado += row[2]
                co2_reducido += row[4]

            cursor.execute(
                """
                SELECT 
                    DATE_FORMAT(rr.fecha_registro, '%%d/%%m/%%Y') AS fecha_registro,
                    rr.nombre_subtipo AS material,
                    rr.cantidad_kg,
                    rr.puntos_obtenidos
                FROM Registro_Reciclaje rr
                WHERE rr.id_usuario = %s
                ORDER BY rr.fecha_registro DESC
                LIMIT 5
                """,
                [user_id]
            )
            ultimas_actividades = cursor.fetchall()

            cursor.execute(
                """
                SELECT r.nombre
                FROM Usuario u
                JOIN Rol r ON u.id_rol = r.id_rol
                WHERE u.id_usuario = %s
                """,
                [user_id]
            )
            rol = cursor.fetchone()
            es_admin = rol and rol[0] == 'Administrador'

    except Exception as e:
        messages.error(request, f'Error al cargar el dashboard: {str(e)}')

    response = render(request, 'usuario_regular/dashboard.html', {
        'nombre_usuario': nombre_usuario,
        'total_reciclado': total_reciclado,
        'puntos_acumulados': puntos_acumulados,
        'co2_reducido': co2_reducido,
        'ultimas_actividades': ultimas_actividades,
        'es_admin': es_admin
    })
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Vista de historial
def historial(request):
    if not request.session.get('user_id'):
        messages.error(request, 'Debes iniciar sesión para ver el historial.')
        return redirect('login')

    user_id = request.session['user_id']
    selected_type = request.GET.get('type', 'reciclajes')  # Valor por defecto: reciclajes
    historial_data = []

    try:
        with connection.cursor() as cursor:
            if selected_type == 'reciclajes':
                cursor.execute(
                    """
                    SELECT 
                        DATE_FORMAT(rr.fecha_registro, '%%d/%%m/%%Y') AS fecha,
                        mr.nombre AS material,
                        rr.cantidad_kg,
                        rr.puntos_obtenidos,
                        rr.co2_reducido,
                        pr.nombre AS punto_reciclaje,
                        rr.nombre_subtipo
                    FROM Registro_Reciclaje rr
                    JOIN Material_Reciclable mr ON rr.id_material_reciclable = mr.id_material_reciclable
                    JOIN Punto_Reciclaje pr ON rr.id_punto_reciclaje = pr.id_punto_reciclaje
                    WHERE rr.id_usuario = %s
                    ORDER BY rr.fecha_registro DESC
                    """,
                    [user_id]
                )
                historial_data = cursor.fetchall()

            elif selected_type == 'canjes':
                cursor.execute(
                    """
                    SELECT 
                        DATE_FORMAT(cr.fecha_canje, '%%d/%%m/%%Y') AS fecha,
                        cat.nombre AS recompensa,
                        cat.puntos_coste AS puntos_descontados,
                        cr.estado,
                        cat.stock
                    FROM Canje_Recompensa cr
                    JOIN Catalogo_Recompensa cat ON cr.id_catalogo_recompensa = cat.id_catalogo_recompensa
                    WHERE cr.id_usuario = %s
                    ORDER BY cr.fecha_canje DESC
                    """,
                    [user_id]
                )
                historial_data = cursor.fetchall()

            elif selected_type == 'donaciones':
                cursor.execute(
                    """
                    SELECT 
                        DATE_FORMAT(cd.fecha_canje, '%%d/%%m/%%Y') AS fecha,
                        d.nombre AS donacion,
                        d.monto_donacion AS puntos_descontados,
                        cd.estado
                    FROM Canje_Donacion cd
                    JOIN Donacion d ON cd.id_donacion = d.id_donacion
                    WHERE cd.id_usuario = %s
                    ORDER BY cd.fecha_canje DESC
                    """,
                    [user_id]
                )
                historial_data = cursor.fetchall()

    except Exception as e:
        messages.error(request, f'Error al cargar el historial: {str(e)}')

    response = render(request, 'usuario_regular/historial.html', {
        'historial_data': historial_data,
        'selected_type': selected_type,
        'has_data': bool(historial_data)
    })
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Vista de registro de reciclaje
def registro_reciclaje(request):
    if not request.session.get('user_id'):
        messages.error(request, 'Debes iniciar sesión para registrar reciclaje.')
        return redirect('login')

    user_id = request.session['user_id']
    materiales = []
    puntos = []
    selected_punto = request.POST.get('punto') if request.method == 'POST' else None

    try:
        with connection.cursor() as cursor:
            # Obtener puntos disponibles
            cursor.execute(
                """
                SELECT id_punto_reciclaje, nombre, latitud, longitud
                FROM Punto_Reciclaje
                WHERE estado_punto = 'Disponible'
                """
            )
            puntos_raw = cursor.fetchall()
            if not puntos_raw:
                messages.error(request, 'No hay puntos de reciclaje disponibles.')
                return redirect('dashboard')

            puntos = [
                {
                    'id_punto_reciclaje': punto[0],
                    'nombre': punto[1],
                    'latitud': float(punto[2]),
                    'longitud': float(punto[3])
                }
                for punto in puntos_raw
            ]

            # Obtener materiales disponibles para el punto seleccionado
            if selected_punto:
                cursor.execute(
                    """
                    SELECT DISTINCT mr.id_material_reciclable, mr.nombre
                    FROM Material_Punto_Reciclaje mpr
                    JOIN Material_Reciclable mr ON mpr.id_material_reciclable = mr.id_material_reciclable
                    WHERE mpr.id_punto_reciclaje = %s
                    """,
                    [selected_punto]
                )
            else:
                cursor.execute("SELECT id_material_reciclable, nombre FROM Material_Reciclable")
            materiales = cursor.fetchall()
            if not materiales:
                messages.error(request, 'No hay materiales reciclables disponibles para este punto.')
                return redirect('dashboard')

            if request.method == 'POST':
                fecha = timezone.now().strftime('%Y-%m-%d')
                id_material = request.POST.get('tipo')
                subtipo = request.POST.get('subtipo')
                id_punto = request.POST.get('punto')
                cantidad = request.POST.get('cantidad')

                if not all([id_punto, id_material, cantidad, subtipo]):
                    messages.error(request, 'Todos los campos son obligatorios.')
                else:
                    # Verificar si el material está permitido en el punto
                    cursor.execute(
                        """
                        SELECT COUNT(*) 
                        FROM Material_Punto_Reciclaje 
                        WHERE id_punto_reciclaje = %s AND id_material_reciclable = %s
                        """,
                        [id_punto, id_material]
                    )
                    if cursor.fetchone()[0] == 0:
                        messages.error(request, 'El material seleccionado no es válido para este punto de reciclaje.')
                        return redirect('registro_reciclaje')

                    try:
                        cursor.callproc('insertar_registro_reciclaje', [
                            user_id,
                            int(id_punto),
                            int(id_material),
                            float(cantidad),
                            fecha,
                            subtipo
                        ])
                        connection.commit()
                        messages.success(request, '¡Registro de reciclaje exitoso!')
                        return redirect('dashboard')
                    except Exception as e:
                        messages.error(request, f'Error al registrar: {str(e)}')
                        connection.rollback()
    except Exception as e:
        messages.error(request, f'Error al cargar datos: {str(e)}')

    # Determinar qué template usar basado en la URL o preferencia (por ahora usa mapa.html)
    template = 'usuario_regular/mapa.html'  # Cambia a 'usuario_regular/registro-reciclaje.html' si prefieres el otro
    response = render(request, template, {
        'materiales': materiales,
        'puntos': puntos,
        'selected_punto': selected_punto
    })
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response