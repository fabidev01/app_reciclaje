from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from datetime import datetime
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
import logging
logger = logging.getLogger(__name__)

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

    current_date_time = datetime.now().strftime("%I:%M %p -%H, %A %d de %B de %Y")
    stats = {}
    try:
        with connection.cursor() as cursor:
            # Contar usuarios
            cursor.execute("SELECT COUNT(*) FROM Usuario")
            stats['usuarios'] = cursor.fetchone()[0]

            # Contar materiales reciclables
            cursor.execute("SELECT COUNT(*) FROM Material_Reciclable")
            stats['materiales'] = cursor.fetchone()[0]

            # Contar puntos de reciclaje
            cursor.execute("SELECT COUNT(*) FROM Punto_Reciclaje")
            stats['puntos'] = cursor.fetchone()[0]

            # Contar registros de reciclaje
            cursor.execute("SELECT COUNT(*) FROM Registro_Reciclaje")
            stats['registros'] = cursor.fetchone()[0]

            # Contar recompensas en catálogo
            cursor.execute("SELECT COUNT(*) FROM Catalogo_Recompensa")
            stats['catalogo'] = cursor.fetchone()[0]

            # Contar donaciones
            cursor.execute("SELECT COUNT(*) FROM Donacion")
            stats['donaciones'] = cursor.fetchone()[0]

    except Exception as e:
        messages.error(request, f'Error al cargar las estadísticas: {str(e)}')

    response = render(request, 'administrador/admin_panel.html', {
        'current_date_time': current_date_time,
        'stats': stats
    })
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def admin_rol(request):
    if not es_admin(request):
        if request.session.get('user_id'):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return HttpResponseRedirect('dashboard')
        else:
            return HttpResponseRedirect('login')

    roles = []
    permisos = []
    try:
        with connection.cursor() as cursor:
            # Obtener todos los roles con descripción y nombres de permisos
            cursor.execute("""
                SELECT r.id_rol, r.nombre, r.descripcion, GROUP_CONCAT(p.nombre SEPARATOR ', ') as permisos
                FROM Rol r
                LEFT JOIN Rol_Permiso rp ON r.id_rol = rp.id_rol
                LEFT JOIN Permiso p ON rp.id_permiso = p.id_permiso
                GROUP BY r.id_rol, r.nombre, r.descripcion
            """)
            roles = cursor.fetchall()

            # Obtener todos los permisos disponibles con IDs y nombres
            cursor.execute("SELECT id_permiso, nombre FROM Permiso")
            permisos = dict(cursor.fetchall())

        if request.method == 'POST':
            action = request.POST.get('action')
            with connection.cursor() as cursor:
                if action == 'add':
                    nombre = request.POST.get('nombre')
                    descripcion = request.POST.get('descripcion')
                    permisos_ids = request.POST.get('permisos', '').split(',')
                    print(f"Permisos recibidos (Añadir): {permisos_ids}")  # Depuración
                    if nombre and descripcion:
                        try:
                            cursor.callproc('insertar_rol', [nombre, descripcion])
                            cursor.execute("SELECT LAST_INSERT_ID()")
                            rol_id = cursor.fetchone()[0]
                            if not rol_id:
                                raise Exception("No se pudo obtener el ID del rol recién creado.")
                            connection.commit()
                            valid_permisos_ids = [int(pid) for pid in permisos_ids if pid.isdigit() and pid]
                            print(f"Permisos válidos a insertar (Añadir): {valid_permisos_ids}")
                            if valid_permisos_ids:
                                for permiso_id in valid_permisos_ids:
                                    cursor.callproc('insertar_rol_permiso', [rol_id, permiso_id])
                            connection.commit()
                            messages.success(request, 'Rol añadido correctamente.')
                        except Exception as e:
                            connection.rollback()
                            messages.error(request, f'Error al añadir el rol: {str(e)}')
                    else:
                        messages.error(request, 'El nombre y la descripción del rol no pueden estar vacíos.')
                elif action == 'update':
                    rol_id = request.POST.get('id_rol')
                    nombre = request.POST.get('nombre')
                    descripcion = request.POST.get('descripcion')
                    permisos_ids = request.POST.get('permisos', '').split(',')
                    print(f"Permisos recibidos (Editar): {permisos_ids}")  # Depuración
                    if rol_id and nombre and descripcion:
                        try:
                            cursor.callproc('actualizar_rol', [rol_id, nombre, descripcion])
                            cursor.execute("DELETE FROM Rol_Permiso WHERE id_rol = %s", [rol_id])
                            valid_permisos_ids = [int(pid) for pid in permisos_ids if pid.isdigit() and pid]
                            print(f"Permisos válidos a insertar (Editar): {valid_permisos_ids}")
                            if valid_permisos_ids:
                                for permiso_id in valid_permisos_ids:
                                    cursor.callproc('insertar_rol_permiso', [rol_id, permiso_id])
                            connection.commit()
                            messages.success(request, 'Rol modificado correctamente.')
                        except Exception as e:
                            connection.rollback()
                            messages.error(request, f'Error al modificar el rol: {str(e)}')
                    else:
                        messages.error(request, 'El nombre y la descripción del rol no pueden estar vacíos.')
                elif action == 'delete':
                    rol_id = request.POST.get('id_rol')
                    if rol_id:
                        try:
                            cursor.execute("DELETE FROM Rol_Permiso WHERE id_rol = %s", [rol_id])
                            cursor.callproc('eliminar_rol', [rol_id])
                            connection.commit()
                            messages.success(request, 'Rol eliminado correctamente.')
                        except Exception as e:
                            connection.rollback()
                            messages.error(request, f'Error al eliminar el rol: {str(e)}')
                elif action == 'add_permiso':
                    nombre_permiso = request.POST.get('nombre_permiso')
                    if nombre_permiso:
                        try:
                            cursor.callproc('insertar_permiso', [nombre_permiso])
                            connection.commit()
                            messages.success(request, 'Permiso añadido correctamente.')
                        except Exception as e:
                            connection.rollback()
                            messages.error(request, f'Error al añadir el permiso: {str(e)}')
                    else:
                        messages.error(request, 'El nombre del permiso no puede estar vacío.')
                elif action == 'update_permiso':
                    permiso_id = request.POST.get('id_permiso')
                    nombre_permiso = request.POST.get('nombre_permiso')
                    if permiso_id and nombre_permiso:
                        try:
                            cursor.callproc('actualizar_permiso', [permiso_id, nombre_permiso])
                            connection.commit()
                            messages.success(request, 'Permiso modificado correctamente.')
                        except Exception as e:
                            connection.rollback()
                            messages.error(request, f'Error al modificar el permiso: {str(e)}')
                    else:
                        messages.error(request, 'El nombre del permiso no puede estar vacío.')
                elif action == 'delete_permiso':
                    permiso_id = request.POST.get('id_permiso')
                    if permiso_id:
                        try:
                            cursor.callproc('eliminar_permiso', [permiso_id])
                            connection.commit()
                            messages.success(request, 'Permiso eliminado correctamente.')
                        except Exception as e:
                            connection.rollback()
                            messages.error(request, f'Error al eliminar el permiso: {str(e)}')
            return redirect('admin_rol')

    except Exception as e:
        messages.error(request, f'Error al cargar los datos: {str(e)}')

    return render(request, 'administrador/admin_rol.html', {
        'roles': roles,
        'permisos_disponibles': permisos.items()
    })

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
                action = request.POST.get('action')
                if action == 'update':
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
                elif action == 'add':
                    nombre = request.POST.get('nombre')
                    correo = request.POST.get('correo')
                    telefono = request.POST.get('telefono')
                    balance_puntos = request.POST.get('balance_puntos', 0)
                    rol_seleccionado = request.POST.get('rol')
                    contraseña = request.POST.get('contraseña')  # Generar o recibir contraseña

                    cursor.execute("SELECT id_rol FROM Rol WHERE nombre = %s", [rol_seleccionado])
                    selected_rol_id_result = cursor.fetchone()
                    if not selected_rol_id_result:
                        raise Exception(f"Rol '{rol_seleccionado}' no encontrado.")
                    selected_rol_id = selected_rol_id_result[0]

                    # Insertar nuevo usuario (contraseña debe ser hasheada en producción)
                    cursor.execute(
                        """
                        INSERT INTO Usuario (nombre, correo, telefono, balance_puntos, contraseña, id_rol, fecha_registro)
                        VALUES (%s, %s, %s, %s, %s, %s, NOW())
                        """,
                        [nombre, correo, telefono, balance_puntos, contraseña, selected_rol_id]
                    )
                    connection.commit()
                    messages.success(request, "Usuario añadido correctamente.")

                return redirect('admin_usuarios')

            # Obtener lista de usuarios (sin contraseña)
            cursor.execute(
                """
                SELECT 
                    u.id_usuario,
                    u.nombre,
                    u.correo,
                    u.telefono,
                    u.balance_puntos,
                    DATE_FORMAT(u.fecha_registro, '%d/%m/%Y') AS fecha_registro,
                    r.nombre AS rol
                FROM Usuario u
                JOIN Rol r ON u.id_rol = r.id_rol
                """
            )
            usuarios_raw = cursor.fetchall()

            # Procesar cada usuario para incluir permisos
            for usuario in usuarios_raw:
                id_usuario = usuario[0]
                cursor.execute("SELECT id_rol FROM Usuario WHERE id_usuario = %s", [id_usuario])
                id_rol = cursor.fetchone()[0]

                # Obtener permisos personalizados
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

                # Si no hay permisos personalizados, obtener los del rol
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
                    permisos_personalizados = [row[0] for row in cursor.fetchall()]

                permisos_str = ", ".join(permisos_personalizados) if permisos_personalizados else ""
                rol_permisos = f"{usuario[6]}: {permisos_str}" if permisos_str else usuario[6]
                usuarios.append(usuario[:6] + (rol_permisos,))

            # Obtener roles y permisos disponibles
            cursor.execute("SELECT nombre FROM Rol")
            roles = [row[0] for row in cursor.fetchall()]

            cursor.execute("SELECT nombre FROM Permiso")
            permisos = [row[0] for row in cursor.fetchall()]

            # Manejo de nuevos roles y permisos
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
                    cursor.callproc('insertar_rol', [nuevo_rol, ''])  # Asegúrate de que este procedimiento existe
                    connection.commit()
                    roles.append(nuevo_rol)

    except Exception as e:
        messages.error(request, f"Error al cargar usuarios: {str(e)}")

    response = render(request, 'administrador/admin_usuarios.html', {
        'usuarios': usuarios,
        'roles': roles,
        'permisos': permisos
    })
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Otras vistas de admin (ajustadas con cabeceras de caché)

def admin_registros(request):
    if not es_admin(request):
        if request.session.get('user_id'):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return HttpResponseRedirect('dashboard')
        else:
            return HttpResponseRedirect('login')
    
    registros = []
    material_stats = []
    user_activity = []
    impacto_ambiental = []
    total_co2_all = 0
    total_puntos_all = 0
    total_kg_all = 0
    max_puntos_material = None

    # Filtros
    reg_user_filter = request.GET.get('reg_user_filter', '')
    reg_material_filter = request.GET.get('reg_material_filter', '')
    reg_point_filter = request.GET.get('reg_point_filter', '')
    reg_day_filter = request.GET.get('reg_day_filter', '')
    reg_month_filter = request.GET.get('reg_month_filter', '')
    reg_year_filter = request.GET.get('reg_year_filter', '')
    user_filter = request.GET.get('user_filter', '')
    impacto_mes_filter = request.GET.get('impacto_mes_filter', '')
    impacto_anno_filter = request.GET.get('impacto_anno_filter', '')
    order_by = request.GET.get('order_by', '')
    group_by = request.GET.get('group_by', '')

    try:
        with connection.cursor() as cursor:
            # Consulta de registros con filtros combinables
            query = """
                SELECT 
                    rr.id_registro_reciclaje,
                    u.nombre AS nombre_usuario,
                    u.correo AS correo_usuario,
                    mr.nombre AS nombre_material,
                    pr.nombre AS nombre_punto,
                    rr.puntos_obtenidos,
                    rr.cantidad_kg,
                    rr.co2_reducido,
                    rr.fecha_registro
                FROM Registro_Reciclaje rr
                LEFT JOIN Usuario u ON rr.id_usuario = u.id_usuario
                LEFT JOIN Punto_Reciclaje pr ON rr.id_punto_reciclaje = pr.id_punto_reciclaje
                LEFT JOIN Material_Reciclable mr ON rr.id_material_reciclable = mr.id_material_reciclable
                WHERE 1=1
            """
            params = []
            if reg_user_filter:
                query += " AND (u.id_usuario = %s OR u.correo LIKE %s OR u.nombre LIKE %s)"
                try:
                    user_id = int(reg_user_filter) if reg_user_filter.isdigit() else None
                    params.append(user_id if user_id else reg_user_filter)
                except ValueError:
                    params.append(reg_user_filter)
                params.extend(['%' + reg_user_filter + '%', '%' + reg_user_filter + '%'])
            if reg_material_filter:
                query += " AND (mr.id_material_reciclable = %s OR mr.nombre LIKE %s)"
                try:
                    material_id = int(reg_material_filter) if reg_material_filter.isdigit() else None
                    params.append(material_id if material_id else reg_material_filter)
                except ValueError:
                    params.append(reg_material_filter)
                params.append('%' + reg_material_filter + '%')
            if reg_point_filter:
                query += " AND (pr.id_punto_reciclaje = %s OR pr.nombre LIKE %s)"
                try:
                    point_id = int(reg_point_filter) if reg_point_filter.isdigit() else None
                    params.append(point_id if point_id else reg_point_filter)
                except ValueError:
                    params.append(reg_point_filter)
                params.append('%' + reg_point_filter + '%')
            if reg_day_filter:
                query += " AND DAY(rr.fecha_registro) = %s"
                try:
                    day = int(reg_day_filter)
                    if 1 <= day <= 31:
                        params.append(day)
                    else:
                        messages.error(request, 'Día inválido. Use un valor entre 1 y 31.')
                except ValueError:
                    messages.error(request, 'Día inválido. Use un valor numérico.')
            if reg_month_filter:
                query += " AND MONTH(rr.fecha_registro) = %s"
                try:
                    month = int(reg_month_filter)
                    if 1 <= month <= 12:
                        params.append(month)
                    else:
                        messages.error(request, 'Mes inválido. Use un valor entre 1 y 12.')
                except ValueError:
                    messages.error(request, 'Mes inválido. Use un valor numérico.')
            if reg_year_filter:
                query += " AND YEAR(rr.fecha_registro) = %s"
                try:
                    year = int(reg_year_filter)
                    params.append(year)
                except ValueError:
                    messages.error(request, 'Año inválido. Use un valor numérico.')
            if order_by:
                order_mapping = {
                    'kg': 'rr.cantidad_kg DESC',
                    'puntos': 'rr.puntos_obtenidos DESC',
                    'co2': 'rr.co2_reducido DESC',
                    'fecha': 'rr.fecha_registro DESC'
                }
                order_field = order_mapping.get(order_by, 'rr.id_registro_reciclaje')
                query += f" ORDER BY {order_field}"
            cursor.execute(query, params)
            registros = cursor.fetchall()

            # Total por tipo de material
            cursor.execute(
                """
                SELECT 
                    mr.nombre,
                    SUM(rr.cantidad_kg) AS total_kg,
                    SUM(rr.co2_reducido) AS total_co2,
                    SUM(rr.puntos_obtenidos) AS total_puntos
                FROM Registro_Reciclaje rr
                JOIN Material_Reciclable mr ON rr.id_material_reciclable = mr.id_material_reciclable
                GROUP BY mr.id_material_reciclable, mr.nombre
                """
            )
            material_stats = cursor.fetchall()

            # Totales generales
            cursor.execute(
                """
                SELECT 
                    SUM(co2_reducido) AS total_co2, 
                    SUM(puntos_obtenidos) AS total_puntos,
                    SUM(cantidad_kg) AS total_kg
                FROM Registro_Reciclaje
                """
            )
            result = cursor.fetchone()
            total_co2_all = round(result[0], 3) if result[0] else 0
            total_puntos_all = round(result[1], 3) if result[1] else 0
            total_kg_all = round(result[2], 3) if result[2] else 0

            # Material con mayor puntos
            cursor.execute(
                """
                SELECT mr.nombre, SUM(rr.puntos_obtenidos) AS max_puntos
                FROM Registro_Reciclaje rr
                JOIN Material_Reciclable mr ON rr.id_material_reciclable = mr.id_material_reciclable
                GROUP BY mr.id_material_reciclable, mr.nombre
                ORDER BY max_puntos DESC
                LIMIT 1
                """
            )
            max_puntos_material = cursor.fetchone()

            # Actividad agrupada según group_by o user_filter
            if group_by or user_filter:
                if group_by == 'usuario_material' or user_filter:
                    query = """
                        SELECT 
                            u.id_usuario AS id,
                            u.nombre AS usuario,
                            mr.nombre AS material,
                            SUM(rr.cantidad_kg) AS total_kg,
                            SUM(rr.puntos_obtenidos) AS total_puntos,
                            SUM(rr.co2_reducido) AS total_co2
                        FROM Registro_Reciclaje rr
                        JOIN Usuario u ON rr.id_usuario = u.id_usuario
                        JOIN Material_Reciclable mr ON rr.id_material_reciclable = mr.id_material_reciclable
                        WHERE 1=1
                    """
                    params = []
                    if reg_user_filter or user_filter:
                        query += " AND (u.id_usuario = %s OR u.correo LIKE %s OR u.nombre LIKE %s)"
                        user_id_to_filter = user_filter if user_filter else reg_user_filter
                        try:
                            user_id = int(user_id_to_filter) if user_id_to_filter.isdigit() else None
                            params.append(user_id if user_id else user_id_to_filter)
                        except ValueError:
                            params.append(user_id_to_filter)
                        params.extend(['%' + user_id_to_filter + '%', '%' + user_id_to_filter + '%'])
                    if reg_material_filter:
                        query += " AND (mr.id_material_reciclable = %s OR mr.nombre LIKE %s)"
                        try:
                            material_id = int(reg_material_filter) if reg_material_filter.isdigit() else None
                            params.append(material_id if material_id else reg_material_filter)
                        except ValueError:
                            params.append(reg_material_filter)
                        params.append('%' + reg_material_filter + '%')
                    if reg_day_filter:
                        query += " AND DAY(rr.fecha_registro) = %s"
                        try:
                            day = int(reg_day_filter)
                            if 1 <= day <= 31:
                                params.append(day)
                        except ValueError:
                            pass
                    if reg_month_filter:
                        query += " AND MONTH(rr.fecha_registro) = %s"
                        try:
                            month = int(reg_month_filter)
                            if 1 <= month <= 12:
                                params.append(month)
                        except ValueError:
                            pass
                    if reg_year_filter:
                        query += " AND YEAR(rr.fecha_registro) = %s"
                        try:
                            year = int(reg_year_filter)
                            params.append(year)
                        except ValueError:
                            pass
                    query += " GROUP BY u.id_usuario, u.nombre, mr.id_material_reciclable, mr.nombre"
                    query += " ORDER BY CASE WHEN mr.nombre = 'Plástico' THEN 0 ELSE 1 END, mr.id_material_reciclable ASC"
                    cursor.execute(query, params)
                    user_activity = cursor.fetchall()

                elif group_by == 'usuario_punto':
                    query = """
                        SELECT 
                            u.id_usuario AS id,
                            u.nombre AS usuario,
                            pr.id_punto_reciclaje AS punto_id,
                            pr.nombre AS punto_nombre,
                            SUM(rr.cantidad_kg) AS total_kg,
                            SUM(rr.puntos_obtenidos) AS total_puntos,
                            SUM(rr.co2_reducido) AS total_co2
                        FROM Registro_Reciclaje rr
                        JOIN Usuario u ON rr.id_usuario = u.id_usuario
                        LEFT JOIN Punto_Reciclaje pr ON rr.id_punto_reciclaje = pr.id_punto_reciclaje
                        WHERE 1=1
                    """
                    params = []
                    if reg_user_filter:
                        query += " AND (u.id_usuario = %s OR u.correo LIKE %s OR u.nombre LIKE %s)"
                        try:
                            user_id = int(reg_user_filter) if reg_user_filter.isdigit() else None
                            params.append(user_id if user_id else reg_user_filter)
                        except ValueError:
                            params.append(reg_user_filter)
                        params.extend(['%' + reg_user_filter + '%', '%' + reg_user_filter + '%'])
                    if reg_point_filter:
                        query += " AND (pr.id_punto_reciclaje = %s OR pr.nombre LIKE %s)"
                        try:
                            point_id = int(reg_point_filter) if reg_point_filter.isdigit() else None
                            params.append(point_id if point_id else reg_point_filter)
                        except ValueError:
                            params.append(reg_point_filter)
                        params.append('%' + reg_point_filter + '%')
                    if reg_day_filter:
                        query += " AND DAY(rr.fecha_registro) = %s"
                        try:
                            day = int(reg_day_filter)
                            if 1 <= day <= 31:
                                params.append(day)
                        except ValueError:
                            pass
                    if reg_month_filter:
                        query += " AND MONTH(rr.fecha_registro) = %s"
                        try:
                            month = int(reg_month_filter)
                            if 1 <= month <= 12:
                                params.append(month)
                        except ValueError:
                            pass
                    if reg_year_filter:
                        query += " AND YEAR(rr.fecha_registro) = %s"
                        try:
                            year = int(reg_year_filter)
                            params.append(year)
                        except ValueError:
                            pass
                    query += " GROUP BY u.id_usuario, u.nombre, pr.id_punto_reciclaje, pr.nombre"
                    query += " ORDER BY pr.nombre ASC"  # Ordenamiento por nombre de punto
                    cursor.execute(query, params)
                    user_activity = cursor.fetchall()

            # Impacto ambiental diario
            current_date = datetime.now().date()  # 06:20 AM -04 on Saturday, June 28, 2025
            query = """
                SELECT 
                    id_impacto_ambiental_diario,
                    fecha_dia,
                    tipo_basura,
                    unidad_medida,
                    cantidad_reciclada_por_tipo,
                    co2_reducido_por_tipo
                FROM Impacto_Ambiental_Diario
                WHERE 1=1
            """
            params = []
            if not impacto_mes_filter and not impacto_anno_filter:
                query += " AND DATE(fecha_dia) = %s"
                params.append(current_date)
            elif impacto_mes_filter:
                query += " AND MONTH(fecha_dia) = %s"
                params.append(impacto_mes_filter)
            if impacto_anno_filter:
                query += " AND YEAR(fecha_dia) = %s"
                params.append(impacto_anno_filter)
            query += " ORDER BY fecha_dia DESC"
            cursor.execute(query, params)
            impacto_ambiental = cursor.fetchall()

    except Exception as e:
        messages.error(request, f'Error al cargar registros: {str(e)}')

    response = render(request, 'administrador/registros.html', {
        'registros': registros,
        'material_stats': material_stats,
        'total_co2_all': total_co2_all,
        'total_puntos_all': total_puntos_all,
        'total_kg_all': total_kg_all,
        'max_puntos_material': max_puntos_material,
        'user_activity': user_activity,
        'reg_user_filter': reg_user_filter,
        'reg_material_filter': reg_material_filter,
        'reg_point_filter': reg_point_filter,
        'reg_day_filter': reg_day_filter,
        'reg_month_filter': reg_month_filter,
        'reg_year_filter': reg_year_filter,
        'user_filter': user_filter,
        'impacto_ambiental': impacto_ambiental,
        'impacto_mes_filter': impacto_mes_filter,
        'impacto_anno_filter': impacto_anno_filter,
        'order_by': order_by,
        'group_by': group_by
    })
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

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
                    # Verificar si hay canjes asociados
                    cursor.execute(
                        "SELECT COUNT(*) FROM Canje_Recompensa WHERE id_catalogo_recompensa = %s",
                        [id_recompensa]
                    )
                    canjes_existentes = cursor.fetchone()[0]
                    if canjes_existentes > 0:
                        messages.error(request, "No se puede eliminar esta recompensa porque tiene canjes asociados.")
                    else:
                        # Verificar bitácoras asociadas
                        cursor.execute(
                            "SELECT COUNT(*) FROM Bitacora_Catalogo WHERE id_catalogo_recompensa = %s",
                            [id_recompensa]
                        )
                        bitacoras_existentes = cursor.fetchone()[0]
                        if bitacoras_existentes > 0:
                            # Desactivar en lugar de eliminar
                            cursor.execute(
                                "UPDATE Catalogo_Recompensa SET disponible = FALSE WHERE id_catalogo_recompensa = %s",
                                [id_recompensa]
                            )
                            connection.commit()
                            messages.success(request, "Recompensa desactivada correctamente (no eliminada por bitácoras asociadas).")
                        else:
                            cursor.execute("DELETE FROM Catalogo_Recompensa WHERE id_catalogo_recompensa = %s", [id_recompensa])
                            connection.commit()
                            messages.success(request, "Recompensa eliminada correctamente.")
                elif action == 'add':
                    nombre = request.POST.get('nombre')
                    puntos_coste = request.POST.get('puntos_coste')
                    disponible = request.POST.get('disponible') == 'on'
                    stock = request.POST.get('stock')
                    descuento = request.POST.get('descuento')
                    categoria = request.POST.get('categoria')
                    cursor.execute("SELECT COALESCE(MAX(id_catalogo_recompensa), 0) + 1 FROM Catalogo_Recompensa")
                    nuevo_id = cursor.fetchone()[0]
                    ruta_imagen = f'img/catalogo/img-{nuevo_id}.png'
                    cursor.callproc('insertar_catalogo_recompensa', [
                        nombre, puntos_coste, disponible, stock, descuento, categoria, ruta_imagen
                    ])
                    connection.commit()
                    messages.success(request, "Recompensa agregada correctamente.")
                else:  # update
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
                SELECT id_catalogo_recompensa, nombre, puntos_coste, disponible, stock, descuento, categoria, ruta_imagen
                FROM Catalogo_Recompensa
                """
            )
            recompensas = cursor.fetchall()
    except Exception as e:
        messages.error(request, f"Error al cargar recompensas: {str(e)}")
    response = render(request, 'administrador/admin_catalogo.html', {'recompensas': recompensas})
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

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
                    # Verificar si hay canjes asociados
                    cursor.execute(
                        "SELECT COUNT(*) FROM Canje_Donacion WHERE id_donacion = %s",
                        [id_donacion]
                    )
                    canjes_existentes = cursor.fetchone()[0]
                    if canjes_existentes > 0:
                        messages.error(request, "No se puede eliminar esta donación porque tiene canjes asociados.")
                    else:
                        cursor.execute("DELETE FROM Donacion WHERE id_donacion = %s", [id_donacion])
                        connection.commit()
                        messages.success(request, "Donación eliminada correctamente.")
                elif action == 'add':
                    nombre = request.POST.get('nombre')
                    entidad_donacion = request.POST.get('entidad_donacion')
                    monto_donacion = request.POST.get('monto_donacion')
                    # Generar una ruta de imagen basada en el siguiente ID
                    cursor.execute("SELECT COALESCE(MAX(id_donacion), 0) + 1 FROM Donacion")
                    nuevo_id = cursor.fetchone()[0]
                    ruta_imagen = f'img/donacion/img-{nuevo_id}.png'
                    cursor.execute(
                        "INSERT INTO Donacion (nombre, entidad_donacion, monto_donacion, ruta_imagen) VALUES (%s, %s, %s, %s)",
                        [nombre, entidad_donacion, monto_donacion, ruta_imagen]
                    )
                    connection.commit()
                    messages.success(request, "Donación añadida correctamente.")
                else:  # update
                    nombre = request.POST.get('nombre')
                    entidad_donacion = request.POST.get('entidad_donacion')
                    monto_donacion = request.POST.get('monto_donacion')
                    cursor.execute(
                        "UPDATE Donacion SET nombre = %s, entidad_donacion = %s, monto_donacion = %s WHERE id_donacion = %s",
                        [nombre, entidad_donacion, monto_donacion, id_donacion]
                    )
                    connection.commit()
                    messages.success(request, "Donación actualizada correctamente.")
                return redirect('admin_donacion')
            cursor.execute("SELECT id_donacion, nombre, entidad_donacion, monto_donacion, ruta_imagen FROM Donacion")
            donaciones = cursor.fetchall()
    except Exception as e:
        messages.error(request, f"Error al cargar donaciones: {str(e)}")
    response = render(request, 'administrador/admin_donacion.html', {'donaciones': donaciones})
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def admin_material(request):
    if not es_admin(request):
        if request.session.get('user_id'):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return HttpResponseRedirect('dashboard')
        else:
            return HttpResponseRedirect('login')

    materiales = []
    try:
        with connection.cursor() as cursor:
            if request.method == 'POST':
                action = request.POST.get('action')
                if action == 'add':
                    nombre = request.POST.get('nombre')
                    puntos_por_unidad = request.POST.get('puntos_por_unidad')
                    co2_por_unidad = request.POST.get('co2_por_unidad')
                    unidad_medida = request.POST.get('unidad_medida')
                    if nombre and puntos_por_unidad and co2_por_unidad and unidad_medida:
                        try:
                            cursor.execute(
                                """
                                INSERT INTO Material_Reciclable (nombre, puntos_por_unidad, co2_por_unidad, unidad_medida)
                                VALUES (%s, %s, %s, %s)
                                """,
                                [nombre, puntos_por_unidad, co2_por_unidad, unidad_medida]
                            )
                            connection.commit()
                            messages.success(request, 'Material añadido correctamente.')
                        except Exception as e:
                            connection.rollback()
                            messages.error(request, f'Error al añadir el material: {str(e)}')
                    else:
                        messages.error(request, 'Todos los campos son obligatorios.')
                elif action == 'update':
                    id_material = request.POST.get('id_material')
                    nombre = request.POST.get('nombre')
                    puntos_por_unidad = request.POST.get('puntos_por_unidad')
                    co2_por_unidad = request.POST.get('co2_por_unidad')
                    unidad_medida = request.POST.get('unidad_medida')
                    if id_material and nombre and puntos_por_unidad and co2_por_unidad and unidad_medida:
                        try:
                            cursor.execute(
                                """
                                UPDATE Material_Reciclable 
                                SET nombre = %s, puntos_por_unidad = %s, co2_por_unidad = %s, unidad_medida = %s
                                WHERE id_material_reciclable = %s
                                """,
                                [nombre, puntos_por_unidad, co2_por_unidad, unidad_medida, id_material]
                            )
                            connection.commit()
                            messages.success(request, 'Material modificado correctamente.')
                        except Exception as e:
                            connection.rollback()
                            messages.error(request, f'Error al modificar el material: {str(e)}')
                    else:
                        messages.error(request, 'Todos los campos son obligatorios.')
                elif action == 'delete':
                    id_material = request.POST.get('id_material')
                    if id_material:
                        try:
                            cursor.execute("DELETE FROM Material_Punto_Reciclaje WHERE id_material_reciclable = %s", [id_material])
                            cursor.execute("DELETE FROM Material_Reciclable WHERE id_material_reciclable = %s", [id_material])
                            connection.commit()
                            messages.success(request, 'Material eliminado correctamente.')
                        except Exception as e:
                            connection.rollback()
                            messages.error(request, f'Error al eliminar el material: {str(e)}')
                return redirect('admin_material')

            # Obtener todos los materiales
            cursor.execute(
                """
                SELECT id_material_reciclable, nombre, puntos_por_unidad, co2_por_unidad, unidad_medida
                FROM Material_Reciclable
                """
            )
            materiales = cursor.fetchall()

    except Exception as e:
        messages.error(request, f'Error al cargar los materiales: {str(e)}')

    return render(request, 'administrador/admin_material.html', {
        'materiales': materiales
    })

def admin_puntos(request):
    if not es_admin(request):
        if request.session.get('user_id'):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('dashboard')
        else:
            return redirect('login')

    puntos_reciclaje = []
    materiales = []
    try:
        with connection.cursor() as cursor:
            # Obtener todos los materiales reciclables
            cursor.execute("SELECT id_material_reciclable, nombre FROM Material_Reciclable")
            materiales = cursor.fetchall()

            # Obtener lista de puntos de reciclaje con sus materiales y condiciones
            cursor.execute("""
                SELECT 
                    pr.id_punto_reciclaje,
                    pr.nombre,
                    pr.capacidad_maxima,
                    pr.hora_apertura,
                    pr.hora_cierre,
                    pr.latitud,
                    pr.longitud,
                    pr.estado_punto,
                    GROUP_CONCAT(CONCAT(mr.id_material_reciclable, ':', COALESCE(mpr.condiciones_especificas, '')) SEPARATOR ',') as material_conditions,
                    GROUP_CONCAT(mr.nombre SEPARATOR ', ') as materiales_permitidos
                FROM Punto_Reciclaje pr
                LEFT JOIN Material_Punto_Reciclaje mpr ON pr.id_punto_reciclaje = mpr.id_punto_reciclaje
                LEFT JOIN Material_Reciclable mr ON mpr.id_material_reciclable = mr.id_material_reciclable
                GROUP BY pr.id_punto_reciclaje, pr.nombre, pr.capacidad_maxima, pr.hora_apertura, 
                         pr.hora_cierre, pr.latitud, pr.longitud, pr.estado_punto
            """)
            puntos_reciclaje = cursor.fetchall()

            if request.method == 'POST':
                action = request.POST.get('action')
                if action == 'add':
                    nombre = request.POST.get('nombre')
                    capacidad_maxima = request.POST.get('capacidad_maxima')
                    hora_apertura = request.POST.get('hora_apertura')
                    hora_cierre = request.POST.get('hora_cierre')
                    latitud = request.POST.get('latitud')
                    longitud = request.POST.get('longitud')
                    estado_punto = request.POST.get('estado_punto')
                    materiales_seleccionados = request.POST.getlist('materiales')
                    condiciones = request.POST.getlist('condiciones')  # Lista de condiciones
                    if not all([nombre, capacidad_maxima, hora_apertura, hora_cierre, latitud, longitud, estado_punto]):
                        messages.error(request, 'Todos los campos son obligatorios.')
                    elif int(capacidad_maxima) < 0:
                        messages.error(request, 'La capacidad máxima no puede ser negativa.')
                    elif hora_apertura >= hora_cierre:
                        messages.error(request, 'La hora de apertura debe ser anterior a la hora de cierre.')
                    else:
                        cursor.callproc('insertar_punto_reciclaje', [nombre, int(capacidad_maxima), hora_apertura, hora_cierre, float(latitud), float(longitud), estado_punto])
                        cursor.execute("SELECT LAST_INSERT_ID()")
                        new_id = cursor.fetchone()[0]
                        for i, mat_id in enumerate(materiales_seleccionados):
                            condicion = condiciones[i] if i < len(condiciones) else None
                            cursor.callproc('insertar_material_punto_reciclaje', [int(mat_id), new_id, condicion])
                        connection.commit()
                        messages.success(request, 'Punto de reciclaje añadido correctamente.')
                        return redirect('admin_puntos')
                elif action == 'edit':
                    id_punto_reciclaje = int(request.POST.get('id_punto_reciclaje'))
                    nombre = request.POST.get('nombre')
                    capacidad_maxima = request.POST.get('capacidad_maxima')
                    hora_apertura = request.POST.get('hora_apertura')
                    hora_cierre = request.POST.get('hora_cierre')
                    latitud = request.POST.get('latitud')
                    longitud = request.POST.get('longitud')
                    estado_punto = request.POST.get('estado_punto')
                    materiales_seleccionados = request.POST.getlist('materiales')
                    condiciones = request.POST.getlist('condiciones')
                    if not all([nombre, capacidad_maxima, hora_apertura, hora_cierre, latitud, longitud, estado_punto]):
                        messages.error(request, 'Todos los campos son obligatorios.')
                    elif int(capacidad_maxima) < 0:
                        messages.error(request, 'La capacidad máxima no puede ser negativa.')
                    elif hora_apertura >= hora_cierre:
                        messages.error(request, 'La hora de apertura debe ser anterior a la hora de cierre.')
                    else:
                        cursor.callproc('actualizar_punto_reciclaje', [id_punto_reciclaje, nombre, int(capacidad_maxima), hora_apertura, hora_cierre, float(latitud), float(longitud), estado_punto])
                        cursor.execute("DELETE FROM Material_Punto_Reciclaje WHERE id_punto_reciclaje = %s", [id_punto_reciclaje])
                        for i, mat_id in enumerate(materiales_seleccionados):
                            condicion = condiciones[i] if i < len(condiciones) else None
                            cursor.callproc('insertar_material_punto_reciclaje', [int(mat_id), id_punto_reciclaje, condicion])
                        connection.commit()
                        messages.success(request, 'Punto de reciclaje actualizado correctamente.')
                        return redirect('admin_puntos')
            elif request.method == 'GET' and request.GET.get('action') == 'delete':
                id_punto_reciclaje = int(request.GET.get('id'))
                cursor.execute("DELETE FROM Material_Punto_Reciclaje WHERE id_punto_reciclaje = %s", [id_punto_reciclaje])
                cursor.callproc('eliminar_punto_reciclaje', [id_punto_reciclaje])
                connection.commit()
                messages.success(request, 'Punto de reciclaje eliminado correctamente.')
                return redirect('admin_puntos')

    except Exception as e:
        messages.error(request, f'Error al procesar puntos de reciclaje: {str(e)}')

    response = render(request, 'administrador/admin_puntos.html', {'puntos_reciclaje': puntos_reciclaje, 'materiales': materiales})
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def admin_historial(request):
    if not es_admin(request):
        if request.session.get('user_id'):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('dashboard')
        else:
            return redirect('login')

    historial_acceso = []
    try:
        with connection.cursor() as cursor:
            # Consulta ajustada para mostrar fecha y hora
            cursor.execute(
                "SELECT id_bitacora_acceso, id_usuario, tipo_acceso, DATE_FORMAT(fecha_acceso, '%Y-%m-%d %H:%i:%s') AS fecha_acceso, resultado, detalle FROM Bitacora_Acceso ORDER BY fecha_acceso DESC"
            )
            historial_acceso = cursor.fetchall()
    except Exception as e:
        messages.error(request, f'Error al cargar el historial: {str(e)}')
        logger.error(f"Error al obtener historial: {str(e)}")

    response = render(request, 'administrador/admin_historial.html', {'historial_acceso': historial_acceso})
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def bitacora_reciclaje(request):
    if not es_admin(request):
        if request.session.get('user_id'):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('dashboard')
        else:
            return redirect('login')
    
    bitacora = []
    search_query = request.GET.get('search', '').strip()
    
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT id_bitacora_reciclaje, ip, id_registro_reciclaje, accion, 
                       DATE_FORMAT(fecha_accion, '%%d/%%m/%%Y %%H:%%i') AS fecha_accion, detalle
                FROM Bitacora_Reciclaje
            """
            params = []
            if search_query:
                query += """
                    WHERE id_bitacora_reciclaje LIKE %s 
                    OR ip LIKE %s 
                    OR detalle LIKE %s
                """
                params = ['%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%']
            
            cursor.execute(query, params)
            raw_bitacora = cursor.fetchall()
            
            # Procesar cada entrada para extraer el usuario
            for entry in raw_bitacora:
                detalle = entry[5] or ""
                usuario = "Usuario Externo"
                if (detalle.startswith("Registro creado por ") and ": " in detalle[17:]) or \
                   (detalle.startswith("Registro actualizado por ") and ": " in detalle[19:]) or \
                   (detalle.startswith("Registro eliminado por ") and ": " in detalle[18:]):
                    usuario_part = detalle.split(": ")[0]
                    usuario = usuario_part.split("por ")[1] if "por " in usuario_part else usuario
                bitacora.append((entry[0], entry[1], entry[3], entry[4], entry[5], usuario))  # (id, ip, accion, fecha, detalle, usuario)
    
    except Exception as e:
        messages.error(request, f'Error al cargar bitácora: {str(e)}')
    
    response = render(request, 'administrador/bitacora_reciclaje.html', {'bitacora': bitacora})
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def bitacora_catalogo(request):
    if not es_admin(request):
        if request.session.get('user_id'):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('dashboard')
        else:
            return redirect('login')
    
    bitacora = []
    search_query = request.GET.get('search', '').strip()
    
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT id_bitacora_catalogo, ip, id_catalogo_recompensa, accion, 
                       DATE_FORMAT(fecha_accion, '%%d/%%m/%%Y %%H:%%i') AS fecha_accion, detalle
                FROM Bitacora_Catalogo
            """
            params = []
            if search_query:
                query += """
                    WHERE id_bitacora_catalogo LIKE %s 
                    OR ip LIKE %s 
                    OR detalle LIKE %s
                """
                params = ['%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%']
            
            cursor.execute(query, params)
            raw_bitacora = cursor.fetchall()
            
            # Procesar cada entrada para extraer el usuario
            for entry in raw_bitacora:
                detalle = entry[5] or ""
                usuario = "Usuario Externo"
                if (detalle.startswith("Recompensa creada por ") and ": " in detalle[19:]) or \
                   (detalle.startswith("Recompensa actualizada por ") and ": " in detalle[23:]) or \
                   (detalle.startswith("Recompensa eliminada por ") and ": " in detalle[23:]):
                    usuario_part = detalle.split(": ")[0]
                    usuario = usuario_part.split("por ")[1] if "por " in usuario_part else usuario
                bitacora.append((entry[0], entry[1], entry[3], entry[4], entry[5], usuario))  # (id, ip, accion, fecha, detalle, usuario)
    
    except Exception as e:
        messages.error(request, f'Error al cargar bitácora: {str(e)}')
    
    response = render(request, 'administrador/bitacora_catalogo.html', {'bitacora': bitacora})
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def bitacora_canje(request):
    if not es_admin(request):
        if request.session.get('user_id'):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('dashboard')
        else:
            return redirect('login')
    
    bitacora = []
    search_query = request.GET.get('search', '').strip()
    
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT id_bitacora_canje, ip, id_canje_recompensa, id_catalogo_recompensa, accion, 
                       DATE_FORMAT(fecha_accion, '%%d/%%m/%%Y %%H:%%i') AS fecha_accion, detalle
                FROM Bitacora_Canje
            """
            params = []
            if search_query:
                query += """
                    WHERE id_bitacora_canje LIKE %s 
                    OR ip LIKE %s 
                    OR detalle LIKE %s
                """
                params = ['%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%']
            
            cursor.execute(query, params)
            raw_bitacora = cursor.fetchall()
            
            # Procesar cada entrada para extraer el usuario
            for entry in raw_bitacora:
                detalle = entry[6] or ""
                usuario = "Usuario Externo"
                if (detalle.startswith("Canje creado por ") and ": " in detalle[14:]) or \
                   (detalle.startswith("Canje actualizado por ") and ": " in detalle[18:]) or \
                   (detalle.startswith("Canje eliminado por ") and ": " in detalle[18:]):
                    usuario_part = detalle.split(": ")[0]
                    usuario = usuario_part.split("por ")[1] if "por " in usuario_part else usuario
                bitacora.append((entry[0], entry[1], entry[4], entry[5], detalle, usuario))  # (id, ip, accion, fecha, detalle, usuario)
    
    except Exception as e:
        messages.error(request, f'Error al cargar bitácora: {str(e)}')
    
    response = render(request, 'administrador/bitacora_canje.html', {'bitacora': bitacora})
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response
