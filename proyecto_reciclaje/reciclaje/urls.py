# reciclaje/urls.py
from django.urls import path
from . import views
from . import views_admin

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro-usuario/', views.registro_usuario, name='registro_usuario'),
    path('donacion/', views.donacion, name='donacion'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('historial/', views.historial, name='historial'),
    path('registro-reciclaje/', views.registro_reciclaje, name='registro_reciclaje'),
    path('admin-panel/', views_admin.admin_panel, name='admin_panel'),
    path('admin-usuarios/', views_admin.admin_usuarios, name='admin_usuarios'),
    path('admin-registros/', views_admin.admin_registros, name='admin_registros'),
    path('admin-catalogo/', views_admin.admin_catalogo, name='admin_catalogo'),
    path('admin-donacion/', views_admin.admin_donacion, name='admin_donacion'),
    path('admin-historial/', views_admin.admin_historial, name='admin_historial'),
    path('bitacora-reciclaje/', views_admin.bitacora_reciclaje, name='bitacora_reciclaje'),
    path('bitacora-catalogo/', views_admin.bitacora_catalogo, name='bitacora_catalogo'),
    path('bitacora-canje/', views_admin.bitacora_canje, name='bitacora_canje'),
]