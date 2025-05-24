# reciclaje/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Página de inicio
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard
    path('historial/', views.historial, name='historial'),  # Historial
    path('login/', views.login_view, name='login'),  # Login
    path('registro-reciclaje/', views.registro_reciclaje, name='registro_reciclaje'),  # Registrar reciclaje
    path('registro-usuario/', views.registro_usuario, name='registro_usuario'),  # Registro de usuario
]