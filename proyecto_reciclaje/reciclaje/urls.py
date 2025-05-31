# reciclaje/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Página de inicio
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard
    path('historial/', views.historial, name='historial'),  # Historial
    path('login/', views.login_view, name='login'),  # Login
    path('login/', views.login_view, name='logout'),  # Loguot
    path('registro-reciclaje/', views.registro_reciclaje, name='registro_reciclaje'),  # Registrar reciclaje
    path('registro-usuario/', views.registro_usuario, name='registro_usuario'),  # Registro de usuario
    path('catalogo/', views.catalogo, name='catalogo'),  # Recompensas
    path('donacion/', views.donacion, name='donacion'),  # Recompensas
    path('administrador/', views.admin_panel, name='admin_panel'),
    path('administrador/usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('administrador/registros/', views.admin_registros, name='admin_registros'),
    path('administrador/catalogo/', views.admin_catalogo, name='admin_catalogo'),
    path('administrador/donacion/', views.admin_donacion, name='admin_donacion'),
    path('administrador/historial-acceso/', views.admin_historial, name='admin_historial'),
    path('administrador/bitacora-reciclaje/', views.bitacora_reciclaje, name='bitacora_reciclaje'),
    path('administrador/bitacora-catalogo/', views.bitacora_catalogo, name='bitacora_catalogo'),
    path('administrador/bitacora-canje/', views.bitacora_canje, name='bitacora_canje'),
]