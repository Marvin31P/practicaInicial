from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),  
    path('', views.login_view, name='login'),  # Página principal
    path('registro/', views.registro, name='register'),  # Página de registro
    path('logout/', views.cerrar_sesion, name='logout'),  # Cerrar sesión
    path('login/', views.login_view, name='login'),  
    path('profile/', views.perfil, name='profile'),
    path('publicacion/nueva/', views.crear_publicacion, name='crear_publicacion'),  # Corregido
    path('publicaciones/', views.listar_publicaciones, name='listar_publicaciones'),  # Corregido
]
