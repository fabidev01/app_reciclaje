# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BitacoraAcceso(models.Model):
    id_bitacora_acceso = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    tipo_acceso = models.CharField(max_length=35)
    fecha_acceso = models.DateField()
    resultado = models.CharField(max_length=35)
    detalle = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bitacora_acceso'


class BitacoraCanje(models.Model):
    id_bitacora_canje = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=45)
    id_canje_recompensa = models.ForeignKey('CanjeRecompensa', models.DO_NOTHING, db_column='id_canje_recompensa')
    id_catalogo_recompensa = models.ForeignKey('CatalogoRecompensa', models.DO_NOTHING, db_column='id_catalogo_recompensa')
    accion = models.CharField(max_length=35)
    fecha_accion = models.DateField()
    detalle = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bitacora_canje'


class BitacoraCatalogo(models.Model):
    id_bitacora_catalogo = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=45)
    id_catalogo_recompensa = models.ForeignKey('CatalogoRecompensa', models.DO_NOTHING, db_column='id_catalogo_recompensa')
    accion = models.CharField(max_length=35)
    fecha_accion = models.DateField()
    detalle = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bitacora_catalogo'


class BitacoraReciclaje(models.Model):
    id_bitacora_reciclaje = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=45)
    id_registro_reciclaje = models.ForeignKey('RegistroReciclaje', models.DO_NOTHING, db_column='id_registro_reciclaje')
    accion = models.CharField(max_length=35)
    fecha_accion = models.DateField()
    detalle = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bitacora_reciclaje'


class CanjeDonacion(models.Model):
    id_canje_donacion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')
    id_donacion = models.ForeignKey('Donacion', models.DO_NOTHING, db_column='id_donacion')
    estado = models.CharField(max_length=35)
    fecha_canje = models.DateField()
    puntos_descontados = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'canje_donacion'


class CanjeRecompensa(models.Model):
    id_canje_recompensa = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')
    id_catalogo_recompensa = models.ForeignKey('CatalogoRecompensa', models.DO_NOTHING, db_column='id_catalogo_recompensa')
    estado = models.CharField(max_length=35)
    fecha_canje = models.DateField()
    puntos_descontados = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'canje_recompensa'


class CatalogoRecompensa(models.Model):
    id_catalogo_recompensa = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=35)
    puntos_coste = models.IntegerField()
    disponible = models.IntegerField()
    stock = models.IntegerField()
    descuento = models.FloatField()
    categoria = models.CharField(max_length=35)

    class Meta:
        managed = False
        db_table = 'catalogo_recompensa'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Donacion(models.Model):
    id_donacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=35)
    entidad_donacion = models.CharField(max_length=35)
    monto_donacion = models.FloatField()

    class Meta:
        managed = False
        db_table = 'donacion'


class ImpactoAmbientalDiario(models.Model):
    id_impacto_ambiental_diario = models.AutoField(primary_key=True)
    fecha_dia = models.DateField()
    tipo_basura = models.CharField(max_length=35)
    unidad_medida = models.CharField(max_length=10)
    cantidad_reciclada_por_tipo = models.FloatField()
    co2_reducido_por_tipo = models.FloatField()

    class Meta:
        managed = False
        db_table = 'impacto_ambiental_diario'
        unique_together = (('fecha_dia', 'tipo_basura'),)


class MaterialPuntoReciclaje(models.Model):
    pk = models.CompositePrimaryKey('id_material_reciclable', 'id_punto_reciclaje')
    id_material_reciclable = models.ForeignKey('MaterialReciclable', models.DO_NOTHING, db_column='id_material_reciclable')
    id_punto_reciclaje = models.ForeignKey('PuntoReciclaje', models.DO_NOTHING, db_column='id_punto_reciclaje')
    condiciones_especificas = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material_punto_reciclaje'


class MaterialReciclable(models.Model):
    id_material_reciclable = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=35)
    puntos_por_unidad = models.IntegerField()
    co2_por_unidad = models.FloatField()
    unidad_medida = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'material_reciclable'


class Permiso(models.Model):
    id_permiso = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=35)

    class Meta:
        managed = False
        db_table = 'permiso'


class PuntoReciclaje(models.Model):
    id_punto_reciclaje = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=35)
    capacidad_maxima = models.IntegerField()
    hora_apertura = models.TimeField()
    hora_cierre = models.TimeField()
    latitud = models.DecimalField(max_digits=10, decimal_places=8)
    longitud = models.DecimalField(max_digits=11, decimal_places=8)
    estado_punto = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'punto_reciclaje'


class RegistroReciclaje(models.Model):
    id_registro_reciclaje = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')
    id_punto_reciclaje = models.ForeignKey(PuntoReciclaje, models.DO_NOTHING, db_column='id_punto_reciclaje')
    id_material_reciclable = models.ForeignKey(MaterialReciclable, models.DO_NOTHING, db_column='id_material_reciclable')
    cantidad_kg = models.FloatField()
    puntos_obtenidos = models.IntegerField()
    co2_reducido = models.FloatField()
    fecha_registro = models.DateField()
    nombre_subtipo = models.CharField(max_length=35)

    class Meta:
        managed = False
        db_table = 'registro_reciclaje'


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=35)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rol'


class RolPermiso(models.Model):
    pk = models.CompositePrimaryKey('id_rol', 'id_permiso')
    id_rol = models.ForeignKey(Rol, models.DO_NOTHING, db_column='id_rol')
    id_permiso = models.ForeignKey(Permiso, models.DO_NOTHING, db_column='id_permiso')

    class Meta:
        managed = False
        db_table = 'rol_permiso'


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=35)
    correo = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    balance_puntos = models.IntegerField()
    fecha_registro = models.DateField()
    contraseña = models.CharField(max_length=200)
    ip = models.CharField(max_length=45)
    id_rol = models.ForeignKey(Rol, models.DO_NOTHING, db_column='id_rol')

    class Meta:
        managed = False
        db_table = 'usuario'
