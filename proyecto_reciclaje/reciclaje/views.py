from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.utils import timezone
from datetime import datetime

def inicio(request):
    return render(request, 'reciclaje/inicio.html')

def donacion(request):
    id_usuario = request.session.get('id_usuario')
    if not id_usuario:
        messages.error(request, 'Debes iniciar sesión para ver las donaciones.')
        return redirect('login')

    nombre_usuario = ""
    donaciones = []
    try:
        with connection.cursor() as cursor:
            # Obtener el nombre del usuario
            cursor.execute(
                "SELECT nombre FROM Usuario WHERE id_usuario = %s",
                [id_usuario]
            )
            result = cursor.fetchone()
            nombre_usuario = result[0] if result else "Usuario"

            # Cargar las donaciones disponibles
            cursor.execute(
                """
                SELECT id_donacion, nombre, entidad_donacion, monto_donacion
                FROM Donacion
                """
            )
            donaciones = cursor.fetchall()

        # Manejar el canje de donaciones
        if request.method == 'POST':
            id_donacion = request.POST.get('id_donacion')
            cantidad = int(request.POST.get('cantidad', 1))
            fecha_canje = timezone.now().date()

            try:
                with connection.cursor() as cursor:
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
                        int(id_usuario),
                        int(id_donacion),
                        cantidad,
                        'Completado',
                        fecha_canje
                    ])
                    connection.commit()
                    messages.success(request, f'Donación realizada con éxito. Puntos descontados: {puntos_totales} (equivalente a {puntos_totales} Bs.)')
            except Exception as e:
                messages.error(request, f'Error al realizar la donación: {str(e)}')
                connection.rollback()

            return redirect('donacion')

    except Exception as e:
        messages.error(request, f'Error al cargar donaciones: {str(e)}')
        print(f"Error en donacion: {str(e)}")

    return render(request, 'reciclaje/donacion.html', {
        'nombre_usuario': nombre_usuario,
        'donaciones': donaciones
    })

def catalogo(request):
    id_usuario = request.session.get('id_usuario')
    if not id_usuario:
        messages.error(request, 'Debes iniciar sesión para ver el catálogo.')
        return redirect('login')

    nombre_usuario = ""
    catalogo = []
    try:
        with connection.cursor() as cursor:
            # Obtener el nombre del usuario
            cursor.execute(
                "SELECT nombre FROM Usuario WHERE id_usuario = %s",
                [id_usuario]
            )
            result = cursor.fetchone()
            nombre_usuario = result[0] if result else "Usuario"

            # Cargar las recompensas del catálogo
            cursor.execute(
                """
                SELECT id_catalogo_recompensa, nombre, puntos_coste, stock
                FROM Catalogo_Recompensa
                WHERE disponible = TRUE AND stock > 0
                """
            )
            catalogo = cursor.fetchall()

        # Manejar el canje de recompensas
        if request.method == 'POST':
            id_catalogo = request.POST.get('id_catalogo')
            cantidad = int(request.POST.get('cantidad', 1))  # Añadimos la cantidad
            fecha_canje = timezone.now().date()

            try:
                with connection.cursor() as cursor:
                    # Obtener el costo por unidad para el mensaje
                    cursor.execute(
                        "SELECT puntos_coste FROM Catalogo_Recompensa WHERE id_catalogo_recompensa = %s",
                        [id_catalogo]
                    )
                    puntos_por_unidad = float(cursor.fetchone()[0])
                    puntos_totales = puntos_por_unidad * cantidad

                    cursor.callproc('canjear_recompensa', [
                        int(id_usuario),
                        int(id_catalogo),
                        'Completado',
                        fecha_canje
                    ])
                    connection.commit()
                    messages.success(request, f'Recompensa canjeada con éxito. Puntos descontados: {puntos_totales}.')
            except Exception as e:
                messages.error(request, f'Error al canjear recompensa: {str(e)}')
                connection.rollback()

            return redirect('catalogo')

    except Exception as e:
        messages.error(request, f'Error al cargar catálogo: {str(e)}')
        print(f"Error en catalogo: {str(e)}")

    return render(request, 'reciclaje/catalogo.html', {
        'nombre_usuario': nombre_usuario,
        'catalogo': catalogo
    })

def dashboard(request):
    id_usuario = request.session.get('id_usuario')
    if not id_usuario:
        messages.error(request, 'Debes iniciar sesión para ver el dashboard.')
        return redirect('login')

    total_reciclado = 0.0
    puntos_acumulados = 0
    co2_reducido = 0.0
    ultimas_actividades = []
    nombre_usuario = ""
    es_admin = False

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT nombre, balance_puntos FROM Usuario WHERE id_usuario = %s",
                [id_usuario]
            )
            result = cursor.fetchone()
            nombre_usuario = result[0]
            puntos_acumulados = result[1]

            cursor.callproc('reporte_actividad_reciclaje', [id_usuario])
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
                [id_usuario]
            )
            ultimas_actividades = cursor.fetchall()

            # Verificar si el usuario es administrador usando id_rol y unión con Rol
            cursor.execute(
                """
                SELECT r.nombre
                FROM Usuario u
                JOIN Rol r ON u.id_rol = r.id_rol
                WHERE u.id_usuario = %s
                """,
                [id_usuario]
            )
            rol = cursor.fetchone()
            es_admin = rol and rol[0] == 'Administrador'

    except Exception as e:
        messages.error(request, f'Error al cargar el dashboard: {str(e)}')
        print(f"Error en el dashboard: {str(e)}")

    # Limpiar mensajes antiguos si es necesario
    if 'messages' in request.session:
        del request.session['messages']

    return render(request, 'reciclaje/dashboard.html', {
        'nombre_usuario': nombre_usuario,
        'total_reciclado': total_reciclado,
        'puntos_acumulados': puntos_acumulados,
        'co2_reducido': co2_reducido,
        'ultimas_actividades': ultimas_actividades,
        'es_admin': es_admin  # Pasar la variable al template
    })

def historial(request):
    return render(request, 'reciclaje/historial.html')

def login_view(request):
    print(f"Método de la solicitud: {request.method}")  # Depuración
    if request.method == 'POST':
        print("Formulario de login enviado con POST")  # Depuración
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        print(f"Datos recibidos: email={email}, password={password}")  # Depuración

        try:
            with connection.cursor() as cursor:
                # Comparar directamente con la contraseña en texto plano
                cursor.execute("SELECT id_usuario FROM usuario WHERE correo = %s AND contraseña = %s", [email, password])
                usuario = cursor.fetchone()
                print(f"Resultado de la consulta: {usuario}")  # Depuración

                if usuario:
                    request.session['id_usuario'] = usuario[0]
                    request.session['ip'] = request.META.get('REMOTE_ADDR') or '0.0.0.0'
                    print(f"Sesión iniciada: id_usuario={request.session['id_usuario']}, ip={request.session['ip']}")  # Depuración
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Correo o contraseña incorrectos.')
                    print("Error: Credenciales incorrectas")  # Depuración
                    return redirect('login')
        except Exception as e:
            messages.error(request, f'Error al iniciar sesión: {str(e)}')
            print(f"Error en el login: {str(e)}")  # Depuración
            return redirect('login')

    print("Mostrando formulario de login (GET)")  # Depuración
    return render(request, 'reciclaje/login.html')

def registro_reciclaje(request):
    id_usuario = request.session.get('id_usuario')
    if not id_usuario:
        messages.error(request, 'Debes iniciar sesión para registrar reciclaje.')
        return redirect('login')

    materiales = []
    puntos = []
    try:
        with connection.cursor() as cursor:
            # Obtener materiales reciclables
            cursor.execute("SELECT id_material_reciclable, nombre FROM Material_Reciclable")
            materiales = cursor.fetchall()
            if not materiales:
                messages.error(request, 'No hay materiales reciclables disponibles. Contacta al administrador.')
                return redirect('dashboard')

            # Obtener puntos de reciclaje (solo los disponibles)
            cursor.execute(
                """
                SELECT id_punto_reciclaje, nombre, latitud, longitud
                FROM Punto_Reciclaje
                WHERE estado_punto = 'Disponible'
                """
            )
            puntos_raw = cursor.fetchall()
            if not puntos_raw:
                messages.error(request, 'No hay puntos de reciclaje disponibles en este momento.')
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

            if request.method == 'POST':
                fecha = datetime.now().strftime('%Y-%m-%d')
                id_material = request.POST.get('tipo')
                subtipo = request.POST.get('subtipo')
                id_punto = request.POST.get('punto')
                cantidad = request.POST.get('cantidad')

                if not all([id_usuario, id_punto, id_material, cantidad, subtipo]):
                    messages.error(request, 'Todos los campos son obligatorios.')
                else:
                    try:
                        cursor.callproc('insertar_registro_reciclaje', [
                            int(id_usuario),
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
                        print(f"Error en registro_reciclaje: {str(e)}")
                        connection.rollback()

    except Exception as e:
        messages.error(request, f'Error al cargar datos: {str(e)}')
        print(f"Error en registro_reciclaje: {str(e)}")

    return render(request, 'reciclaje/mapa.html', {
        'materiales': materiales,
        'puntos': puntos
    })

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

def logout_view(request):
    request.session.flush()
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('login')

# Nuevas vistas de administración
def es_admin(request):
    id_usuario = request.session.get('id_usuario')
    if not id_usuario:
        return False
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT r.nombre
                FROM Usuario u
                JOIN Rol r ON u.id_rol = r.id_rol
                WHERE u.id_usuario = %s
                """,
                [id_usuario]
            )
            rol = cursor.fetchone()
            return rol and rol[0] == 'Administrador'
    except Exception as e:
        print(f"Error al verificar rol: {str(e)}")
        return False

def admin_panel(request):
    if not es_admin(request):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('dashboard')
    return render(request, 'reciclaje/admin.html')

def admin_usuarios(request):
    if not es_admin(request):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('dashboard')

    usuarios = []
    roles = []
    permisos = []
    try:
        with connection.cursor() as cursor:
            if request.method == 'POST':
                # Manejar la actualización del usuario
                id_usuario = request.POST.get('id_usuario')
                rol_seleccionado = request.POST.get('rol')
                permisos_seleccionados = request.POST.get('permisos', '').split(',')

                try:
                    # Obtener el id del rol seleccionado
                    cursor.execute("SELECT id_rol FROM Rol WHERE nombre = %s", [rol_seleccionado])
                    selected_rol_id_result = cursor.fetchone()
                    if not selected_rol_id_result:
                        raise Exception(f"Rol '{rol_seleccionado}' no encontrado.")
                    selected_rol_id = selected_rol_id_result[0]

                    # Actualizar el rol del usuario
                    cursor.execute(
                        """
                        UPDATE Usuario SET id_rol = %s WHERE id_usuario = %s
                        """,
                        [selected_rol_id, id_usuario]
                    )

                    # Eliminar permisos personalizados antiguos del usuario
                    cursor.execute("DELETE FROM Usuario_Permiso WHERE id_usuario = %s", [id_usuario])

                    # Asignar nuevos permisos personalizados al usuario
                    for permiso in permisos_seleccionados:
                        if permiso:  # Ignorar cadenas vacías
                            cursor.execute(
                                "SELECT id_permiso FROM Permiso WHERE nombre = %s",
                                [permiso]
                            )
                            id_permiso_result = cursor.fetchone()
                            if id_permiso_result:
                                id_permiso = id_permiso_result[0]
                                cursor.execute(
                                    "INSERT INTO Usuario_Permiso (id_usuario, id_permiso) VALUES (%s, %s)",
                                    [id_usuario, id_permiso]
                                )

                    connection.commit()
                    messages.success(request, "Usuario actualizado correctamente.")
                except Exception as e:
                    connection.rollback()
                    messages.error(request, f"Error al actualizar usuario: {str(e)}")
                    print(f"Error al actualizar usuario: {str(e)}")

                response = redirect('admin_usuarios')
                response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response['Pragma'] = 'no-cache'
                response['Expires'] = '0'
                return response

            # Obtener lista de usuarios
            cursor.execute(
                """
                SELECT 
                    u.id_usuario,
                    u.nombre,
                    u.correo,
                    u.telefono,
                    u.balance_puntos,
                    u.contraseña,
                    DATE_FORMAT(u.fecha_registro, '%d/%m/%Y') AS fecha_registro,
                    r.nombre AS rol
                FROM Usuario u
                JOIN Rol r ON u.id_rol = r.id_rol
                """
            )
            usuarios_raw = cursor.fetchall()

            # Obtener permisos para cada usuario
            usuarios = []
            for usuario in usuarios_raw:
                id_usuario = usuario[0]
                id_rol = None
                cursor.execute("SELECT id_rol FROM Usuario WHERE id_usuario = %s", [id_usuario])
                id_rol_result = cursor.fetchone()
                if id_rol_result:
                    id_rol = id_rol_result[0]

                # Obtener permisos personalizados del usuario (Usuario_Permiso)
                cursor.execute(
                    """
                    SELECT p.nombre
                    FROM Usuario_Permiso up
                    JOIN Permiso p ON up.id_permiso = p.id_permiso
                    WHERE up.id_usuario = %s
                    """,
                    [id_usuario]
                )
                permisos_personalizados = [row[0] for row in cursor.fetchall()]

                # Si el usuario no tiene permisos personalizados, usar los permisos base del rol
                permisos_mostrar = permisos_personalizados
                if not permisos_personalizados:
                    cursor.execute(
                        """
                        SELECT p.nombre
                        FROM Rol_Permiso rp
                        JOIN Permiso p ON rp.id_permiso = p.id_permiso
                        WHERE rp.id_rol = %s
                        """,
                        [id_rol]
                    )
                    permisos_mostrar = [row[0] for row in cursor.fetchall()]

                permisos_str = ", ".join(permisos_mostrar) if permisos_mostrar else ""
                rol_permisos = f"{usuario[7]}: {permisos_str}" if permisos_str else usuario[7]
                usuario_con_permiso = usuario[:7] + (rol_permisos,)
                usuarios.append(usuario_con_permiso)

            # Obtener lista de roles disponibles
            cursor.execute("SELECT nombre FROM Rol")
            roles = [row[0] for row in cursor.fetchall()]

            # Obtener lista de permisos disponibles
            cursor.execute("SELECT nombre FROM Permiso")
            permisos = [row[0] for row in cursor.fetchall()]

            # Permitir añadir nuevos permisos o roles si se envían desde el formulario
            nuevo_permiso = request.POST.get('nuevo_permiso')
            nuevo_rol = request.POST.get('nuevo_rol')
            if nuevo_permiso and request.method == 'POST':
                cursor.execute("SELECT nombre FROM Permiso WHERE nombre = %s", [nuevo_permiso])
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO Permiso (nombre) VALUES (%s)", [nuevo_permiso])
                    connection.commit()
                    permisos.append(nuevo_permiso)
            if nuevo_rol and request.method == 'POST':
                cursor.execute("SELECT nombre FROM Rol WHERE nombre = %s", [nuevo_rol])
                if not cursor.fetchone():
                    cursor.callproc('insertar_rol', [nuevo_rol, ''])
                    connection.commit()
                    roles.append(nuevo_rol)

    except Exception as e:
        messages.error(request, f"Error al cargar usuarios: {str(e)}")
        print(f"Error en admin_usuarios: {str(e)}")

    return render(request, 'reciclaje/admin_usuarios.html', {
        'usuarios': usuarios,
        'roles': roles,
        'permisos': permisos
    })

def admin_registros(request):
    if not es_admin(request):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('dashboard')

    registros = []
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_registro_reciclaje, id_usuario, id_punto_reciclaje, cantidad_kg, 
                       puntos_obtenidos, co2_reducido, fecha_registro, 
                       nombre_subtipo
                FROM Registro_Reciclaje
                """
            )
            registros = cursor.fetchall()
    except Exception as e:
        messages.error(request, f'Error al cargar registros: {str(e)}')
        print(f"Error en admin_registros: {str(e)}")

    return render(request, 'reciclaje/registros.html', {'registros': registros})

def admin_catalogo(request):
    if not es_admin(request):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('dashboard')

    recompensas = []
    try:
        with connection.cursor() as cursor:
            if request.method == 'POST':
                # Manejar la actualización o eliminación de la recompensa
                action = request.POST.get('action')
                id_recompensa = request.POST.get('id_recompensa')
                if action == 'delete':
                    try:
                        cursor.execute(
                            "DELETE FROM Catalogo_Recompensa WHERE id_catalogo_recompensa = %s",
                            [id_recompensa]
                        )
                        connection.commit()
                        messages.success(request, "Recompensa eliminada correctamente.")
                    except Exception as e:
                        connection.rollback()
                        messages.error(request, f"Error al eliminar recompensa: {str(e)}")
                        print(f"Error al eliminar recompensa: {str(e)}")
                else:
                    nombre = request.POST.get('nombre')
                    puntos_coste = request.POST.get('puntos_coste')
                    disponible = request.POST.get('disponible') == 'on'  # Checkbox
                    stock = request.POST.get('stock')
                    descuento = request.POST.get('descuento')
                    categoria = request.POST.get('categoria')

                    try:
                        cursor.execute(
                            """
                            UPDATE Catalogo_Recompensa
                            SET nombre = %s, puntos_coste = %s, disponible = %s, stock = %s, descuento = %s, categoria = %s
                            WHERE id_catalogo_recompensa = %s
                            """,
                            [nombre, puntos_coste, disponible, stock, descuento, categoria, id_recompensa]
                        )
                        connection.commit()
                        messages.success(request, "Recompensa actualizada correctamente.")
                    except Exception as e:
                        connection.rollback()
                        messages.error(request, f"Error al actualizar recompensa: {str(e)}")
                        print(f"Error al actualizar recompensa: {str(e)}")

                response = redirect('admin_catalogo')
                response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response['Pragma'] = 'no-cache'
                response['Expires'] = '0'
                return response

            # Obtener lista de recompensas
            cursor.execute(
                """
                SELECT 
                    id_catalogo_recompensa,  -- Ajustar según la clave primaria real
                    nombre,
                    puntos_coste,
                    disponible,
                    stock,
                    descuento,
                    categoria
                FROM Catalogo_Recompensa
                """
            )
            recompensas = cursor.fetchall()

    except Exception as e:
        messages.error(request, f"Error al cargar recompensas: {str(e)}")
        print(f"Error en admin_catalogo: {str(e)}")

    return render(request, 'reciclaje/admin_catalogo.html', {
        'recompensas': recompensas
    })

def admin_donacion(request):
    if not es_admin(request):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('dashboard')

    donaciones = []
    try:
        with connection.cursor() as cursor:
            if request.method == 'POST':
                # Manejar la actualización, eliminación o creación
                action = request.POST.get('action')
                id_donacion = request.POST.get('id_donacion')
                if action == 'delete':
                    try:
                        cursor.execute(
                            "DELETE FROM Donacion WHERE id_donacion = %s",  # Ajustar según la clave primaria real
                            [id_donacion]
                        )
                        connection.commit()
                        messages.success(request, "Donación eliminada correctamente.")
                    except Exception as e:
                        connection.rollback()
                        messages.error(request, f"Error al eliminar donación: {str(e)}")
                        print(f"Error al eliminar donación: {str(e)}")
                elif action == 'add':
                    nombre = request.POST.get('nombre')
                    puntos_coste = request.POST.get('puntos_coste')
                    disponible = request.POST.get('disponible') == 'on'
                    stock = request.POST.get('stock')
                    descuento = request.POST.get('descuento')
                    categoria = request.POST.get('categoria')
                    try:
                        cursor.execute(
                            """
                            INSERT INTO Donacion (nombre, puntos_coste, disponible, stock, descuento, categoria)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            """,
                            [nombre, puntos_coste, disponible, stock, descuento, categoria]
                        )
                        connection.commit()
                        messages.success(request, "Donación añadida correctamente.")
                    except Exception as e:
                        connection.rollback()
                        messages.error(request, f"Error al añadir donación: {str(e)}")
                        print(f"Error al añadir donación: {str(e)}")
                else:
                    nombre = request.POST.get('nombre')
                    puntos_coste = request.POST.get('puntos_coste')
                    disponible = request.POST.get('disponible') == 'on'
                    stock = request.POST.get('stock')
                    descuento = request.POST.get('descuento')
                    categoria = request.POST.get('categoria')
                    try:
                        cursor.execute(
                            """
                            UPDATE Donacion
                            SET nombre = %s, puntos_coste = %s, disponible = %s, stock = %s, descuento = %s, categoria = %s
                            WHERE id_donacion = %s
                            """,
                            [nombre, puntos_coste, disponible, stock, descuento, categoria, id_donacion]
                        )
                        connection.commit()
                        messages.success(request, "Donación actualizada correctamente.")
                    except Exception as e:
                        connection.rollback()
                        messages.error(request, f"Error al actualizar donación: {str(e)}")
                        print(f"Error al actualizar donación: {str(e)}")

                response = redirect('admin_donacion')
                response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response['Pragma'] = 'no-cache'
                response['Expires'] = '0'
                return response

            # Obtener lista de donaciones
            cursor.execute(
                """
                SELECT 
                    id_donacion,  -- Ajustar según la clave primaria real
                    nombre,
                    puntos_coste,
                    disponible,
                    stock,
                    descuento,
                    categoria
                FROM Donacion
                """
            )
            donaciones = cursor.fetchall()

    except Exception as e:
        messages.error(request, f"Error al cargar donaciones: {str(e)}")
        print(f"Error en admin_donacion: {str(e)}")

    return render(request, 'reciclaje/admin_donacion.html', {
        'donacion': donaciones
    })

    
def admin_historial(request):
    if not es_admin(request):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('dashboard')
    return render(request, 'reciclaje/admin_historial.html')

def bitacora_reciclaje(request):
    if not es_admin(request):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('dashboard')

    bitacora = []
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_bitacora_reciclaje, ip, id_registro_reciclaje, accion, 
                       DATE_FORMAT(fecha_accion, '%%d/%%m/%%Y') AS fecha_accion, detalle
                FROM Bitacora_Reciclaje
                """
            )
            bitacora = cursor.fetchall()
    except Exception as e:
        messages.error(request, f'Error al cargar bitácora: {str(e)}')
        print(f"Error en bitacora_reciclaje: {str(e)}")

    return render(request, 'reciclaje/bitacora_reciclaje.html', {'bitacora': bitacora})

def bitacora_catalogo(request):
    if not es_admin(request):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('dashboard')

    bitacora = []
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_bitacora_catalogo, ip, id_catalogo_recompensa, accion, 
                       DATE_FORMAT(fecha_accion, '%%d/%%m/%%Y') AS fecha_accion, detalle
                FROM Bitacora_Catalogo
                """
            )
            bitacora = cursor.fetchall()
    except Exception as e:
        messages.error(request, f'Error al cargar bitácora: {str(e)}')
        print(f"Error en bitacora_catalogo: {str(e)}")

    return render(request, 'reciclaje/bitacora_catalogo.html', {'bitacora': bitacora})

def bitacora_canje(request):
    if not es_admin(request):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('dashboard')

    bitacora = []
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_bitacora_canje, ip, id_canje_recompensa, id_catalogo_recompensa, accion, 
                       DATE_FORMAT(fecha_accion, '%%d/%%m/%%Y') AS fecha_accion, detalle
                FROM Bitacora_Canje
                """
            )
            bitacora = cursor.fetchall()
    except Exception as e:
        messages.error(request, f'Error al cargar bitácora: {str(e)}')
        print(f"Error en bitacora_canje: {str(e)}")

    return render(request, 'reciclaje/bitacora_canje.html', {'bitacora': bitacora})