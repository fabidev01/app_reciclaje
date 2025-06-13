from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection

def es_admin(request):
    user_id = request.session.get('user_id')
    if not user_id:
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
                [user_id]
            )
            rol = cursor.fetchone()
            if rol:
                return rol[0] == 'Administrador'
            return False
    except Exception as e:
        print(f"Error al verificar rol: {str(e)}")
        return False

# Panel de administración
def admin_panel(request):
    if not es_admin(request):
        if request.session.get('user_id'):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('dashboard')
        else:
            return redirect('login')
    return render(request, 'administrador/admin.html')

# Gestión de usuarios
def admin_usuarios(request):
    if not es_admin(request):
        if request.session.get('user_id'):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('dashboard')
        else:
            return redirect('login')

    usuarios = []
    roles = []
    permisos = []
    try:
        with connection.cursor() as cursor:
            if request.method == 'POST':
                id_usuario = request.POST.get('id_usuario')
                rol_seleccionado = request.POST.get('rol')
                permisos_seleccionados = request.POST.get('permisos', '').split(',')

                cursor.execute("SELECT id_rol FROM Rol WHERE nombre = %s", [rol_seleccionado])
                selected_rol_id_result = cursor.fetchone()
                if not selected_rol_id_result:
                    raise Exception(f"Rol '{rol_seleccionado}' no encontrado.")
                selected_rol_id = selected_rol_id_result[0]

                cursor.execute(
                    "UPDATE Usuario SET id_rol = %s WHERE id_usuario = %s",
                    [selected_rol_id, id_usuario]
                )

                cursor.execute("DELETE FROM Usuario_Permiso WHERE id_usuario = %s", [id_usuario])
                for permiso in permisos_seleccionados:
                    if permiso:
                        cursor.execute("SELECT id_permiso FROM Permiso WHERE nombre = %s", [permiso])
                        id_permiso_result = cursor.fetchone()
                        if id_permiso_result:
                            id_permiso = id_permiso_result[0]
                            cursor.execute(
                                "INSERT INTO Usuario_Permiso (id_usuario, id_permiso) VALUES (%s, %s)",
                                [id_usuario, id_permiso]
                            )

                connection.commit()
                messages.success(request, "Usuario actualizado correctamente.")
                return redirect('admin_usuarios')

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

            usuarios = []
            for usuario in usuarios_raw:
                id_usuario = usuario[0]
                cursor.execute("SELECT id_rol FROM Usuario WHERE id_usuario = %s", [id_usuario])
                id_rol = cursor.fetchone()[0]

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

                permisos_mostrar = permisos_personalizados if permisos_personalizados else [
                    row[0] for row in cursor.execute(
                        """
                        SELECT p.nombre
                        FROM Rol_Permiso rp
                        JOIN Permiso p ON rp.id_permiso = p.id_permiso
                        WHERE rp.id_rol = %s
                        """,
                        [id_rol]
                    ).fetchall()
                ]
                permisos_str = ", ".join(permisos_mostrar) if permisos_mostrar else ""
                rol_permisos = f"{usuario[7]}: {permisos_str}" if permisos_str else usuario[7]
                usuarios.append(usuario[:7] + (rol_permisos,))

            cursor.execute("SELECT nombre FROM Rol")
            roles = [row[0] for row in cursor.fetchall()]

            cursor.execute("SELECT nombre FROM Permiso")
            permisos = [row[0] for row in cursor.fetchall()]

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

    response = render(request, 'administrador/admin_usuarios.html', {
        'usuarios': usuarios,
        'roles': roles,
        'permisos': permisos
    })
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Otras vistas de admin (mantenidas iguales con la lógica corregida)
def admin_registros(request):
    if not es_admin(request):
        if request.session.get('user_id'):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('dashboard')
        else:
            return redirect('login')
    registros = []
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_registro_reciclaje, id_usuario, id_punto_reciclaje, cantidad_kg, 
                       puntos_obtenidos, co2_reducido, fecha_registro, nombre_subtipo
                FROM Registro_Reciclaje
                """
            )
            registros = cursor.fetchall()
    except Exception as e:
        messages.error(request, f'Error al cargar registros: {str(e)}')
    return render(request, 'administrador/registros.html', {'registros': registros})

def admin_catalogo(request):
    if not es_admin(request):
        if request.session.get('user_id'):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('dashboard')
        else:
            return redirect('login')
    recompensas = []
    try:
        with connection.cursor() as cursor:
            if request.method == 'POST':
                action = request.POST.get('action')
                id_recompensa = request.POST.get('id_recompensa')
                if action == 'delete':
                    cursor.execute("DELETE FROM Catalogo_Recompensa WHERE id_catalogo_recompensa = %s", [id_recompensa])
                    connection.commit()
                    messages.success(request, "Recompensa eliminada correctamente.")
                else:
                    nombre = request.POST.get('nombre')
                    puntos_coste = request.POST.get('puntos_coste')
                    disponible = request.POST.get('disponible') == 'on'
                    stock = request.POST.get('stock')
                    descuento = request.POST.get('descuento')
                    categoria = request.POST.get('categoria')
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
                return redirect('admin_catalogo')
            cursor.execute(
                """
                SELECT id_catalogo_recompensa, nombre, puntos_coste, disponible, stock, descuento, categoria
                FROM Catalogo_Recompensa
                """
            )
            recompensas = cursor.fetchall()
    except Exception as e:
        messages.error(request, f"Error al cargar recompensas: {str(e)}")
    return render(request, 'administrador/admin_catalogo.html', {'recompensas': recompensas})

def admin_donacion(request):
    if not es_admin(request):
        if request.session.get('user_id'):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('dashboard')
        else:
            return redirect('login')
    donaciones = []
    try:
        with connection.cursor() as cursor:
            if request.method == 'POST':
                action = request.POST.get('action')
                id_donacion = request.POST.get('id_donacion')
                if action == 'delete':
                    cursor.execute("DELETE FROM Donacion WHERE id_donacion = %s", [id_donacion])
                    connection.commit()
                    messages.success(request, "Donación eliminada correctamente.")
                elif action == 'add':
                    nombre = request.POST.get('nombre')
                    monto_donacion = request.POST.get('monto_donacion')
                    cursor.execute(
                        "INSERT INTO Donacion (nombre, monto_donacion) VALUES (%s, %s)",
                        [nombre, monto_donacion]
                    )
                    connection.commit()
                    messages.success(request, "Donación añadida correctamente.")
                else:
                    nombre = request.POST.get('nombre')
                    monto_donacion = request.POST.get('monto_donacion')
                    cursor.execute(
                        "UPDATE Donacion SET nombre = %s, monto_donacion = %s WHERE id_donacion = %s",
                        [nombre, monto_donacion, id_donacion]
                    )
                    connection.commit()
                    messages.success(request, "Donación actualizada correctamente.")
                return redirect('admin_donacion')
            cursor.execute("SELECT id_donacion, nombre, monto_donacion FROM Donacion")
            donaciones = cursor.fetchall()
    except Exception as e:
        messages.error(request, f"Error al cargar donaciones: {str(e)}")
    return render(request, 'administrador/admin_donacion.html', {'donacion': donaciones})

def admin_historial(request):
    if not es_admin(request):
        if request.session.get('user_id'):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('dashboard')
        else:
            return redirect('login')
    return render(request, 'administrador/admin_historial.html')

def bitacora_reciclaje(request):
    if not es_admin(request):
        if request.session.get('user_id'):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('dashboard')
        else:
            return redirect('login')
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
    return render(request, 'administrador/bitacora_reciclaje.html', {'bitacora': bitacora})

def bitacora_catalogo(request):
    if not es_admin(request):
        if request.session.get('user_id'):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('dashboard')
        else:
            return redirect('login')
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
    return render(request, 'administrador/bitacora_catalogo.html', {'bitacora': bitacora})

def bitacora_canje(request):
    if not es_admin(request):
        if request.session.get('user_id'):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('dashboard')
        else:
            return redirect('login')
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
    return render(request, 'administrador/bitacora_canje.html', {'bitacora': bitacora})